import os
import pandas as pd
from scipy.stats import ttest_rel

BC_SCORES_FILE_PATH = 'M:\\data\\contrastsensitivity\\lieke\\output\\defaultpipeline\\calculatescorestask\\bc_scores.csv'
BC_SCORES_UNENHANCED_FILE_PATH = 'M:\\data\\contrastsensitivity\\lieke\\output\\bc_scores_unenhanced.xlsx'
BC_SCORES_ARTERIAL_FILE_PATH = 'M:\\data\\contrastsensitivity\\lieke\\output\\bc_scores_arterial.xlsx'
BC_SCORES_VENOUS_FILE_PATH = 'M:\\data\\contrastsensitivity\\lieke\\output\\bc_scores_venous.xlsx'

def load_data():
    df = pd.read_csv(BC_SCORES_FILE_PATH, sep=';')
    df = df.assign(patient_id=df['file'].str.split('_').str[0])
    return df

def load_scores_unenhanced(df):
    return df[df["file"].str.contains("unenhanced", case=False, na=False)].copy()

def load_scores_arterial(df):
    return df[df["file"].str.contains("arterial", case=False, na=False)].copy()

def load_scores_venous(df):
    return df[df["file"].str.contains("venous", case=False, na=False)].copy()

def align_on_common_patients(*dfs):
    common = set(dfs[0]["patient_id"])
    for d in dfs[1:]:
        common &= set(d["patient_id"])
    return [d[d["patient_id"].isin(common)].copy() for d in dfs], common

def ttest(df1, df2, column):
    t_stat, p_value = ttest_rel(df1[column], df2[column], nan_policy='omit')
    print(f'[{column}] t = {t_stat:.3f}, p-value = {p_value:.3g}')
    return t_stat, p_value

def print_ttest_results(df_venous, df_unenhanced, df_arterial):
    print('\nUnenhanced -> venous:')
    ttest(df_unenhanced, df_venous, column='muscle_ra')
    ttest(df_unenhanced, df_venous, column='muscle_area')
    ttest(df_unenhanced, df_venous, column='vat_area')
    ttest(df_unenhanced, df_venous, column='vat_ra')
    ttest(df_unenhanced, df_venous, column='sat_area')
    ttest(df_unenhanced, df_venous, column='sat_ra')
    print('\nArterial -> venous:')
    ttest(df_arterial, df_venous, column='muscle_ra')
    ttest(df_arterial, df_venous, column='muscle_area')
    ttest(df_arterial, df_venous, column='vat_area')
    ttest(df_arterial, df_venous, column='vat_ra')
    ttest(df_arterial, df_venous, column='sat_area')
    ttest(df_arterial, df_venous, column='sat_ra')

def create_scatter_plots(df_venous, df_unenhanced, df_arterial):
    pass

def save_dfs(df_venous, df_unenhanced, df_arterial):
    df_venous.to_excel(BC_SCORES_VENOUS_FILE_PATH, engine='openpyxl')
    df_unenhanced.to_excel(BC_SCORES_UNENHANCED_FILE_PATH, engine='openpyxl')
    df_arterial.to_excel(BC_SCORES_ARTERIAL_FILE_PATH, engine='openpyxl')

def main():
    df = load_data()
    df_venous = load_scores_venous(df)
    df_smallest = df_venous
    df_unenhanced = load_scores_unenhanced(df)
    if df_unenhanced.shape[0] < df_smallest.shape[0]:
        df_smallest = df_unenhanced
    df_arterial = load_scores_arterial(df)
    if df_arterial.shape[0] < df_smallest.shape[0]:
        df_smallest = df_arterial
    (dfs_aligned, common_ids) = align_on_common_patients(df_venous, df_unenhanced, df_arterial)
    df_venous, df_unenhanced, df_arterial = dfs_aligned
    print_ttest_results(
        df_venous, df_unenhanced, df_venous)
    create_scatter_plots(
        df_venous, df_unenhanced, df_venous)
    save_dfs(df_venous, df_unenhanced, df_venous)

if __name__ == '__main__':
    main()