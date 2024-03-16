from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from pathlib import Path
import json


class StarClass(str, Enum):
    A = "A"
    F = "F"
    G = "G"
    K = "K"
    M = "M"
    L = "L"
    T = "T"
    Y = "Y"


class RightAscension(BaseModel):
    hours: int
    minutes: int
    seconds: int

    model_config = ConfigDict(extra="forbid")


class Declination(BaseModel):
    degrees: int
    minutes: int
    seconds: int

    model_config = ConfigDict(extra="forbid")


class Center(BaseModel):
    name: str
    star_class: StarClass = Field(alias="class")

    model_config = ConfigDict(extra="forbid")


class Star(BaseModel):
    name: str
    right_ascension: RightAscension
    declination: Declination
    distance: float
    star_class: StarClass = Field(alias="class")

    model_config = ConfigDict(extra="forbid")


class SingleStarSystem(BaseModel):
    planets: list[str]

    model_config = ConfigDict(extra="forbid")


class MultipleStarSystem(BaseModel):
    name: str
    stars: list[Star]

    model_config = ConfigDict(extra="forbid")


class NearestStars(BaseModel):
    center: Center
    single_star_systems: list[SingleStarSystem]
    multiple_star_systems: list[MultipleStarSystem]

    model_config = ConfigDict(extra="forbid")


def parse_nearest_stars_data() -> NearestStars:
    path = Path(__file__).parent / "nearest_stars.json"

    return NearestStars.model_validate(json.loads(path.read_text()))


print(parse_nearest_stars_data())
