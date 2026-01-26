import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel, linregress

BC_SCORES_FILE_PATH = 'M:\\data\\contrastsensitivity\\lieke\\output\\defaultpipeline\\calculatescorestask\\bc_scores.csv'
COEFFICIENT_FILE_PATH = 'M:\\data\\contrastsensitivity\\lieke\\output\\coefficients.json'

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
    print('\nUnenhanced vs. venous:')
    ttest(df_unenhanced, df_venous, column='muscle_ra')
    ttest(df_unenhanced, df_venous, column='muscle_area')
    ttest(df_unenhanced, df_venous, column='vat_area')
    ttest(df_unenhanced, df_venous, column='vat_ra')
    ttest(df_unenhanced, df_venous, column='sat_area')
    ttest(df_unenhanced, df_venous, column='sat_ra')
    print('\nArterial vs venous:')
    ttest(df_arterial, df_venous, column='muscle_ra')
    ttest(df_arterial, df_venous, column='muscle_area')
    ttest(df_arterial, df_venous, column='vat_area')
    ttest(df_arterial, df_venous, column='vat_ra')
    ttest(df_arterial, df_venous, column='sat_area')
    ttest(df_arterial, df_venous, column='sat_ra')

def create_scatter_plots(df_venous, df_unenhanced, df_arterial):
    fig = plt.figure(figsize=(30, 15), layout='constrained')
    subfigs = fig.subfigures(nrows=1, ncols=2)
    subfigs[0].suptitle('Unenhanced vs. venous')
    axes0 = subfigs[0].subplots(3, 2, sharex=False, sharey=False)
    axes0[0, 0].scatter(x=df_unenhanced['muscle_area'], y=df_venous['muscle_area'])
    axes0[0, 0].set_xlabel('Unenhanced')
    axes0[0, 0].set_ylabel('Venous')
    axes0[0, 0].set_title('Muscle area')
    axes0[0, 1].scatter(x=df_unenhanced['muscle_ra'], y=df_venous['muscle_ra'])
    axes0[0, 1].set_xlabel('Unenhanced')
    axes0[0, 1].set_ylabel('Venous')
    axes0[0, 1].set_title('Muscle RA')
    axes0[1, 0].scatter(x=df_unenhanced['vat_area'], y=df_venous['vat_area'])
    axes0[1, 0].set_xlabel('Unenhanced')
    axes0[1, 0].set_ylabel('Venous')
    axes0[1, 0].set_title('VAT area')
    axes0[1, 1].scatter(x=df_unenhanced['vat_ra'], y=df_venous['vat_ra'])
    axes0[1, 1].set_xlabel('Unenhanced')
    axes0[1, 1].set_ylabel('Venous')
    axes0[1, 1].set_title('VAT RA')
    axes0[2, 0].scatter(x=df_unenhanced['sat_area'], y=df_venous['sat_area'])
    axes0[2, 0].set_xlabel('Unenhanced')
    axes0[2, 0].set_ylabel('Venous')
    axes0[2, 0].set_title('SAT area')
    axes0[2, 1].scatter(x=df_unenhanced['sat_ra'], y=df_venous['sat_ra'])
    axes0[2, 1].set_xlabel('Unenhanced')
    axes0[2, 1].set_ylabel('Venous')
    axes0[2, 1].set_title('SAT RA')
    subfigs[1].suptitle('Arterial vs. venous')
    axes1 = subfigs[1].subplots(3, 2, sharex=False, sharey=False)
    axes1[0, 0].scatter(x=df_arterial['muscle_area'], y=df_venous['muscle_area'])
    axes1[0, 0].set_xlabel('Arterial')
    axes1[0, 0].set_ylabel('Venous')
    axes1[0, 0].set_title('Muscle area')
    axes1[0, 1].scatter(x=df_arterial['muscle_ra'], y=df_venous['muscle_ra'])
    axes1[0, 1].set_xlabel('Arterial')
    axes1[0, 1].set_ylabel('Venous')
    axes1[0, 1].set_title('Muscle RA')
    axes1[1, 0].scatter(x=df_arterial['vat_area'], y=df_venous['vat_area'])
    axes1[1, 0].set_xlabel('Arterial')
    axes1[1, 0].set_ylabel('Venous')
    axes1[1, 0].set_title('VAT area')
    axes1[1, 1].scatter(x=df_arterial['vat_ra'], y=df_venous['vat_ra'])
    axes1[1, 1].set_xlabel('Arterial')
    axes1[1, 1].set_ylabel('Venous')
    axes1[1, 1].set_title('VAT RA')
    axes1[2, 0].scatter(x=df_arterial['sat_area'], y=df_venous['sat_area'])
    axes1[2, 0].set_xlabel('Arterial')
    axes1[2, 0].set_ylabel('Venous')
    axes1[2, 0].set_title('SAT area')
    axes1[2, 1].scatter(x=df_arterial['sat_ra'], y=df_venous['sat_ra'])
    axes1[2, 1].set_xlabel('Arterial')
    axes1[2, 1].set_ylabel('Venous')
    axes1[2, 1].set_title('SAT RA')
    plt.show()

