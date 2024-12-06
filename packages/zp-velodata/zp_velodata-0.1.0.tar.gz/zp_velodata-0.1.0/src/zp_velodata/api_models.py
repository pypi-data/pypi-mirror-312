from enum import Enum
from typing import Any, Literal

import pandas as pd
from pydantic import BaseModel, Field, model_validator

from zp_velodata import zp_client

from .logging_config import get_logger, setup_logging

# Set up default logging configuration
setup_logging()

# Create a logger for the package
logger = get_logger(__name__)


class AgeCategory(str, Enum):
    """Age categories in ZwiftPower"""

    SENIOR = "Snr"
    MASTER = "Mas"
    VETERAN = "Vet"
    UNDER_23 = "U23"
    JUNIOR = "Jnr"
    OVER_50 = "50+"
    OVER_60 = "60+"
    OVER_70 = "70+"
    OVER_80 = "80+"
    UNKNOWN = "-"


class Rider(BaseModel):
    """Main rider model representing a team member"""

    # Basic Info
    zwid: int = Field(..., description="Zwift ID")
    name: str = Field(..., description="Rider name")
    div: int = Field(..., description="Division")
    divw: int = Field(..., description="Women's division")
    flag: str = Field(..., description="Country flag code")
    r: str = Field(..., description="Race number")
    age: Literal["Snr", "Mas", "Vet", "U23", "Jnr", "50+", "60+", "70+", "80+", "-", None] = Field(
        ..., description="Age category"
    )

    # Optional Fields
    aid: str = Field("", description="Additional ID")
    status: str = Field("", description="Rider status")
    email: str = Field("", description="Email")
    zada: int = Field(0, description="ZADA status")
    reg: int = Field(1, description="Registration status")

    # Skill
    skill: int = Field(0, description="Overall skill rating")
    skill_race: int = Field(0, description="Race skill rating")
    skill_seg: int = Field(0, description="Segment skill rating")
    skill_power: int = Field(0, description="Power skill rating")
    rank: str | None = Field(None, description="Rider's rank")

    # Activity
    distance: int = Field(..., description="Total distance in meters")
    climbed: int = Field(..., description="Total elevation gained in meters")
    energy: int = Field(..., description="Total energy expended in kJ")
    time: int = Field(..., description="Total time in seconds")

    # Power
    # ftp: list[str | int] = Field(..., description="FTP [value, flag]")
    ftp: int = Field(..., description="FTP")
    ftp_flag: int = Field(..., description="FTP flag")
    # w: list[str | int] = Field(..., description="Weight [value, flag]")
    w: float = Field(..., description="Weight")
    w_flag: float = Field(..., description="Weight flag")
    h_1200_watts: str | None = Field(None, description="1200s power")
    h_1200_wkg: str | None = Field(None, description="1200s power/kg")
    h_15_watts: str | None = Field(None, description="15s power")
    h_15_wkg: str | None = Field(None, description="15s power/kg")

    @model_validator(mode="before")
    def split_ftp_values(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "ftp" in values and isinstance(values["ftp"], list):
            values["ftp_flag"] = int(values["ftp"][1])
            values["ftp"] = int(values["ftp"][0])
        if "w" in values and isinstance(values["w"], list):
            values["w_flag"] = int(values["w"][1])
            values["w"] = float(values["w"][0])
        return values


class TeamRiders(BaseModel):
    id: int
    data: dict | None = None
    riders: list[Rider] | None = None

    @property
    def api_url(self):
        """API URL"""
        return f"https://zwiftpower.com/api3.php?do=team_riders&id={self.id}"

    @property
    def df(self):
        """Convert the data to a DataFrame"""
        try:
            if self.riders is None:
                return None
            else:
                df = pd.DataFrame([r.model_dump() for r in self.riders])
                # for col in ["ftp", "w"]:
                #     df[col] = df[col].apply(lambda x: x[0])
                #     df[col] = pd.to_numeric(df[col], errors="coerce")
                return df
        except Exception as e:
            raise e

    def get_rider_by_zwid(self, zwid: int) -> Rider | None:
        """Get a rider by their Zwift ID"""
        for rider in self.data:
            if rider.zwid == zwid:
                return rider
        return None

    def get_riders_by_division(self, div: int) -> list[Rider]:
        """Get all riders in a specific division"""
        return [rider for rider in self.data if rider.div == div]

    def fetch(self, client: zp_client.ZPSession):
        """Fetch the data from the API"""
        try:
            resp = client.session.get("https://zwiftpower.com/events.php")
            resp.raise_for_status()
            api_data = client.session.get(self.api_url)
            api_data.raise_for_status()
            self.data = api_data.json()
        except Exception as e:
            logger.error(f"Failed to get team riders: {e}")
        try:
            self.riders = [Rider.model_validate(r) for r in self.data["data"]]
        except Exception as e:
            logger.error(f"Failed to parse team riders: {e}")


class Profile(BaseModel):
    zwid: int
    results: dict | None = None

    @property
    def api_url(self):
        return f"https://zwiftpower.com/cache3/profile/{self.zwid}_all.json"

    def fetch(self, client: zp_client.ZPSession):
        api_data = client.session.get(self.api_url)
        if api_data.status_code != 200:
            logger.error(f"Failed to get profile: {api_data.status_code}")
            return None
        self.results = api_data.json()
