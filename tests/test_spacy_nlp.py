import spacy
from pybdm_insee.tools.insee import _insee_data

idb_ref = "2341"

idb = _insee_data().get("idbank")

nlp = spacy.load("en_core_web_md")


for v in idb.head(100).idbank.values:
    tkref, tk = nlp(idb_ref), nlp(str(v))
    print(tk.similarity(tkref))