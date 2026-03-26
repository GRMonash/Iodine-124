# Consensus AI CSV Strict Cross-Check (as of 2026-03-26)

## Scope and conservative rules used
- Cross-checked against repository assets: workbook structure (`Data - Full.xlsx`, `Data Reduced.xlsx`), repository PDF corpus, and reference list.
- De-duplicated repeated rows in the pasted CSV (the table was repeated).
- Treated **method families** as one method unless a paper clearly adds a practically new implementation step.
- Classified each paper into:
  - **A = already-doing method** (implemented or directly represented in workbook/repo workflow)
  - **B = method-family-only** (same family; useful corroboration, but no new practical method for this repo right now)
  - **C = background/review-only**
  - **D = not relevant** to I-124/I-131 thyroid dosimetry workflow in this repo
  - **E = missing but feasible method** (practical next methods that the current data can support)

## Current repo capability baseline inferred from workbook + docs
1. Patient-specific blood + whole-body retention workflow for I-124 pre-therapy leading to I-131-equivalent blood/WB constraints.
2. Serial PET timepoint handling (up to ~5 points) and serial blood counting (up to ~5 points).
3. Mono-exponential/log-linear fitting workflow for WB and blood residence and derived maximum activity.
4. A lesion/nodule dosimetry block (spherical lesion assumptions).
5. Optional Traino-style patient-mass scaling section (explicitly present as “New Bone Marrow Method”).

---

## 1) Per-paper classification table

| # | Paper (short title) | Classification | Practical cross-check note |
|---|---|---|---|
| 1 | Red bone marrow dose estimation using several internal dosimetry models... | **E** | Directly aligns with comparing RBM model variants; useful for adding side-by-side model outputs. |
| 2 | Bone Marrow Dosimetry Using 124I-PET (Schwartz et al.) | **A** | Core repo theme; blood/marrow with I-124 PET is already in active workflow family. |
| 3 | I-124 pre-therapy dosimetry ... single center experience | **B** | Supports current approach, but mainly confirms implementation family. |
| 4 | Evaluation of dosimetry ... by means of iodine-124 and PET (Eschmann et al.) | **B** | Same I-124 PET pre-therapy dosimetry family. |
| 5 | Iodine-124 PET dosimetry ... recovery coefficient in 2D and 3D modes | **E** | RC/PVE correction appears not fully operationalized in workbook; feasible extension. |
| 6 | Quantitative imaging of I-124 using PET... (Pentlow et al.) | **B** | Foundational quantification family; largely method background for current pipeline. |
| 7 | EANM Dosimetry Committee guidelines for bone marrow and whole-body dosimetry | **A** | Guideline basis for blood/WB framework already reflected in workbook structure. |
| 8 | 124I-PET dosimetry in advanced DTC: therapeutic impact | **B** | Clinical utility evidence for same method family. |
| 9 | Quantitate iodine-124 contamination in iodine-123 radiopharmaceuticals | **D** | Radiopharmacy QC topic, not therapeutic patient dosimetry workflow here. |
| 10 | Patient specific dosimetry versus whole body retention constraints... | **A** | Core “patient-specific vs limit-based” decision logic already in workbook outputs. |
| 11 | IAZA I-123/I-131/I-124 dosimetric comparison (SU-E-CAMPUS...) | **D** | Different tracer/disease context; not thyroid I-124 pre-therapy workflow. |
| 12 | Impact of different blood/image models after 177Lu-PRRT | **E** | Strong analog for model-comparison framework; feasible transplant of comparison logic. |
| 13 | I-124 Imaging and Dosimetry (Kuker et al.) | **C** | Broad review/background rather than a distinct implementable step. |
| 14 | 124I-L19SIP dosimetric PET (brain metastasis RIT) | **D** | Different agent/indication; not directly transferable operationally here. |
| 15 | 124I PET-Based 3D-RD for pediatric thyroid patient | **E** | Voxel/radiobiological 3D dosimetry not currently implemented; feasible with imaging pipeline work. |
| 16 | Toxicity spectrum of immunotherapy in advanced lung cancer | **D** | Off-topic oncology toxicity review. |
| 17 | Dosimetry-guided RAI in metastatic DTC: largest safe dose | **A** | Matches max safe activity/risk-adapted intent already present. |
| 18 | Radiation Dosimetry of Theragnostic Pairs in IAZA | **D** | IAZA theragnostics, not current thyroid pipeline. |
| 19 | Bone Marrow Dosimetry in Radioiodine (I-131) Treatment | **B** | Same marrow dosimetry family; likely confirmatory. |
| 20 | Pulmonary toxicology of PET nanoplastics in vitro | **D** | Not relevant. |
| 21 | Blood and bone marrow dosimetry in radioiodine therapy of thyroid cancer (Sgouros) | **A** | Core blood-based marrow framework already represented. |
| 22 | Simplified Blood Dose Protocols ... MTA using 124I (Jentzen et al.) | **E** | Feasible immediate protocol simplification study using existing data columns. |
| 23 | Dialysis management during 131I therapy | **D** | Clinical management niche; not a dosimetry method extension for current data. |
| 24 | New PET Tracers in lung cancer | **D** | Not relevant. |
| 25 | Effect of RAI on hematological parameters: systematic review/meta-analysis | **B** | Outcome validation context; not a new dosimetry method itself. |
| 26 | Dosimetry in Radiopharmaceutical Therapy | **C** | General review/background. |
| 27 | Standardization of I-124 by liquid scintillation methods | **D** | Metrology/standardization, not patient dosimetry workflow step. |
| 28 | Predicting toxicity in prostate radiotherapy | **D** | External disease/external beam context. |
| 29 | Red Marrow Absorbed Dose... Simplified Excel Spreadsheet | **B** | Same spreadsheet simplification family; supportive but not distinct from current style. |
| 30 | miR-124-3p exosomes... steatotic graft I/R injury | **D** | Not radioiodine dosimetry. |
| 31 | ICRP recommended methods of red bone marrow dosimetry | **C** | High-level recommendations/background framework. |
| 32 | Review of cancer immunotherapy toxicity | **D** | Not relevant. |
| 33 | Dosimetry of internal emitters | **C** | Foundational review/background. |
| 34 | Pulmonary toxicity of systemic lung cancer therapy | **D** | Not relevant. |
| 35 | 3D-RD with 124I PET for 131I therapy of thyroid cancer | **E** | Advanced voxel/radiobiological method absent in current workbook, feasible future path. |
| 36 | Blood and bone marrow dosimetry for thyroid patients prepared with rhTSH | **E** | Feasible subgroup/stratified analysis if stimulation mode metadata available. |
| 37 | Physical models and dose factors for internal dose assessment | **C** | General theory/background. |
| 38 | Comparisons of dosimetric approaches for fractionated RIT in NHL (Ferrer) | **B** | Strong model-comparison concept, but different disease/agent; method family evidence. |
| 39 | Pre-therapeutic blood dosimetry using 124-iodine; predicts blood count changes | **E** | Very actionable toxicity-correlation extension from existing blood-dose outputs. |
| 40 | Bone marrow MSC exosomal miR-124-3p in spinal cord I/R | **D** | Not relevant. |
| 41 | Radiopharmaceuticals for PET/SPECT: decade review | **C** | Broad review. |
| 42 | FAP-targeted radionuclide therapy background/opportunities | **D** | Different therapeutic domain. |
| 43 | Dosimetry and thyroid cancer: individual RAI dosage | **B** | Same individualized-dosing family; supports current paradigm. |
| 44 | Extension of BED to MIRD schema | **E** | Radiobiological/BED extension not currently operationalized; feasible later. |
| 45 | Hematologic safety of Radium-223... | **D** | Different isotope/disease; only indirect toxicity context. |
| 46 | Optimized 124I PET Dosimetry Protocol for DTC (Jentzen et al.) | **A** | Directly aligned with existing serial time-point protocol style in workbook/repo. |
| 47 | Hematologic toxicity + BM-sparing in cervical chemoradiation | **D** | External beam, unrelated treatment modality. |
| 48 | Radiation Dose Assessment for I-131 Therapy Using I-124 PET (Erdi et al.) | **A** | Core I-124-to-I-131 pre-therapy dosimetry method already central. |
| 49 | BM absorbed doses + hematologic response in 177Lu-DOTATATE | **B** | Cross-isotope model sensitivity evidence; method-family analogue. |
| 50 | First Strike personalized predictive radioiodine prescription | **B** | Same personalized prescription family; likely policy/clinical framing extension. |

