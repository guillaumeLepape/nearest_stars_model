from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from pydantic import BaseModel, ConfigDict, Field


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
    spectral_type: str

    model_config = ConfigDict(extra="forbid")


class MultipleStarSystem(BaseModel):
    name: str
    stars: list[Star] = Field(min_length=2)

    model_config = ConfigDict(extra="forbid")


class NearestStars(BaseModel):
    single_star_systems: list[Star]
    multiple_star_systems: list[MultipleStarSystem]

    model_config = ConfigDict(extra="forbid")


def parse_nearest_stars_data() -> NearestStars:
    path = Path(__file__).parent / "nearest_stars.json"

    return NearestStars.model_validate(json.loads(path.read_text()))


def spherical_to_cartesian(r: float, theta: float, phi: float) -> tuple[float, float, float]:
    x = r * np.cos(phi) * np.sin(theta)
    y = r * np.cos(phi) * -np.cos(theta)
    z = r * np.sin(phi)

    return x, y, z


def hms_to_radians(hours: int, minutes: int, seconds: float) -> float:
    return dms_to_radians(hours, minutes, seconds) * 15  # since 1 hour = 15 degrees


def dms_to_radians(degrees: int | float, minutes: int, seconds: float) -> float:
    return (degrees + minutes / 60 + seconds / 3600) * (np.pi / 180)


def displayed_color(spectral_type: str) -> str:
    mapping = {
        "A": "#D7E1FF",
        "F": "#FFFFE0",
        "G": "#FFFF00",
        "K": "#FFA500",
        "M": "#FF0000",
        "L": "#FF6347",
        "T": "#FF69B4",
        "Y": "#DA70D6",
        "D": "#808080",
    }

    star_class = spectral_type[0]

    return mapping[star_class]


def display_plot(nearest_stars: NearestStars) -> None:
    ax = plt.figure().add_subplot(projection="3d")

    for star in nearest_stars.single_star_systems:
        x, y, z = spherical_to_cartesian(
            star.distance.light_years,
            hms_to_radians(
                star.right_ascension.hours,
                star.right_ascension.minutes,
                star.right_ascension.seconds,
            ),
            dms_to_radians(
                star.declination.degrees, star.declination.minutes, star.declination.seconds
            ),
        )

        ax.scatter(x, y, z, c=displayed_color(star.spectral_type))
        ax.text(x, y, z, star.name)

    for system in nearest_stars.multiple_star_systems:
        x, y, z = spherical_to_cartesian(
            system.stars[0].distance.light_years,
            hms_to_radians(
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
            for offset, color in zip(
                (0.3, -0.3), [displayed_color(star.spectral_type) for star in system.stars]
            ):
                ax.scatter(x, y, z + offset, c=color)
        elif len(system.stars) == 3:
            for offset, color in zip(
                (0.6, 0, -0.6), [displayed_color(star.spectral_type) for star in system.stars]
            ):
                ax.scatter(x, y, z + offset, c=color)

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
