import os
import json
import pandas as pd

DF_SCORES_1 = "M:\\data\\emmymaas\\13-03-2026\\output\\defaultpipeline\\calculatescorestask\\bc_scores.xlsx"
DF_SCORES_2 = "M:\\data\\emmymaas\\23-03-2026\\output\\defaultpipeline\\calculatescorestask\\bc_scores.xlsx"
DF_SCORES_JOINED = "M:\\data\\emmymaas\\bc_scores_joined.xlsx"
DF_EMMY = "M:\\data\\emmymaas\\Database IMPACT 31-3-2026.xlsx"
DF_BC = "M:\\data\\emmymaas\\Database IMPACT BC.xlsx"


def load_scores():
    df_scores_1 = pd.read_excel(DF_SCORES_1)
    df_scores_2 = pd.read_excel(DF_SCORES_2)
    # Check that there are no overlapping file names
    for fname in df_scores_1["file"]:
        if fname in df_scores_2["file"]:
            raise RuntimeError()
    # Concatenate dataframes
    df = pd.concat([df_scores_1, df_scores_2], ignore_index=True)
    df.to_excel(DF_SCORES_JOINED, index=False)
    return df


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
    rows = df_scores[df_scores["file"].str.endswith(f"_ppn{ppn}")]
    print(rows)


def main():
    df = pd.read_excel(DF_BC, dtype={'PPN': str})
    df_scores = load_scores()
    ppn_scores = load_scores_for('2', df_scores)
    # for idx, row in df.iterrows():
    #     ppn = row['PPN']
    #     scores = load_scores_for(ppn, df_scores)


if __name__ == '__main__':
    main()