---

## 2) A) Already-doing methods (implemented family)
- I-124 PET pre-therapy patient-specific dosimetry mapped to I-131 therapeutic planning.
- Blood + whole-body dosimetry with constraint-based maximum activity logic.
- Risk-adapted/personalized prescribing approach based on dosimetric limits.
- Guideline-consistent blood/WB workflow (EANM-style operational structure).
- Optimized multi-timepoint protocol family (as represented by existing serial columns and fits).

Representative papers from CSV classified in A: #2, #7, #10, #17, #21, #46, #48.

## 3) B) Method-family-only papers
These generally reinforce existing families but do not force a new distinct implementation step for this repo right now:
- #3, #4, #8, #19, #25, #29, #38, #43, #49, #50.

## 4) C) Background/review-only papers
Useful for rationale/citations, but not immediate “add-to-workbook” methods:
- #13, #26, #31, #33, #37, #41.

## 5) D) Not relevant papers
Off-topic disease areas, non-dosimetry biology, unrelated toxicity domains, or radiopharmacy QC not tied to patient I-124/I-131 workflow:
- #9, #11, #14, #16, #18, #20, #23, #24, #27, #28, #30, #32, #34, #40, #42, #45, #47.

## 6) E) Missing but feasible methods
Most practical missing methods given current data structure:
1. **Multi-model RBM comparison panel** (blood-only vs blood+image variants, with/without mass scaling).
2. **Protocol simplification analysis** (reduced blood sampling schedules and error vs full protocol).
3. **PET recovery-coefficient / partial-volume correction workflow** for lesion and possibly WB quantitation.
4. **Dose-toxicity correlation module** (predicted blood/RBM dose vs observed blood count change, where outcomes exist).
5. **3D voxel/radiobiological dosimetry pilot (3D-RD/BED)** as advanced extension.
6. **TSH-mode stratified analysis** (rhTSH vs withdrawal), if stimulation metadata are available.

Papers mapped to E: #1, #5, #12, #15, #22, #35, #36, #39, #44.

## 7) F) Single best next step (based on actual available data)
**Best next step:** implement a **“Simplified Blood Sampling Validation” module** inside the existing workbook/report pipeline.

Why this is best with current assets:
- Current workbook already has repeated serial blood counts and times plus fitted blood kinetics fields.
- This can be done immediately without new imaging segmentation or Monte Carlo infrastructure.
- It directly translates to operational benefit (fewer samples, lower burden) while preserving safety constraints.
- It is strongly supported by the CSV paper set (notably Jentzen simplified blood protocol + pre-therapeutic blood dose outcome correlations).

Minimal deliverable definition:
- For each patient with >=4 blood points, compare full-fit dose vs reduced schedules (e.g., 2- or 3-point subsets).
- Report absolute/relative error and bias at cohort level.
- Provide a conservative rule: reduced protocol only accepted if underestimation risk remains below a preset safety margin.

