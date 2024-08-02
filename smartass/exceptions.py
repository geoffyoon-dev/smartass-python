class EmptyCommand(Exception):
    """Raised when empty command passed to `thefuck`."""

class ScriptNotInLog(Exception):
    """Script not found in log."""