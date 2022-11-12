from importlib.resources import files
from pathlib import Path
from typing import Union
from functools import cache
from lxml import etree
import pandas as pd
import requests as rq
import difflib as dfl


DATA_PATH = files("pybdm_insee").parent.joinpath("data/")\
    if isinstance(files("pybdm_insee"), Path)\
    else files("pybdm_insee")._paths.pop().parent.joinpath("data/")

def _insee_varcode_data_url(insee_row):
    
    return f"""
    https://bdm.insee.fr/series/sdmx/data/{insee_row.VAR_CODE}/.......{insee_row.MOD_CODE}.
    """

def _insee_idb_data_url(idbank: str):
    return f"""
    https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/{idbank}
    """.strip()


@cache
def _insee_data(translate=True):
    res = {
        "variables" : pd.read_csv(DATA_PATH.joinpath("202211_liste_variables_modalites.csv.gz"), sep =";", compression={'method': 'gzip'}),
        "naf" : pd.read_csv(DATA_PATH.joinpath("naf2008-listes-completes-5-niveaux.csv.gz"), sep =";", compression={'method': 'gzip'}),
        "idbank": pd.read_csv(DATA_PATH.joinpath("202211_correspondance_idbank_dimension.csv.gz"), sep =";", compression={'method': 'gzip'})
    }
    return res

def idb_exists(_idbank : str):
    _fidbank = _idbank.zfill(9)
    idb = _insee_data().get("idbank")
    return idb[idb.idbank.apply(lambda v : str(v).zfill(9)) == _fidbank].any().any()

def find_closest_idbank(idbank : str, n=5):
    idb = _insee_data().get("idbank")
    dfl.get_close_matches(idbank, idb.idbank.unique().tolist(), n=n)

def insee_get_access_token():
    r = rq.post(
        "https://api.insee.fr/token",
        data="grant_type=client_credentials",
        headers={"Authorization" : "Basic a2tEb3BGWEh0d1hXUGN1Tzh5NWJ0QlZGQWw4YTowaWZOVTA3SEtfU3VDV3lhMnlJSWQ1WFQ2TEFh"},
        )

    return r.json()['access_token']


def insee_bdm_get(idbank: Union[str, int]):
    """Tries to mimic the following cURL command:

    curl -X GET
    --header 'Accept: application/xml'
    --header 'Authorization: Bearer ce39f356-d3f3-3b99-838e-8326267d8488'
    'https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001656506'

    Args:
        idbank (Union): the idbank either str or int, will be padded to 9 chars
    """
    idbank = str(idbank).zfill(9)
    token = insee_get_access_token()

    r = rq.get(
        url=_insee_idb_data_url(idbank),
        headers={
            'Accept': 'application/xml',
            'Authorization': f'Bearer {token}'
        }
    )

    return r.text

def process_xml_output(_xmlstr : str):
    doc = etree.XML(_xmlstr.encode('utf-8'))
    ss = doc.find(".//Series")
    res = [val.items() for val in ss.iter()]
    obj = {
        "metadata":{ k:v for k,v in res[0] },
        "series":[
            {k:v for k,v in row} for row in res[1:]
        ]
    }

    return obj