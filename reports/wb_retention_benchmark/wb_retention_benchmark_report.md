# WB retention benchmark report (`wb_retention_benchmark_v0`)

This benchmark is a **whole-body retention/planning benchmark only**.
It is **not a marrow method** and **not a lesion/image method**.

## Status labeling
- source_lock_status: `source_locked`
- implementation_status: `implementation_default`
- provisional_status: `provisional`

## Cohort summary
| method_name               |   processed_count |   valid_count |   invalid_count |   mean_benchmark_activity_limit_gbq |   median_benchmark_activity_limit_gbq | source_lock_status   | implementation_status   | provisional_status   |
|:--------------------------|------------------:|--------------:|----------------:|------------------------------------:|--------------------------------------:|:---------------------|:------------------------|:---------------------|
| wb_retention_benchmark_v0 |                26 |            25 |               1 |                              18.798 |                               12.1263 | source_locked        | implementation_default  | provisional          |

## Method comparisons
- Method 1 vs WB benchmark pairs: 3
- Method 2 vs WB benchmark pairs: 3

### Method 1 vs WB benchmark (GBq)
- median absolute difference: 4.64746
- median percent difference vs Method 1: 62.1416%

### Method 2 vs WB benchmark (GBq)
- median absolute difference: 55.0505
- median percent difference vs Method 2: 81.9487%

## Method 1 driver/dominance proxy
- Classification based on Method 1 final limit vs WB benchmark limit (tolerance = 1%).
- Counts: {'blood_or_marrow_dominated': 2, 'near_equal_or_mixed': 1}

## Caution
Method 2 comparisons remain provisional where coefficient provenance is not fully locked.
This benchmark is intended as a comparator for manuscript interpretation, not as a new clinical standard.