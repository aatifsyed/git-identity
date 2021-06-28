import git_identity as subject
import logging

logger = logging.getLogger(__name__)


def test_example_is_valid():
    config: subject.Config = subject.Config.schema().loads(subject.EXAMPLE_JSON)
    assert config.identities["alias"] == subject.GitIdentity(
        name="Alex Ample", email="alexample@example.com"
    )
