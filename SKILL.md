---
name: multi-channel-job-search
description: Use when a user needs current or recent jobs, employer discovery, or a location-specific hiring inventory across company sites, public ATS, government and talent-service channels, official social accounts, or job boards, with source verification and coverage reporting
---

# Multi-Channel Job Search

## Operating Principle

This is a **platform-neutral, evidence-first** workflow. Agent-Reach is the preferred internet capability layer; it selects, installs, diagnoses, and routes upstream tools, but it is not the evidence authority. Use the tools actually available in the host agent, and state the capability and access mode used for every source.

For the detailed schema and acceptance criteria, read [SPEC.md](SPEC.md). When the host does not support Agent Skills, use [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) or paste [PROMPT.md](PROMPT.md).

## Capability Preflight

1. If `agent-reach` is available, run `agent-reach doctor` and record which channels are healthy, degraded, or unavailable. Read the installed Agent-Reach instructions before using a channel-specific command.
2. If it is unavailable, automatically bootstrap a user-local installation before searching. Prefer `pipx install https://github.com/Panniantong/agent-reach/archive/main.zip`; if `pipx` is missing or fails, create `~/.agent-reach-venv` with a working Python 3.10+ interpreter and install the same archive into that virtual environment. Do not use `sudo`, modify system directories, or write into the workspace.
3. After user-local installation, run `agent-reach install --env=auto` (read-only check) and `agent-reach doctor`. If the package install fails, record the exact error and continue with the host's native web search, browser, HTTP, RSS, PDF, or page-reading tools as `native-fallback`. Ask before any system-level dependency installation or configuration change; do not silently use `--system`.
4. Agent-Reach may route web reading, semantic search, RSS, GitHub, LinkedIn public pages, YouTube, and user-authorized browser channels. Use the upstream tool directly after routing. Never infer that a channel is searchable merely because Agent-Reach is installed.

## Mandatory User-Intent Intake

Before company discovery or job queries, ask the user to confirm the brief. Do not choose a location, industry, role, or hiring type on the user's behalf. Collect:

- exact geography: country/province/city, district, industrial park, or permitted commute radius;
- industry/subindustry and role family, with Chinese and English synonyms;
- hiring intent: `social-recruitment`, `campus-recruitment`, `internship`, contract/dispatch, or a named combination;
- company scope: all discoverable employers in the requested place/industry, a named list, or both;
- date window and high-impact constraints: education, experience, salary, language, work authorization, remote/onsite, and start date.

Use: `请确认搜索地点（国家/省市/区县或通勤范围）、行业、岗位及中英文关键词、社招/校招/实习、公司范围、时间范围和学历/经验/薪资等限制。只搜索你指定的地区，不会自行扩大范围。`

If a high-impact field is missing, ask a targeted follow-up and **do not start company discovery**. After confirmation, search only the user-requested geography and explicitly permitted radius. Never reuse a previous location, silently add nearby cities, or substitute a supposedly better market.

### Education constraint interpretation

When the user says **“无学历限制”/“学历不限”** as a search condition, interpret it as **the user imposes no education filter**. Collect openings with every disclosed education requirement (including no degree, secondary/vocational, associate, bachelor's, master's, doctorate), plus openings where education is not disclosed. Do not discard a bachelor's-or-above opening merely because the user has no education restriction. Preserve the employer's exact education text and classify it in the output. Only treat a job as explicitly “学历不限” when the source itself says so.

## Company-First Discovery

Build a company registry before collecting canonical jobs. Use Agent-Reach or the available fallback to search, in separate streams:

- local government, HR bureau, talent service center, public talent network, development zone, SASAC, SOE/central-SOE, industry association, chamber, and university employer directories;
- Chinese and English company names, brands, legal entities, subsidiaries, branches, industrial parks, annual reports, investor-relations pages, and employer domains;
- official career pages and public ATS tenants;
- verified official social-account articles and dated recruitment notices.

Keep two classifications:

- **domestic-company track:** Chinese-owned, state-owned, collectively owned, or locally registered employers, with ownership evidence;
- **foreign-company track:** foreign-owned, joint-venture, multinational, or overseas-headquartered employers, with local legal entity/branch and global/local career domains.

Do not infer ownership from a brand name, language, or logo. Use `unknown` when evidence is missing. Deduplicate parent, subsidiary, branch, and brand records while retaining the relationships. A company with no matching opening remains in the registry with `no accessible matching opening` or an exact blocker.

