from pybdm_insee.tools.dataframes import modalitesHelper as modHelp

hlp = modHelp()


tests = [4]

if 0 in tests:
    print(hlp.ask_desc(0))

if 1 in tests:
    print(hlp.filter(data="S").ask_desc(2))
if 2 in tests:
    for key, answer in hlp.filter(data="S").ask(
            query = {2:"n", 3:"d", 7:"n", 8:"n", "J":"d"}
        ).items():
        print(key, answer)

if 3 in tests:
    print(hlp.ask_desc("MNHI"))

if 4 in tests:
    print(hlp.filter(no_var=3, var_value="RATIO")\
        .filter(no_var=2, var_value = "INEGALITES-REVENUS")\
        .to_dataframe()
        )
