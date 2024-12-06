import os
import pickle
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

from .logging_config import get_logger, setup_logging

# Set up default logging configuration
setup_logging()

# Create a logger for the package
logger = get_logger(__name__)

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


class ZPSession:
    """Create a zwift_power_com session and methods for api's access and parsing:

    Currently, available api's:
    - team_riders=f"{self.zp_url}/api3.php?do=team_riders&id={id}",
    - team_pending=f"{self.zp_url}/api3.php?do=team_pending&id={id}",
    - team_results=f"{self.zp_url}/api3.php?do=team_results&id={id}",
    - profile_profile=f"{self.zp_url}/cache3/profile/{id}_all.json",
    """

    def __init__(self, login_data: dict):
        """Init for class
        login dictionary is a dict of {"username":"YOUR USERNAME", "password":YOUR PASSWORD"}
        """
        self.login_data: dict[str, str] = login_data
        self.zp_url: str = "https://zwiftpower.com"
        self.cookie_dir: Path | None = None
        self.session: httpx.Client | None = None
        self.user_agent: str = "VeloData: [zp_client, zwift_team_util, ladder_teams_util]"  # User Agent required or will be blocked at some apis

    def check_status(self, create_session=True) -> bool:
        """Returns True if the session is logged in else False"""
        if self.session is None and not create_session:
            logger.debug("No session, return False")
            return False
        elif self.session is None:
            logger.debug("No session, creating new session")
            self.session = httpx.Client(follow_redirects=True, headers={"User-Agent": self.user_agent})
        try:
            logger.info("Checking session status")
            r = self.session.get(self.zp_url)
            r.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to load zp_url: {e}")
            return False

        if "Login Required" not in r.text:
            logger.info("Session is logged in")
            return True
        else:
            logger.info("Session is not logged in, Login Required")
            return False

    # def check_status(self) -> bool:
    #     """Returns True if the session status is OK else False"""
    #     if self.session is None:
    #         logger.debug("No session")
    #         return False
    #     else:
    #         ki = self.session.cookies.get("KEYCLOAK_IDENTITY", False)
    #         if not ki:
    #             logger.debug("Missing Keycloak cookies")
    #             return False
    #         else:
    #             return True

    def login(self, use_cookie=False) -> str:
        s = httpx.Client(follow_redirects=True, headers={"User-Agent": self.user_agent})
        self.login_data.update({"rememberMe": "on"})
        logger.info(
            f"Login username is: {self.login_data["username"]} and password is not None: {self.login_data["password"] is not None}"
        )
        if self.login_data["username"] is None or self.login_data["password"] is None:
            logger.error("Username or password is None")
            return False
        resp = s.get("https://zwiftpower.com/")
        if use_cookie:
            if self.load_cookies():
                logger.info("Loaded cookies from file")
                return True
            else:
                logger.info("No cookies found")
        logger.info(resp.status_code)
        r2 = s.get(
            "https://zwiftpower.com/ucp.php?mode=login&login=external&oauth_service=oauthzpsso", follow_redirects=True
        )
        soup = BeautifulSoup(r2.text, "html.parser")
        # logging.info(soup.find("form"))

        post_url = soup.find("form")["action"]

        logger.info(f"Post URL: {post_url}")
        r3 = s.post(post_url, data=self.login_data, follow_redirects=True)
        logger.info(f"Post LOGIN URL: {r3.url}")
        try:  # make sure we are logged in
            assert "'https://secure.zwift.com/" not in str(r3.url)
            assert "https://zwiftpower.com/events.php" in str(r3.url)
            assert "invalid username or password." not in r3.text.lower()
        except AssertionError as e:
            logger.error(f"Failed to login to ZP(1):\n{e}")
            raise e
            self.session = None
            return False
        logger.info("Logged in session created")
        self.session = s
        return True

    def save_cookies(self) -> None:
        """Save current session cookies to file."""
        if self.cookie_dir is None:
            logger.error("No cookie dir specified")
            return None
        try:
            if not self.cookie_dir.exists():
                os.makedirs(self.cookie_dir)
                logger.info("Created cookie directory")
            self.cookie_file = self.cookie_dir / f"{self.login_data['username']}_cookies.pkl"
            with open(self.cookie_file, "wb") as f:
                pickle.dump(self.session.cookies.jar._cookies, f)
            logger.info("Successfully saved cookies to file")
            return True
        except Exception as e:
            logger.warning(f"Error saving cookies: {e}")

    def load_cookies(self) -> bool:
        """Load cookies from file if they exist and aren't expired.

        Returns:
            bool: True if valid cookies were loaded, False otherwise

        """
        if self.cookie_dir is None:
            logger.error("No cookie dir specified")
            return None
        try:
            self.check_status()
            self.cookie_file = self.cookie_dir / f"{self.login_data['username']}_cookies.pkl"
            if not self.cookie_file.exists():
                logger.debug("No cookie file found")
                return False

            with open(self.cookie_file, "rb") as f:
                cookie_data = pickle.load(f)

            # Restore cookies to session
            if not self.session.cookies.jar._cookies:
                self.session.cookies.jar._cookies.update(cookie_data)
            logger.info("Successfully loaded cookies from file")
            return True

        except Exception as e:
            logger.warning(f"Error loading cookies: {e}")
            raise e
            # return False

    def get_session(self):
        if self.check_status():
            return self.session
        else:
            try:
                self.login()
                return self.session
            except Exception as e:
                logger.error(f"Failed to login to ZP and get session:\n{e}")
                return None
