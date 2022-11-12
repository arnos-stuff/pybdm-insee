import pandas as pd
import json
from typing import Optional, Union, List, Dict

from pybdm_insee.tools.insee import _insee_data, DATA_PATH as dpath


def insee_modalites_as_dataframe():
    with open(dpath.joinpath('insee_modalites_2022.json'), 'r') as fp :
        mods = json.load(fp)

    data = _insee_data()
    idb = data["idbank"]

    modcols = idb.list_mod.map(lambda v: v.split('.'))

    ncols = max([len(row) for row in modcols])

    dfmod = pd.DataFrame.from_records(data=modcols, columns=[f"var{i}" for i in range(ncols)])

    dfmod["idbank"] = idb.idbank
    dfmod["family"] = idb.famille

    return dfmod

def filter_modalites(
    data : Union[str, List[str], Dict[int,str]] = [],
    no_var : Optional[Union[int, List[int]]] = None,
    var_value : Optional[Union[str, List[str]]] = None,
    block_missing : Optional[bool] = False,
    reference : pd.DataFrame = None
    ) -> pd.DataFrame:
    """
    Takes either a single column value, a list of column values, or a dictionary of column values.
    There is an option to pick the col numbers are the col values separately using two arguments (no_var, var_value)

    Args:
        data (Union[str, List, Dict]): Either the value of var0, the values of var0, var1, ..., varN (N=len(List)),
            or a dict of (index, value) pairs
        no_var (Optional[int]): a single value as a number or a list of number,
            this field is used (as an option) to specify on which columns we filter,
            cannot be used without var_value
        var_value (Optional[str]): a list of the values each specified column should take
        block_missing (Optional[bool], optional): if the function should raise in case of wrong input. Defaults to False.

    Returns:
       pd.DataFrame: the sliced dataframe filtered on the given columns & values
    """
    df = insee_modalites_as_dataframe() if reference is None else reference

    if not len(data):
        if no_var is None or var_value is None:
            if block_missing:
                raise NotImplementedError("Only two options to give data, none were used.")
            else:
                return df
        else:
            no_var = no_var if isinstance(no_var, list) else [no_var]
            var_value = var_value if isinstance(var_value, list) else [var_value]
            return df[
                eval(
                    " & ".join([
                        f"(df['var{i}'] == '{val}')" for i, val in zip(no_var, var_value)
                        ])
                    )
                ]
    else:
        if isinstance(data, str):
            return df[df.var0 == data]
        elif isinstance(data, list):
            return df[
                eval(
                    " & ".join([
                        f"(df['var{i}'] == '{val}')" for i, val in enumerate(data)
                        ])
                    )
                ]
        elif isinstance(data, dict):
            return df[
                eval(
                    " & ".join([
                        f"(df['var{i}'] == '{val}')" for i, val in data.items()
                        ])
                    )
                ]

class modalitesHelper:
    """A helper class to guide people to the right INSEE series
    """
    def __init__(
        self,
        filter_data : Union[str, List[str], Dict[int,str]] = [],
        filter_no_var : Optional[Union[int, List[int]]] = None,
        filter_var_value : Optional[Union[str, List[str]]] = None,
        block_missing : Optional[bool] = False
        ) -> pd.DataFrame:
        """
        A helper which outputs an english language explanation of what a column means and the corresponding values.
        It is possible to ask the helper 
        Takes either a single column value, a list of column values, or a dictionary of column values.
        There is an option to pick the col numbers are the col values separately using two arguments (no_var, var_value)

        Args:
            data (Union[str, List, Dict]): Either the value of var0, the values of var0, var1, ..., varN (N=len(List)),
                or a dict of (index, value) pairs
            no_var (Optional[int]): a single value as a number or a list of number,
                this field is used (as an option) to specify on which columns we filter,
                cannot be used without var_value
            var_value (Optional[str]): a list of the values each specified column should take
            block_missing (Optional[bool], optional): if the function should raise in case of wrong input. Defaults to False.

        Returns:
        pd.DataFrame: the sliced dataframe filtered on the given columns & values
        """
        self.df = filter_modalites(data=filter_data, no_var=filter_no_var, var_value=filter_var_value)
        self.descriptions = pd.read_csv(dpath.joinpath("202211_liste_variables_modalites.csv"), sep=";")

    def filter(
        self,
        data : Union[str, List[str], Dict[int,str]] = [],
        no_var : Optional[Union[int, List[int]]] = None,
        var_value : Optional[Union[str, List[str]]] = None,
        block_missing : Optional[bool] = False
        ) -> pd.DataFrame:
        """
        Allows for recursive filtering of the dataframe to help people narrow down the options

        Args:
            data (Union[str, List[str], Dict[int,str]], optional): Similar to `filter_modalites`. Defaults to [].
            no_var (Optional[Union[int, List[int]]], optional): Similar to `filter_modalites`. Defaults to None.
            var_value (Optional[Union[str, List[str]]], optional): Similar to `filter_modalites`. Defaults to None.
            block_missing (Optional[bool], optional): Similar to `filter_modalites`. Defaults to False.

        Returns:
            pd.DataFrame: returns self to allow chaining (hlp.filter(..).filter(..) etc)
        """
        self.df = filter_modalites(data=data, no_var=no_var, var_value=var_value, reference=self.df)

        return self

    def reset(self):
        self.df = insee_modalites_as_dataframe()

    def to_dataframe(self):
        return self.df

    def ask_column_values(self, numbers : Union[int, List[int]]):
        if isinstance(numbers, int):
            col = self.df[f"var{numbers}"]
            values = col.unique().tolist()
            return values
        elif isinstance(numbers, list):
            return {
                nb: self.df[f"var{nb}"].values.uniques().to_list() for nb in numbers
            }
    
    def ask_column_desc_by_name(self, name : str):
        desc = self.descriptions[self.descriptions.MOD_CODE == name].MOB_LIBEN
        return desc if desc.size > 1 else desc.item()

    def ask_column_desc_by_number(self, nb : int):
        names = self.ask_column_values(nb)
        desc = self.descriptions.loc[self.descriptions.MOD_CODE.isin(names), ["MOD_CODE", "MOB_LIBEN"]]
        return desc

    def ask_desc(self, _input : Union[str, int]):
        return self.ask_column_desc_by_name(_input) if isinstance(_input, str) else self.ask_column_desc_by_number(_input)

    def ask(self, query : Union[str, int, Dict[Union[str, int], str]]):
        """_summary_

        Args:
            query (Union[str, int, Dict[Union[str, int], str]]): A dict with either names or numbers as keys, and as a value
                whether one wants help on the values the column takes or the description. Accepts a single number or name aswell.
        """
        if isinstance(query, str):
            return self.ask_column_desc_by_name(query)
        elif isinstance(query, int):
            return self.ask_column_values(query)
        elif isinstance(query, dict):
            is_asking_names = (lambda k,v :  False if isinstance(k,str) else v not in ['d','desc', 'description'])
            return { k : self.ask_column_values(k) if is_asking_names(k,v) else self.ask(k) for k,v in query.items() }