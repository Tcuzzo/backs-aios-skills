# Translations

This directory holds complete language mirrors of the BACKS AIOS Skills pack.
**English is canonical.** Translations track it release by release and may lag
between releases; when a mirror and the English source disagree, the English
source is the law.

## Structure

Each mirror is a full drop-in copy of the pack under `i18n/<lang>/`:

- `i18n/<lang>/skills/<name>/SKILL.md` — all 27 skills, same directory names
- `i18n/<lang>/plays/*.md` — all 8 plays, same file names
- `i18n/<lang>/README.md`, `INSTALL.md`, `NAMING.md`

Available: [es](es/README.md) · [pt-BR](pt-BR/README.md) · [fr](fr/README.md) ·
[de](de/README.md) · [hi](hi/README.md) · [zh-CN](zh-CN/README.md)

## What stays English, and why

`LICENSE`, `NOTICE.md`, and `CITATION.cff` are legal text and factual citations —
translating them could change their meaning, so they exist once, in English, at the
repo root. `commands/` and `hooks/` are executable wiring — agents load them by
their English identifiers, so translating them would break the pack. The mirrors do
not copy any of these. Skill names, play names, file names, and trigger keys also
stay English everywhere: they are the pack's invocation keys.

## Using a mirror as a drop-in skills directory

A mirror has the same tree shape as the root pack, so it drops in the same way:
point your agent's skill directory at `i18n/<lang>/skills/` instead of `skills/`,
and every relative link resolves inside the mirror. The English trigger words still
work — each translated skill keeps them and adds natural native-language triggers.

## Contributing a new language

Open a pull request that mirrors the tree: `i18n/<code>/` with all 38 files
(27 skills + 8 plays + `README.md`, `INSTALL.md`, `NAMING.md`), using the
language's standard code (like `pt-BR` or `zh-CN`). The translation contract's
laws apply: native register over word-for-word, full depth kept, names and links
unchanged, English triggers kept plus native ones added, community tech terms,
citations verbatim, numbers and hard rules identical. Open your mirror's
`README.md` with one line linking back to this canonical English pack.
