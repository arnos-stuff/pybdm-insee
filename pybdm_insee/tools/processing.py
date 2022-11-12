from pandas import DataFrame
from .attrdict.dictionary import AttrDict
from zlib import compress, decompress
from json import dumps, loads

def parse_insee_mods(idb : DataFrame) -> AttrDict:
    insee_mods = {}

    for idx, row in idb.iterrows():
        _mods = row.list_mod.split('.')
        _root = insee_mods
        for m in _mods:
            if m in _root:
                    _root = _root[m]
            else:
                    _root[m] = {}
                    _root = _root[m]


    return AttrDict(insee_mods)


def add_idbanks(idb: DataFrame, insee_mods : AttrDict) -> AttrDict:
    for idx, row in idb.iterrows():
        _mods = row.list_mod.split('.')
        _m = insee_mods
        for m in _mods[:-1]:
            _m = _m.get(m)

        if not len(_m.get(_mods[-1])):
            _m[_mods[-1]]["_data"] = [row.idbank]
        elif _m.get(_mods[-1]) == {}:
            _m[_mods[-1]]["_data"] = [row.idbank]
        elif isinstance(_m[_mods[-1]], dict) and len(_m[_mods[-1]].keys()):
            _m[_mods[-1]]["_data"] = [row.idbank]
        else:
            _m[_mods[-1]]["_data"].append(row.idbank)
    return insee_mods

def get_dict_insee_mods(idb: DataFrame) -> AttrDict:
    mods = parse_insee_mods(idb)
    mods = add_idbanks(idb, mods)
    return mods

def write_compress_json(attrdict : AttrDict, path: str) -> None:
    cjson = compress(dumps(attrdict).encode('utf-8'))
    if path.suffix == '.cjson':
        _path = path
    else:
        _path = path
        _path.suffix = '.cjson'
    with open(path, 'wb') as fp:
        fp.write(cjson)


def read_decompress_json(path: str) -> None:
    with open(path, 'rb') as fp:
        djson = loads(decompress(fp.read()).decode('utf-8'))
    return AttrDict(djson)