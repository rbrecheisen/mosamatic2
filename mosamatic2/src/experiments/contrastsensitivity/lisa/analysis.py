import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel, linregress


BC_SCORES_FILE_PATH = 'M:\\data\\contrastsensitivity\\lisavalidation\\output\\defaultpipeline\\calculatescorestask\\bc_scores.csv'
COEFFICIENT_FILE_PATH = 'M:\\data\\contrastsensitivity\\lieke\\output\\coefficients.json'


# LOADING DATA

def load_scores():
    # Format: L3_MUMC-LIV-001_unenhanced.dcm
    df = pd.read_csv(BC_SCORES_FILE_PATH, sep=';')
    df = df.assign(patient_id=df["file"].str.rsplit("_", n=1).str[0])
    return df

def load_scores_unenhanced(df):
    return df[df["file"].str.contains("unenhanced", case=False, na=False)].copy()

def load_scores_arterial(df):
    return df[df["file"].str.contains("arterial", case=False, na=False)].copy()

def load_scores_venous(df):
    return df[df["file"].str.contains("venous", case=False, na=False)].copy()

def load_coefficients():
    with open(COEFFICIENT_FILE_PATH, 'r') as f:
        return json.load(f)

# STATISTICS

def ttest(df1, df2, column):
    t_stat, p_value = ttest_rel(df1[column], df2[column], nan_policy='omit')
    print(f'[{column}] t = {t_stat:.3f}, p-value = {p_value:.3g}')
    return t_stat, p_value

# TRANSFORM

def transform_df_to_venous(df_old, coefficients):
    df_new = df_old.copy()
    for column in ['muscle_area', 'muscle_ra', 'vat_area', 'vat_ra', 'sat_area', 'sat_ra']:
        slope = coefficients[column]['slope']
        intercept = coefficients[column]['intercept']
        df_new[column] = slope * df_new[column].to_numpy() + intercept
    return df_new

# DISPLAY

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

# MAIN

def main():

    # Load BC scores for unenhanced, arterial and venous phase images
    scores = load_scores()
    scores_unenhanced = load_scores_unenhanced(scores)
    scores_arterial = load_scores_arterial(scores)
    scores_venous = load_scores_venous(scores)

    # Load regression coefficients
    coefficients = load_coefficients()
    coefficients_unenhanced = coefficients['unenhanced_to_venous']
    coefficients_arterial = coefficients['arterial_to_venous']

    # Plot raw scores and print t-test results before conversion
    # create_scatter_plots(scores_venous, scores_unenhanced, scores_arterial)
    print_ttest_results(
        scores_venous, scores_unenhanced, scores_arterial)

    # Convert unenhanced and arterial scores to venous
    scores_unenhanced_converted = transform_df_to_venous(scores_unenhanced, coefficients_unenhanced)
    scores_arterial_converted = transform_df_to_venous(scores_arterial, coefficients_arterial)

    # Plot new scores and print t-test results
    # create_scatter_plots(scores_venous, scores_unenhanced_converted, scores_arterial_converted)
    print_ttest_results(
        scores_venous, scores_unenhanced_converted, scores_arterial_converted)

if __name__ == '__main__':
    main()