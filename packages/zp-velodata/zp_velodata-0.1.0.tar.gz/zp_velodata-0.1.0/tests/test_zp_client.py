import logging

import pytest

from src.zp_velodata.zp_client import ZPSession

# # Setting up the basic configuration for logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#
# # Creating a logger object
# logger = logging.getLogger(__name__)
#
# # Creating a console handler
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
#
# # Formatting for the console handler
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# console_handler.setFormatter(formatter)
#
# # Adding the console handler to the logger
# logger.addHandler(console_handler)


class TestZPSession:
    @pytest.fixture
    def login_data(self):
        from dotenv import load_dotenv

        load_dotenv("../.env")
        import os

        # logger.info(f"Can we load username:{os.getenv("ZP_USERNAME")}")
        return {"username": os.getenv("ZP_USERNAME"), "password": os.getenv("ZP_PASSWORD")}

    def test_not_logged_in_status(self, login_data):
        zp = ZPSession(login_data=login_data)
        assert zp.check_status() == False

    def test_login(self, login_data):
        zp = ZPSession(login_data=login_data)
        assert zp.check_status() == False
        assert zp.login() == True
        assert zp.check_status() == True
