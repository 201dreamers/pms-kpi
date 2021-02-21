from __future__ import annotations
from enum import Enum


class Direction(Enum):
    LONGITUDE = 0
    LATITUDE = 1


class CoordinateHD():
    """ Abbreviations in this class:
        d - degree
        m - minute
        s - second
        D - direction
    """

    _CARDINAL_DIRECTIONS = (('N', 'S'), ('W', 'E'))

    def __init__(self, degrees: int = 0, minutes: int = 0, seconds: int = 0,
                 direction: Direction = Direction.LONGITUDE):
        self._degrees: int = 0
        self._minutes: int = 0
        self._seconds: int = 0

        self.direction = direction
        self.degrees = degrees
        self.minutes = minutes
        self.seconds = seconds

    def get_format_ddmmssD(self):
        return (f'{self.degrees}° {self.minutes}\' {self.seconds}″'
                f' {self.cardinal_direction}')

    def get_format_ddddD(self):
        return f'{self._convert_dms_to_degrees()}° {self.cardinal_direction}'

    def get_coordinate_beetween_current_and(self, coordinate: CoordinateHD):
        try:
            result_coordinate = (self + coordinate) / 2
        except ValueError:
            result_coordinate = None
        return result_coordinate

    @classmethod
    def get_coordinate_beetween(cls, coordinate1: CoordinateHD,
                                coordinate2: CoordinateHD):
        try:
            result_coordinate = (coordinate1 + coordinate2) / 2
        except ValueError:
            result_coordinate = None
        return result_coordinate

    @property
    def cardinal_direction(self):
        _degrees = self._convert_dms_to_degrees()

        if _degrees >= 0:
            return self._CARDINAL_DIRECTIONS[Direction.LONGITUDE.value][0]
        elif _degrees < 0:
            return self._CARDINAL_DIRECTIONS[Direction.LATITUDE.value][1]

    @property
    def degrees(self) -> int:
        return self._degrees

    @degrees.setter
    def degrees(self, value) -> None:
        if (
            (
                self.direction is Direction.LONGITUDE
                and value >= -180 and value <= 180
            )
            or
            (
                self.direction is Direction.LATITUDE
                and value >= -90 and value <= 90
            )
        ):
            self._degrees = value
        else:
            raise ValueError(f'Degrees value <{value}> is incorrect')

    @property
    def minutes(self) -> int:
        return self._minutes

    @minutes.setter
    def minutes(self, value) -> None:
        if value >= 0 and value <= 59:
            self._minutes = value
        else:
            raise ValueError(f'Minutes value <{value}> is incorrect')

    @property
    def seconds(self) -> int:
        return self._seconds

    @seconds.setter
    def seconds(self, value) -> None:
        if value >= 0 and value <= 59:
            self._seconds = value
        else:
            raise ValueError(f'Seconds value <{value}> is incorrect')

    def _convert_dms_to_degrees(self):
        return self.degrees + self.minutes / 60 + self.seconds / 3600

    def __add__(self, coordinate) -> CoordinateHD:
        if self.direction == coordinate.direction:
            return CoordinateHD(
                degrees=self.degrees + coordinate.degrees,
                minutes=self.minutes + coordinate.minutes,
                seconds=self.seconds + coordinate.seconds,
                direction=self.direction,
            )
        raise ValueError('Directions in coordinates should be the same')

    def __sub__(self, coordinate) -> CoordinateHD:
        if self.direction == coordinate.direction:
            return CoordinateHD(
                degrees=self.degrees - coordinate.degrees,
                minutes=self.minutes - coordinate.minutes,
                seconds=self.seconds - coordinate.seconds,
                direction=self.direction,
            )
        raise ValueError('Directions in coordinates should be the same')

    def __mul__(self, number) -> CoordinateHD:
        return CoordinateHD(
            degrees=self.degrees * number,
            minutes=self.minutes * number,
            seconds=self.seconds * number,
            direction=self.direction,
        )

    def __truediv__(self, number) -> CoordinateHD:
        return CoordinateHD(
            degrees=self.degrees // number,
            minutes=self.minutes // number,
            seconds=self.seconds // number,
            direction=self.direction,
        )

    def __str__(self):
        return (f'<Coordinate: degrees - {self.degrees};'
                f' minutes - {self.minutes};'
                f' seconds - {self.seconds};'
                f' direction - {self.direction};'
                f' cardinal_direction - {self.cardinal_direction}>')
