import json
from pathlib import Path
import numpy as np
import pandas as pd

INPUT_XLSX = Path('Data - Full.xlsx')  # validation/parity workbook with required retained WB fields
METHOD12_INPUT = Path('reports/sampling_sensitivity/patient_level_results.csv')
OUT_DIR = Path('reports/wb_retention_benchmark')

METHOD_NAME = 'wb_retention_benchmark_v0'
METHOD_FAMILY = 'whole_body_retention'
METHOD_VERSION = 'v0'

SOURCE_LOCKED_STATUS = 'source_locked'  # reuses Method-1 whole-body retention/planning pathway already present in workbook
IMPLEMENTATION_DEFAULT_STATUS = 'implementation_default'  # benchmark extraction from existing validated WB pathway
PROVISIONAL_STATUS = 'provisional'  # benchmark/comparator framing only, not new clinical standard


def _as_patient_id(v):
    if pd.isna(v):
        return None
    try:
        fv = float(v)
        if fv.is_integer():
            return str(int(fv))
    except Exception:
        pass
    return str(v)


def load_wb_inputs() -> pd.DataFrame:
    df = pd.read_excel(INPUT_XLSX, sheet_name='Inputs-new')

    needed = [
        'Patient UR',
        'LOGEST Normalised (m) WB',
        'LOGEST Normalised (b) WB',
        'Half Life WB (Bio + Phys) (h)',
        'Residence Time (h) WB',
        'LUNGS (GBq)',
        'Injected Activity- Based on deay correction PET measurement (MBq)',
        'WB Activity 1',
        'WB Activity 2',
        'WB Activity 3',
        'WB Activity 4',
        'WB Activity 5',
    ]

    wb = df[needed].copy()
    wb['patient_ur'] = wb['Patient UR'].apply(_as_patient_id)

    wb = wb[wb['patient_ur'].notna()].copy()

    wb['method_name'] = METHOD_NAME
    wb['method_family'] = METHOD_FAMILY
    wb['method_version'] = METHOD_VERSION

    wb['source_lock_status'] = SOURCE_LOCKED_STATUS
    wb['implementation_status'] = IMPLEMENTATION_DEFAULT_STATUS
    wb['provisional_status'] = PROVISIONAL_STATUS

    wb['benchmark_activity_limit_gbq'] = pd.to_numeric(wb['LUNGS (GBq)'], errors='coerce')
    wb['fit_success'] = (
        wb['benchmark_activity_limit_gbq'].notna()
        & pd.to_numeric(wb['Residence Time (h) WB'], errors='coerce').notna()
        & pd.to_numeric(wb['LOGEST Normalised (m) WB'], errors='coerce').notna()
        & pd.to_numeric(wb['LOGEST Normalised (b) WB'], errors='coerce').notna()
    )

    wb['invalid_reason'] = np.where(
        wb['fit_success'],
        '',
        'missing_wb_retention_or_limit_inputs'
    )

    wb['notes'] = np.where(
        wb['fit_success'],
        'Whole-body retention/planning benchmark only; excludes blood/marrow and lesion/image terms.',
        'Invalid benchmark output due to missing required whole-body retained activity/planning fields.'
    )

    return wb


def load_method12_baseline() -> pd.DataFrame:
    m = pd.read_csv(METHOD12_INPUT)
    m = m[m['scenario'] == 'full_5pt'].copy()
    m['patient_ur'] = m['patient_ur'].apply(_as_patient_id)
    return m[['patient_ur', 'method1_limit_gbq', 'method2_limit_gbq']]


def method1_driver_label(row, tol_pct=1.0):
    m1 = row.get('method1_limit_gbq')
    wb = row.get('benchmark_activity_limit_gbq')
    if pd.isna(m1) or pd.isna(wb) or m1 <= 0:
        return 'indeterminate'

    pct = abs(m1 - wb) / m1 * 100.0
    if pct <= tol_pct:
        return 'near_equal_or_mixed'
    if m1 < wb:
        return 'blood_or_marrow_dominated'
    if m1 > wb:
        return 'whole_body_planning_dominated'
    return 'indeterminate'


