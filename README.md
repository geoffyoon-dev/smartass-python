# Smartass-python [![Version][version-badge]][version-link] [![Build Status][workflow-badge]][workflow-link] [![Coverage][coverage-badge]][coverage-link] [![MIT License][license-badge]](LICENSE.md)

Inspired by [The fuck](https://github.com/nvbn/thefuck), a great app for fixing errors in previous console commands, Smartass is an app that uses an LLM rather than a rule base to fix errors in previous console commands.


[![gif with examples][examples-link]][examples-link]

More examples:

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ damn
sudo apt-get install vim [enter/↑/↓/ctrl+c]
[sudo] password for ubuntu:
Reading package lists... Done
...
```

```bash
➜ git push
fatal: The current branch main has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin main


➜ damn
git push --set-upstream origin main [enter/↑/↓/ctrl+c]
Counting objects: 9, done.
...
```

```bash
➜ puthon
No command 'puthon' found, did you mean:
 Command 'python' from package 'python-minimal' (main)
 Command 'python' from package 'python3' (main)
zsh: command not found: puthon

➜ damn
python [enter/↑/↓/ctrl+c]
Python 3.4.2 (default, Oct  8 2014, 13:08:17)
...
```

```bash
➜ git brnch
git: 'brnch' is not a git command. See 'git --help'.

Did you mean this?
    branch

➜ damn
git branch [enter/↑/↓/ctrl+c]
* main
```

```bash
➜ lein rpl
'rpl' is not a task. See 'lein help'.

Did you mean this?
         repl

➜ damn
lein repl [enter/↑/↓/ctrl+c]
nREPL server started on port 54848 on host 127.0.0.1 - nrepl://127.0.0.1:54848
REPL-y 0.3.1
...
```

If you're not afraid of blindly running corrected commands, the
`require_confirmation` [settings](#settings) option can be disabled:

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ damn
sudo apt-get install vim
[sudo] password for ubuntu:
Reading package lists... Done
...
```

## Contents

- [Smartass-python    ](#smartass-python----)
  - [Contents](#contents)
  - [Requirements](#requirements)
        - [Back to Contents](#back-to-contents)
  - [Installation](#installation)
        - [Back to Contents](#back-to-contents-1)
  - [How it works](#how-it-works)
        - [Back to Contents](#back-to-contents-2)
  - [Settings](#settings)
        - [Back to Contents](#back-to-contents-3)
  - [License MIT](#license-mit)
        - [Back to Contents](#back-to-contents-4)

## Requirements

- python (3.5+)
- pip
- python-dev

##### [Back to Contents](#contents)

## Installation


```bash
pip install -r requirements.txt
python setup.py install
```

It is recommended that you place this command in your `.bash_profile`,
`.bashrc`, `.zshrc` or other startup script:

```bash
eval $(smartass --alias)
```

[Or in your shell config (Bash, Zsh, Fish, Powershell, tcsh).](https://github.com/nvbn/thefuck/wiki/Shell-aliases)

Changes are only available in a new shell session. To make changes immediately
available, run `source ~/.bashrc` (or your shell config file like `.zshrc`).


##### [Back to Contents](#contents)



## How it works

*Smartass* generates new commands and executes them via LLM over previous commands. The LLMs we currently support are as follows:

* `Gemini` &ndash; Google's LLM, developed by Google Deepmind and served through GCP.


##### [Back to Contents](#contents)


## Settings

Several *Smartass* parameters can be changed in the file `$XDG_CONFIG_HOME/thefuck/settings.py`
(`$XDG_CONFIG_HOME` defaults to `~/.config`):

* `require_confirmation` &ndash; requires confirmation before running new command, by default `True`;
* `wait_command` &ndash; the max amount of time in seconds for getting previous command output;
* `no_colors` &ndash; disable colored output;
* `priority` &ndash; dict with rules priorities, rule with lower `priority` will be matched first;
* `debug` &ndash; enables debug output, by default `False`;
* `history_limit` &ndash; the numeric value of how many history commands will be scanned, like `2000`;
* `alter_history` &ndash; push fixed command to history, by default `True`;
* `wait_slow_command` &ndash; max amount of time in seconds for getting previous command output if it in `slow_commands` list;
* `slow_commands` &ndash; list of slow commands;
* `excluded_search_path_prefixes` &ndash; path prefixes to ignore when searching for commands, by default `[]`.
* `provider` &ndash; LLM model provider.
* `model` &ndash; The name of LLM model for fix commands.
* `api_key` &ndash; This is the token or API key that authenticates to use the LLM API.

An example of `settings.py`:

```python
wait_command = 3
require_confirmation = True
no_colors = False
debug = False
priority = {}
history_limit = None
alter_history = True
wait_slow_command = 15
slow_commands = ['lein', 'react-native', 'gradle', './gradlew', 'vagrant']
repeat = False
instant_mode = False
env = {'LC_ALL': 'C', 'LANG': 'C', 'GIT_TRACE': '1'}
excluded_search_path_prefixes = []
provider = google
model = gemini-1.5-flash
api_key = 'i0GSp7UelXASFAIzaSyCciEmlTdYE_NEFfA'
```

Or via environment variables:

* `SMARTASS_REQUIRE_CONFIRMATION` &ndash; require confirmation before running new command, `true/false`;
* `SMARTASS_WAIT_COMMAND` &ndash; the max amount of time in seconds for getting previous command output;
* `SMARTASS_NO_COLORS` &ndash; disable colored output, `true/false`;
* `SMARTASS_PRIORITY` &ndash; priority of the rules, like `no_command=9999:apt_get=100`,
rule with lower `priority` will be matched first;
* `SMARTASS__DEBUG` &ndash; enables debug output, `true/false`;
* `SMARTASS_HISTORY_LIMIT` &ndash; how many history commands will be scanned, like `2000`;
* `SMARTASS_ALTER_HISTORY` &ndash; push fixed command to history `true/false`;
* `SMARTASS_WAIT_SLOW_COMMAND` &ndash; the max amount of time in seconds for getting previous command output if it in `slow_commands` list;
* `SMARTASS_SLOW_COMMANDS` &ndash; list of slow commands, like `lein:gradle`;
* `SMARTASS_NUM_CLOSE_MATCHES` &ndash; the maximum number of close matches to suggest, like `5`.
* `SMARTASS_EXCLUDED_SEARCH_PATH_PREFIXES` &ndash; path prefixes to ignore when searching for commands, by default `[]`.

For example:

```bash




export SMARTASS_REQUIRE_CONFIRMATION='true'
export SMARTASS_WAIT_COMMAND=10
export SMARTASS_NO_COLORS='false'
export SMARTASS_HISTORY_LIMIT='2000'
export SMARTASS_NUM_CLOSE_MATCHES='5'
export SMARTASS_PROVIDER='google'
export SMARTASS_MODEL='gemini-1.5-flash'
export SMARTASS_API_KEY='i0GSp7UelXASFAIzaSyCciEmlTdYE_NEFfA'
```

##### [Back to Contents](#contents)


## License MIT
Project License can be found [here](LICENSE.md).


[version-badge]:   https://img.shields.io/pypi/v/thefuck.svg?label=version
[version-link]:    https://pypi.python.org/pypi/thefuck/
[workflow-badge]:  https://github.com/nvbn/thefuck/workflows/Tests/badge.svg
[workflow-link]:   https://github.com/nvbn/thefuck/actions?query=workflow%3ATests
[coverage-badge]:  https://img.shields.io/coveralls/nvbn/thefuck.svg
[coverage-link]:   https://coveralls.io/github/nvbn/thefuck
[license-badge]:   https://img.shields.io/badge/license-MIT-007EC7.svg
[examples-link]:   https://s5.ezgif.com/tmp/ezgif-5-0fde38e5ad.gif
[homebrew]:        https://brew.sh/

##### [Back to Contents](#contents)