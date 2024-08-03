import os
import sys
from . import logs
from .shells import shell
from .conf import settings, load_source
from .exceptions import EmptyCommand
from .utils import format_raw_script
from .output_readers import get_output


class Command(object):
    """Command that should be fixed."""

    def __init__(self, script, output):
        """Initializes command with given values.

        :type script: basestring
        :type output: basestring

        """
        self.script = script
        self.output = output

    @property
    def stdout(self):
        logs.warn('`stdout` is deprecated, please use `output` instead')
        return self.output

    @property
    def stderr(self):
        logs.warn('`stderr` is deprecated, please use `output` instead')
        return self.output

    @property
    def script_parts(self):
        if not hasattr(self, '_script_parts'):
            try:
                self._script_parts = shell.split_command(self.script)
            except Exception:
                logs.debug(u"Can't split command script {} because:\n {}".format(
                    self, sys.exc_info()))
                self._script_parts = []

        return self._script_parts

    def __eq__(self, other):
        if isinstance(other, Command):
            return (self.script, self.output) == (other.script, other.output)
        else:
            return False

    def __repr__(self):
        return u'Command(script={}, output={})'.format(
            self.script, self.output)

    def update(self, **kwargs):
        """Returns new command with replaced fields.

        :rtype: Command

        """
        kwargs.setdefault('script', self.script)
        kwargs.setdefault('output', self.output)
        return Command(**kwargs)

    @classmethod
    def from_raw_script(cls, raw_script):
        """Creates instance of `Command` from a list of script parts.

        :type raw_script: [basestring]
        :rtype: Command
        :raises: EmptyCommand

        """
        script = format_raw_script(raw_script)
        if not script:
            raise EmptyCommand

        expanded = shell.from_shell(script)
        output = get_output(script, expanded)
        return cls(expanded, output)


class LLM(object):
    
    
    def __init__(self, provider, model, client, get_new_commands):
        self.provider = provider
        self.model = model
        self.client = client
        self.get_new_commands = get_new_commands
        
        
    @classmethod
    def from_path(cls, path):
        module_name = path.name[:-3]
        rule_module = load_source(module_name, str(path))
        
        provider = settings.provider
        model = settings.model
        api_key = settings.api_key
        client = rule_module.create_client(model, api_key)
        get_new_commands = rule_module.get_new_commands
        
        return cls(provider, model, client, get_new_commands)
        
    def get_corrected_commands(self, command):
        """Returns generator with corrected commands.

        :type command: Command
        :rtype: Iterable[CorrectedCommand]

        """
        new_commands = self.get_new_commands(self.client, command)
        if not isinstance(new_commands, list):
            new_commands = (new_commands,)
        for new_command in new_commands:
            yield CorrectedCommand(script=new_command.get('command', command.script),
                                   side_effect=None,
                                   priority=new_command.get('priority', 1))
            
            

class CorrectedCommand(object):
    """Corrected by rule command."""

    def __init__(self, script, side_effect, priority):
        """Initializes instance with given fields.

        :type script: basestring
        :type side_effect: (Command, basestring) -> None
        :type priority: int

        """
        self.script = script
        self.side_effect = side_effect
        self.priority = priority

    def __eq__(self, other):
        """Ignores `priority` field."""
        if isinstance(other, CorrectedCommand):
            return (other.script, other.side_effect) == \
                   (self.script, self.side_effect)
        else:
            return False

    def __hash__(self):
        return (self.script, self.side_effect).__hash__()

    def __repr__(self):
        return u'CorrectedCommand(script={}, side_effect={}, priority={})'.format(
            self.script, self.side_effect, self.priority)

    def _get_script(self):
        """Returns fixed commands script.

        If `settings.repeat` is `True`, appends command with second attempt
        of running fuck in case fixed command fails again.

        """
        if settings.repeat:
            repeat_fuck = '{} --repeat {}--force-command {}'.format(
                get_alias(),
                '--debug ' if settings.debug else '',
                shell.quote(self.script))
            return shell.or_(self.script, repeat_fuck)
        else:
            return self.script

    def run(self, old_cmd):
        """Runs command from rule for passed command.

        :type old_cmd: Command

        """
        if self.side_effect:
            self.side_effect(old_cmd, self.script)
        if settings.alter_history:
            shell.put_to_history(self.script)
        # This depends on correct setting of PYTHONIOENCODING by the alias:
        logs.debug(u'PYTHONIOENCODING: {}'.format(
            os.environ.get('PYTHONIOENCODING', '!!not-set!!')))

        sys.stdout.write(self._get_script())