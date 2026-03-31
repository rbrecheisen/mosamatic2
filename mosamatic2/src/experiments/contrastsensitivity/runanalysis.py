import os
import pandas as pd
import pydicom
import pydicom.errors

from scipy.stats import ttest_rel, linregress


class DicomLoader:
    def load(self, f_path, stop_before_pixels=False):
        try:
            return pydicom.dcmread(f_path, stop_before_pixels=stop_before_pixels)
        except pydicom.errors.InvalidDicomError:
            return None


class ContrastSensitivityAnalysis:
    def __init__(self, train_scores_file, valid_scores_file, output_dir):
        self._train_scores_file = train_scores_file
        self._train_df = self.load_df(self._train_scores_file)
        self._valid_scores_file = valid_scores_file
        self._valid_df = self.load_df(self._valid_scores_file)
        self._output_dir = output_dir
        os.makedirs(self._output_dir, exist_ok=True)

    # LOADERS

    def load_df(self, f):
        df = pd.read_csv(f, sep=";")
        df = df.assign(patient_id=df["file"].str.split("_").str[0])
        return df
    
    def load_unenhanced_df(self, df):
        return df[df["file"].str.contains("unenhanced", case=False, na=False)].copy()

    def load_arterial_df(self, df):
        return df[df["file"].str.contains("arterial", case=False, na=False)].copy()

    def load_venous_df(self, df):
        return df[df["file"].str.contains("venous", case=False, na=False)].copy()
    
    # HELPERS
    
    def align_on_common_patients(self, *dfs):
        common = set(dfs[0]["patient_id"])
        for d in dfs[1:]:
            common &= set(d["patient_id"])
        return [d[d["patient_id"].isin(common)].copy() for d in dfs], common

    def ttest(self, df1, df2, column):
        t_stat, p_value = ttest_rel(df1[column], df2[column], nan_policy="omit")
        print(f"[{column}] t = {t_stat:.3f}, p-value = {p_value:.3g}")
        return t_stat, p_value
    
    # ANALYSIS

    def calculate_regression_coefficients(self):
        return []

    def run(self):
        coefficients = self.calculate_regression_coefficients()


def main():
    analysis = ContrastSensitivityAnalysis(
        train_scores_file="M:\\data\\contrastsensitivity\\lieke\\output\\defaultpipeline\\calculatescorestask\\bc_scores.csv",
        valid_scores_file="M:\\data\\contrastsensitivity\\lisavalidation\\output\\defaultpipeline\\calculatescorestask\\bc_scores.csv",
        output_dir="M:\\data\\contrastsensitivity\\output",
    )
    analysis.run()


if __name__ == "__main__":
    main()