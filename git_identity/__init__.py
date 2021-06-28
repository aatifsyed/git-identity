import argparse
import dataclasses
import logging
from pathlib import Path
from typing import Dict

import argcomplete
import git
from dataclasses_json import DataClassJsonMixin
from xdg import xdg_config_home


@dataclasses.dataclass(frozen=True)
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
        logger.debug(f"""{repo_config.items_all("user")=}""")


def main(config_file: Path = CONFIG_FOLDER.joinpath("git-identity.json")):
    try:
        config: Config = Config.schema().loads(config_file.read_text())
    except Exception as e:
        logger.critical(
            f"Error while reading config file: {e}.\nPlease populate {config_file.absolute()} with configuration like:\n{EXAMPLE_JSON}"
        )
        raise SystemExit

    parser = argparse.ArgumentParser(
        description="Configure user.name and user.email for this repository"
    )
    parser.add_argument(
        "-l",
        "--log-level",
        type=lambda s: getattr(logging, s.upper()),
        default=logging.INFO,
    )
    parser.add_argument(
        "alias",
        choices=config.identities.keys(),
    )

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s %(levelname)5s %(name)s: %(message)s",
        datefmt="%H:%M",
    )

    logger.debug(f"{args=}")
    logger.debug(f"{config_file.absolute()=}")

    identity: GitIdentity = config.identities[args.alias]
    logger.debug(f"{identity=}")

    repo = git.Repo(Path.cwd(), search_parent_directories=True)
    logger.debug(f"{repo=}")

    set_identity(repo=repo, identity=identity)
