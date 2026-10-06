"""Stable Manim entrypoint: only catalogue lessons are exposed for discovery."""
from importlib import import_module
from dna_animations.catalog import LESSONS

SCENES = {}
for _name, _module, *_ in LESSONS:
    _implementation = getattr(import_module(f"dna_animations.{_module}"), _name)
    # Carry this module identity for Manim discovery, without helper classes.
    _scene = type(_name, (_implementation,), {"__module__": __name__})
    globals()[_name] = _scene
    SCENES[_name] = _scene
del _name, _module, _implementation, _scene