## Company-Specific Retrieval Contract

## Mandatory Per-Company Pass

After the company registry is saved, **every in-scope company must receive a company pass before the run can finish**. The pass is mandatory even when the first search already found enough jobs.

For each company, execute and log these three channel families separately:

1. **Tianjin local public channels:** the relevant municipal and district HR bureau, talent service center, public talent network, development-zone/industrial-park talent page, and public-sector/SOE portal.
2. **Employer-owned channels:** the official homepage, careers page, ATS, legal-name variants, parent/subsidiary domains, and official recruitment portal.
3. **Official accounts:** verified public account(s), recruitment account, dated recruitment articles, RSS/PDF/event pages linked from the account, and account主体 when visible.

The company pass is complete only when all three families have a row with `attempted=yes` and one of `opened`, `no_match`, or `blocked`, plus query, pages traversed, observations, canonical jobs, stop reason, and blocker. `not_attempted` is an incomplete run, not a negative result.

**Hard stop:** do not report the run as complete, claim “all companies searched”, or finalize a current-job count while any in-scope company has `not_attempted` for one of the three mandatory families. Use `partial-incomplete-company-passes` and list remaining company IDs instead.

Required coverage fields: `company_id,channel_family,attempted,opened_or_status,pages_traversed,queries,observations,canonical_jobs,stop_reason,blocker,checked_at`.

## High-Recall Collection

When the user asks for “尽可能多/全部可发现/不少于 N 条”, optimize discovery for recall before verification. Never stop at the first page or first successful source.

1. Build a query matrix across Chinese/English role synonyms, hiring types, Tianjin districts, date terms, and source families. Save every query with its observations.
2. Search in layers: national and Tianjin public employment portals; municipal/district HR and talent sites; development zones and parks; SASAC/SOE pages; associations; university employment sites; employer ATS/career pages; official-account articles; RSS/PDF/event pages; then permitted boards.
3. Traverse pagination and result boundaries until no next page, repeated employers/jobs, a documented date boundary, or a blocker. “Top 10” and “first page” are not stop conditions.
4. Separate `candidate` (high recall, C/D allowed), `review queue` (company/location/type present), and `current verified` (A/B + explicit open signal). Report all three counts separately.
5. Checkpoint after each source family. Record `pages_traversed`, `next_page_seen`, `stop_reason`, and `remaining_scope`; resume from the checkpoint.

Minimum broad-search budget: 5 role queries x 3 hiring-type queries x 4 source-family passes, plus one company-specific pass for every discovered employer. Unrun cells must be recorded as blockers.

Search is company-bound, not keyword-bound. **No company, no canonical job.** A result saying only “某知名企业” or “某公司” is a lead and cannot enter the confirmed-opening list. deduplicate only clear duplicates while retaining every source observation.

For each canonical company record, capture the standard name, legal entity, ownership evidence, parent/subsidiary relationship, industry, local presence, official homepage, careers/ATS URL, official account and主体 where applicable, source channels attempted, and confidence.

For each canonical opening, capture the company ID, employer, original and normalized title, location, remote mode, hiring type, job ID, salary and treatment source text, education/experience, dates/status, application URL, retrieval time, matched query, original confirmation page, all provenance URLs, evidence grade, freshness, match rationale, and risks.

Run employer-specific queries only after registry creation: `公司名 招聘`, `公司名 社会招聘`, `公司名 校园招聘`, `公司名 实习`, `公司名 careers`, `公司名 jobs`, and the employer's legal-name variants. Merge duplicates across sources but preserve every observation and conflict.

## Hiring-Type Channel Split

Keep independent streams; never merge a campus program into a social opening solely because the title is similar.

| Type | Priority channels and terms |
|---|---|
| `social-recruitment` | employer careers/ATS, HR bureaus, talent centers, official accounts, SOE portals; `社会招聘`, `社招`, `experienced hire`, `professional` |
| `campus-recruitment` | university career centers, campus pages/accounts, campus-fair notices, employer ATS; `校园招聘`, `校招`, `应届`, `毕业生`, `管培生`, `campus`, `graduate`, `early careers` |
| `internship` | employer internship pages, university centers, public talent centers, dated notices; `实习`, `intern`, `internship` |

If a source omits the type, record `unknown` rather than guessing.

## Source Passes And Access Modes

