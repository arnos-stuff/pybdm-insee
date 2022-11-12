import platform
from subprocess import call
from pkgutil import iter_modules

cmdline = {
    "Linux":"curl -sSL https://install.python-poetry.org | python3 -",
    "Darwin":"curl -sSL https://install.python-poetry.org | python3 -",
    "Windows":"(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing) | python3 -"
}

def run_poetry_install():
        # call(cmdline[platform.system()], shell=True)
        pass