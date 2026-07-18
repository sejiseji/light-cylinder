from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin, sqrt


@dataclass(frozen=True, slots=True)
class Vec2:
    x: float
    y: float

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vec2:
        return Vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vec2:
        return self * scalar

    def __truediv__(self, scalar: float) -> Vec2:
        if scalar == 0:
            raise ZeroDivisionError("cannot divide Vec2 by zero")
        return Vec2(self.x / scalar, self.y / scalar)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y

    def length(self) -> float:
        return sqrt(self.length_squared())

    def normalized(self) -> Vec2:
        length = self.length()
        if length == 0:
            return Vec2(0.0, 0.0)
        return self / length

    def dot(self, other: Vec2) -> float:
        return self.x * other.x + self.y * other.y


@dataclass(frozen=True, slots=True)
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> Vec3:
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, scalar: float) -> Vec3:
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> Vec3:
        return self * scalar

    def __truediv__(self, scalar: float) -> Vec3:
        if scalar == 0:
            raise ZeroDivisionError("cannot divide Vec3 by zero")
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self) -> float:
        return sqrt(self.length_squared())

    def normalized(self) -> Vec3:
        length = self.length()
        if length == 0:
            return Vec3(0.0, 0.0, 0.0)
        return self / length

    def dot(self, other: Vec3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )


def clamp(value: float, minimum: float, maximum: float) -> float:
    if minimum > maximum:
        raise ValueError("minimum must be less than or equal to maximum")
    return max(minimum, min(maximum, value))


def lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * t


def lerp_vec3(start: Vec3, end: Vec3, t: float) -> Vec3:
    return Vec3(
        lerp(start.x, end.x, t),
        lerp(start.y, end.y, t),
        lerp(start.z, end.z, t),
    )


def rotate_x(vector: Vec3, angle: float) -> Vec3:
    c = cos(angle)
    s = sin(angle)
    return Vec3(vector.x, vector.y * c - vector.z * s, vector.y * s + vector.z * c)


def rotate_y(vector: Vec3, angle: float) -> Vec3:
    c = cos(angle)
    s = sin(angle)
    return Vec3(vector.x * c + vector.z * s, vector.y, -vector.x * s + vector.z * c)
