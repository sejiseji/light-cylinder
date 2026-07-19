import pytest

from light_cylinder.config import RAIN_SPLASHES_PER_IMPACT
from light_cylinder.grass import GrassBlade
from light_cylinder.math3d import Vec3
from light_cylinder.rain import RainImpact
from light_cylinder.reactions import GrassReactionField, GroundReactionField


def _impact(position: Vec3 | None = None) -> RainImpact:
    return RainImpact(
        position=position or Vec3(0.0, 0.0, 0.0),
        direction=Vec3(0.0, -1.0, 0.0),
        strength=1.0,
        phase=0.0,
    )


def _blade(base: Vec3) -> GrassBlade:
    return GrassBlade(
        base=base,
        height=32.0,
        natural_bend=Vec3(0.0, 0.0, 0.0),
        stiffness=0.7,
        phase=0.0,
        width_class=0,
        color_variant=0,
    )


def test_ground_reaction_adds_short_lived_splashes_and_wetness() -> None:
    field = GroundReactionField()

    field.update(1.0 / 30.0, (_impact(),))

    assert len(field.splashes) == RAIN_SPLASHES_PER_IMPACT
    assert field.wetness > 0.0

    field.update(1.0)

    assert field.splashes == ()


def test_ground_wetness_drains_when_rain_stops() -> None:
    field = GroundReactionField(wetness=0.5)

    field.update(1.0, ())

    assert 0.0 < field.wetness < 0.5


def test_grass_reaction_hits_only_nearby_blade() -> None:
    blades = (_blade(Vec3(0.0, 0.0, 0.0)), _blade(Vec3(60.0, 0.0, 0.0)))
    field = GrassReactionField.create(len(blades))

    field.apply_impacts(blades, (_impact(Vec3(1.0, 0.0, 0.0)),))

    assert field.reactions[0].impact > 0.0
    assert field.reactions[1].impact == 0.0
    assert field.active_count == 1
    assert field.bend_for(0).y < 0.0


def test_grass_reaction_decays() -> None:
    blades = (_blade(Vec3(0.0, 0.0, 0.0)),)
    field = GrassReactionField.create(len(blades))
    field.apply_impacts(blades, (_impact(),))

    before = field.reactions[0].impact
    field.update(0.05)

    assert 0.0 <= field.reactions[0].impact < before


def test_grass_reaction_rejects_mismatched_counts() -> None:
    field = GrassReactionField.create(2)

    with pytest.raises(ValueError):
        field.apply_impacts((_blade(Vec3(0.0, 0.0, 0.0)),), ())
