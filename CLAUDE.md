# BACKS AIOS — repo operating rules

This is the public home of the BACKS AIOS skills pack. Two rules are iron,
on every commit, every branch, from every agent and harness that touches it:

## 1. Attribution (BACKS invariant 21)

The work belongs to the operator and BACKS. Models are tools that ran inside
his harness — never authors. That means:

- **No `Co-Authored-By: <model>` trailers, ever, on any commit or PR.**
- **No "Generated with <model>" footers** in commits, code, or docs.
- Provenance (which model built/graded) is a fact for the private ledger,
  not credit on the public record.
- Genuinely borrowed external scaffolds are cited by their author and
  license — that stays.

## 2. Public-safety scrub (BACKS invariant 26 class)

Nothing personal ever ships in this repo — tree or history:

- No real emails (only `*.example.invalid`, `*.nostore`/fixture, and
  GitHub `noreply` identities).
- No private IPs (`192.168.*`, `10.*`, `172.16-31.*`) or hostnames.
- No real machine paths (`/home/<name>`, `/mnt/...`, `/opt/...`).
- No phone numbers, chat IDs, tokens, or keys.

`tests/test_public_hygiene.py` enforces both rules and runs in CI — a leak
fails the build loudly. If it trips, the fix is to scrub BEFORE pushing,
not to weaken the test.

## Method

The skills in this repository are the harness. When building or fixing
anything here, load the matching BACKS skill first
(`optimus`/`building-with-backs` to ground, `wayfinder` to chart,
`elite-build-understanding` to plan, `fix-shit` for breakage) — a skill
named but not invoked did not happen.
