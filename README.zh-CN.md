# 插件契约统一化 (Plugin Contract Unification)

> 一个自包含的原子技能蛋 —— 破解「异构组件强耦合」困局。

## 这是什么

受 DeepSeek Harness 公开设计启发的原子剑招：
强制所有组件遵循同一套生命周期钩子、输入输出 Schema 与错误传播规范，
用一层 Plugin 中介形态屏蔽底层差异，实现无差别加载、替换与编排。

- 破解模式：`form-shift`（破形式 — 加一层中介）
- 原理：`interpose`（中介）

## 怎么跑

零依赖，直接运行：

```bash
python skill.py
```

打印 10 组验证，全部 assert 通过即 OK。

Claude Code / Codex 可通过 `SKILL.md` 加载本技能。

一致性测试：

```bash
python -B conformance.py
```

语言无关契约见 `SPEC.md`。

## 输入 → 输出

原始能力定义（函数/类/API） → 标准化 Plugin 描述符与运行时句柄

## 适用 / 不适用

- 适用：需要热插拔、动态组合的框架；多形态能力统一编排
- 不适用：单一固定能力集；极致性能、无法容忍中介层开销

## 后续应用方向

这个原子技能可以作为轻量控制面，复用于：

- Claude Code / Codex 的 Skill 与工具加载器
- DeepSeek Harness 兼容的插件注册中心
- MCP Server 与 API 适配器路由
- 可热切换的模型供应商
- 沙箱与权限生命周期管理
- 多智能体能力编排
- 企业内部 API 统一工具总线
- 实现同一契约的私有行业技能包

## 推荐优先验证

| 优先级 | 应用方向 | 原因 |
|---|---|---|
| 1 | Claude Code / Codex Skill 运行时 | 在真实 Agent 宿主中验证契约 |
| 2 | 公开插件注册中心参考实现 | 建立中立的集成标准 |
| 3 | 工具/API 适配器总线 | 让 MCP 与内部 API 复用同一生命周期 |
| 4 | 私有垂直技能包 | 保持私有技能兼容，但不暴露私有实现 |

## 验证状态

- 本地 `python -B skill.py` 自测通过。
- Claude Code 与 Codex 的加载正在独立验证。
- 当前公开版本定位为参考契约，不是完整 Agent 运行时。

## 许可

本公开蛋代码采用 GPLv3。设计灵感来自 DeepSeek Harness 的公开 MIT 设计，详见 `NOTICE`。

> 免责声明：本项目与 DeepSeek 无隶属关系，仅受其公开 MIT 设计启发。

付费私有蛋为个人买断许可（下载）/ 企业使用条款（API），非代码开源许可。
