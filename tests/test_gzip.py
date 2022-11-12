import pandas as pd
from pybdm_insee.tools.insee import _insee_data, DATA_PATH as dpath

paths = {
    "variables" : dpath.joinpath("202211_liste_variables_modalites.csv.gz"),
    "naf" : dpath.joinpath("naf2008-listes-completes-5-niveaux.csv.gz"),
    "idbank": dpath.joinpath("202211_correspondance_idbank_dimension.csv.gz")
}

# data = _insee_data()

# for name in paths:
#     _df = data[name]
#     _path = paths[name]
#     _df.to_csv(_path, sep =";", compression={'method': 'gzip'})


# for name in paths:
#     _df = pd.read_csv(paths[name], sep =";", compression={'method': 'gzip'})
#     print(_df)

# _df = pd.read_csv(dpath.joinpath("202211_liste_variables_modalites.csv"), sep =";")
# _df.to_csv(dpath.joinpath("202211_liste_variables_modalites.csv.gz"), sep =";", compression={'method': 'gzip'})

_df = pd.read_csv(dpath.joinpath("202211_liste_variables_modalites.csv.gz"), sep =";", compression={'method': 'gzip'})

print(_df)