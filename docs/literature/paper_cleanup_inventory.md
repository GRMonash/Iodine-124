# Paper cleanup inventory

Date: 2026-03-25

## A) Final PDF inventory and duplicate assessment

### Primary references (15)
- `references/blood_protocols/2008_EANM_blood_bone_marrow_guidelines.pdf`
- `references/blood_protocols/patient_approach_dosimetric_role.pdf`
- `references/whole_body/2023_EANM_whole_body_dosimetry_guidelines.pdf`
- `references/marrow/2007_Traino_S_factors_red_marrow_dosimetry.pdf`
- `references/marrow/2008_Schwartz_124I_PET_bone_marrow_dosimetry.pdf`
- `references/marrow/2010_Ferrer_three_red_marrow_dosimetry_methods.pdf`
- `references/marrow/2011_Verburg_pediatric_I131_dosimetry_AHASA.pdf`
- `references/lesion_imaging/2008_Jentzen_optimized_124I_PET_protocol.pdf`
- `references/lesion_imaging/2016_Plyku_Sgouros_organ_lesion_blood_dosimetry.pdf`
- `references/lesion_imaging/2022_Plyku_Sgouros_124I_PET_monte_carlo_methods.pdf`
- `references/lesion_imaging/2023_EANM_lesion_dosimetry_detailed.pdf`
- `references/reviews/2000_Sgouros_patient_specific_dosimetry_foundations.pdf`
- `references/reviews/I124_dosimetry_methods_review.pdf`
- `references/reviews/clinical_radionuclide_therapy_dosimetry_review.pdf`
- `references/reviews/thyroid_cancer_dosimetry_review.pdf`

### Duplicate / alternate copies (14)
- `references/duplicates/2008_Jentzen_optimized_124I_PET_protocol_duplicate.pdf`
- `references/duplicates/2008_Schwartz_124I_PET_bone_marrow_dosimetry_duplicate.pdf`
- `references/duplicates/2010_Ferrer_three_red_marrow_dosimetry_methods_duplicate.pdf`
- `references/duplicates/2016_Plyku_Sgouros_organ_lesion_blood_dosimetry_duplicate.pdf`
- `references/duplicates/2022_Plyku_Sgouros_124I_PET_monte_carlo_methods_duplicate_A.pdf`
- `references/duplicates/2022_Plyku_Sgouros_124I_PET_monte_carlo_methods_duplicate_B.pdf`
- `references/duplicates/2022_Plyku_Sgouros_124I_PET_monte_carlo_methods_duplicate_C.pdf`
- `references/duplicates/2023_EANM_lesion_dosimetry_detailed_duplicate.pdf`
- `references/duplicates/EANM_2008_blood_bone_marrow_guidelines_duplicate.pdf`
- `references/duplicates/EANM_whole_body_dosimetry_duplicate.pdf`
- `references/duplicates/I124_dosimetry_methods_review_duplicate.pdf`
- `references/duplicates/clinical_radionuclide_therapy_dosimetry_review_duplicate.pdf`
- `references/duplicates/patient_approach_dosimetric_role_duplicate.pdf`
- `references/duplicates/thyroid_cancer_dosimetry_review_duplicate.pdf`

### Unclear / manual review (1)
- `references/unclear/s00259-023-06568-8_needs_manual_title_verification.pdf`

Duplicate determination used exact SHA-256 hash and file size matching.

## B) Files moved/renamed

All root-level PDFs were moved under `references/` with standardized names and category folders:
- `references/marrow/`
- `references/whole_body/`
- `references/blood_protocols/`
- `references/lesion_imaging/`
- `references/reviews/`
- `references/duplicates/`
- `references/unclear/`

## C) Files kept as duplicates or flagged for review

- Duplicate files were retained in `references/duplicates/` for traceability.
- The single unclear-title file was isolated in `references/unclear/` for manual identification.

## D) Links/paths updated

- `references/README.md` was replaced with the new organized inventory.
- No additional markdown/pdf path references were found elsewhere in the repo during search.

## E) Remaining cleanup suggestions

1. Open and inspect `references/unclear/s00259-023-06568-8_needs_manual_title_verification.pdf` and rename with author/year/title.
2. After verification, consider deleting unneeded duplicates from `references/duplicates/`.
3. Add citation metadata (DOI, year, first author) in a structured `references/index.csv` or `references/index.md`.
