"""Minimal conformance suite for Plugin Contract Unification."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from skill import Plugin, PluginContractError, Registry, detect, verify  # noqa: E402


def test_schema_requires_input_and_output():
    try:
        Plugin("bad", {"only_input": "int"}, lambda x: x)
    except PluginContractError as exc:
        assert exc.code == "INVALID_SCHEMA"
        return
    raise AssertionError("invalid schema was accepted")


def test_invalid_plugin_rejected():
    registry = Registry()
    try:
        registry.register("not-a-plugin")
    except PluginContractError as exc:
        assert exc.code == "INVALID_PLUGIN"
        return
    raise AssertionError("invalid plugin was accepted")


def test_register_and_invoke():
    registry = Registry()
    registry.register(Plugin("double", {"input": "int", "output": "int"}, lambda x: x * 2))
    assert registry.invoke("double", 4) == 8


def test_duplicate_register_rejected():
    registry = Registry()
    plugin = Plugin("double", {"input": "int", "output": "int"}, lambda x: x * 2)
    registry.register(plugin)
    try:
        registry.register(plugin)
    except PluginContractError as exc:
        assert exc.code == "DUPLICATE_PLUGIN"
        return
    raise AssertionError("duplicate plugin was accepted")


def test_missing_plugin_rejected():
    registry = Registry()
    try:
        registry.invoke("ghost", 1)
    except PluginContractError as exc:
        assert exc.code == "NOT_FOUND"
        return
    raise AssertionError("missing plugin was accepted")


def test_not_loaded_plugin_rejected():
    plugin = Plugin("lazy", {"input": "int", "output": "int"}, lambda x: x)
    try:
        plugin.run(1)
    except PluginContractError as exc:
        assert exc.code == "NOT_LOADED"
        return
    raise AssertionError("unloaded plugin was executed")


def test_replace_plugin():
    registry = Registry()
    registry.register(Plugin("double", {"input": "int", "output": "int"}, lambda x: x * 2))
    registry.replace(Plugin("double", {"input": "int", "output": "int"}, lambda x: x * 3))
    assert registry.invoke("double", 5) == 15


def test_unregister_plugin():
    registry = Registry()
    registry.register(Plugin("double", {"input": "int", "output": "int"}, lambda x: x * 2))
    registry.unregister("double")
    assert "double" not in registry.list_all()


def test_detect_returns_structured_result():
    result = detect("plugin registry middleware contract")
    assert set(result) == {"score", "matched", "evidence"}
    assert result["score"] >= 4


def test_verify_confirmed():
    result = verify({"statement": "统一 plugin contract registry"})
    assert result["verdict"] == "confirmed"
    assert result["evidence_strength"] in {"moderate", "strong"}


def test_verify_unknown():
    result = verify({"statement": "这是一个无关领域的问题"})
    assert result["verdict"] == "unknown"


def test_registry_list_sorted():
    registry = Registry()
    registry.register(Plugin("b", {"input": "int", "output": "int"}, lambda x: x))
    registry.register(Plugin("a", {"input": "int", "output": "int"}, lambda x: x))
    assert registry.list_all() == ["a", "b"]


def test_metadata_preserved():
    plugin = Plugin(
        "meta",
        {"input": "int", "output": "int"},
        lambda x: x,
        version="2.0.0",
        metadata={"owner": "public"},
    )
    assert plugin.version == "2.0.0"
    assert plugin.metadata["owner"] == "public"


def test_error_carries_plugin_name():
    registry = Registry()
    try:
        registry.invoke("ghost", 1)
    except PluginContractError as exc:
        assert exc.plugin == "ghost"
        assert exc.code == "NOT_FOUND"
        return
    raise AssertionError("missing error details")


if __name__ == "__main__":
    tests = [
        test_schema_requires_input_and_output,
        test_invalid_plugin_rejected,
        test_register_and_invoke,
        test_duplicate_register_rejected,
        test_missing_plugin_rejected,
        test_not_loaded_plugin_rejected,
        test_replace_plugin,
        test_unregister_plugin,
        test_detect_returns_structured_result,
        test_verify_confirmed,
        test_verify_unknown,
        test_registry_list_sorted,
        test_metadata_preserved,
        test_error_carries_plugin_name,
    ]
    for test in tests:
        test()
        print(f"[OK] {test.__name__}")
    print(f"ALL PASS ({len(tests)} cases)")
