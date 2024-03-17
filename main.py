from __future__ import annotations

import json
from decimal import Decimal
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


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
    seconds: Decimal

    model_config = ConfigDict(extra="forbid")


class Declination(BaseModel):
    degrees: int
    minutes: int
    seconds: Decimal

    model_config = ConfigDict(extra="forbid")


class Center(BaseModel):
    name: str
    star_class: StarClass = Field(alias="class")

    model_config = ConfigDict(extra="forbid")


class Star(BaseModel):
    name: str
    right_ascension: RightAscension
    declination: Declination
    distance: Decimal
    star_class: StarClass = Field(alias="class")

    model_config = ConfigDict(extra="forbid")


class MultipleStarSystem(BaseModel):
    name: str
    stars: list[Star]

    model_config = ConfigDict(extra="forbid")


class NearestStars(BaseModel):
    center: Center
    single_star_systems: list[Star]
    multiple_star_systems: list[MultipleStarSystem]

    model_config = ConfigDict(extra="forbid")


def parse_nearest_stars_data() -> NearestStars:
    path = Path(__file__).parent / "nearest_stars.json"

    return NearestStars.model_validate(json.loads(path.read_text()))


print(parse_nearest_stars_data())
