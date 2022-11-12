from pybdm_insee.tools.insee import idb_exists


print([
    idb_exists("010596189"),
    idb_exists("010596204"),
    idb_exists("010586937"),
    idb_exists("010586980"),

    idb_exists("12"),
    idb_exists("4"),
    idb_exists("25422")
])