import yaml, datetime
from pytz import timezone

_cfg = None

def load(filename = 'config.yaml'):
    global _cfg
    with open(filename, 'r') as ymlfile:
        _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return _cfg

def get_available_exchanges():
    if not _cfg: load()
    return _cfg['exchanges']

