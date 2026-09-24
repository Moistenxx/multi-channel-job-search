# Specification: Cross-Agent Multi-Channel Job Search

## Objective

Provide a platform-neutral workflow that discovers location-specific employers and retrieves their public recruitment information through Agent-Reach or a clearly labelled native fallback. The output must distinguish companies from jobs, preserve source evidence, classify domestic and foreign employers, separate social/campus/internship hiring, and expose coverage gaps.

“All” means every retrievable record from the declared geography, date window, channels, query variants, and reachable pages. It never means every job on the internet.

## Runtime Contract

- Preferred capability layer: Agent-Reach, checked with `agent-reach doctor`.
- If the command is absent, automatically install it to a user-local `pipx` environment from the official GitHub archive; if pipx is missing or fails, fall back to `~/.agent-reach-venv` with a working Python 3.10+ interpreter before searching. Never use `sudo` or system directories for this bootstrap.
- After installation, run `agent-reach install --env=auto` as a read-only check, then `agent-reach doctor`. If user-local installation fails, preserve the original error and use host-native web search, browser, HTTP, RSS, PDF, or page reader, labelled `native-fallback`.
- Agent-Reach is a router/installer/diagnostic layer, not the evidence authority and not a guarantee that every channel is available.
- System-changing installation requires explicit user approval. No `sudo`, firewall changes, workspace pollution, credential collection, CAPTCHA bypass, proxy/account rotation, or rate-limit evasion.
- A user-visible browser is required for login-capable sources. The user authenticates directly; the agent never receives passwords, OTPs, cookies, tokens, or private messages.

## Required Intake

Before searching, confirm exact country/province/city/district/park or commute radius, industry and synonyms, role family and Chinese/English synonyms, hiring type, company scope, date window, education, experience, salary, language, work authorization, remote/onsite, and start-date constraints. Missing high-impact fields block company discovery until clarified.

“学历不限” in the user's brief means **no education-based exclusion**. It does not mean “only jobs whose employer writes 学历不限”. Include and classify all education levels and undisclosed education requirements.

## Discovery And Source Matrix

For high-recall requests, use a query matrix and traverse every reachable source to its natural boundary. “Top results”, “first page”, or a fixed result count is not coverage. Candidate discovery and current-job verification are separate measures.

Create a company registry before the opening list. Use separate search streams for:

- government HR bureaus, talent service centers, public talent networks, development zones, SASAC/SOE/central-SOE notices, industry associations, chambers, and university career centers;
- domestic and foreign employer names, legal entities, group/subsidiary/branch names, industrial parks, annual reports, investor-relations pages, and employer domains;
- employer careers pages, public ATS, verified official accounts, and dated recruitment notices;
- user-permitted job boards, only with original-page verification.

Keep `domestic-company track` and `foreign-company track`. Ownership is evidence-based; otherwise `unknown`. Preserve companies with no matching opening and state the outcome or blocker.

Run independent streams for `social-recruitment`, `campus-recruitment`, and `internship`. An omitted type is `unknown`.

## Company And Job Contracts

Every canonical job is company-bound: **No company, no canonical job.** A company record includes:

`company_id`, canonical name, legal entity, parent/subsidiary/branch relationship, domestic/foreign classification and evidence, industry, local presence, official homepage, careers/ATS URL, official account identity, attempted channels, opening outcome, confidence, and blocker.

An opening includes:

`stable_id`, `company_id`, employer, original title, normalized title, matched synonym, job ID, location/district, remote mode, salary source text and normalized range where unambiguous, treatment/benefit source fields, education, experience, hiring type, published/updated/deadline dates, status, date-window state, retrieval times, primary source, all provenance URLs, evidence grade, freshness, match rationale, and risks.

For every in-scope company, the coverage ledger must contain mandatory attempted rows for: (a) Tianjin municipal/district talent and public-employment channels, (b) the employer official website/careers/ATS, and (c) official public accounts and dated recruitment articles. `not_attempted` fails the run; `no_match` or `blocked` is acceptable only with evidence and a stop reason.

## Access Modes And Evidence

Declare `public-only`, `public-discovery-only`, `browser-assisted`, or `hybrid`. For every source record attempted/opened/pages/observations/canonical jobs/stop condition/blocker. A search-result domain does not prove platform coverage.

Evidence grades:

- `A official-confirmed`: employer/official ATS page confirms employer, role, place, application path, and an open/unexpired signal.
- `B platform-confirmed`: individual platform detail page is accessible with substantive fields and an actionable path.
- `C lead`: snippet, aggregator, repost, list page, or incomplete official-account article.
- `D unverifiable`: blocked, withdrawn, login/CAPTCHA wall, or missing actionable evidence.

Only A/B with an explicit open/unexpired signal may be called current. Missing dates/statuses are `unknown`; missing compensation or requirements are `未披露`.

## Workflow

1. Run the Agent-Reach preflight or document the native fallback.
2. Confirm the user brief and lock geography.
3. Build and deduplicate the company registry.
4. Query each company across official, government/talent, university, official-account, ATS, and allowed board sources.
5. Preserve raw observations, verify original pages, normalize fields, and merge clear duplicates while retaining provenance.
6. Recheck A/B records when possible; separate possibly open, expired/closed, and unknown statuses.
7. Produce artifacts and a coverage report whose totals reconcile.

For broad requests, add a high-recall pass before verification: role synonym x hiring type x district x source family; paginate until an explicit boundary or blocker; checkpoint each source family; report candidate, review-queue, and current-verified counts separately.

## Output Artifacts

Create:

- `job-search-YYYYMMDD-HHmm-companies.csv`
- `job-search-YYYYMMDD-HHmm-records.csv`
- `job-search-YYYYMMDD-HHmm-observations.csv`
- `job-search-YYYYMMDD-HHmm-full.md`
- `job-search-YYYYMMDD-HHmm-summary.md`

The summary separately reports domestic/foreign companies, social/campus/internship jobs, A/B/C/D, current/expired/unknown, duplicates, blockers, engine mode, and channel coverage. Counts must reconcile across artifacts.

## Acceptance Criteria

- The brief is confirmed before company discovery.
- Search never leaves the requested geography without explicit permission.
- The company registry exists before canonical jobs.
- Every canonical job has a named company and original source evidence.
- All declared source families have attempted/opened/blocked coverage rows.
- Every in-scope company has completed the three mandatory channel-family passes; missing rows force `partial-incomplete-company-passes`.
- Raw observations survive deduplication in `observations.csv`.
- No protected credential or session data appears in chat, queries, logs, or artifacts.
- No external side effect occurs without action-time confirmation.
- The run discloses uncertainty and never claims global completeness.
