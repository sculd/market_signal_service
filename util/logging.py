from google.cloud import logging

_log_name = 'market_signal'
_client = None

def set_log_name(log_name):
    global _log_name
    _log_name = log_name

def get_log_name():
    return _log_name

def _get_client():
    global _client
    if _client is None:
        _client = logging.Client()
    return _client

def get_logger(log_name=_log_name):
    return _get_client().logger(log_name)

def _print_with_severity_prefix(signal):
    print('{text}'.format(text=signal))

def _log_print_signal(signal):
    _print_with_severity_prefix(signal)
    log_name = get_log_name()
    logger = get_logger(log_name=log_name)
    logger.log_struct(signal)

def log_signal(signal):
    _log_print_signal(signal)

def list_entries():
    log_name = get_log_name()
    logger = get_logger(log_name=log_name)
    return logger.list_entries()

