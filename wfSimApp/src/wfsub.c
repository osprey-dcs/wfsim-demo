
#include <epicsStdlib.h>
#include <epicsMath.h>
#include <alarm.h>
#include <recGbl.h>
#include <menuFtype.h>
#include <aSubRecord.h>

#include <registryFunction.h>
#include <epicsExport.h>

/* Log scale example (for real, use aCalcoutRecord!!!)
 *
 * record(aSub, "$(P)C$(CH):V_") {
 *     field(SNAM, "wfsimScale")
 *     field(FTA, "DOUBLE")
 *     field(NOA , "$(NELM=512)")
 *     field(INPA, "") # volts
 *     field(FTVA, "DOUBLE")
 *     field(NOVA, "$(NELM=512)")
 *     field(OUTA, "") # dBm
 * }
 */
static
long wfsimScale(aSubRecord *prec)
{
    if(prec->fta != menuFtypeDOUBLE) {
        recGblSetSevrMsg(prec, COMM_ALARM, INVALID_ALARM, "Wrong FTA");
        return -1;
    }
    if(prec->ftva != menuFtypeDOUBLE) {
        recGblSetSevrMsg(prec, COMM_ALARM, INVALID_ALARM, "Wrong FTVA");
        return -1;
    }

    const double *a = prec->a;
    const size_t a_count = prec->nea;

    double *vala = prec->vala;
    const size_t vala_capacity = prec->nova;

    size_t desired = a_count;
    if(desired > vala_capacity)
        desired = vala_capacity;

    for(size_t i=0; i<desired; i++) {
        double e = a[i];
        if(!isfinite(e) || e <= 0.0) {
            recGblSetSevrMsg(prec, CALC_ALARM, INVALID_ALARM, "NaN @%zu", i);
            vala[i] = 1e-30;
        } else {
            vala[i] = 20*log10(a[i]);
        }
    }

    prec->neva = desired;

    return 0;
}

// match with .dbd entry:
//   function(wfsimScale)
epicsRegisterFunction(wfsimScale);
