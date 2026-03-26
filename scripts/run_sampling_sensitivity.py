import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from openpyxl import load_workbook

INPUT_XLSX = Path('Data - Full.xlsx')
OUT_DIR = Path('reports/sampling_sensitivity')

PHYS_HALF_LIFE_I131_H = 192.6048
LAMBDA_I124 = 0.006909361847686856
LAMBDA_I131 = 0.0035988053286311935
MAX_DOSE_BLOOD_GY = 2.0
MAX_DOSE_WB_GBQ = 2.96
S_BLOOD_BLOOD_GY_PER_GBQ_H = 108.0

SCENARIOS = {
    'full_5pt': {'label': 'Full baseline (5 blood samples)', 'points': [1, 2, 3, 4, 5]},
    'triad_1_3_5': {'label': '3-point early/mid/late (1,3,5)', 'points': [1, 3, 5]},
    'triad_2_3_5': {'label': '3-point mid/late (2,3,5)', 'points': [2, 3, 5]},
    'dyad_1_5': {'label': '2-point early/late (1,5)', 'points': [1, 5]},
    'dyad_2_5': {'label': '2-point practical ward+late (2,5)', 'points': [2, 5]},
}


@dataclass
class PatientBase:
    patient_ur: str
    sex: str
    weight_kg: float
    effective_mass_kg: float
    injected_mbq: float
    ref_mbq_per_ml: float
    ref_counts_decay_corrected: float
    inj_time: object
    wb_residence_h: float
    lung_limit_gbq: float


BLOOD_COLS = {
    1: ('Time Bloods Taken 1', 'Time Bloods Measured 1', 'Counts (Background Corrected) (CPM)'),
    2: ('Time Bloods Taken 2', 'Time Bloods Measured 2', 'Counts (Background Corrected) (CPM).1'),
    3: ('Time Bloods Taken 3', 'Time Bloods Measured 3', 'Counts (Background Corrected) (CPM).2'),
    4: ('Time Bloods Taken 4', 'Time Bloods Measured 4', 'Counts (Background Corrected) (CPM).3'),
    5: ('Time Bloods Taken 5', 'Time Bloods Measured 5', 'Counts (Background Corrected) (CPM).4'),
}


def load_inputs() -> pd.DataFrame:
    df = pd.read_excel(INPUT_XLSX, sheet_name='Inputs-new')
    return df


def valid_num(x):
    if pd.isna(x):
        return None
    try:
        v = float(x)
    except Exception:
        return None
    if np.isfinite(v):
        return v
    return None


def fit_log_linear(times_h: List[float], values: List[float]) -> Tuple[float, float]:
    # y = b * exp(-lambda*t)
    x = np.asarray(times_h, dtype=float)
    y = np.asarray(values, dtype=float)
    if len(x) < 2:
        raise ValueError('need_at_least_2_points')
    if np.any(y <= 0):
        raise ValueError('non_positive_activity')
    coeff = np.polyfit(x, np.log(y), 1)
    slope, intercept = coeff[0], coeff[1]
    if not np.isfinite(slope) or not np.isfinite(intercept):
        raise ValueError('fit_non_finite')
    return float(slope), float(intercept)


def method1_limit_gbq(base: PatientBase, blood_residence_h: float) -> float:
    if not np.isfinite(base.wb_residence_h) or base.wb_residence_h <= 0:
        return np.nan
    if not np.isfinite(blood_residence_h) or blood_residence_h <= 0:
        return np.nan
    mass_for_s = min(base.effective_mass_kg, base.weight_kg)
    s_blood_wb = 0.0188 * (mass_for_s ** (-2.0 / 3.0))
    dose_per_gbq = s_blood_wb * base.wb_residence_h + blood_residence_h * S_BLOOD_BLOOD_GY_PER_GBQ_H
    if dose_per_gbq <= 0:
        return np.nan
    blood_limit = MAX_DOSE_BLOOD_GY / dose_per_gbq
    return float(min(base.lung_limit_gbq, blood_limit))


