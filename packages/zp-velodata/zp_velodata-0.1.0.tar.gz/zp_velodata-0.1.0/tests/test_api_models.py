import json

import pytest

from src.zp_velodata.api_models import TeamRiders

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


class TestTeamProfile:
    """
    This test class validates the functionality of the TeamRiders class, specifically its initialization and data
    fetching mechanisms.

    The class includes fixtures for loading test data from JSON and login credentials from the environment variables,
    along with the actual test cases to ensure the correct behavior of the TeamRiders class.

    :ivar team_riders_data: Fixture that loads the team riders data from a JSON file.
    :ivar login_data: Fixture that loads login credentials from environment variables.
    """
    @pytest.fixture
    def team_riders_data(self):
        """
        Fixture to load and return team riders data from a JSON file.

        :rtype: dict
        :return: The dictionary containing team riders data loaded from the JSON file.
        """
        with open("test_data/team_riders_example.json") as file:
            return json.load(file)

    @pytest.fixture
    def login_data(self):
        """
        Fixture that loads login data from environment variables.

        :return: Dictionary containing `username` and `password` fetched from environment
            variables.
        :rtype: dict

        :raises FileNotFoundError: If the `.env` file is not found in the parent directory.
        """
        from dotenv import load_dotenv

        load_dotenv("../.env")
        import os

        return {"username": os.getenv("ZP_USERNAME"), "password": os.getenv("ZP_PASSWORD")}

    def test_team_profile_initialization(self, team_riders_data):
        # Create an instance of TeamRiders using the test JSON data
        team_riders = TeamRiders(id=1)
        team_riders.data = team_riders_data

        # Add your assertions here to validate the initialization
        assert team_riders is not None
        assert team_riders.id == 1

    def test_fetch_team_riders(self, login_data):
        from zp_velodata.zp_client import ZPSession

        zp = ZPSession(login_data=login_data)
        zp.login()
        team_riders = TeamRiders(id=4516)
        team_riders.fetch(zp)
        assert team_riders.df is not None
        assert team_riders.data is not None
        # print(team_riders.data)
