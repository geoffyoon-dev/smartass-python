import sys
from .conf import settings
from .types import LLM
from .system import Path
from . import logs



def get_llm_import_path(llm_provider):
    module_file_name = f'{llm_provider}.py'
    return Path(__file__).parent.joinpath('llm', module_file_name)

def organize_commands(corrected_commands):
    """Yields sorted commands without duplicates.

    :type corrected_commands: Iterable[thefuck.types.CorrectedCommand]
    :rtype: Iterable[thefuck.types.CorrectedCommand]

    """
    try:
        first_command = next(corrected_commands)
        yield first_command
    except StopIteration:
        return

    without_duplicates = {
        command for command in sorted(
            corrected_commands, key=lambda command: command.priority)
        if command != first_command}

    sorted_commands = sorted(
        without_duplicates,
        key=lambda corrected_command: corrected_command.priority)

    logs.debug(u'Corrected commands: {}'.format(
        ', '.join(u'{}'.format(cmd) for cmd in [first_command] + sorted_commands)))

    for command in sorted_commands:
        yield command

def get_corrected_commands(command):
    """Returns generator with sorted and unique corrected commands.

    :type command: smartass.types.Command
    :rtype: Iterable[smartass.types.CorrectedCommand]

    """
    llm_provider = settings.get('provider')
    llm_path = get_llm_import_path(llm_provider)
    llm = LLM.from_path(llm_path)
    
    
    corrected_commands = (
        corrected for corrected in llm.get_corrected_commands(command)
    )
    return organize_commands(corrected_commands)