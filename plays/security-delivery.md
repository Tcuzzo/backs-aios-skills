# Play: Security & Delivery

The ship gate for anything a customer or another machine will run. Safe by
construction: the harness enforces it, the model is never trusted to remember.

## When to run

- A repo, agent, or app is about to be delivered, published, or deployed.
- An agent with tools touches untrusted content — web pages, issues, email, input.
- You are adding dependencies or CI to something that ships.

The ship gate, at a glance:

```
+--------------------------------------------+
| 1 secret gate  verified-only scan; one     |
|   live credential fails the build          |
+--------------------------------------------+
| 2 egress lockdown  deny by default;        |
|   canonicalize before allowlist match      |
+--------------------------------------------+
| 3 break the lethal trifecta  one leg       |
|   always missing on every path             |
+--------------------------------------------+
| 4 taint tracking  tainted session =>       |
|   policy-gate every exfil-capable action   |
+--------------------------------------------+
| 5 supply chain  hash-pin every dep, no     |
|   install scripts, SHA-pinned CI           |
+--------------------------------------------+
| 6 clean-code-gauntlet  mutate detectors,   |<--------------------------+
|   parsers, predicates to zero survivors    |  a survivor or a          |
+--------------------------------------------+  sandbox catch ->         |
| 7 sniper-testing  mock outbound network    |   +---------------------+ |
|   only, never payload or parser            |   |  LORD OF THE LOOP   |-+
+--------------------------------------------+   | one hand drives the |
| 8 sandbox before ship  outbound blocked,   |-->| loop: dispatch,     |
|   watch writes + calls, hard-kill armed    |   | judge, loop back    |
+--------------------------------------------+   | until the gate is   |
| 9 provenance  SBOM + signed provenance;    |   | green. a lane never |
|   still review the source                  |   | lands its own work. |
+--------------------------------------------+   +---------------------+
          |
          | every gate green
          v
+--------------------------------------------+
| LANDING GATE -- all green or no ship:      |
| no live credential anywhere . no path      |
| holds all three trifecta legs . deps +     |
| CI hash-pinned . zero surviving mutants    |
| . sandboxed before ship                    |
+--------------------------------------------+
```

## The chain

1. Secret gate — run a secret scanner in verified-only mode (it checks each
   candidate credential against the live provider). One confirmed-live credential
   fails the build. No exception.
2. Egress lockdown — deny outbound by default; route everything through a proxy
   that allowlists bare hostnames. Canonicalize and validate the hostname BEFORE
   matching: reject null bytes, percent tricks, and CRLF. The null-byte
   `evil-host\x00.trusted.com` bypass is real and has shipped.
3. Break the lethal trifecta — architect every execution path so at least ONE of
   these is always missing: private-data access, untrusted-content exposure,
   external communication. You cannot fully block prompt injection; you can make
   it unable to steal.
4. Taint tracking — ingesting untrusted content marks the session tainted. While
   tainted, policy-gate every exfil-capable action (outbound HTTP, email, PR
   creation) in the harness — never leave it to the model's judgment.
5. Supply chain — hash-pin every dependency and block install-time scripts. Pin
   every CI action to a full commit hash, not a tag.
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — security code
   carries the strictest bar. Run mutation testing over every detector, parser,
   and policy predicate, and drive surviving mutants to zero. A flipped comparison
   inside a threat check that the suite still passes IS the vulnerability.
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — mock ONLY the outbound
   network, never the payload or the parser under test: a mocked detector is a
   blind sensor in production.
8. Sandbox before ship — run the built artifact in an ephemeral sandbox with all
   outbound blocked and a resource hard-kill armed. Watch what it writes and what
   it tries to call.
9. Provenance — emit a software bill of materials, plus signed provenance if you
   have it. Then still review the source: provenance signs malicious source
   faithfully too.

## Standing protections during any build run

- Deny-write on sensitive paths: shell startup files, git config and hooks, DNS
  config, SSH keys.
- Least-privilege tools. A confirm-step is reserved ONLY for genuinely destructive
  or irreversible operations — data loss, spend, an irreversible external action.
  Never gate a benign capability, and never gate your human.

## Hard gates — any one fails the play

- A confirmed-live credential anywhere in the deliverable or its history.
- Any execution path holding all three trifecta legs at once.
- An unpinned dependency, an install script, or a tag-pinned CI action.
- A surviving mutant in a detector, parser, or policy predicate.
- The artifact was never run in a sandbox before ship.

**Weight:** mostly free construction discipline plus light scanner and sandbox passes; the heavy step is mutation over every detector and policy predicate — it pays on anything a customer or another machine will run.
