# Initialize output before importing any module, that can use colorama.
from ..system import init_output

init_output()

import os  
import sys  
from .. import logs  
from ..argument_parser import Parser
from ..utils import get_installation_version
from ..shells import shell  
from .alias import print_alias
from .fix_command import fix_command


def main():
    parser = Parser()
    known_args = parser.parse(sys.argv)
    
    if known_args.help:
        parser.print_help()
        return
        
    if known_args.version:
        logs.version(get_installation_version(),
                     sys.version.split()[0], shell.info())
        return
        
        
    # It's important to check if an alias is being requested before checking if
    # `TF_HISTORY` is in `os.environ`, otherwise it might mess with subshells.
    if known_args.alias:
        print_alias(known_args)
        return
    
    
    
    if known_args.command or 'TF_HISTORY' in os.environ:
        fix_command(known_args)
        return
    
    parser.print_usage()
        
    
