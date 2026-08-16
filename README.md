# 插件契约统一化 (Plugin Contract Unification)

> 一个自包含的原子技能蛋 —— 破解「异构组件强耦合」困局。

## 这是什么

从 deepseek-harness（83k+ star）逆向提取的原子剑招：
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

## 输入 → 输出

原始能力定义（函数/类/API） → 标准化 Plugin 描述符与运行时句柄

## 适用 / 不适用

- 适用：需要热插拔、动态组合的框架；多形态能力统一编排
- 不适用：单一固定能力集；极致性能、无法容忍中介层开销

## 许可

本公开蛋代码采用 GPLv3。设计灵感来自 DeepSeek Harness 的公开 MIT 设计，详见 `NOTICE`。

付费私有蛋为个人买断许可（下载）/ 企业使用条款（API），非代码开源许可。