def run():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    wb = load_wb_inputs()
    m12 = load_method12_baseline()

    patient_level = wb[[
        'patient_ur',
        'method_name',
        'method_family',
        'method_version',
        'fit_success',
        'LOGEST Normalised (m) WB',
        'LOGEST Normalised (b) WB',
        'Half Life WB (Bio + Phys) (h)',
        'Residence Time (h) WB',
        'benchmark_activity_limit_gbq',
        'WB Activity 1',
        'WB Activity 2',
        'WB Activity 3',
        'WB Activity 4',
        'WB Activity 5',
        'source_lock_status',
        'implementation_status',
        'provisional_status',
        'notes',
        'invalid_reason',
    ]].copy()

    patient_level.to_csv(OUT_DIR / 'patient_level_wb_retention_benchmark_v0.csv', index=False)

    valid = patient_level[patient_level['fit_success']].copy()
    processed = patient_level[patient_level['patient_ur'].notna()].copy()
    cohort_summary = pd.DataFrame([{
        'method_name': METHOD_NAME,
        'processed_count': int(processed.shape[0]),
        'valid_count': int(valid.shape[0]),
        'invalid_count': int(processed.shape[0] - valid.shape[0]),
        'mean_benchmark_activity_limit_gbq': valid['benchmark_activity_limit_gbq'].mean(),
        'median_benchmark_activity_limit_gbq': valid['benchmark_activity_limit_gbq'].median(),
        'source_lock_status': SOURCE_LOCKED_STATUS,
        'implementation_status': IMPLEMENTATION_DEFAULT_STATUS,
        'provisional_status': PROVISIONAL_STATUS,
    }])
    cohort_summary.to_csv(OUT_DIR / 'cohort_summary_wb_retention_benchmark_v0.csv', index=False)

    # Comparisons with method1/method2 baselines
    comp = valid[['patient_ur', 'benchmark_activity_limit_gbq']].merge(m12, on='patient_ur', how='inner')

    c1 = comp.copy()
    c1['abs_diff_gbq'] = (c1['method1_limit_gbq'] - c1['benchmark_activity_limit_gbq']).abs()
    c1['pct_diff_vs_method1'] = np.where(c1['method1_limit_gbq'] > 0, 100.0 * c1['abs_diff_gbq'] / c1['method1_limit_gbq'], np.nan)
    c1.to_csv(OUT_DIR / 'comparison_method1_vs_wb_retention_benchmark_v0.csv', index=False)

    c2 = comp.copy()
    c2['abs_diff_gbq'] = (c2['method2_limit_gbq'] - c2['benchmark_activity_limit_gbq']).abs()
    c2['pct_diff_vs_method2'] = np.where(c2['method2_limit_gbq'] > 0, 100.0 * c2['abs_diff_gbq'] / c2['method2_limit_gbq'], np.nan)
    c2.to_csv(OUT_DIR / 'comparison_method2_vs_wb_retention_benchmark_v0.csv', index=False)

    # Method-1 driver/dominance proxy from final method1 vs WB benchmark
    dom = comp.copy()
    dom['dominance_label'] = dom.apply(method1_driver_label, axis=1)
    dom.to_csv(OUT_DIR / 'method1_driver_dominance_vs_wb_benchmark.csv', index=False)

    dom_counts = dom['dominance_label'].value_counts(dropna=False).to_dict()

    manifest = {
        'method_name': METHOD_NAME,
        'method_family': METHOD_FAMILY,
        'method_version': METHOD_VERSION,
        'status': {
            'source_lock_status': SOURCE_LOCKED_STATUS,
            'implementation_status': IMPLEMENTATION_DEFAULT_STATUS,
            'provisional_status': PROVISIONAL_STATUS,
        },
        'inputs': {
            'workbook': str(INPUT_XLSX),
            'method1_method2_baseline': str(METHOD12_INPUT),
        },
        'outputs': {
            'patient_level': 'patient_level_wb_retention_benchmark_v0.csv',
            'cohort_summary': 'cohort_summary_wb_retention_benchmark_v0.csv',
            'comparison_method1_vs_wb': 'comparison_method1_vs_wb_retention_benchmark_v0.csv',
            'comparison_method2_vs_wb': 'comparison_method2_vs_wb_retention_benchmark_v0.csv',
            'method1_driver_dominance': 'method1_driver_dominance_vs_wb_benchmark.csv',
            'report': 'wb_retention_benchmark_report.md',
        },
    }
    (OUT_DIR / 'index.json').write_text(json.dumps(manifest, indent=2))

    report_lines = [
        '# WB retention benchmark report (`wb_retention_benchmark_v0`)',
        '',
        'This benchmark is a **whole-body retention/planning benchmark only**.',
        'It is **not a marrow method** and **not a lesion/image method**.',
        '',
        '## Status labeling',
        f'- source_lock_status: `{SOURCE_LOCKED_STATUS}`',
        f'- implementation_status: `{IMPLEMENTATION_DEFAULT_STATUS}`',
        f'- provisional_status: `{PROVISIONAL_STATUS}`',
        '',
        '## Cohort summary',
        cohort_summary.to_markdown(index=False),
        '',
        '## Method comparisons',
        f"- Method 1 vs WB benchmark pairs: {len(c1)}",
        f"- Method 2 vs WB benchmark pairs: {len(c2)}",
        '',
        '### Method 1 vs WB benchmark (GBq)',
        f"- median absolute difference: {c1['abs_diff_gbq'].median():.6g}" if len(c1) else '- median absolute difference: NA',
        f"- median percent difference vs Method 1: {c1['pct_diff_vs_method1'].median():.6g}%" if len(c1) else '- median percent difference: NA',
        '',
        '### Method 2 vs WB benchmark (GBq)',
        f"- median absolute difference: {c2['abs_diff_gbq'].median():.6g}" if len(c2) else '- median absolute difference: NA',
        f"- median percent difference vs Method 2: {c2['pct_diff_vs_method2'].median():.6g}%" if len(c2) else '- median percent difference: NA',
        '',
        '## Method 1 driver/dominance proxy',
        '- Classification based on Method 1 final limit vs WB benchmark limit (tolerance = 1%).',
        f'- Counts: {dom_counts}',
        '',
        '## Caution',
        'Method 2 comparisons remain provisional where coefficient provenance is not fully locked.',
        'This benchmark is intended as a comparator for manuscript interpretation, not as a new clinical standard.',
    ]

    (OUT_DIR / 'wb_retention_benchmark_report.md').write_text('\n'.join(report_lines))


if __name__ == '__main__':
    run()
