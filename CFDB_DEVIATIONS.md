# Deviation: CFdb score threshold

**Written before reading any MVP row.** `CFDB_PREREGISTRATION.md` referred to partners "above
threshold" without naming a number, because the file's scoring columns had not been seen when it was
written.

The file carries `Score` and `Precision` columns for 47,455,274 pairs. Counting rows per precision band
**without filtering on any gene**:

| precision | pairs |
|---|---|
| >= 0.90 | 12,343 |
| >= 0.75 | 25,262 |
| **>= 0.50** | **69,120** |
| >= 0.25 | 268,115 |

**Primary threshold fixed here at precision >= 0.50**, the conventional high-confidence level for this
resource, with **0.75 and 0.90 reported as sensitivity analyses** for every registered test. The choice
is made from the precision distribution alone; no MVP, PARP4 or TEP1 row had been inspected.

Both positive-control gates and all registered tests use whichever threshold is being reported, applied
identically to MVP and to the controls.
