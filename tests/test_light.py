import pytest

from light_cylinder.config import LIGHT_GROUND_SPARK_COUNT, LIGHT_PARTICLE_COUNT
from light_cylinder.light import LightBeam, LightField
from light_cylinder.world import CylinderWorld


def test_light_beam_intensity_is_strong_on_axis() -> None:
    beam = LightBeam.create_default()
    center = beam.axis_point_at(0.5)

    assert beam.intensity_at(center) == pytest.approx(1.0)


def test_light_beam_intensity_rejects_outside_radius() -> None:
    beam = LightBeam.create_default()
    basis_u, _basis_v = beam.basis()
    outside = beam.axis_point_at(0.5) + basis_u * (beam.radius + 1.0)

    assert beam.intensity_at(outside) == 0.0


def test_light_beam_intensity_rejects_outside_length() -> None:
    beam = LightBeam.create_default()
    before_start = beam.origin - beam.direction
    after_end = beam.axis_point(beam.length + 1.0)

    assert beam.intensity_at(before_start) == 0.0
    assert beam.intensity_at(after_end) == 0.0


def test_light_beam_basis_is_perpendicular_to_direction() -> None:
    beam = LightBeam.create_default()
    basis_u, basis_v = beam.basis()

    assert basis_u.length() == pytest.approx(1.0)
    assert basis_v.length() == pytest.approx(1.0)
    assert basis_u.dot(beam.direction) == pytest.approx(0.0)
    assert basis_v.dot(beam.direction) == pytest.approx(0.0)


def test_light_field_generates_sparse_particles_and_ground_sparks() -> None:
    field = LightField.create_default(CylinderWorld())

    assert len(field.particles) == LIGHT_PARTICLE_COUNT
    assert len(field.ground_sparks) == LIGHT_GROUND_SPARK_COUNT
    assert all(spark.position.y == 0.0 for spark in field.ground_sparks)
    assert all(field.beam.intensity_at(spark.position) > 0.0 for spark in field.ground_sparks)


def test_light_particles_stay_inside_beam() -> None:
    field = LightField.create_default(CylinderWorld())

    for _particle, position in field.particle_positions():
        assert field.beam.intensity_at(position) > 0.0


def test_light_field_update_advances_time() -> None:
    field = LightField.create_default(CylinderWorld())

    field.update(0.25)

    assert field.elapsed_time == pytest.approx(0.25)


def test_light_field_update_rejects_negative_time() -> None:
    field = LightField.create_default(CylinderWorld())

    with pytest.raises(ValueError):
        field.update(-0.1)
