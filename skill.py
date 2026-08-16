"""
插件契约统一化 · 原子技能
=========================
来源: deepseek-harness 逆向分析
破解模式: form-shift (破形式 — 加一层中介)
原理: 通过统一插件契约与运行时注册中心，将所有异构能力(函数/类/服务)
      转化为标准形态，利用中介层实现动态编织、隔离与热替换。

公开参考蛋采用 GPLv3。设计灵感来自公开的 DeepSeek Harness 项目，
该项目以 MIT 许可开放，详见 NOTICE。

核心接口:
  Plugin             统一契约与生命周期
  Registry           契约校验、统一调度、热替换
  detect()           项目描述检测
  verify()           声明校验
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Any, Callable


class PluginContractError(Exception):
    """违反插件契约时抛出。"""

    def __init__(self, message: str, *, plugin: str = "", code: str = "CONTRACT_ERROR"):
        super().__init__(message)
        self.message = message
        self.plugin = plugin
        self.code = code


def _validate_schema(schema: Any) -> dict[str, Any]:
    if not isinstance(schema, dict):
        raise PluginContractError(
            "schema must be a dictionary",
            code="INVALID_SCHEMA",
        )
    if "input" not in schema or "output" not in schema:
        raise PluginContractError(
            "schema must declare input and output",
            code="INVALID_SCHEMA",
        )
    return dict(schema)


@dataclass(frozen=True)
class PluginDescriptor:
    """机器可读的插件描述符。"""

    name: str
    schema: dict[str, Any]
    handler: Callable[[Any], Any]
    version: str = "1.0.0"
    metadata: dict[str, Any] = field(default_factory=dict)


class Plugin:
    """统一契约：任何能力想进系统，先长成这个样子。"""

    def __init__(
        self,
        name: str,
        schema: dict[str, Any],
        handler: Callable[[Any], Any],
        *,
        version: str = "1.0.0",
        metadata: dict[str, Any] | None = None,
    ):
        if not name or not isinstance(name, str):
            raise PluginContractError("plugin name is required", code="INVALID_NAME")
        self.descriptor = PluginDescriptor(
            name=name,
            schema=_validate_schema(schema),
            handler=handler,
            version=version,
            metadata=dict(metadata or {}),
        )
        self.loaded = False

    @property
    def name(self) -> str:
        return self.descriptor.name

    @property
    def schema(self) -> dict[str, Any]:
        return self.descriptor.schema

    @property
    def version(self) -> str:
        return self.descriptor.version

    @property
    def metadata(self) -> dict[str, Any]:
        return self.descriptor.metadata

    def load(self) -> str:
        self.loaded = True
        return f"[load] {self.name} 就绪"

    def run(self, payload: Any) -> Any:
        if not self.loaded:
            raise PluginContractError(
                f"{self.name} 未 load",
                plugin=self.name,
                code="NOT_LOADED",
            )
        return self.descriptor.handler(payload)

    def unload(self) -> str:
        self.loaded = False
        return f"[unload] {self.name} 卸载"


class Registry:
    """注册中心：契约校验 + 统一调度 + 热替换。"""

    def __init__(self):
        self._plugins: dict[str, Plugin] = {}
        self._lock = RLock()

    def register(self, plugin: Plugin) -> str:
        self._require_plugin(plugin)
        with self._lock:
            if plugin.name in self._plugins:
                raise PluginContractError(
                    f"plugin already registered: {plugin.name}",
                    plugin=plugin.name,
                    code="DUPLICATE_PLUGIN",
                )
            plugin.load()
            self._plugins[plugin.name] = plugin
            return f"[register] {plugin.name} 就绪"

    def replace(self, plugin: Plugin) -> str:
        self._require_plugin(plugin)
        with self._lock:
            plugin.load()
            old = self._plugins.get(plugin.name)
            if old is not None:
                old.unload()
            self._plugins[plugin.name] = plugin
            return f"[replace] {plugin.name} 就绪"

    def unregister(self, name: str) -> str:
        with self._lock:
            plugin = self._plugins.pop(name, None)
            if plugin is None:
                raise PluginContractError(
                    f"未注册的插件: {name}",
                    plugin=name,
                    code="NOT_FOUND",
                )
            plugin.unload()
            return f"[unregister] {name} 完成"

    def invoke(self, name: str, payload: Any) -> Any:
        with self._lock:
            plugin = self._plugins.get(name)
        if plugin is None:
            raise PluginContractError(
                f"未注册的插件: {name}",
                plugin=name,
                code="NOT_FOUND",
            )
        return plugin.run(payload)

    def get(self, name: str) -> Plugin | None:
        with self._lock:
            return self._plugins.get(name)

    def list_all(self) -> list[str]:
        with self._lock:
            return sorted(self._plugins.keys())

    @staticmethod
    def _require_plugin(plugin: Plugin) -> None:
        if not isinstance(plugin, Plugin):
            raise PluginContractError(
                "必须遵守统一契约",
                code="INVALID_PLUGIN",
            )


_KEYWORDS = [
    "plugin", "adapter", "intermediary", "proxy", "wrapper",
    "registry", "middleware", "contract", "hotswap", "hot-swap",
    "统一", "中介", "插件", "契约", "适配器", "中间层", "注册中心", "热插拔",
]


def detect(project_desc: str) -> dict[str, Any]:
    """DUGU skill execution interface: run this skill as an analyzer."""
    text = (project_desc or "").lower()
    matched = [kw for kw in _KEYWORDS if kw in text]
    evidence = (
        "Executed skill detector: "
        f"{len(matched)} signature terms for plugin contract unification (form-shift)."
    )
    return {"score": len(matched), "matched": matched, "evidence": evidence}


def verify(claim: dict[str, Any] | None, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    """Verify a claim against the plugin-contract domain."""
    claim = claim or {}
    evidence = evidence or {}
    claim_text = str(claim.get("statement") or claim.get("claim") or "").lower()
    evidence_text = str(evidence.get("artifacts") or evidence.get("text") or "").lower()
    haystack = f"{claim_text}\n{evidence_text}"
    matched = [kw for kw in _KEYWORDS if kw in haystack]
    if not matched:
        return {
            "verdict": "unknown",
            "matched": [],
            "reasoning": "No plugin-contract signature terms detected.",
            "evidence_strength": "weak",
        }
    strength = "strong" if len(matched) >= 3 else "moderate"
    return {
        "verdict": "confirmed",
        "matched": matched,
        "reasoning": f"Matched {len(matched)} plugin-contract signature terms.",
        "evidence_strength": strength,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("插件契约统一化验证 (form-shift / 破形式)")
    print("=" * 60)

    def double(x):
        return x * 2

    class Adder:
        def __init__(self, n):
            self.n = n

        def __call__(self, x):
            return x + self.n

    reg = Registry()

    print("\n1. 异构能力统一包装注册")
    print("  ", reg.register(Plugin("double", {"input": "int", "output": "int"}, double)))
    print("  ", reg.register(Plugin("add3", {"input": "int", "output": "int"}, Adder(3))))
    assert reg.list_all() == ["add3", "double"]
    print("  OK - 函数与类实例被压成统一形态")

    print("\n2. 统一调度")
    assert reg.invoke("double", 5) == 10
    assert reg.invoke("add3", 5) == 8
    print("  OK - 异构能力经同一接口无差别调用")

    print("\n3. 重复注册拒绝")
    try:
        reg.register(Plugin("double", {"input": "int", "output": "int"}, double))
        raise AssertionError("应拒绝重复注册")
    except PluginContractError as exc:
        assert exc.code == "DUPLICATE_PLUGIN"
        print("  OK - 同名重复注册被拒绝")

    print("\n4. 热替换")
    reg.replace(Plugin("double", {"input": "int", "output": "int"}, lambda x: x * 3))
    assert reg.invoke("double", 5) == 15
    print("  OK - 同名插件无缝切换")

    print("\n5. 注销插件")
    reg.unregister("add3")
    assert "add3" not in reg.list_all()
    print("  OK - 插件可被正确注销")

    print("\n6. 契约校验")
    try:
        reg.register("not-a-plugin")
        raise AssertionError("应拒绝非 Plugin 对象")
    except PluginContractError as exc:
        assert exc.code == "INVALID_PLUGIN"
        print("  OK - 非标准形态被拒绝")

    print("\n7. Schema 校验")
    try:
        Plugin("bad", {"only_input": "int"}, double)
        raise AssertionError("应拒绝缺少 input/output 的 schema")
    except PluginContractError as exc:
        assert exc.code == "INVALID_SCHEMA"
        print("  OK - 不合规 schema 被拒绝")

    print("\n8. 生命周期强制")
    lazy = Plugin("lazy", {"input": "int", "output": "int"}, lambda x: x)
    try:
        lazy.run(1)
        raise AssertionError("未 load 的插件不应能运行")
    except PluginContractError as exc:
        assert exc.code == "NOT_LOADED"
        print("  OK - 生命周期钩子被强制")

    print("\n9. 未注册插件查询")
    try:
        reg.invoke("ghost", 1)
        raise AssertionError("未注册插件不应可调用")
    except PluginContractError as exc:
        assert exc.code == "NOT_FOUND"
        print("  OK - 未注册插件被正确拒绝")

    print("\n10. detect / verify")
    hit = detect("registry plugin middleware contract hot-swap")
    assert hit["score"] >= 4
    claim = {"statement": "所有组件通过统一 plugin contract 注册"}
    result = verify(claim)
    assert result["verdict"] == "confirmed"
    print("  OK - 检测与校验接口可用")

    print("\n" + "=" * 60)
    print("OK - 插件契约统一化验证通过")
    print("=" * 60)
