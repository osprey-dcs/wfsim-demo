
#define USE_TYPED_RSET

#include <epicsUnitTest.h>
#include <dbUnitTest.h>
#include <testMain.h>

#include <alarm.h>
#include <dbDefs.h>
#include <dbAccess.h>
#include <dbStaticLib.h>

static
void testCase1()
{
    {
        const double inp[] = {1.0, 10.0, 0.0, -1.0};
        testdbPutArrFieldOk("tst1:V", DBR_DOUBLE, NELEMENTS(inp), inp);
    }
    testdbGetFieldEqual("tst1:sub.SEVR", DBF_LONG, INVALID_ALARM);
    testdbGetFieldEqual("tst1:sub.AMSG", DBF_STRING, "NaN @2");
    {
        const double expect[] = {0.0, 20.0, 1e-30, 1e-30};
        testdbGetArrFieldEqual("tst1:dB", DBR_DOUBLE,
                               NELEMENTS(expect)+1,
                               NELEMENTS(expect), expect);
    }
}

static
void testCase2()
{
    {
        const double inp[] = {1.0, 10.0, 100.0};
        testdbPutArrFieldOk("tst1:V", DBR_DOUBLE, NELEMENTS(inp), inp);
    }
    testdbGetFieldEqual("tst1:sub.SEVR", DBF_LONG, NO_ALARM);
    testdbGetFieldEqual("tst1:sub.AMSG", DBF_STRING, "");
    {
        const double expect[] = {0.0, 20.0, 40};
        testdbGetArrFieldEqual("tst1:dB", DBR_DOUBLE,
                               NELEMENTS(expect)+1,
                               NELEMENTS(expect), expect);
    }
}

int testwfsub_registerRecordDeviceDriver(DBBASE *pbase);

MAIN(testwfsub) {
    testPlan(8);
    testdbPrepare();
    testdbReadDatabase("testwfsub.dbd", NULL, NULL);
    testwfsub_registerRecordDeviceDriver(pdbbase);
    testdbReadDatabase("test1.db", NULL, "P=tst1:");
    testIocInitOk();
    // "isolated" IOC running
    testCase1();
    testCase2();
    testIocShutdownOk();
    testdbCleanup();
    return testDone();
}
