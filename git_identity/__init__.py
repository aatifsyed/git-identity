import argparse
import dataclasses
import logging
from pathlib import Path
from typing import Dict

import argcomplete
import git
from dataclasses_json import DataClassJsonMixin
from xdg import xdg_config_home
from logging_actions import log_level_action


@dataclasses.dataclass
class GitIdentity(DataClassJsonMixin):
    name: str
    email: str


@dataclasses.dataclass
class Config(DataClassJsonMixin):
    identities: Dict[str, GitIdentity]


logger = logging.getLogger(__name__)

EXAMPLE_JSON = r"""{
    "identities" : {
        "alias": {
            "name": "Alex Ample",
            "email": "alexample@example.com"
        }
    }
}"""


CONFIG_FOLDER = xdg_config_home()


def set_identity(repo: git.Repo, identity: GitIdentity):
    with repo.config_writer() as repo_config:
        repo_config.set_value("user", "name", identity.name)
        repo_config.set_value("user", "email", identity.email)
        logger.debug(f"""User config for repo is now {repo_config.items_all("user")}""")


def main(config_file: Path = CONFIG_FOLDER.joinpath("git-identity.json")):
    logger.addHandler(logging.StreamHandler())

    try:
        config: Config = Config.schema().loads(config_file.read_text())
    except Exception as e:
        logger.critical(
            f"Error while reading config file: {e}.\nPlease populate {config_file.absolute()} with configuration like:\n{EXAMPLE_JSON}"
        )
        raise SystemExit

    parser = argparse.ArgumentParser(
        description=f"Configure user.name and user.email for this repository from presets defined in `{config_file.absolute()}`"
    )
    parser.add_argument("--log-level", action=log_level_action(logger), default="info")
    parser.add_argument("alias", choices=config.identities.keys())

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    logger.debug(f"Invoked with {args}")
    logger.debug(f"Using config file at {config_file.absolute()}")

    identity: GitIdentity = config.identities[args.alias]
    logger.debug(f"Selected identity {identity} from config file")

    repo = git.Repo(Path.cwd(), search_parent_directories=True)
    logger.debug(f"Using git repo {repo}")

    set_identity(repo=repo, identity=identity)
