import difflib as dfl
from functools import reduce
from pybdm_insee.tools.insee import _insee_data

idb_ref = "2341"

idb = _insee_data().get("idbank")
# dfl.get_close_matches(idbank, idb.idbank.unique().tolist(), n=n)

diffs = idb.idbank.map(
    lambda v: reduce(
        lambda acc, x: acc+1 if x[0] in ["+","-"] else acc,
        dfl.ndiff([str(v).zfill(9)], [idb_ref.zfill(9)]),
        0
    )
)

diffs = dfl.ndiff(
    idb.idbank.astype('str').values.tolist(),
    [idb_ref.zfill(9) for _ in range(len(idb.idbank))]
)
print(list(diffs))