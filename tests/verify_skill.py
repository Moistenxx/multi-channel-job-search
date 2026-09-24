from pathlib import Path


ROOT = Path(__file__).parents[1]
required = {
    "SKILL.md",
    "SKILL.zh-CN.md",
    "AGENT_INSTRUCTIONS.md",
    "PROMPT.md",
    "README.md",
    "SPEC.md",
}

for name in required:
    assert (ROOT / name).is_file(), name

skill = (ROOT / "SKILL.md").read_text()
zh_skill = (ROOT / "SKILL.zh-CN.md").read_text()
instructions = (ROOT / "AGENT_INSTRUCTIONS.md").read_text()
prompt = (ROOT / "PROMPT.md").read_text()
readme = (ROOT / "README.md").read_text()
spec = (ROOT / "SPEC.md").read_text()
pressure = (ROOT / "tests" / "pressure-scenarios.md").read_text()

assert skill.startswith("---\nname: multi-channel-job-search\n")
assert "Use when" in skill.split("---", 2)[1]
for phrase in (
    "platform-neutral",
    "Agent-Reach",
    "capability layer",
    "agent-reach doctor",
    "company-bound",
    "No company, no canonical job.",
    "Mandatory User-Intent Intake",
    "user-requested geography",
    "domestic-company track",
    "foreign-company track",
    "social-recruitment",
    "campus-recruitment",
    "talent service center",
    "official-confirmed",
    "user-visible browser",
    "bypass CAPTCHA",
    "deduplicate",
    "separate confirmation",
    "Mandatory Per-Company Pass",
    "partial-incomplete-company-passes",
    "not_attempted",
    "official accounts",
    "Tianjin local public channels",
):
    assert phrase in skill, phrase

for text in (skill, zh_skill, instructions, prompt, readme, spec):
    assert "anysearch" not in text.lower()

for text in (instructions, prompt, readme):
    assert "Agent-Reach" in text

for phrase in (
    "Agent-Reach unavailable",
    "visible browser",
    "No company, no canonical job",
    "domestic",
    "foreign",
    "social",
    "campus",
    "internship",
    "company registry",
    "coverage",
    "partial-incomplete-company-passes",
):
    assert phrase.lower() in (instructions + "\n" + prompt).lower(), phrase

for artifact in ("companies.csv", "records.csv", "observations.csv", "summary.md"):
    assert artifact in spec, artifact

assert "cross-agent" in readme.lower() or "任何智能体" in readme
assert "Agent-Reach" in spec
assert "agent-reach doctor" in spec
for phrase in ("tianjin_local_public", "employer_site_ats", "official_accounts", "partial-incomplete-company-passes"):
    assert phrase in pressure, phrase
print("universal skill package: ok")
