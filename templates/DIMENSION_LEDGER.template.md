# Dimension ledger

Asset: `<manufacturer product variant>`

Accuracy claim: `<A engineering reconstruction | B dimensionally grounded visual | C visual approximation>`

Canonical unit: `<mm | m | inch>`

Master source revision/hash: `<value>`

## Datums and axes

- Origin:
- Up / forward / right:
- Primary datum A:
- Secondary datum B:
- Tertiary datum C:
- Ground/contact plane:
- Runtime pivot:

## Source register

| Source ID | Document/file | Variant/revision | Date | Exact URL/location | License/redistribution | Hash |
|---|---|---|---|---|---|---|
| S-001 | `<datasheet>` | `<revision>` | `<date>` | `<URL>` | `<terms>` | `<sha256>` |

## Measurement ledger

Allowed status: `stated`, `derived`, `estimated`, `unknown`, `conflicting`.

| ID | Feature/relationship | Original value | Canonical value | Tolerance | Datum/axis | Status | Source/page/figure | Derivation or estimation | Criticality |
|---|---|---:|---:|---:|---|---|---|---|---|
| D-001 | overall width | `<value unit>` | `<value>` | `<±value>` | B–C | stated | S-001 p.4 fig.2 | — | critical |

## Conflicts and unknowns

| ID | Problem | Affected features | Decision authority | Resolution/status |
|---|---|---|---|---|
| Q-001 | `<conflict or missing value>` | `<features>` | `<owner>` | `<open/resolved>` |

## Parametric mapping

| Dimension ID | CAD/script parameter | Model feature | Verification method |
|---|---|---|---|
| D-001 | `overall_width_mm` | `Body.MainEnvelope` | bounding-box script |

## Review

- Prepared by/date:
- Geometry reviewer/date:
- Domain/engineering reviewer/date where required:
- Approved accuracy class and limitations:
