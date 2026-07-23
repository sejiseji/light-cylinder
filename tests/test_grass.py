from itertools import pairwise
from math import isfinite, tau

import pytest

from light_cylinder.config import (
    GRASS_COUNT,
    GRASS_MAX_BEND,
    GRASS_MAX_HEIGHT,
    GRASS_MAX_STIFFNESS,
    GRASS_MIN_BEND,
    GRASS_MIN_HEIGHT,
    GRASS_MIN_STIFFNESS,
    GRASS_SEGMENTS,
    WIND_MAX_BEND_RATIO,
)
from light_cylinder.grass import (
    GrassBlade,
    GrassField,
    clump_density_weight,
    compute_wind_bend,
    density_weight,
    sample_blade_points,
)
from light_cylinder.math3d import Vec3
from light_cylinder.world import CylinderWorld


def bend_length(blade: GrassBlade) -> float:
    return blade.natural_bend.length()


def test_grass_blade_holds_fields() -> None:
    blade = GrassBlade(
        base=Vec3(1.0, 0.0, 2.0),
        height=20.0,
        natural_bend=Vec3(3.0, 0.0, 4.0),
        stiffness=0.7,
        phase=1.5,
        width_class=2,
        color_variant=1,
    )

    assert blade.base == Vec3(1.0, 0.0, 2.0)
    assert blade.height == 20.0
    assert blade.natural_bend.y == 0.0
    assert blade.stiffness == 0.7
    assert blade.phase == 1.5
    assert blade.width_class == 2
    assert blade.color_variant == 1


def test_generate_requested_count_and_ranges() -> None:
    world = CylinderWorld()
    field = GrassField.generate(world, seed=1729, grass_count=GRASS_COUNT)

    assert len(field) == GRASS_COUNT
    for blade in field.blades:
        assert world.contains(blade.base)
        assert blade.base.y == pytest.approx(world.bottom_y)
        assert GRASS_MIN_HEIGHT <= blade.height <= GRASS_MAX_HEIGHT
        assert blade.natural_bend.y == 0.0
        assert GRASS_MIN_BEND <= bend_length(blade) <= GRASS_MAX_BEND
        assert GRASS_MIN_STIFFNESS <= blade.stiffness <= GRASS_MAX_STIFFNESS
        assert 0.0 <= blade.phase <= tau
        assert 0 <= blade.width_class <= 2
        assert 0 <= blade.color_variant <= 2


def test_generation_is_deterministic_by_seed() -> None:
    world = CylinderWorld()

    first = GrassField.generate(world, seed=123, grass_count=24)
    second = GrassField.generate(world, seed=123, grass_count=24)
    other = GrassField.generate(world, seed=124, grass_count=24)

    assert first == second
    assert first != other


def test_generation_respects_attempt_limit() -> None:
    with pytest.raises(ValueError):
        GrassField.generate(CylinderWorld(), seed=1, grass_count=10, max_attempts=1)


def test_density_weight_is_deterministic_and_prefers_middle_radius() -> None:
    center = density_weight(0.0)
    middle = density_weight(0.65)
    outer = density_weight(1.0)

    assert density_weight(0.5) == density_weight(0.5)
    assert middle > center
    assert middle > outer


def test_clump_density_weight_prefers_planted_groups_over_open_soil() -> None:
    world = CylinderWorld()
    cluster_center = world.sample_bottom_point(0.46 * 0.46, 0.58)
    open_soil = world.sample_bottom_point(0.92 * 0.92, 0.05)

    assert clump_density_weight(cluster_center, world) > clump_density_weight(open_soil, world)


def test_sample_blade_points_shape() -> None:
    blade = GrassBlade(
        base=Vec3(1.0, 2.0, 3.0),
        height=10.0,
        natural_bend=Vec3(6.0, 0.0, 0.0),
        stiffness=0.8,
        phase=0.0,
        width_class=0,
        color_variant=0,
    )

    points = sample_blade_points(blade, GRASS_SEGMENTS)

    assert len(points) == GRASS_SEGMENTS + 1
    assert points[0] == blade.base
    assert points[-1] == blade.base + Vec3(0.0, blade.height, 0.0) + blade.natural_bend
    assert all(first.y <= second.y for first, second in pairwise(points))
    assert points[1].x - blade.base.x < points[-1].x - blade.base.x


def test_sample_blade_points_rejects_zero_segments() -> None:
    blade = GrassBlade(Vec3(0.0, 0.0, 0.0), 1.0, Vec3(0.0, 0.0, 0.0), 1.0, 0.0, 0, 0)

    with pytest.raises(ValueError):
        sample_blade_points(blade, 0)


def test_sample_blade_points_are_finite_and_deterministic() -> None:
    blade = GrassBlade(Vec3(0.0, 0.0, 0.0), 8.0, Vec3(2.0, 0.0, 1.0), 1.0, 0.0, 0, 0)

    first = sample_blade_points(blade, 4)
    second = sample_blade_points(blade, 4)

    assert first == second
    assert all(isfinite(point.x) and isfinite(point.y) and isfinite(point.z) for point in first)


def test_wind_bend_none_matches_static_curve() -> None:
    blade = GrassBlade(Vec3(0.0, 0.0, 0.0), 8.0, Vec3(2.0, 0.0, 1.0), 1.0, 0.0, 0, 0)

    assert sample_blade_points(blade, 4) == sample_blade_points(blade, 4, None)


def test_wind_bend_moves_tip_but_not_root() -> None:
    blade = GrassBlade(Vec3(0.0, 0.0, 0.0), 20.0, Vec3(2.0, 0.0, 0.0), 0.8, 0.0, 0, 0)
    static = sample_blade_points(blade, 5)
    windy = sample_blade_points(blade, 5, Vec3(5.0, 0.0, 0.0))

    assert windy[0] == static[0]
    assert windy[-1].x > static[-1].x
    assert all(first.y <= second.y for first, second in pairwise(windy))


def test_stiffer_grass_reacts_less_to_wind() -> None:
    soft = GrassBlade(Vec3(0.0, 0.0, 0.0), 24.0, Vec3(0.0, 0.0, 0.0), 0.5, 0.0, 0, 0)
    stiff = GrassBlade(Vec3(0.0, 0.0, 0.0), 24.0, Vec3(0.0, 0.0, 0.0), 1.0, 0.0, 0, 0)
    wind = Vec3(0.5, 0.0, 0.0)

    assert compute_wind_bend(soft, wind).length() > compute_wind_bend(stiff, wind).length()


def test_taller_grass_reacts_more_to_wind() -> None:
    short = GrassBlade(Vec3(0.0, 0.0, 0.0), 18.0, Vec3(0.0, 0.0, 0.0), 1.0, 0.0, 0, 0)
    tall = GrassBlade(Vec3(0.0, 0.0, 0.0), 46.0, Vec3(0.0, 0.0, 0.0), 1.0, 0.0, 0, 0)
    wind = Vec3(0.5, 0.0, 0.0)

    assert compute_wind_bend(tall, wind).length() > compute_wind_bend(short, wind).length()


def test_wind_bend_is_limited_and_horizontal() -> None:
    blade = GrassBlade(Vec3(0.0, 0.0, 0.0), 20.0, Vec3(0.0, 0.0, 0.0), 0.45, 0.0, 0, 0)

    bend = compute_wind_bend(blade, Vec3(999.0, 10.0, 0.0))

    assert bend.y == 0.0
    assert bend.length() <= blade.height * WIND_MAX_BEND_RATIO
