from unittest import mock

import pytest

from quetz import cli
from quetz.db_models import User


@pytest.fixture
def user_group():
    return "admins"


@pytest.fixture
def config_extra(user_group):
    if user_group is None:
        return ""
    else:
        return f"""[users]
                {user_group} = ["bartosz"]
                """


@pytest.mark.parametrize(
    "user_group,expected_role",
    [("admins", "owner"), ("maintainers", "maintainer"), ("members", "member")],
)
def test_init_db(db, config, config_dir, user_group, expected_role):

    def get_db(_):
        return db

    with mock.patch("quetz.cli.get_session", get_db):
        cli.init_db(config_dir)

    user = db.query(User).filter(User.username == "bartosz").one_or_none()

    assert user

    assert user.role == expected_role
    assert user.username == "bartosz"
    assert not user.profile


@pytest.mark.parametrize("user_group", [None])
def test_init_db_no_users(db, config, config_dir, user_group):
    def get_db(_):
        return db

    with mock.patch("quetz.cli.get_session", get_db):
        cli.init_db(config_dir)

    user = db.query(User).filter(User.username == "bartosz").one_or_none()

    assert user is None


def test_init_db_user_exists(db, config, config_dir, user):
    def get_db(_):
        return db

    with mock.patch("quetz.cli.get_session", get_db):
        cli.init_db(config_dir)

    user = db.query(User).filter(User.username == "bartosz").one_or_none()

    assert user

    assert user.role == 'owner'
    assert user.username == "bartosz"
