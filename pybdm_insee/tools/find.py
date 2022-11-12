from importlib.resources import files
from pathlib import Path

def _get_package_dir(pkg):
    return files(pkg).parent if isinstance(files(pkg), Path)\
        else files(pkg)._paths.pop().parent