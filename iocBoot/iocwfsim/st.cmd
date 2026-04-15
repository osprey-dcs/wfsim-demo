#!../../bin/linux-x86_64/wfSim

dbLoadDatabase "../../dbd/wfSim.dbd"
wfSim_registerRecordDeviceDriver(pdbbase)

createPSC("DEV", "localhost", 6789, 1)
setPSCSendBlockSize("DEV", 11, 68)

dbLoadRecords("../../db/wfsim.db","P=TST:,NAME=DEV")

iocInit()
