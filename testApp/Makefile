# SPDX-FileCopyrightText: 2003 Argonne National Laboratory
#
# SPDX-License-Identifier: EPICS

TOP=..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

PROD_LIBS += Com

TESTPROD_HOST += testwfsub
testwfsub_SRCS += testwfsub.c
TESTS += testwfsub

TESTSCRIPTS_HOST += $(TESTS:%=%.t)

#=============================
# Build the IOC application

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

