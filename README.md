# Multi-Channel Job Search（跨智能体通用交付包）

这个文件夹是一套平台无关、cross-agent 的求职搜索规范，核心搜索能力改为 **Agent-Reach**。它不绑定 Codex、Claude、Gemini、OpenClaw、Cursor 或其他特定智能体。

## 交付方式

- 支持 Agent Skills 的平台：加载 `SKILL.md`。
- 只支持普通文件上传的平台：上传整个文件夹，至少包含 `SKILL.md`、`AGENT_INSTRUCTIONS.md` 和 `SPEC.md`。
- 只支持自定义提示词的平台：复制 `PROMPT.md` 作为系统提示词或任务提示词。
- 只想让人阅读中文规则：打开 `SKILL.zh-CN.md`。

不要把历史搜索生成的 `job-search-*` 结果文件当作 skill 的一部分。它们是运行产物，不是指令。

## Agent-Reach

Agent-Reach 是互联网能力层：负责选择、安装、诊断和路由网页搜索、网页阅读、RSS、GitHub、LinkedIn 公开页面、YouTube 和用户授权浏览器等上游工具。它不是万能爬虫，也不是职位事实数据库。运行时优先执行：

```text
agent-reach doctor
```

如果当前智能体没有 Agent-Reach，应自动尝试用户级安装：优先使用 `pipx install https://github.com/Panniantong/agent-reach/archive/main.zip`，pipx 不存在或失败时使用可用 Python 创建 `~/.agent-reach-venv`。安装后运行 `agent-reach install --env=auto` 和 `agent-reach doctor`。用户级安装失败时报告 `Agent-Reach unavailable`，再使用已有联网搜索或可见浏览器并标记 `native-fallback`。安装系统依赖前必须征得用户明确同意；不要把密码、Cookie、Token 或验证码交给智能体。

## 核心承诺

- 先确认用户指定地点、行业、岗位、社招/校招/实习、公司范围和时间范围；不擅自换地点。
- 先建立公司目录，再逐家公司查岗位。
- 国内企业和国外企业分开分类，并记录分类依据。
- **No company, no canonical job.** 没有具体公司只能算线索。
- 公众号、官网、ATS、政府/人才服务中心、高校就业网和公开招聘平台分开记录来源。
- 社招、校招、实习分开搜索和统计。
- 用 A/B/C/D 证据等级区分官方确认、平台确认、线索和无法验证。
- 记录覆盖范围、阻塞原因、检索时间和所有来源，不声称全网绝对完整。