def create_regression_coefficients(df_venous, df_unenhanced, df_arterial):
    coefficients = {
        'unenhanced_to_venous': {
            'muscle_area': {'slope': 0, 'intercept': 0},
            'muscle_ra': {'slope': 0, 'intercept': 0},
            'vat_area': {'slope': 0, 'intercept': 0},
            'vat_ra': {'slope': 0, 'intercept': 0},
            'sat_area': {'slope': 0, 'intercept': 0},
            'sat_ra': {'slope': 0, 'intercept': 0},
        },
        'arterial_to_venous': {
            'muscle_area': {'slope': 0, 'intercept': 0},
            'muscle_ra': {'slope': 0, 'intercept': 0},
            'vat_area': {'slope': 0, 'intercept': 0},
            'vat_ra': {'slope': 0, 'intercept': 0},
            'sat_area': {'slope': 0, 'intercept': 0},
            'sat_ra': {'slope': 0, 'intercept': 0},
        }
    }
    for column in ['muscle_area', 'muscle_ra', 'vat_area', 'vat_ra', 'sat_area', 'sat_ra']:
        result = linregress(x=df_unenhanced[column].to_numpy(), y=df_venous[column].to_numpy())
        coefficients['unenhanced_to_venous'][column]['slope'] = result.slope
        coefficients['unenhanced_to_venous'][column]['intercept'] = result.intercept
    for column in ['muscle_area', 'muscle_ra', 'vat_area', 'vat_ra', 'sat_area', 'sat_ra']:
        result = linregress(x=df_arterial[column].to_numpy(), y=df_venous[column].to_numpy())
        coefficients['arterial_to_venous'][column]['slope'] = result.slope
        coefficients['arterial_to_venous'][column]['intercept'] = result.intercept
    with open(COEFFICIENT_FILE_PATH, 'w') as f:
        json.dump(coefficients, f, indent=4)
    return coefficients

def transform_df_to_venous(df_old, coefficients):
    df_new = df_old.copy()
    for column in ['muscle_area', 'muscle_ra', 'vat_area', 'vat_ra', 'sat_area', 'sat_ra']:
        slope = coefficients[column]['slope']
        intercept = coefficients[column]['intercept']
        df_new[column] = slope * df_new[column].to_numpy() + intercept
    return df_new

def main():
    # Load BC scores, determine smallest df and align all dfs 
    # on common patients
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
        df_venous, df_unenhanced, df_arterial)
    coefficients = create_regression_coefficients(df_venous, df_unenhanced, df_arterial)
    df_unenhanced_new = transform_df_to_venous(df_unenhanced, coefficients['unenhanced_to_venous'])
    df_arterial_new = transform_df_to_venous(df_arterial, coefficients['arterial_to_venous'])
    print_ttest_results(
        df_venous, df_unenhanced_new, df_arterial_new)
    # create_scatter_plots(df_venous, df_unenhanced, df_arterial)

if __name__ == '__main__':
    main()