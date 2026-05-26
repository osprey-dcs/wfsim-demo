#!/usr/bin/env python3

import logging
import time
import struct
import signal
import asyncio

import numpy as np

_log = logging.getLogger(__name__)

_chan = np.dtype([
    ('amp', '>i4'),
    ('freq', '>f4'),
])

def build_msg(msgid:int, body:bytes):
    blen = len(body)
    return struct.pack('>2sHI', b'PS', msgid, blen) + body

async def sendmsg(writer:asyncio.StreamWriter, msgid:int, body:bytes):
    msg = build_msg(msgid, body)
    writer.write(msg)
    await asyncio.wait_for(writer.drain(), timeout=0.1)

class Device:
    def __init__(self):
        self.clients: {asyncio.StreamWriter} = set()
        self.nchan = 8
        self.nsamp = 256
        self.pha60 = 0.0

        self.settings = S = np.zeros((), dtype=[
            ('rate', '>f4'),
            ('ch', _chan, self.nchan),
        ])
        S['rate'] = 1.0 # Hz
        S['ch']['freq'][:] = 10.0
        S['ch']['amp'][:] = 0
        print('Initial', S)

    async def bcast(self, msgid:int, body:bytes, *, skip:asyncio.StreamWriter = None):
        for cli in self.clients:
            if cli is not skip:
                await sendmsg(cli, msgid, body)

    async def handle_tcp_client(self, reader, writer):
        peer = writer.get_extra_info('peername')
        try:
            _log.info('client connects %s', peer)

            # send initial messages
            await sendmsg(writer, 10, f'hello {peer[0]}:{peer[1]}'.encode())
            await sendmsg(writer, 11, self.settings.tobytes())

            self.clients.add(writer)

            while True:
                P, S, msgid, blen = struct.unpack('>ccHI', await reader.readexactly(8))
                _log.debug('RX %s msgid %d blen %d', peer, msgid, blen)

                if P!=b'P' or S!=b'S':
                    raise RuntimeError('Framing error')

                body = await reader.readexactly(blen)

                if msgid==11:
                    cur = self.settings.tobytes()
                    body = body[:len(cur)]
                    body = np.frombuffer(body, count=1, dtype=self.settings.dtype)[0]

                    if body['rate']<=0 or (body['ch']['freq']<=0).any():
                        _log.error('Ignore Settings %r', body)
                    else:
                        self.settings = body
                        _log.info('Update %r', body)

                else:
                    _log.debug('Unhandled msgid %d', msgid)

        except asyncio.exceptions.IncompleteReadError as e:
            if len(e.partial)!=0:
                raise
        finally:
            try:
                self.clients.remove(writer)
            except KeyError:
                pass # ignore
            _log.info('client disconnects %s', peer)

    async def data_loop(self):
        while True:
            try:
                await asyncio.sleep(1/float(self.settings['rate']))
                S = self.settings # snapshot
                self.pha60 = np.fmod(self.pha60 + np.pi/13, 2*np.pi)

                now = time.time()
                sec, nsec = int(now), (int(now*1e9)%1000000000)

                adc = np.ndarray((self.nsamp, self.nchan), dtype='>i4')

                T = 2*np.pi*np.arange(self.nsamp)
                for chan in range(self.nchan):
                    F = S['ch'][chan]['freq']/1000
                    phas = chan*np.pi/4
                    adc[:,chan] = np.sin(T*F + phas)*S['ch'][chan]['amp'] \
                            + np.sin(T*3/1000 + self.pha60)*15 \
                            + np.random.randn(self.nsamp)*10

                # status (unused), sec, nsec
                msg = struct.pack('>III', 0, sec, nsec) + adc.tobytes()
                await self.bcast(12, msg)

            except asyncio.CancelledError:
                return
            except:
                _log.exception('Unhandled')

def getargs():
    from argparse import ArgumentParser
    P = ArgumentParser()
    P.add_argument('-v', '--verbose', action='store_const',
                   default=logging.INFO,
                   const=logging.DEBUG,
                   help='Make some noise')

    def endpoint(s: str) -> (str, int):
        host, _sep, port = s.partition(':')
        port = int(port or 0)
        return host, port

    P.add_argument('endpoint', type=endpoint,
                   default=('127.0.0.1', 0),
                   help='Listening endpoint host:port')
    return P

async def main(args):
    host, port =args.endpoint
    port = port or 6789
    _log.info('Binding to %s:%s', host, port)

    dev = Device()

    serv = await asyncio.start_server(dev.handle_tcp_client, host=host, port=port)
    serv: asyncio.Server

    done = asyncio.Event()
    asyncio.get_running_loop().add_signal_handler(signal.SIGINT, done.set)

    dl = None
    try:
        dl = asyncio.create_task(dev.data_loop())
        _log.info('Running')
        await done.wait()
        _log.info('Stopping')
    except asyncio.CancelledError:
        pass
    except:
        _log.exception('Unhandled')
    finally:
        _log.debug('close')
        serv.close()
        if dl is not None:
            _log.debug('cancel')
            dl.cancel()
        _log.debug('wait_closed')
        await serv.wait_closed()
        _log.debug('wait cancel')
        try:
            await dl
        except asyncio.CancelledError:
            pass

    _log.info('Done')

if __name__ == "__main__":
    args = getargs().parse_args()
    logging.basicConfig(level=args.verbose)
    asyncio.run(main(args))
