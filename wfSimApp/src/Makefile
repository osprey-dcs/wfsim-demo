# SPDX-FileCopyrightText: 2003 Argonne National Laboratory
#
# SPDX-License-Identifier: EPICS

TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = wfSim
# wfSim.dbd will be created and installed
DBD += wfSim.dbd

# wfSim.dbd will be made up from these files:
wfSim_DBD += base.dbd
wfSim_DBD += pscCore.dbd

wfSim_LIBS += pscCore

ifdef PVXS_MAJOR_VERSION # prefer v2
wfSim_DBD += pvxsIoc.dbd
wfSim_LIBS += pvxsIoc pvxs
endif

# wfSim_registerRecordDeviceDriver.cpp derives from wfSim.dbd
wfSim_SRCS += wfSim_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
wfSim_SRCS_DEFAULT += wfSimMain.cpp
wfSim_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#wfSim_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
wfSim_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

