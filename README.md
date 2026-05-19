# 🚀 AgentCost-Profiler

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/agentcost-profiler/)

**Lightweight AI Agent Performance & Cost Optimization Engine**

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

---

<a name="english"></a>
## 🎉 English

### Overview

AgentCost-Profiler is a comprehensive tool designed for AI Agent developers to monitor performance, analyze API costs, and receive actionable optimization recommendations. It helps you build more efficient and cost-effective AI applications.

### ✨ Key Features

- 📊 **Performance Profiling**: Monitor execution time, CPU, and memory usage with nanosecond precision
- 💰 **Cost Analysis**: Calculate costs for 15+ LLM models across 6 providers (OpenAI, Anthropic, Google, etc.)
- 💡 **Smart Optimization**: Get actionable recommendations to improve efficiency and reduce costs
- 🎨 **Beautiful Reports**: Generate stunning console output (with Rich) and HTML reports
- 🔌 **Zero Dependencies**: Core functionality works without any external dependencies
- 🚀 **Easy Integration**: Simple API for seamless integration into existing projects

### 🚀 Quick Start

#### Installation

```bash
# Basic installation (zero dependencies)
pip install agentcost-profiler

# With enhanced terminal output
pip install agentcost-profiler[rich]

# Full features including system monitoring
pip install agentcost-profiler[full]
```

#### Usage

```python
from agentcost_profiler import AgentProfiler, CostCalculator, TokenUsage, Provider

# Initialize profiler
profiler = AgentProfiler()

# Profile your agent operations
with profiler.profile("agent_execution"):
    result = your_agent.execute()

# Calculate API costs
calculator = CostCalculator()
usage = TokenUsage(prompt_tokens=1000, completion_tokens=500)
cost = calculator.calculate(Provider.OPENAI, "gpt-4o", usage)

print(f"Cost: ${cost.total_cost:.4f}")
```

#### CLI Usage

```bash
# Run demo
agentcost-profiler demo

# Calculate cost for specific usage
agentcost-profiler cost --provider openai --model gpt-4o --prompt-tokens 1000 --completion-tokens 500

# Compare costs across models
agentcost-profiler compare --prompt-tokens 1000 --completion-tokens 500

# Generate HTML report
agentcost-profiler report --profiling-data stats.json --output report.html
```

### 📖 Detailed Usage

#### Performance Profiling

```python
from agentcost_profiler import AgentProfiler

profiler = AgentProfiler()

# Profile synchronous code
with profiler.profile("database_query"):
    data = db.query()

# Profile async code
async with profiler.profile_async("api_call"):
    response = await api.fetch()

# Get statistics
stats = profiler.get_statistics()
bottlenecks = profiler.identify_bottlenecks(threshold_ms=100)

print(profiler.summary())
```

#### Cost Calculation

```python
from agentcost_profiler import CostCalculator, TokenUsage, Provider

calculator = CostCalculator()

# Single calculation
usage = TokenUsage(prompt_tokens=1000, completion_tokens=500)
cost = calculator.calculate(Provider.OPENAI, "gpt-4o", usage)

# Compare multiple models
models = [
    (Provider.OPENAI, "gpt-4o"),
    (Provider.ANTHROPIC, "claude-3-sonnet"),
    (Provider.GOOGLE, "gemini-1.5-pro"),
]
results = calculator.compare_costs(usage, models)

# Estimate before API call
estimated = calculator.estimate_cost(
    Provider.OPENAI, "gpt-4o",
    prompt_tokens=1000,
    expected_completion_tokens=500
)
```

#### Optimization Recommendations

```python
from agentcost_profiler import Optimizer

optimizer = Optimizer()

# Analyze profiling and cost data
recommendations = optimizer.analyze(
    profiler_stats=profiler.get_statistics(),
    cost_breakdown=[cost.to_dict()]
)

# Get high priority recommendations
high_priority = optimizer.get_priority_recommendations(Priority.HIGH)

print(optimizer.summary())
```

### 💡 Design Philosophy

AgentCost-Profiler was designed with these principles:

1. **Simplicity**: Easy to use with minimal configuration
2. **Accuracy**: Precise performance measurements and cost calculations
3. **Actionability**: Recommendations you can implement immediately
4. **Flexibility**: Works with any AI Agent framework
5. **Transparency**: Open source with clear pricing data

### 📦 Supported Providers & Models

| Provider | Models |
|----------|--------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-4o, gpt-4o-mini, gpt-3.5-turbo |
| Anthropic | claude-3-opus, claude-3-sonnet, claude-3-haiku, claude-3.5-sonnet |
| Google | gemini-pro, gemini-ultra, gemini-1.5-pro, gemini-1.5-flash |
| Cohere | command, command-light, command-r, command-r-plus |
| Mistral | mistral-tiny, mistral-small, mistral-medium, mistral-large |
| DeepSeek | deepseek-chat, deepseek-coder |

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🎉 简体中文

