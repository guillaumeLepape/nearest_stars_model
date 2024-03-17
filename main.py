from __future__ import annotations

import json
from enum import Enum
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
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
    D = "D"


class RightAscension(BaseModel):
    hours: int
    minutes: int
    seconds: float

    model_config = ConfigDict(extra="forbid")


class Declination(BaseModel):
    degrees: int
    minutes: int
    seconds: float

    model_config = ConfigDict(extra="forbid")


class Distance(BaseModel):
    light_years: float

    model_config = ConfigDict(extra="forbid")


class Star(BaseModel):
    name: str
    right_ascension: RightAscension
    declination: Declination
    distance: Distance
    star_class: StarClass = Field(alias="class")

    model_config = ConfigDict(extra="forbid")


class MultipleStarSystem(BaseModel):
    name: str
    stars: list[Star]

    model_config = ConfigDict(extra="forbid")


class NearestStars(BaseModel):
    single_star_systems: list[Star]
    multiple_star_systems: list[MultipleStarSystem]

    model_config = ConfigDict(extra="forbid")


def parse_nearest_stars_data() -> NearestStars:
    path = Path(__file__).parent / "nearest_stars.json"

    return NearestStars.model_validate(json.loads(path.read_text()))


def spherical_to_cartesian(rho: float, theta: float, phi: float) -> tuple[float, float, float]:
    x = rho * np.cos(phi) * np.sin(theta)
    y = rho * np.cos(phi) * -np.cos(theta)
    z = rho * np.sin(phi)

    return x, y, z


def hours_to_radian(hours: int, minutes: int, seconds: float) -> float:
    return dms_to_radians(hours * 360 / 24, minutes, seconds)


def dms_to_radians(degrees: int | float, minutes: int, seconds: float) -> float:
    return (degrees + minutes / 60 + seconds / 3600) * (np.pi / 180)


def star_class_color(star_class: StarClass) -> str:
    mapping = {
        StarClass.A: "#FFFFFF",
        StarClass.F: "#FFFFE0",
        StarClass.G: "#FFFF00",
        StarClass.K: "#FFA500",
        StarClass.M: "#FF0000",
        StarClass.L: "#FF6347",
        StarClass.T: "#FF69B4",
        StarClass.Y: "#DA70D6",
        StarClass.D: "#808080",
    }

    return mapping[star_class]


def display_plot(nearest_stars: NearestStars) -> None:
    ax = plt.figure().add_subplot(projection="3d")

    for star in nearest_stars.single_star_systems:
        x, y, z = spherical_to_cartesian(
            star.distance.light_years,
            hours_to_radian(
                star.right_ascension.hours,
                star.right_ascension.minutes,
                star.right_ascension.seconds,
            ),
            dms_to_radians(
                star.declination.degrees, star.declination.minutes, star.declination.seconds
            ),
        )

        ax.scatter(x, y, z, c=star_class_color(star.star_class))
        ax.text(x, y, z, star.name)

    for system in nearest_stars.multiple_star_systems:
        x, y, z = spherical_to_cartesian(
            star.distance.light_years,
            hours_to_radian(
                system.stars[0].right_ascension.hours,
                system.stars[0].right_ascension.minutes,
                system.stars[0].right_ascension.seconds,
            ),
            dms_to_radians(
                system.stars[0].declination.degrees,
                system.stars[0].declination.minutes,
                system.stars[0].declination.seconds,
            ),
        )

        if len(system.stars) == 2:
            ax.scatter(
                [x, x],
                [y, y],
                [z - 0.2, z + 0.2],
                c=[star_class_color(star.star_class) for star in system.stars],
            )
        elif len(system.stars) == 3:
            ax.scatter(
                [x, x, x],
                [y, y, y],
                [z - 0.4, z, z + 0.4],
                c=[star_class_color(star.star_class) for star in system.stars],
            )

        ax.text(x, y, z, system.name)

    lim = 12.5

    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()


if __name__ == "__main__":
    nearest_stars = parse_nearest_stars_data()
    display_plot(nearest_stars)
