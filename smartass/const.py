# -*- encoding: utf-8 -*-

class _GenConst(object):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return u'<const: {}>'.format(self._name)

KEY_UP = _GenConst('↑')
KEY_DOWN = _GenConst('↓')
KEY_CTRL_C = _GenConst('Ctrl+C')
KEY_CTRL_N = _GenConst('Ctrl+N')
KEY_CTRL_P = _GenConst('Ctrl+P')

KEY_MAPPING = {'\x0e': KEY_CTRL_N,
               '\x03': KEY_CTRL_C,
               '\x10': KEY_CTRL_P}

ACTION_SELECT = _GenConst('select')
ACTION_ABORT = _GenConst('abort')
ACTION_PREVIOUS = _GenConst('previous')
ACTION_NEXT = _GenConst('next')

DEFAULT_SETTINGS = {
    'wait_command': 3,
    'require_confirmation': True,
    'no_colors': False,
    'debug': False,
    'priority': {},
    'history_limit': None,
    'alter_history': True,
    'wait_slow_command': 15,
    'slow_commands': ['lein', 'react-native', 'gradle',
                        './gradlew', 'vagrant'],
    'repeat': False,
    'instant_mode': False,
    'env': {'LC_ALL': 'C', 'LANG': 'C', 'GIT_TRACE': '1'},
    'excluded_search_path_prefixes': [],
    
    'provider': 'google',
    'model': 'gemini-1.5-flash',
    'api_key': '',
}


ENV_TO_ATTR = {
    'SMARTASS_REQUIRE_CONFIRMATION': 'require_confirmation',
    'SMARTASS_NO_COLORS': 'no_colors',
    'SMARTASS_DEBUG': 'debug',
    'SMARTASS_PRIORITY': 'priority',
    'SMARTASS_HISTORY_LIMIT': 'history_limit',
    'SMARTASS_ALTER_HISTORY': 'alter_history',
    'SMARTASS_WAIT_SLOW_COMMAND': 'wait_slow_command',
    'SMARTASS_SLOW_COMMANDS': 'slow_commands',
    
    'SMARTASS_INSTANT_MODE': 'instant_mode',
    'SMARTASS_EXCLUDED_SEARCH_PATH_PREFIXES': 'excluded_search_path_prefixes',
    
    'SMARTASS_PROVIDER': 'provider',
    'SMARTASS_MODEL': 'model',
    'SMARTASS_API_KEY': 'api_key',
}

SETTINGS_HEADER = u"""# Smartass settings file
#
# See https://github.com/geoffyoon-dev/smartass-python#settings for more information.

"""

ARGUMENT_PLACEHOLDER = 'SMARTASS_ARGUMENT_PLACEHOLDER'

CONFIGURATION_TIMEOUT = 60

USER_COMMAND_MARK = u'\u200B' * 10

DIFF_WITH_ALIAS = 0.5



SHELL_LOGGER_SOCKET_ENV = 'SHELL_LOGGER_SOCKET'