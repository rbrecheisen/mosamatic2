import os
import pandas as pd


def main():
    df = pd.read_excel('C:\\Users\\r.brecheisen\\OneDrive - Maastricht University\\Research\\Documents\\Projects\\IMAGIO\\Vaughtey CT levers\\Selectie scans.xlsx', sheet_name='400 selectie')
    df_all_phases = df[(df['Procedure RIS'] == 'CT Abdomen') & (df['art'] == 1) & (df['blanco'] == 1) & (df['Pvp'] == 1)]
    print(f'Found {df_all_phases.shape[0]} rows')
    with open('accessionnumbers.txt', 'w') as f:
        for idx, row in df_all_phases.iterrows():
            f.write(row['Onderzoeksnummer'] + '\n')

if __name__ == '__main__':
    main()