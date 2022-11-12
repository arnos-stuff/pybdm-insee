import click
import json
import sys
import pandas as pd
from subprocess import call
from importlib.util import find_spec

from pybdm_insee.tools.insee import (
    process_xml_output,
    insee_bdm_get, process_xml_output,
    _insee_data, idb_exists, find_closest_idbank
)

from pybdm_insee.installs.poetry_install import run_poetry_install


obj = process_xml_output(insee_bdm_get("001656506"))
df = pd.DataFrame.from_records(obj["series"])

def echo_json_pager(json_series):
    def _generate_output():
        for row in json_series:
            yield row
    click.echo_via_pager(_generate_output())

@click.group()
def cli():
    """
    Hi ! This is a small CLI and python toolbox to help people query INSEE databases easily.
    Two commands as of the latest release:

    - ask : opens a prompt and helps the user figure out which series they are interested in through iterative querying\n
    - fetch : uses either the IDBANK identifiers, or the so-called "modality" values to identify the series, fetches them and saves or display them.
    """
    pass

@cli.command()
def ask():
    click.echo('Nothing :/')

@cli.command()
@click.argument('pkg')
def install(pkg):
    click.secho(f'Attempting to install package {pkg}...', fg="blue")
    if pkg == 'spacy':
        try:
            # cmdline = ["python", "-m", "spacy", "download", "en_core_web_md"]
            # call(cmdline, shell=True, executable=sys.executable)
            from spacy.cli.download import download
            download("en_core_web_md")
        except Exception as e:
            click.secho(f"Please install Poetry at https://python-poetry.org/docs/", fg="yellow", bold=True, err=True)
            raise e

@cli.command()
@click.option('--idbank', default=0,
    help="""
    A unique series ID used by INSEE to identify data.
    See https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=BDM&version=V1&provider=insee
    for more information. Please use other options to query using different means. If you wish to explore the datasets,
    please use the `ask` feature
    """, type=click.STRING)
@click.option('--mod', default="",
    help="""
    Each series belongs to a hierarchy of more or less 9 categories and subcategories called "modalités" (modality).
    If you know the modality's name, it restricts the number of series you might care about.
    There are two approaches which can be further specified using the `--ask` option : either you want additional information
    to narrow down series to a few idbanks, or you want a bulk query which gives you multiple tables. 
    """, type=click.STRING)
@click.option('--out', default="cli",
    help="""
    Whether you want the output to go to the console or to be stored in a file,
    Any value other than 'cli' will be taken as the path+name of the file, defaulting to csv storage.
    You can still set the 'clifmt' if your output is cli, it will simply change the way the result is displayed
    """, type=click.STRING)
@click.option('--clifmt', default="df", help='What format to print in the terminal', type=click.STRING)
@click.option('--format', default="csv", help='Whether to store the result as csv, json or pickle', type=click.STRING)
@click.option('--sep', default=";", help='If output is csv, separator to use.', type=click.STRING)
@click.option('--ask', is_flag=True, default=False, help='Whether to run the `ask` command if you input wrong information.')
def fetch(idbank, mod, out, clifmt, format, sep, ask):
    """
    This script will fetch the specified series using the INSEE BDM service using 2022 codes.
    Returns data either as csv, json or pickle for storage, or as dataframe or json for display.
    For more information: https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=BDM&version=V1&provider=insee)
    """
    if idbank != '0':
        if idb_exists(idbank):
            obj = process_xml_output(insee_bdm_get(idbank))
            df = pd.DataFrame.from_records(obj["series"])

            if clifmt == 'json':
                echo_json_pager(obj["series"])
            elif clifmt == 'df':
                click.echo(df)
            else:
                click.secho('WARNING: cli format incorrect !', fg='red', blink=True, bold=True, err=True)
                click.secho('Printing df as default..', fg='green', bold=True, err=True)
                click.echo(df)
        else:
            click.secho('WARNING: IDBANK value incorrect !', fg='red', blink=True, bold=True, err=True)
            
            if not ask:
                click.secho('NB: use either the `ask` command or the --ask flag if you want suggestions :)', fg='green', bold=True, err=True)
            else:
                matches = find_closest_idbank(idbank)
                click.secho('NB: Here are the closest 5 idbanks, use `ask` to figure what they are ;)', fg='green', bold=True, err=True)
                click.echo(matches)
    else:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

cli.add_command(fetch)
cli.add_command(ask)

if __name__ == "__main__":
    cli()