from pybdm_insee.tools.dataframes import insee_modalites_as_dataframe, filter_modalites

tests = [0,4]

if 0 in tests:
    print(
    filter_modalites(
        data="A"
        )
    )

if 1 in tests:
    print(
    filter_modalites(
        data=["A", "BDM"]
        )
    )
if 2 in tests:
    print(
    filter_modalites(
        data={5:"MILLIONS_TONNES"}
        )
    )

if 3 in tests:
    print(
    filter_modalites(
        no_var=5,
        var_value="MILLIONS_TONNES"
        )
    )

if 4 in tests:
    print(
    filter_modalites(
        no_var=[2,5],
        var_value=["DECHETS_DANGEUREUX","MILLIONS_TONNES"]
        )
    )