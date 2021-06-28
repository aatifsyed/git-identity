import logging
from pathlib import Path

import git
import git_identity as subject
import pytest

logger = logging.getLogger(__name__)


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    git.Repo.init(tmp_path)
    return tmp_path


def test_example_is_valid():
    config: subject.Config = subject.Config.schema().loads(subject.EXAMPLE_JSON)
    assert config.identities["alias"] == subject.GitIdentity(
        name="Alex Ample", email="alexample@example.com"
    )


def test_configured(tmp_repo: Path):
    repo = git.Repo(tmp_repo)
    with pytest.raises(
        Exception, match="No section: 'user'"
    ), repo.config_reader() as repo_config:
        repo_config.get_value("user", "name")
        repo_config.get_value("user", "email")

    subject.set_identity(repo=repo, identity=subject.GitIdentity("hello", "world"))

    with repo.config_reader() as repo_config:
        name = repo_config.get_value("user", "name")
        email = repo_config.get_value("user", "email")
        assert name == "hello"
        assert email == "world"
