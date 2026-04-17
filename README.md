# Waveform Simulator Demo

Demonstration simulator and EPICS IOC using [PSCDRV]().

## Depends

- IOC
  - EPICS Base >= 7.0.9
  - PSCDRV
  - PVXS
  - autosave
- Simulator
  - python >= 3.13
- Display
  - cs-studio phoebus

## Building

```sh
git clone https://github.com/epics-base/epics-base
git clone https://github.com/epics-base/pvxs
git clone https://github.com/epics-modules/autosave
git clone https://github.com/osprey-dcs/pscdrv
git clone https://github.com/osprey-dcs/wfsim-demo

cat <<EOF > pvxs/configure/RELEASE.local
EPICS_BASE = \$(TOP)/../epics-base
EOF

cat <<EOF > autosave/configure/RELEASE.local
EPICS_BASE = \$(TOP)/../epics-base
EOF

cat <<EOF > pscdrv/configure/RELEASE.local
EPICS_BASE = \$(TOP)/../epics-base
EOF

cat <<EOF > wfsim-demo/configure/RELEASE.local
AUTOSAVE = \$(TOP)/../autosave
PVXS = \$(TOP)/../pvxs
PSCDRV = \$(TOP)/../pscdrv
EPICS_BASE = \$(TOP)/../epics-base
EOF

make -C epics-base -j2
make -C pvxs -j2
make -C autosave -j2
make -C pscdrv -j2
make -C wfsim-demo -j2
```

## Running

In one terminal run:

```sh
./wfsim.py 127.0.0.1
```

In another terminal run:

```sh
cd iocBoot/iocwfsim
./st.cmd
```

Open `opi/wfsim.bob` in phoebus.