### 项目介绍

AgentCost-Profiler 是一款专为 AI Agent 开发者设计的综合性工具，用于监控性能、分析 API 成本，并提供可执行的优化建议。帮助您构建更高效、更具成本效益的 AI 应用。

### ✨ 核心特性

- 📊 **性能分析**：以纳秒级精度监控执行时间、CPU 和内存使用
- 💰 **成本分析**：计算 6 个提供商的 15+ 个 LLM 模型成本（OpenAI、Anthropic、Google 等）
- 💡 **智能优化**：获取可执行的建议，提高效率和降低成本
- 🎨 **精美报告**：生成精美的终端输出（使用 Rich）和 HTML 报告
- 🔌 **零依赖**：核心功能无需任何外部依赖即可工作
- 🚀 **易于集成**：简单的 API，可无缝集成到现有项目中

### 🚀 快速开始

#### 安装

```bash
# 基础安装（零依赖）
pip install agentcost-profiler

# 带增强终端输出
pip install agentcost-profiler[rich]

# 完整功能，包括系统监控
pip install agentcost-profiler[full]
```

#### 使用示例

```python
from agentcost_profiler import AgentProfiler, CostCalculator, TokenUsage, Provider

# 初始化分析器
profiler = AgentProfiler()

# 分析 Agent 操作
with profiler.profile("agent_execution"):
    result = your_agent.execute()

# 计算 API 成本
calculator = CostCalculator()
usage = TokenUsage(prompt_tokens=1000, completion_tokens=500)
cost = calculator.calculate(Provider.OPENAI, "gpt-4o", usage)

print(f"成本: ${cost.total_cost:.4f}")
```

#### 命令行使用

```bash
# 运行演示
agentcost-profiler demo

# 计算特定使用量的成本
agentcost-profiler cost --provider openai --model gpt-4o --prompt-tokens 1000 --completion-tokens 500

# 比较不同模型的成本
agentcost-profiler compare --prompt-tokens 1000 --completion-tokens 500

# 生成 HTML 报告
agentcost-profiler report --profiling-data stats.json --output report.html
```

### 📖 详细使用指南

#### 性能分析

```python
from agentcost_profiler import AgentProfiler

profiler = AgentProfiler()

# 分析同步代码
with profiler.profile("database_query"):
    data = db.query()

# 分析异步代码
async with profiler.profile_async("api_call"):
    response = await api.fetch()

# 获取统计信息
stats = profiler.get_statistics()
bottlenecks = profiler.identify_bottlenecks(threshold_ms=100)

print(profiler.summary())
```

#### 成本计算

```python
from agentcost_profiler import CostCalculator, TokenUsage, Provider

calculator = CostCalculator()

# 单次计算
usage = TokenUsage(prompt_tokens=1000, completion_tokens=500)
cost = calculator.calculate(Provider.OPENAI, "gpt-4o", usage)

# 比较多个模型
models = [
    (Provider.OPENAI, "gpt-4o"),
    (Provider.ANTHROPIC, "claude-3-sonnet"),
    (Provider.GOOGLE, "gemini-1.5-pro"),
]
results = calculator.compare_costs(usage, models)

# API 调用前估算
estimated = calculator.estimate_cost(
    Provider.OPENAI, "gpt-4o",
    prompt_tokens=1000,
    expected_completion_tokens=500
)
```

### 💡 设计理念

AgentCost-Profiler 遵循以下设计原则：

1. **简洁性**：配置简单，易于使用
2. **准确性**：精确的性能测量和成本计算
3. **可操作性**：可立即实施的建议
4. **灵活性**：适用于任何 AI Agent 框架
5. **透明性**：开源，定价数据清晰

### 📦 支持的提供商和模型

| 提供商 | 模型 |
|--------|------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-4o, gpt-4o-mini, gpt-3.5-turbo |
| Anthropic | claude-3-opus, claude-3-sonnet, claude-3-haiku, claude-3.5-sonnet |
| Google | gemini-pro, gemini-ultra, gemini-1.5-pro, gemini-1.5-flash |
| Cohere | command, command-light, command-r, command-r-plus |
| Mistral | mistral-tiny, mistral-small, mistral-medium, mistral-large |
| DeepSeek | deepseek-chat, deepseek-coder |

### 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 📄 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

<a name="繁體中文"></a>
## 🎉 繁體中文

### 專案介紹

AgentCost-Profiler 是一款專為 AI Agent 開發者設計的綜合性工具，用於監控效能、分析 API 成本，並提供可執行的優化建議。幫助您建構更高效、更具成本效益的 AI 應用。