def method2_traino_limit_gbq(base: PatientBase, blood_residence_h: float) -> float:
    if not np.isfinite(base.injected_mbq) or base.injected_mbq <= 0:
        return np.nan
    if not np.isfinite(base.wb_residence_h) or base.wb_residence_h <= 0:
        return np.nan
    if not np.isfinite(blood_residence_h) or blood_residence_h <= 0:
        return np.nan

    sex = str(base.sex).strip().upper()
    if sex not in {'M', 'F'}:
        return np.nan
    m_rm = 1.12 if sex == 'M' else 1.3
    m_tb = base.weight_kg
    m_TB = 73.7 if sex == 'M' else 56.912
    m_rb = m_TB - m_rm
    s_rm_rm = 0.0000155 if sex == 'M' else 0.0000141
    s_rm_tb = 0.000000629 if sex == 'M' else 0.000000772
    rmblr = 1.0

    A_bl = blood_residence_h * base.injected_mbq * 3600.0 / m_tb
    A_tb = base.wb_residence_h * base.injected_mbq * 3600.0

    dose_mgy = (
        A_bl * m_rm * rmblr * s_rm_rm
        + (A_tb - (A_bl * m_rm * (m_tb / m_TB) * rmblr))
        * (s_rm_tb * (m_TB / m_rb) - s_rm_rm * (m_rm / m_rb))
        * (m_TB / m_tb)
    )
    if dose_mgy <= 0:
        return np.nan
    max_admin_mbq = (2000.0 / dose_mgy) * base.injected_mbq
    return float(max_admin_mbq / 1000.0)