For every company and channel family, record attempted, opened, pages traversed, observations, canonical openings, stop condition, and blocker. Run passes in this order: official domain/ATS; official account/article; local government and talent channels; declared public boards followed by original-page verification.

For in-scope companies, the employer ATS, official account, and Tianjin local public channels are mandatory passes. A broad search result or an already-populated candidate list never substitutes for a missing company pass.

Declare one collection mode:

- `public-only`: open web, official pages, public ATS, RSS, PDF, and public account articles;
- `public-discovery-only`: employer, government, university, and public account sources only; named major boards are explicitly excluded;
- `browser-assisted`: a user-visible browser with the user authenticating normally;
- `hybrid`: public sources plus authorized browser channels.

Agent-Reach availability does not change these evidence rules. A board is not searched merely because a search result mentions its domain. A login wall, CAPTCHA, risk-control page, robots block, JavaScript-only result, missing PDF text, or rate limit is recorded as a blocker.

## Authenticated Browser Handoff

When a source requires login:

1. Open its normal page in a visible browser and name the source; do not claim coverage yet.
2. Ask the user to log in directly and reply `已登录`. Never request passwords, OTPs, cookies, tokens, or exported session data in chat.
3. Verify the visible authenticated state, then continue only in that user-authorized session.
4. Stop at CAPTCHA, QR confirmation, identity verification, risk control, or consent dialogs; return control to the user.
5. Reading/searching does not authorize applying, messaging, following, subscribing, uploading a resume, or changing account data. Ask immediately before each side effect.

## Evidence And Freshness

Use exactly these evidence states:

- `A official-confirmed`: employer/official ATS source shows employer, role, place, application path, and an open or unexpired state;
- `B platform-confirmed`: individual job-board detail page is accessible with substantive fields and an actionable path;
- `C lead`: snippet, aggregator, repost, list page, or incomplete official-account article;
- `D unverifiable`: blocked, withdrawn, login/CAPTCHA wall, or missing actionable evidence.

Only A or B records with an explicit open/unexpired signal may be described as current, and B must be labeled platform-confirmed. Missing dates or deadlines are `unknown`; never infer them from ranking, recency, or title. Missing salary, benefits, education, experience, location, or hiring type is `未披露`/`unknown`.

## Retrieval And Normalization

1. Create a query matrix: channel x role synonym x hiring type x geography, plus company-specific queries.
2. Use Agent-Reach's routed search/page/RSS/browser capability, or the host's native fallback. Follow every reachable page to a natural end, repeated state, result boundary, or blocker; no arbitrary top-N cap unless the user sets it.
3. Save every raw observation before deduplication, including expired, duplicate, weak, and unverified records.
4. Normalize employer, title, location, hiring type, salary, dates, job ID, application URL, and evidence. Merge only clear duplicates and retain all provenance.
5. Give each record a status bucket (`possibly open`, `expired/closed`, `unknown`) and a date-window state (`verified in window`, `date unknown`, `outside window`).
6. Recheck A/B records before reporting when possible. Do not claim current status from retrieval time alone.

## Required Deliverables

Create a company directory and canonical opening list, plus the raw observation ledger:

- `job-search-YYYYMMDD-HHmm-companies.csv`
- `job-search-YYYYMMDD-HHmm-records.csv`
- `job-search-YYYYMMDD-HHmm-observations.csv`
- `job-search-YYYYMMDD-HHmm-full.md`
- `job-search-YYYYMMDD-HHmm-summary.md`

The summary must reconcile counts for domestic/foreign companies, social/campus/internship jobs, status, evidence grade, duplicates, blockers, attempted channels, and engine/access mode. Keep official-confirmed jobs, platform-confirmed jobs, leads, and unverifiable items separate. Do not claim “全部” or “全网完整”; define completeness only against declared sources, queries, dates, and reachable pages.

## Safety Boundaries

- Always disclose source gaps, blocked channels, date uncertainty, engine mode, and retrieval time.
- Ask first before installing system dependencies, adding a new platform outside the declared matrix, using a resume or contact data, or performing any application/account action.
- Never bypass CAPTCHA, access controls, robots, rate limits, or platform protections; never rotate accounts or use proxies to evade limits.
- Never request or persist passwords, OTPs, cookies, tokens, private chats, or resume data in third-party search queries or output files.
- Every application, message, upload, subscription, or account change requires separate confirmation immediately before the action.
