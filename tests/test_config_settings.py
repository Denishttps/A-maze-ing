"""Tests for src/config.py — Settings configuration."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import Settings, settings


# ─────────────────────────────────────────────
# 1. Class constants
# ─────────────────────────────────────────────


class TestSettingsConstants:
    def test_pattern_42_exists(self):
        assert hasattr(Settings, 'pattern_42')
        assert isinstance(Settings.pattern_42, list)
        assert len(Settings.pattern_42) > 0

    def test_pattern_42_contains_tuples(self):
        for item in Settings.pattern_42:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_wall_character_defined(self):
        assert hasattr(Settings, 'wall')
        assert Settings.wall == "\u2588\u2588"

    def test_cell_character_defined(self):
        assert hasattr(Settings, 'cell')
        assert Settings.cell == "  "

    def test_path_character_defined(self):
        assert hasattr(Settings, 'path')
        assert Settings.path == "\u2591\u2591"


# ─────────────────────────────────────────────
# 2. Global settings instance
# ─────────────────────────────────────────────


class TestSettingsInstance:
    def test_global_settings_instance_exists(self):
        assert settings is not None

    def test_global_settings_is_settings_type(self):
        # The global settings object should have the configuration values
        assert hasattr(settings, 'width')
        assert hasattr(settings, 'height')

    def test_settings_has_required_fields(self):
        required_fields = ['width', 'height', 'entry_raw', 'exit_raw', 'output_file', 'perfect']
        for field in required_fields:
            assert hasattr(settings, field)


# ─────────────────────────────────────────────
# 3. Configuration values
# ─────────────────────────────────────────────


class TestSettingsValues:
    def test_width_is_integer(self):
        assert isinstance(settings.width, int)

    def test_height_is_integer(self):
        assert isinstance(settings.height, int)

    def test_entry_raw_is_string(self):
        assert isinstance(settings.entry_raw, str)

    def test_exit_raw_is_string(self):
        assert isinstance(settings.exit_raw, str)

    def test_output_file_is_string(self):
        assert isinstance(settings.output_file, str)

    def test_perfect_is_boolean(self):
        assert isinstance(settings.perfect, bool)

    def test_seed_is_int_or_none(self):
        assert settings.seed is None or isinstance(settings.seed, int)


# ─────────────────────────────────────────────
# 4. Computed fields
# ─────────────────────────────────────────────


class TestComputedFields:
    def test_entry_computed_field_exists(self):
        assert hasattr(settings, 'entry')

    def test_entry_is_tuple(self):
        assert isinstance(settings.entry, tuple)
        assert len(settings.entry) == 2

    def test_entry_contains_integers(self):
        x, y = settings.entry
        assert isinstance(x, int)
        assert isinstance(y, int)

    def test_exit_computed_field_exists(self):
        assert hasattr(settings, 'exit')

    def test_exit_is_tuple(self):
        assert isinstance(settings.exit, tuple)
        assert len(settings.exit) == 2

    def test_exit_contains_integers(self):
        x, y = settings.exit
        assert isinstance(x, int)
        assert isinstance(y, int)


# ─────────────────────────────────────────────
# 5. Configuration constraints
# ─────────────────────────────────────────────


class TestConfigurationConstraints:
    def test_width_positive(self):
        assert settings.width > 0

    def test_height_positive(self):
        assert settings.height > 0

    def test_entry_in_bounds(self):
        x, y = settings.entry
        assert 0 <= x < settings.width
        assert 0 <= y < settings.height

    def test_exit_in_bounds(self):
        x, y = settings.exit
        assert 0 <= x < settings.width
        assert 0 <= y < settings.height
