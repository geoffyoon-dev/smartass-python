class EmptyCommand(Exception):
    """Raised when empty command passed to `smartass`."""
    
class NoRuleMatched(Exception):
    """Raised when no rule matched for some command."""

class ScriptNotInLog(Exception):
    """Script not found in log."""
    
class NoLlmProviderAPIKey(Exception):
    """API Key not found."""
    