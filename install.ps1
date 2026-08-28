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
$Runtime = Join-Path $HOME ".local/share/backs-aios/current"
$ManagedCommandMarker = "backs-aios-managed-command"
$PackEntries = @(
    ".claude-plugin", ".codex-plugin", ".cursor-plugin", ".gitignore",
    "commands", "docs", "hooks", "i18n", "plays", "skills",
    "CITATION.cff", "INSTALL.md", "LICENSE", "NAMING.md", "NOTICE.md", "README.md",
    "install.sh", "install.ps1"
)
$script:Conflicts = 0

function Copy-PortableTree([string]$Source, [string]$Destination) {
    if (Test-Path -PathType Leaf $Source) {
        Copy-Item -Path $Source -Destination $Destination
        return
    }
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -Force $Source | ForEach-Object {
        if ($_.Name -notin @(".git", ".pytest_cache", "__pycache__") -and $_.Extension -ne ".pyc") {
            Copy-PortableTree $_.FullName (Join-Path $Destination $_.Name)
        }
    }
}

function Copy-Pack([string]$Destination) {
    foreach ($Name in $PackEntries) {
        Copy-PortableTree (Join-Path $Root $Name) (Join-Path $Destination $Name)
    }
}

function Install-Skills(
    [string]$Label,
    [string]$Destination,
    [string]$SkillsRoot = $Skills
) {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -Directory $SkillsRoot | ForEach-Object {
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

function Install-CommandSkills([string]$Label, [string]$Destination) {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    foreach ($Name in @("agent-build", "bughunt", "elite-build", "grade", "parallel-work", "secure-delivery", "tribunal", "web-build")) {
        $Source = Join-Path $Root "skills/$Name"
        $Path = Join-Path $Destination $Name
        if (Test-Path $Path) {
            Write-Error "CONFLICT $Label $Path already exists" -ErrorAction Continue
            $script:Conflicts++
        } else {
            Copy-Item -Recurse -Path $Source -Destination $Path
            Write-Host "COPIED   $Label $Path"
        }
    }
}

function Install-Runtime {
    $Destination = Split-Path -Parent $Runtime
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    if (Test-Path $Runtime) {
        Write-Error "CONFLICT runtime $Runtime already exists" -ErrorAction Continue
        $script:Conflicts++
        return
    }
    New-Item -ItemType Directory -Path $Runtime | Out-Null
    Copy-Pack $Runtime
    Write-Host "COPIED   runtime $Runtime"
}

function Install-Commands([string]$Label, [string]$Destination) {
    # Native roots: ~/.config/opencode/commands and ~/.claude/commands
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -File (Join-Path $Root "commands/*.md") | ForEach-Object {
        $Path = Join-Path $Destination $_.Name
        $Rendered = Get-Content -Raw $_.FullName
        $Rendered = $Rendered.Replace('${CLAUDE_PLUGIN_ROOT}', $Runtime)
        $Rendered = $Rendered.Replace('${CURSOR_PLUGIN_ROOT}', $Runtime)
        $Rendered = $Rendered.TrimEnd() + "`n`n<!-- $ManagedCommandMarker -->`n"
        if (Test-Path $Path) {
            $Existing = Get-Content -Raw $Path
            if (-not $Existing.Contains($ManagedCommandMarker)) {
                Write-Error "CONFLICT $Label $Path already exists" -ErrorAction Continue
                $script:Conflicts++
                return
            }
            if ($Existing -eq $Rendered) {
                Write-Host "OK       $Label $Path"
            } else {
                Set-Content -NoNewline -Encoding utf8 -Path $Path -Value $Rendered
                Write-Host "UPDATED  $Label $Path"
            }
        } else {
            Set-Content -NoNewline -Encoding utf8 -Path $Path -Value $Rendered
            Write-Host "CREATED  $Label $Path"
        }
    }
}

function Install-Codex {
    Install-Skills "codex" (Join-Path $HOME ".codex/skills")
    if ($Locale -ne "en") {
        Install-CommandSkills "codex-cmd" (Join-Path $HOME ".codex/skills")
    }
}

function Install-OpenCode {
    Install-Skills "opencode" (Join-Path $HOME ".config/opencode/skills")
    Install-Commands "opencode" (Join-Path $HOME ".config/opencode/commands")
}

function Install-Claude {
    Install-Skills "claude" (Join-Path $HOME ".claude/skills")
    Install-Commands "claude-cmd" (Join-Path $HOME ".claude/commands")
}

function Install-Portable {
    Install-Skills "portable" (Join-Path $HOME ".agents/skills")
    if ($Locale -ne "en") {
        Install-CommandSkills "portable-cmd" (Join-Path $HOME ".agents/skills")
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
        Copy-Pack $Path
        Write-Host "COPIED   cursor $Path"
    }
    if ($Locale -ne "en") {
        Write-Host "NOTE: Cursor's full plugin stays English; locale $Locale was installed only to skill-only targets."
    }
}

switch ($Target) {
    "all" {
        Install-Runtime
        Install-Codex
        Install-CursorPlugin
        Install-OpenCode
        Install-Claude
        Install-Portable
    }
    "codex" { Install-Runtime; Install-Codex }
    "cursor" { Install-CursorPlugin }
    "opencode" { Install-Runtime; Install-OpenCode }
    "claude" { Install-Runtime; Install-Claude }
    "portable" { Install-Runtime; Install-Portable }
}

if ($script:Conflicts -gt 0) {
    throw "$script:Conflicts conflict(s) left untouched. Move or rename them, then rerun."
}

Write-Host "BACKS AIOS skills and host-native commands registered. Start a new agent session and invoke optimus."
