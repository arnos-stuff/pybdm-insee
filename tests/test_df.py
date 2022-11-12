from pybdm_insee.tools.dataframes import insee_modalites_as_dataframe
from pybdm_insee.tools.insee import DATA_PATH as dpath

import colorama as co

co.just_fix_windows_console()
poetry 
df = insee_modalites_as_dataframe()

#df.to_csv(dpath.joinpath("insee_modalites_2022.csv"), sep = ";", index=False)

print(df)