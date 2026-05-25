
#include <alarm.h>
#include <recGbl.h>
#include <aSubRecord.h>

#include <registryFunction.h>
#include <epicsExport.h>

static
long wfsimScale(aSubRecord *prec) {
    recGblSetSevrMsg(prec, COMM_ALARM, INVALID_ALARM, "Nope");
    return 0;
}

// match with .dbd entry:
//   function(wfsimScale)
epicsRegisterFunction(wfsimScale);
