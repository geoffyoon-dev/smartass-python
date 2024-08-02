import os
import sys
from . import logs
from .shells import shell
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
    
    
    def __init__(self, provider, model, token, client, prompt, get_new_command):
        self.provider = provider
        self.model = model
        self.token = token
        self.client = client
        self.prompt = prompt
        self.get_new_command = get_new_command
        
        
    @classmethod
    def from_path(cls, path):
        
        name = path.name[:-3]
        print(name)