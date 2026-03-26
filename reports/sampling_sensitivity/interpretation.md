# Sampling sensitivity interpretation (conservative)

Method equations were kept unchanged; only blood sample subsets were varied.
Whole-body inputs were preserved across all scenarios.

## Scenarios tested
- **full_5pt**: Full baseline (5 blood samples) (points [1, 2, 3, 4, 5])
- **triad_1_3_5**: 3-point early/mid/late (1,3,5) (points [1, 3, 5])
- **triad_2_3_5**: 3-point mid/late (2,3,5) (points [2, 3, 5])
- **dyad_1_5**: 2-point early/late (1,5) (points [1, 5])
- **dyad_2_5**: 2-point practical ward+late (2,5) (points [2, 5])

## Cohort-level readout
| scenario    | scenario_label                    | blood_points   |   processed_count |   included_count |   excluded_count |   fit_failure_count | top_exclusion_reasons                                                                                |   method1_mean_limit_gbq |   method1_median_limit_gbq |   method2_mean_limit_gbq |   method2_median_limit_gbq |   m1_median_abs_diff_vs_base_gbq |   m1_median_pct_diff_vs_base |   m2_median_abs_diff_vs_base_gbq |   m2_median_pct_diff_vs_base |   major_disagreement_stability_ratio |
|:------------|:----------------------------------|:---------------|------------------:|-----------------:|-----------------:|--------------------:|:-----------------------------------------------------------------------------------------------------|-------------------------:|---------------------------:|-------------------------:|---------------------------:|---------------------------------:|-----------------------------:|---------------------------------:|-----------------------------:|-------------------------------------:|
| dyad_1_5    | 2-point early/late (1,5)          | 1,5            |                26 |                3 |               23 |                   0 | missing_sample_point_5:20; missing_base_inputs:3                                                     |                  7.9068  |                    7.37703 |                  67.0874 |                    67.1767 |                        0.101785  |                     1.36097  |                      6.37976e-05 |                  9.09588e-05 |                                    1 |
| dyad_2_5    | 2-point practical ward+late (2,5) | 2,5            |                26 |                3 |               23 |                   0 | missing_sample_point_5:20; missing_base_inputs:3                                                     |                  7.85771 |                    7.49588 |                  67.0873 |                    67.1768 |                        0.0170621 |                     0.228139 |                      8.29953e-05 |                  0.000125231 |                                    1 |
| full_5pt    | Full baseline (5 blood samples)   | 1,2,3,4,5      |                26 |                3 |               23 |                   0 | missing_sample_point_4:13; missing_sample_point_5:6; missing_base_inputs:3; missing_sample_point_3:1 |                  7.86998 |                    7.47882 |                  67.0873 |                    67.1768 |                        0         |                     0        |                      0           |                  0           |                                    1 |
| triad_1_3_5 | 3-point early/mid/late (1,3,5)    | 1,3,5          |                26 |                3 |               23 |                   0 | missing_sample_point_5:19; missing_base_inputs:3; missing_sample_point_3:1                           |                  7.872   |                    7.41379 |                  67.0874 |                    67.1767 |                        0.0650324 |                     0.869554 |                      6.18357e-05 |                  8.81615e-05 |                                    1 |
| triad_2_3_5 | 3-point mid/late (2,3,5)          | 2,3,5          |                26 |                3 |               23 |                   0 | missing_sample_point_5:19; missing_base_inputs:3; missing_sample_point_3:1                           |                  7.83062 |                    7.49986 |                  67.0873 |                    67.1768 |                        0.0210392 |                     0.281317 |                      3.63107e-05 |                  5.17695e-05 |                                    1 |

## Best reduced schedule (by conservative combined median % drift)
- **dyad_2_5** (2-point practical ward+late (2,5)) with combined median % drift = 0.23%

## Conservative interpretation
- Prefer schedules that keep both Method 1 and Method 2 median percent drift low and preserve major-disagreement case identity.
- 2-point schedules are operationally attractive but can be less stable in individual cases.
- Results are suitable for manuscript discussion as sensitivity analysis, not as replacement of baseline protocol without prospective confirmation.