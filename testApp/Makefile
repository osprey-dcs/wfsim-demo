# SPDX-FileCopyrightText: 2003 Argonne National Laboratory
#
# SPDX-License-Identifier: EPICS

TOP=..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

# peek at implementation
SRC_DIRS += $(TOP)/wfSimApp/src

DBDDEPENDS_FILES += testwfsub.dbd$(DEP)
testwfsub_DBD = base.dbd
testwfsub_DBD += wfsim.dbd
TESTFILES += $(COMMON_DIR)/testwfsub.dbd

PROD_LIBS += $(EPICS_BASE_IOC_LIBS)

TESTPROD_HOST += testwfsub
testwfsub_SRCS += testwfsub.c
testwfsub_SRCS += wfsub.c
testwfsub_SRCS += testwfsub_registerRecordDeviceDriver.cpp
TESTS += testwfsub

TESTSCRIPTS_HOST += $(TESTS:%=%.t)

#=============================
# Build the IOC application

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

