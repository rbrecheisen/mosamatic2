import os
import pandas as pd

DB_IKNL = "D:\\Data\\EvaClaasens\\IKNL dataset 2017-2022 KWF retrospectief 02.05.2024.xlsx"
DB_PALG = "D:\\Data\\EvaClaasens\\PALGA_retrospective 2017-2022.xlsx"
DB_INFO = "D:\\Data\\EvaClaasens\\output.xlsx"


def main():
    df_iknl = pd.read_excel(DB_IKNL, index_col='key_nkr')
    df_palg = pd.read_excel(DB_PALG, index_col='KEY_NKR')
    data = {
        'key_nkr': [],
        'excerpt_nrs': [],
    }
    for idx1, row1 in df_iknl.iterrows():
        key_nkr = idx1
        dcisbiopt = row1['dcisbiopt']
        if dcisbiopt == 1.0:
            excerpt_nrs = ''
            for idx2, row2 in df_palg.iterrows():
                if idx2 == key_nkr:
                    palgaexcerptnr = str(row2['PALGAexcerptnr'])
                    excerpt_nrs += palgaexcerptnr + '/'
            data['key_nkr'].append(key_nkr)
            data['excerpt_nrs'].append(excerpt_nrs)
            print(key_nkr)
    df = pd.DataFrame(data=data)
    df.to_excel(DB_INFO, index=False, engine='openpyxl')


if __name__ == '__main__':
    main()