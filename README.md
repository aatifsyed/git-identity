# `git-identity`
## Installation
Recommended installation is with [`pipx`](https://pypi.org/project/pipx):
```bash
pipx install git-identity
```
### Autocompletion
Autocompletion is done with [`argcomplete`](https://pypi.org/project/argcomplete/). 
Install, and add the following to your shell's startup scripts:
```bash
eval "$(register-python-argcomplete git-identity)"
```
## Configuration
This project will look for `git-identity.json` in the XDG config folder (typically `$HOME/.config/`).
```json
{
    "identities" : {
        "alias": {
            "name": "Alex Ample",
            "email": "alexample@example.com"
        }
    }
}
```
`alias` is what is used when invoking the command.
## Usage
After installation, you [may use this as a git subcommand](https://github.com/git/git/blob/670b81a890388c60b7032a4f5b879f2ece8c4558/Documentation/howto/new-command.txt) (though argcomplete only works when you invoke it as `git-identity`)
```bash
git identity <alias>
```