def run():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_inputs()

    patient_rows = []
    excluded_rows = []

    for idx, row in df.iterrows():
        patient_ur = row.get('Patient UR')
        if pd.isna(patient_ur):
            continue
        patient_ur = str(int(patient_ur)) if isinstance(patient_ur, (int, float, np.integer, np.floating)) and float(patient_ur).is_integer() else str(patient_ur)

        weight = valid_num(row.get('Weight (Kg)'))
        eff_mass = valid_num(row.get('Patient Effective Mass (kg)'))
        inj_mbq = valid_num(row.get('Injected Activity- Based on deay correction PET measurement (MBq)'))
        ref = valid_num(row.get('Reference Dose Activity (MBq)'))
        ref_counts = valid_num(row.get('Reference Counts (CPM)'))
        ref_vol = valid_num(row.get('Volume of Diluted Radioisotope Solution (ml)'))
        wb_res_h = valid_num(row.get('Residence Time (h) WB'))
        lung_limit = valid_num(row.get('LUNGS (GBq)'))
        inj_time = row.get('Injection Time')
        sex = row.get('Sex (M/F)')

        if eff_mass is None:
            eff_mass = weight

        if None in [weight, eff_mass, inj_mbq, ref, ref_counts, ref_vol, wb_res_h, lung_limit] or pd.isna(inj_time):
            excluded_rows.append({
                'patient_ur': patient_ur,
                'scenario': 'all',
                'reason': 'missing_base_inputs',
            })
            continue

        ref_mbq_per_ml = ref / ref_vol
        ref_counts_decay_corrected = ref_counts

        base = PatientBase(
            patient_ur=patient_ur,
            sex=str(sex),
            weight_kg=weight,
            effective_mass_kg=eff_mass,
            injected_mbq=inj_mbq,
            ref_mbq_per_ml=ref_mbq_per_ml,
            ref_counts_decay_corrected=ref_counts_decay_corrected,
            inj_time=inj_time,
            wb_residence_h=wb_res_h,
            lung_limit_gbq=lung_limit,
        )

        for scenario_key, scenario in SCENARIOS.items():
            pts = scenario['points']
            t_h = []
            c_i131 = []
            scenario_reason = None

            for p in pts:
                t_col, m_col, c_col = BLOOD_COLS[p]
                t_taken = row.get(t_col)
                t_measured = row.get(m_col)
                counts = valid_num(row.get(c_col))
                if pd.isna(t_taken) or pd.isna(t_measured) or counts is None:
                    scenario_reason = f'missing_sample_point_{p}'
                    break

                dt_h = (t_taken - inj_time).total_seconds() / 3600.0
                delay_h = (t_measured - t_taken).total_seconds() / 3600.0
                if dt_h < 0:
                    scenario_reason = f'negative_time_point_{p}'
                    break

                counts_decay = counts * np.exp(LAMBDA_I124 * delay_h)
                counts_i131 = counts_decay * np.exp(dt_h * LAMBDA_I124) * np.exp(-dt_h * LAMBDA_I131)
                activity_i131 = counts_i131 * (base.ref_mbq_per_ml / base.ref_counts_decay_corrected)

                if activity_i131 <= 0:
                    scenario_reason = f'non_positive_activity_point_{p}'
                    break

                t_h.append(dt_h)
                c_i131.append(activity_i131)

            if scenario_reason is not None:
                excluded_rows.append({'patient_ur': patient_ur, 'scenario': scenario_key, 'reason': scenario_reason})
                continue

            try:
                slope, intercept = fit_log_linear(t_h, c_i131)
            except ValueError as exc:
                excluded_rows.append({'patient_ur': patient_ur, 'scenario': scenario_key, 'reason': str(exc)})
                continue

            lambda_bio = -slope
            if lambda_bio <= 0:
                excluded_rows.append({'patient_ur': patient_ur, 'scenario': scenario_key, 'reason': 'non_positive_lambda_bio'})
                continue

            lambda_eff = lambda_bio + LAMBDA_I131
            if lambda_eff <= 0:
                excluded_rows.append({'patient_ur': patient_ur, 'scenario': scenario_key, 'reason': 'non_positive_lambda_eff'})
                continue

            b_non_norm = np.exp(intercept)
            b_norm = b_non_norm / base.injected_mbq
            residence_blood_h = b_norm / lambda_eff

            m1 = method1_limit_gbq(base, residence_blood_h)
            m2 = method2_traino_limit_gbq(base, residence_blood_h)

            patient_rows.append({
                'patient_ur': patient_ur,
                'scenario': scenario_key,
                'scenario_label': scenario['label'],
                'n_points': len(pts),
                'blood_points': ','.join(map(str, pts)),
                'blood_residence_h': residence_blood_h,
                'method1_limit_gbq': m1,
                'method2_limit_gbq': m2,
                'method1_lung_limit_gbq': base.lung_limit_gbq,
            })

    res = pd.DataFrame(patient_rows)
    exc = pd.DataFrame(excluded_rows)

    baseline = res[res['scenario'] == 'full_5pt'][['patient_ur', 'method1_limit_gbq', 'method2_limit_gbq']].rename(
        columns={'method1_limit_gbq': 'm1_base', 'method2_limit_gbq': 'm2_base'}
    )
    res = res.merge(baseline, on='patient_ur', how='left')
    res['m1_abs_diff_vs_base_gbq'] = (res['method1_limit_gbq'] - res['m1_base']).abs()
    res['m2_abs_diff_vs_base_gbq'] = (res['method2_limit_gbq'] - res['m2_base']).abs()
    res['m1_pct_diff_vs_base'] = np.where(res['m1_base'] > 0, 100.0 * res['m1_abs_diff_vs_base_gbq'] / res['m1_base'], np.nan)
    res['m2_pct_diff_vs_base'] = np.where(res['m2_base'] > 0, 100.0 * res['m2_abs_diff_vs_base_gbq'] / res['m2_base'], np.nan)

    # major disagreement stability: top quartile of |M1-M2| in full baseline
    b = res[res['scenario'] == 'full_5pt'].copy()
    b['abs_m1_m2'] = (b['method1_limit_gbq'] - b['method2_limit_gbq']).abs()
    if len(b) > 0:
        q75 = b['abs_m1_m2'].quantile(0.75)
        major_set = set(b.loc[b['abs_m1_m2'] >= q75, 'patient_ur'])
    else:
        major_set = set()

    summary_rows = []
    for scenario_key, sc in SCENARIOS.items():
        s = res[res['scenario'] == scenario_key]
        included = len(s)
        processed = len(df[df['Patient UR'].notna()])
        excl_s = exc[exc['scenario'].isin([scenario_key, 'all'])]

        overlap = set(s['patient_ur']).intersection(major_set)
        baseline_major_available = set(res.loc[res['scenario'] == 'full_5pt', 'patient_ur']).intersection(major_set)
        stability_ratio = (len(overlap) / len(baseline_major_available)) if baseline_major_available else np.nan

        summary_rows.append({
            'scenario': scenario_key,
            'scenario_label': sc['label'],
            'blood_points': ','.join(map(str, sc['points'])),
            'processed_count': processed,
            'included_count': included,
            'excluded_count': int(len(excl_s)),
            'fit_failure_count': int(excl_s[excl_s['reason'].str.contains('fit|lambda|non_positive', na=False)].shape[0]),
            'top_exclusion_reasons': '; '.join(
                [f"{k}:{v}" for k, v in excl_s['reason'].value_counts().head(5).to_dict().items()]
            ),
            'method1_mean_limit_gbq': s['method1_limit_gbq'].mean(),
            'method1_median_limit_gbq': s['method1_limit_gbq'].median(),
            'method2_mean_limit_gbq': s['method2_limit_gbq'].mean(),
            'method2_median_limit_gbq': s['method2_limit_gbq'].median(),
            'm1_median_abs_diff_vs_base_gbq': s.loc[s['scenario'] != 'full_5pt', 'm1_abs_diff_vs_base_gbq'].median() if scenario_key != 'full_5pt' else 0.0,
            'm1_median_pct_diff_vs_base': s.loc[s['scenario'] != 'full_5pt', 'm1_pct_diff_vs_base'].median() if scenario_key != 'full_5pt' else 0.0,
            'm2_median_abs_diff_vs_base_gbq': s.loc[s['scenario'] != 'full_5pt', 'm2_abs_diff_vs_base_gbq'].median() if scenario_key != 'full_5pt' else 0.0,
            'm2_median_pct_diff_vs_base': s.loc[s['scenario'] != 'full_5pt', 'm2_pct_diff_vs_base'].median() if scenario_key != 'full_5pt' else 0.0,
            'major_disagreement_stability_ratio': stability_ratio,
        })

    summary = pd.DataFrame(summary_rows)
    summary = summary.sort_values(by='scenario').reset_index(drop=True)

    # conservative best schedule by combined median percent drift
    cand = summary[summary['scenario'] != 'full_5pt'].copy()
    cand['combined_median_pct_drift'] = cand[['m1_median_pct_diff_vs_base', 'm2_median_pct_diff_vs_base']].max(axis=1)
    best = cand.sort_values(['combined_median_pct_drift', 'included_count'], ascending=[True, False]).head(1)

    OUT_DIR.mkdir(exist_ok=True, parents=True)
    res.to_csv(OUT_DIR / 'patient_level_results.csv', index=False)
    exc.to_csv(OUT_DIR / 'excluded_rows.csv', index=False)
    summary.to_csv(OUT_DIR / 'scenario_summary.csv', index=False)

    manifest = {
        'input_workbook': str(INPUT_XLSX),
        'scenarios': SCENARIOS,
        'outputs': {
            'scenario_summary': 'scenario_summary.csv',
            'patient_level': 'patient_level_results.csv',
            'excluded_rows': 'excluded_rows.csv',
            'interpretation': 'interpretation.md',
        },
    }
    (OUT_DIR / 'manifest.json').write_text(json.dumps(manifest, indent=2))

    best_row = best.iloc[0].to_dict() if len(best) else {}

    lines = []
    lines.append('# Sampling sensitivity interpretation (conservative)')
    lines.append('')
    lines.append('Method equations were kept unchanged; only blood sample subsets were varied.')
    lines.append('Whole-body inputs were preserved across all scenarios.')
    lines.append('')
    lines.append('## Scenarios tested')
    for k, v in SCENARIOS.items():
        lines.append(f"- **{k}**: {v['label']} (points {v['points']})")
    lines.append('')
    lines.append('## Cohort-level readout')
    lines.append(summary.to_markdown(index=False))
    lines.append('')
    if best_row:
        lines.append('## Best reduced schedule (by conservative combined median % drift)')
        lines.append(
            f"- **{best_row['scenario']}** ({best_row['scenario_label']}) with combined median % drift = {best_row['combined_median_pct_drift']:.2f}%"
        )
    lines.append('')
    lines.append('## Conservative interpretation')
    lines.append('- Prefer schedules that keep both Method 1 and Method 2 median percent drift low and preserve major-disagreement case identity.')
    lines.append('- 2-point schedules are operationally attractive but can be less stable in individual cases.')
    lines.append('- Results are suitable for manuscript discussion as sensitivity analysis, not as replacement of baseline protocol without prospective confirmation.')

    (OUT_DIR / 'interpretation.md').write_text('\n'.join(lines))


if __name__ == '__main__':
    run()
