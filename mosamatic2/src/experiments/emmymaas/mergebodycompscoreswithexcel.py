import os
import json
import pandas as pd

DF_SCORES_ALL = "M:\\data\\emmymaas\\defaultpipeline\\calculatescorestask\\bc_scores.xlsx"
DF_EMMY = "M:\\data\\emmymaas\\Database IMPACT 31-3-2026.xlsx"
DF_BC = "M:\\data\\emmymaas\\Database IMPACT BC.xlsx"
DF_BC_FINISHED = "M:\\data\\emmymaas\\Database IMPACT BC finished.xlsx"
COLUMN_MAPPING = "M:\\data\\emmymaas\\columnmapping.json"


def load_scores():
    df = pd.read_excel(DF_SCORES_ALL)
    return df


def load_column_mapping():
    with open(COLUMN_MAPPING, 'r') as f:
        return json.load(f)


def get_scores(identifier, row):
    if identifier in row["file"].lower():
        return {
            "sm": row["muscle_area"],
            "vat": row["vat_area"],
            "sat": row["sat_area"],
            "smra": row["muscle_ra"],
            "vatra": row["vat_ra"],
            "satra": row["sat_ra"],
        }
    return {}


def load_scores_for(ppn, df_scores):
    return df_scores[df_scores["file"].str.endswith(f"_ppn{ppn}")]


def main():
    # Read empty database Emmy for BC scores. This is the database where we need to insert
    # BC scores that can be copy-pasted to the main database. Set the index of this dataframe
    # to be the PPN column for easy setting values later
    df = pd.read_excel(DF_BC, dtype={"PPN": str})
    df = df.set_index(df["PPN"])

    # Load all BC scores
    df_scores = load_scores()

    # Load column mapping and reverse column mapping
    short2long = load_column_mapping()
    long2short = {v: k for k, v in short2long.items()}

    round_factor = 2

    for i in range(1, 110):
        
        ppn = str(i)
        ppn_scores = load_scores_for(ppn, df_scores)
        ppn_scores = ppn_scores.set_index(ppn_scores["file"])

        for idx2, row2 in ppn_scores.iterrows():
            phase = row2["file"].split("_")[0] # Either one of: Baseline, FU4m, FU8m, FU12m, FU18m, FU24m
            for column in ["muscle_area", "vat_area", "sat_area", "muscle_ra", "vat_ra", "sat_ra"]:
                short_column = long2short[f"{phase}_{column}"]
                short_column_value = ppn_scores.loc[f"{phase}_ppn{ppn}", column]
                df.loc[ppn, short_column] = round(short_column_value, round_factor)

    df.to_excel(DF_BC_FINISHED, index=False)
    print(df)


def check_output():
    pass


if __name__ == '__main__':
    main()