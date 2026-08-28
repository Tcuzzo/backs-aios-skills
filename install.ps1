param(
    [ValidateSet("all", "codex", "cursor", "opencode", "claude", "portable")]
    [string]$Target = "all",
    [ValidateSet("en", "de", "es", "fr", "hi", "pt-BR", "zh-CN")]
    [string]$Locale = "en"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Skills = if ($Locale -eq "en") {
    Join-Path $Root "skills"
} else {
    Join-Path $Root "i18n/$Locale/skills"
}
$script:Conflicts = 0

function Install-Skills([string]$Label, [string]$Destination) {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -Directory $Skills | ForEach-Object {
        if (-not (Test-Path (Join-Path $_.FullName "SKILL.md"))) { return }
        $Path = Join-Path $Destination $_.Name
        if (Test-Path $Path) {
            Write-Error "CONFLICT $Label $Path already exists" -ErrorAction Continue
            $script:Conflicts++
        } else {
            Copy-Item -Recurse -Path $_.FullName -Destination $Path
            Write-Host "COPIED   $Label $Path"
        }
    }
}

function Install-CursorPlugin {
    $Destination = Join-Path $HOME ".cursor/plugins/local"
    $Path = Join-Path $Destination "backs-aios"
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    if (Test-Path $Path) {
        Write-Error "CONFLICT cursor $Path already exists" -ErrorAction Continue
        $script:Conflicts++
    } else {
        New-Item -ItemType Directory -Path $Path | Out-Null
        Get-ChildItem -Force $Root |
            Where-Object { $_.Name -ne ".git" } |
            Copy-Item -Recurse -Destination $Path
        Write-Host "COPIED   cursor $Path"
    }
    if ($Locale -ne "en") {
        Write-Host "NOTE: Cursor's full plugin stays English; locale $Locale was installed only to skill-only targets."
    }
}

switch ($Target) {
    "all" {
        Install-Skills "codex" (Join-Path $HOME ".codex/skills")
        Install-CursorPlugin
        Install-Skills "opencode" (Join-Path $HOME ".config/opencode/skills")
        Install-Skills "claude" (Join-Path $HOME ".claude/skills")
        Install-Skills "portable" (Join-Path $HOME ".agents/skills")
    }
    "codex" { Install-Skills "codex" (Join-Path $HOME ".codex/skills") }
    "cursor" { Install-CursorPlugin }
    "opencode" { Install-Skills "opencode" (Join-Path $HOME ".config/opencode/skills") }
    "claude" { Install-Skills "claude" (Join-Path $HOME ".claude/skills") }
    "portable" { Install-Skills "portable" (Join-Path $HOME ".agents/skills") }
}

if ($script:Conflicts -gt 0) {
    throw "$script:Conflicts conflict(s) left untouched. Move or rename them, then rerun."
}

Write-Host "BACKS AIOS registered. Start a new agent session and invoke optimus."
