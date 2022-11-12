import pandas as pd
import json

from pybdm_insee.tools.insee import (
    process_xml_output, _insee_idb_data_url,
    insee_bdm_get, process_xml_output, _insee_data,
    DATA_PATH as dpath
)

with open(dpath.joinpath('insee_modalites_2022.json'), 'r') as fp : mods = json.load(fp)

data = _insee_data()
idb = data["idbank"]

modcols = idb.list_mod.map(lambda v: v.split('.'))

ncols = max([len(row) for row in modcols])

dfmod = pd.DataFrame.from_records(data=modcols, columns=[f"var{i}" for i in range(ncols)])

dfmod.idbank = idb.idbank
dfmod.family = idb.famille