### ✨ 核心特性

- 📊 **效能分析**：以奈秒級精度監控執行時間、CPU 和記憶體使用
- 💰 **成本分析**：計算 6 個提供商的 15+ 個 LLM 模型成本（OpenAI、Anthropic、Google 等）
- 💡 **智慧優化**：獲取可執行的建議，提高效率和降低成本
- 🎨 **精美報告**：生成精美的終端輸出（使用 Rich）和 HTML 報告
- 🔌 **零依賴**：核心功能無需任何外部依賴即可工作
- 🚀 **易於整合**：簡單的 API，可無縫整合到現有專案中

### 🚀 快速開始

#### 安裝

```bash
# 基礎安裝（零依賴）
pip install agentcost-profiler

# 帶增強終端輸出
pip install agentcost-profiler[rich]

# 完整功能，包括系統監控
pip install agentcost-profiler[full]
```

#### 使用範例

```python
from agentcost_profiler import AgentProfiler, CostCalculator, TokenUsage, Provider

# 初始化分析器
profiler = AgentProfiler()

# 分析 Agent 操作
with profiler.profile("agent_execution"):
    result = your_agent.execute()

# 計算 API 成本
calculator = CostCalculator()
usage = TokenUsage(prompt_tokens=1000, completion_tokens=500)
cost = calculator.calculate(Provider.OPENAI, "gpt-4o", usage)

print(f"成本: \${cost.total_cost:.4f}")
```

#### 命令列使用

```bash
# 執行演示
agentcost-profiler demo

# 計算特定使用量的成本
agentcost-profiler cost --provider openai --model gpt-4o --prompt-tokens 1000 --completion-tokens 500

# 比較不同模型的成本
agentcost-profiler compare --prompt-tokens 1000 --completion-tokens 500

# 生成 HTML 報告
agentcost-profiler report --profiling-data stats.json --output report.html
```

### 📖 詳細使用指南

#### 效能分析

```python
from agentcost_profiler import AgentProfiler

profiler = AgentProfiler()

# 分析同步程式碼
with profiler.profile("database_query"):
    data = db.query()

# 分析非同步程式碼
async with profiler.profile_async("api_call"):
    response = await api.fetch()

# 獲取統計資訊
stats = profiler.get_statistics()
bottlenecks = profiler.identify_bottlenecks(threshold_ms=100)

print(profiler.summary())
```

#### 成本計算

```python
from agentcost_profiler import CostCalculator, TokenUsage, Provider

calculator = CostCalculator()

# 單次計算
usage = TokenUsage(prompt_tokens=1000, completion_tokens=500)
cost = calculator.calculate(Provider.OPENAI, "gpt-4o", usage)

# 比較多個模型
models = [
    (Provider.OPENAI, "gpt-4o"),
    (Provider.ANTHROPIC, "claude-3-sonnet"),
    (Provider.GOOGLE, "gemini-1.5-pro"),
]
results = calculator.compare_costs(usage, models)

# API 呼叫前估算
estimated = calculator.estimate_cost(
    Provider.OPENAI, "gpt-4o",
    prompt_tokens=1000,
    expected_completion_tokens=500
)
```

### 💡 設計理念

AgentCost-Profiler 遵循以下設計原則：

1. **簡潔性**：配置簡單，易於使用
2. **準確性**：精確的效能測量和成本計算
3. **可操作性**：可立即實施的建議
4. **靈活性**：適用於任何 AI Agent 框架
5. **透明性**：開源，定價資料清晰

### 📦 支援的提供商和模型

| 提供商 | 模型 |
|--------|------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-4o, gpt-4o-mini, gpt-3.5-turbo |
| Anthropic | claude-3-opus, claude-3-sonnet, claude-3-haiku, claude-3.5-sonnet |
| Google | gemini-pro, gemini-ultra, gemini-1.5-pro, gemini-1.5-flash |
| Cohere | command, command-light, command-r, command-r-plus |
| Mistral | mistral-tiny, mistral-small, mistral-medium, mistral-large |
| DeepSeek | deepseek-chat, deepseek-coder |

### 🤝 貢獻指南

歡迎貢獻！請隨時提交 Pull Request。

1. Fork 本倉庫
2. 建立您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 📄 開源協議

本專案採用 MIT 協議 - 檢視 [LICENSE](LICENSE) 檔案瞭解詳情。

---

## 🔗 Links

- **GitHub**: https://github.com/gitstq/AgentCost-Profiler
- **PyPI**: https://pypi.org/project/agentcost-profiler/
- **Issues**: https://github.com/gitstq/AgentCost-Profiler/issues

## 🙏 Acknowledgments

- Inspired by the growing need for AI Agent observability
- Built with ❤️ for the AI development community
