import click
import json
import difflib

from pybdm_insee.tools.insee import (
    process_xml_output,
    insee_bdm_get, process_xml_output,
    _insee_data, idb_exists
)


obj = process_xml_output(insee_bdm_get("001656506"))
df = pd.DataFrame.from_records(obj["series"])

def echo_json_pager(json_series):
    def _generate_output():
        for row in json_series:
            yield row
    click.echo_via_pager(_generate_output())

@click.group()
def cli():
    pass

@click.command()
def ask():
    click.echo('Nothing :/')

@click.command()
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
    """, , type=click.STRING)
@click.option('--clifmt', default="df", help='What format to print in the terminal', type=click.STRING)
@click.option('--format', default="csv", help='Whether to store the result as csv, json or pickle', type=click.STRING)
@click.option('--sep', default=";", help='If output is csv, separator to use.', type=click.STRING)
@click.option('--ask', is_flag=True, default=False, 'Whether to run the `ask` command if you input wrong information.')
def fetch(idbank, mod, out, clifmt, format, sep, ask):
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


cli.add_command(fetch)
cli.add_command(ask)

if __name__ == "__main__":
    cli()