from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from light_cylinder.config import (
    CAMERA_FOCAL_LENGTH,
    CAMERA_INITIAL_DISTANCE,
    CAMERA_INITIAL_PITCH,
    CAMERA_INITIAL_YAW,
    CAMERA_MAX_DISTANCE,
    CAMERA_MAX_PITCH,
    CAMERA_MIN_DISTANCE,
    CAMERA_MIN_PITCH,
    CYLINDER_HEIGHT,
    CYLINDER_TARGET_HEIGHT_FACTOR,
    RENDER_HEIGHT,
    RENDER_WIDTH,
)
from light_cylinder.math3d import Vec3, clamp, rotate_x, rotate_y


@dataclass(frozen=True, slots=True)
class ProjectedPoint:
    x: float
    y: float
    depth: float


@dataclass(slots=True)
class Camera:
    target: Vec3
    yaw: float
    pitch: float
    distance: float
    focal_length: float
    near_clip: float
    screen_center_x: float
    screen_center_y: float

    @classmethod
    def create_default(cls) -> Camera:
        return cls(
            target=Vec3(0.0, CYLINDER_HEIGHT * CYLINDER_TARGET_HEIGHT_FACTOR, 0.0),
            yaw=CAMERA_INITIAL_YAW,
            pitch=CAMERA_INITIAL_PITCH,
            distance=CAMERA_INITIAL_DISTANCE,
            focal_length=CAMERA_FOCAL_LENGTH,
            near_clip=8.0,
            screen_center_x=RENDER_WIDTH / 2,
            screen_center_y=RENDER_HEIGHT * 0.58,
        )

    def world_to_camera(self, point: Vec3) -> Vec3:
        relative = point - self.target
        yaw_space = rotate_y(relative, -self.yaw)
        pitch_space = rotate_x(yaw_space, -self.pitch)
        return Vec3(pitch_space.x, pitch_space.y, pitch_space.z + self.distance)

    def project(self, point: Vec3) -> ProjectedPoint | None:
        camera_point = self.world_to_camera(point)
        depth = camera_point.z
        if depth <= self.near_clip:
            return None

        screen_x = self.screen_center_x + camera_point.x * self.focal_length / depth
        screen_y = self.screen_center_y - camera_point.y * self.focal_length / depth
        if not all(isfinite(value) for value in (screen_x, screen_y, depth)):
            return None

        return ProjectedPoint(screen_x, screen_y, depth)

    def orbit(self, delta_yaw: float, delta_pitch: float) -> None:
        self.yaw += delta_yaw
        self.pitch = self.clamp_pitch(self.pitch + delta_pitch)

    def zoom(self, delta: float) -> None:
        self.distance = self.clamp_distance(self.distance + delta)

    def clamp_pitch(self, pitch: float) -> float:
        return clamp(pitch, CAMERA_MIN_PITCH, CAMERA_MAX_PITCH)

    def clamp_distance(self, distance: float) -> float:
        return clamp(distance, CAMERA_MIN_DISTANCE, CAMERA_MAX_DISTANCE)

    def is_on_screen(self, point: ProjectedPoint, margin: float = 0.0) -> bool:
        return (
            -margin <= point.x <= RENDER_WIDTH + margin
            and -margin <= point.y <= RENDER_HEIGHT + margin
        )
