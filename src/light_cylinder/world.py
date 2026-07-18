from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin, sqrt

from light_cylinder.config import CYLINDER_HEIGHT, CYLINDER_RADIUS
from light_cylinder.math3d import Vec3, clamp


@dataclass(frozen=True, slots=True)
class CylinderWorld:
    center_x: float = 0.0
    center_z: float = 0.0
    bottom_y: float = 0.0
    radius: float = CYLINDER_RADIUS
    height: float = CYLINDER_HEIGHT
    epsilon: float = 1e-9

    @property
    def top_y(self) -> float:
        return self.bottom_y + self.height

    @property
    def bottom_center(self) -> Vec3:
        return Vec3(self.center_x, self.bottom_y, self.center_z)

    @property
    def top_center(self) -> Vec3:
        return Vec3(self.center_x, self.top_y, self.center_z)

    def contains(self, point: Vec3) -> bool:
        return (
            self.bottom_y - self.epsilon <= point.y <= self.top_y + self.epsilon
            and self.contains_horizontal(point)
        )

    def contains_horizontal(self, point: Vec3) -> bool:
        return self.radial_distance_squared(point) <= self.radius * self.radius + self.epsilon

    def radial_distance_squared(self, point: Vec3) -> float:
        dx = point.x - self.center_x
        dz = point.z - self.center_z
        return dx * dx + dz * dz

    def radial_distance(self, point: Vec3) -> float:
        return sqrt(self.radial_distance_squared(point))

    def normalized_radius(self, point: Vec3) -> float:
        return self.radial_distance(point) / self.radius

    def bottom_ring_points(self, segment_count: int) -> tuple[Vec3, ...]:
        return self._ring_points(segment_count, self.bottom_y, self.radius)

    def top_ring_points(self, segment_count: int) -> tuple[Vec3, ...]:
        return self._ring_points(segment_count, self.top_y, self.radius)

    def ring_points_at(
        self, segment_count: int, y: float, radius: float | None = None
    ) -> tuple[Vec3, ...]:
        return self._ring_points(segment_count, y, self.radius if radius is None else radius)

    def vertical_guide_segments(self, guide_count: int) -> tuple[tuple[Vec3, Vec3], ...]:
        if guide_count < 1:
            raise ValueError("guide_count must be positive")
        bottom = self.bottom_ring_points(guide_count)
        top = self.top_ring_points(guide_count)
        return tuple(zip(bottom, top, strict=True))

    def sample_bottom_point(self, u_radius: float, u_angle: float) -> Vec3:
        safe_radius = clamp(u_radius, 0.0, 1.0)
        safe_angle = clamp(u_angle, 0.0, 1.0)
        radius = self.radius * sqrt(safe_radius)
        theta = 2 * pi * safe_angle
        return Vec3(
            self.center_x + radius * cos(theta),
            self.bottom_y,
            self.center_z + radius * sin(theta),
        )

    def _ring_points(self, segment_count: int, y: float, radius: float) -> tuple[Vec3, ...]:
        if segment_count < 3:
            raise ValueError("segment_count must be at least 3")
        return tuple(
            Vec3(
                self.center_x + radius * cos(2 * pi * index / segment_count),
                y,
                self.center_z + radius * sin(2 * pi * index / segment_count),
            )
            for index in range(segment_count)
        )
