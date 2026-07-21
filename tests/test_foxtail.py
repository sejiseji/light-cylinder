from light_cylinder.config import (
    FOXTAIL_COUNT,
    FOXTAIL_HEAD_SEGMENTS_MAX,
    FOXTAIL_HEAD_SEGMENTS_MIN,
    FOXTAIL_HEIGHT_MAX_FACTOR,
    FOXTAIL_HEIGHT_MIN_FACTOR,
    GRASS_MAX_HEIGHT,
)
from light_cylinder.foxtail import FoxtailField, sample_foxtail_shape
from light_cylinder.math3d import Vec3
from light_cylinder.world import CylinderWorld


def test_foxtail_field_generates_a_few_tall_specimens() -> None:
    world = CylinderWorld()
    field = FoxtailField.generate(world)

    assert len(field.foxtails) == FOXTAIL_COUNT
    assert 2 <= len(field.foxtails) <= 3
    for foxtail in field.foxtails:
        assert world.contains(foxtail.base)
        assert foxtail.height >= GRASS_MAX_HEIGHT * FOXTAIL_HEIGHT_MIN_FACTOR
        assert foxtail.height <= GRASS_MAX_HEIGHT * FOXTAIL_HEIGHT_MAX_FACTOR
        assert FOXTAIL_HEAD_SEGMENTS_MIN <= foxtail.head_segments <= FOXTAIL_HEAD_SEGMENTS_MAX


def test_foxtail_shape_has_stem_head_and_delayed_head_motion() -> None:
    foxtail = FoxtailField.generate(CylinderWorld()).foxtails[0]

    calm = sample_foxtail_shape(foxtail, Vec3(0.0, 0.0, 0.0))
    windy = sample_foxtail_shape(foxtail, Vec3(1.5, 0.0, 0.4))

    assert len(calm.stem_points) == 6
    assert len(calm.head_points) == foxtail.head_segments + 1
    assert calm.stem_points[-1] == calm.head_points[0]
    assert windy.stem_points[-1] != calm.stem_points[-1]
    assert windy.head_points[-1] != calm.head_points[-1]


def test_foxtail_rain_droop_lowers_the_seed_head() -> None:
    foxtail = FoxtailField.generate(CylinderWorld()).foxtails[0]

    dry = sample_foxtail_shape(foxtail, Vec3(0.0, 0.0, 0.0), rain_weight=0.0)
    rainy = sample_foxtail_shape(foxtail, Vec3(0.0, 0.0, 0.0), rain_weight=1.0)

    assert rainy.head_points[-1].y < dry.head_points[-1].y


def test_foxtail_after_rain_keeps_a_few_head_droplets() -> None:
    foxtail = FoxtailField.generate(CylinderWorld()).foxtails[0]

    dry = sample_foxtail_shape(foxtail, Vec3(0.0, 0.0, 0.0), after_rain_weight=0.0)
    after_rain = sample_foxtail_shape(foxtail, Vec3(0.0, 0.0, 0.0), after_rain_weight=1.0)

    assert dry.droplet_points == ()
    assert 1 <= len(after_rain.droplet_points) <= 2
