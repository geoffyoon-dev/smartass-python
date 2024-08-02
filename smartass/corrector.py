import sys
from .conf import settings
from .types import LLM
from .system import Path
from . import logs



def get_llm_import_path():
    provider = settings.get('provider')
    token = settings.get('token')
    print(token)
    

def get_corrected_commands(command):
    """Returns generator with sorted and unique corrected commands.

    :type command: smartass.types.Command
    :rtype: Iterable[smartass.types.CorrectedCommand]

    """
    get_llm_import_path()