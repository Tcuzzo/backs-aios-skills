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
$ManagedMarkerFile = "backs-aios-managed"
$ManagedMarkerContent = "backs-aios-managed 0.7.5"
$PackEntries = @(
    ".claude-plugin", ".codex-plugin", ".cursor-plugin", ".gitignore",
    "command-adapters", "docs", "hooks", "i18n", "plays", "skills",
    "CITATION.cff", "INSTALL.md", "LICENSE", "NAMING.md", "NOTICE.md", "README.md",
    "install.sh", "install.ps1"
)
$script:Conflicts = 0

function New-UniqueSibling([string]$Base, [string]$Tag) {
    $candidate = $null
    do {
        $candidate = "$Base.$Tag.$([System.IO.Path]::GetRandomFileName())"
    } while (Test-Path $candidate)
    return $candidate
}

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

function Test-ManagedRoot([string]$Path) {
    if (-not (Test-Path $Path -PathType Container)) { return $false }
    $marker = Join-Path $Path $ManagedMarkerFile
    if (-not (Test-Path $marker -PathType Leaf)) { return $false }
    $content = (Get-Content -Raw $marker -ErrorAction SilentlyContinue).Trim()
    return ($content -match '^backs-aios-managed \d+\.\d+\.\d+$')
}

function Write-ManagedMarker([string]$Marker) {
    $tmp = "$Marker.tmp.$([System.IO.Path]::GetRandomFileName())"
    try {
        Set-Content -NoNewline -Encoding utf8 -Path $tmp -Value "$ManagedMarkerContent`n"
        Move-Item -Path $tmp -Destination $Marker -Force
    } finally {
        if ($tmp -and (Test-Path $tmp)) { Remove-Item -Force $tmp -ErrorAction SilentlyContinue }
    }
}

function Write-ManagedRootMarker([string]$Path) {
    Write-ManagedMarker (Join-Path $Path $ManagedMarkerFile)
}

function Compare-Directories([string]$A, [string]$B) {
    $aFiles = Get-ChildItem -Recurse -Force -File $A | Where-Object { $_.Name -ne $ManagedMarkerFile }
    $bFiles = Get-ChildItem -Recurse -Force -File $B | Where-Object { $_.Name -ne $ManagedMarkerFile }
    if ($aFiles.Count -ne $bFiles.Count) { return $false }
    $aMap = @{}
    foreach ($f in $aFiles) {
        $rel = $f.FullName.Substring($A.Length).TrimStart('\', '/')
        $aMap[$rel] = $f.FullName
    }
    foreach ($f in $bFiles) {
        $rel = $f.FullName.Substring($B.Length).TrimStart('\', '/')
        if (-not $aMap.ContainsKey($rel)) { return $false }
        $ha = (Get-FileHash -Algorithm SHA256 -Path $aMap[$rel]).Hash
        $hb = (Get-FileHash -Algorithm SHA256 -Path $f.FullName).Hash
        if ($ha -ne $hb) { return $false }
    }
    return $true
}

function Install-DirectorySwap([string]$Staging, [string]$Destination) {
    $result = @{ Status = "success"; Holder = $null }
    $holder = $null
    $backup = $null
    $existed = Test-Path $Destination
    try {
        if ($existed) {
            $holder = "$Destination.backs-aios-holder.$([System.IO.Path]::GetRandomFileName())"
            New-Item -ItemType Directory -Path $holder | Out-Null
            $result.Holder = $holder
            $backup = Join-Path $holder "backup"
            Move-Item -Path $Destination -Destination $backup
        }
        Move-Item -Path $Staging -Destination $Destination
        if ($holder -and (Test-Path $holder)) {
            try {
                Remove-Item -Recurse -Force $holder
                $result.Holder = $null
            } catch {
                $result.Status = "cleanup-failed"
            }
        }
    } catch {
        $restored = $false
        if ($backup -and (Test-Path $backup)) {
            try {
                Move-Item -Path $backup -Destination $Destination -Force
                $restored = Test-Path $Destination
            } catch { $restored = $false }
        }
        if ($Staging -and (Test-Path $Staging)) { Remove-Item -Recurse -Force $Staging -ErrorAction SilentlyContinue }
        if ($existed) {
            if ($restored) {
                if ($holder -and (Test-Path $holder)) { Remove-Item -Recurse -Force $holder -ErrorAction SilentlyContinue }
                $result.Status = "restored"
            } else {
                $result.Status = "recovery-failure"
            }
        } else {
            $result.Status = "create-failed"
        }
    }
    return $result
}

function Install-CopyRoot([string]$Label, [string]$Source, [string]$Destination) {
    if (Test-Path $Destination -PathType Leaf) {
        Write-Error "CONFLICT $Label $Destination is a file" -ErrorAction Continue
        $script:Conflicts++
        return
    }
    if (Test-Path $Destination) {
        if (-not (Test-ManagedRoot $Destination)) {
            Write-Error "CONFLICT $Label $Destination already exists (not managed)" -ErrorAction Continue
            $script:Conflicts++
            return
        }
    }
    $staging = $null
    try {
        $staging = New-UniqueSibling $Destination "backs-aios-staging"
        New-Item -ItemType Directory -Path $staging | Out-Null
        Copy-PortableTree $Source $staging
        Write-ManagedRootMarker $staging
        $existed = Test-Path $Destination
        if ($existed) {
            if (Compare-Directories $staging $Destination) {
                Remove-Item -Recurse -Force $staging
                $staging = $null
                try {
                    Write-ManagedRootMarker $Destination
                    Write-Host "OK       $Label $Destination"
                } catch {
                    Write-Error "ERROR    $Label $Destination marker refresh failed" -ErrorAction Continue
                    $script:Conflicts++
                }
                return
            }
        }
        $result = Install-DirectorySwap $staging $Destination
        switch ($result.Status) {
            "success" {
                if ($existed) { Write-Host "UPDATED  $Label $Destination" }
                else { Write-Host "CREATED  $Label $Destination" }
            }
            "cleanup-failed" {
                if ($existed) { Write-Host "UPDATED  $Label $Destination" }
                else { Write-Host "CREATED  $Label $Destination" }
                Write-Host "WARNING  $Label $Destination holder cleanup failed: $($result.Holder)"
            }
            "create-failed" {
                Write-Error "ERROR    $Label $Destination create failed" -ErrorAction Continue
                $script:Conflicts++
            }
            "restored" {
                Write-Error "ERROR    $Label $Destination swap failed; restored original" -ErrorAction Continue
                $script:Conflicts++
            }
            "recovery-failure" {
                Write-Error "ERROR    $Label $Destination recovery failure: original retained in holder $($result.Holder)" -ErrorAction Continue
                $script:Conflicts++
            }
        }
    } catch {
        if ($staging -and (Test-Path $staging)) { Remove-Item -Recurse -Force $staging -ErrorAction SilentlyContinue }
        Write-Error "ERROR    $Label $Destination : $_" -ErrorAction Continue
        $script:Conflicts++
    }
}

function Install-PackCopy([string]$Label, [string]$Destination) {
    if (Test-Path $Destination -PathType Leaf) {
        Write-Error "CONFLICT $Label $Destination is a file" -ErrorAction Continue
        $script:Conflicts++
        return
    }
    if (Test-Path $Destination) {
        if (-not (Test-ManagedRoot $Destination)) {
            Write-Error "CONFLICT $Label $Destination already exists (not managed)" -ErrorAction Continue
            $script:Conflicts++
            return
        }
    }
    $staging = $null
    try {
        $staging = New-UniqueSibling $Destination "backs-aios-staging"
        New-Item -ItemType Directory -Path $staging | Out-Null
        Copy-Pack $staging
        Write-ManagedRootMarker $staging
        $existed = Test-Path $Destination
        if ($existed) {
            if (Compare-Directories $staging $Destination) {
                Remove-Item -Recurse -Force $staging
                $staging = $null
                try {
                    Write-ManagedRootMarker $Destination
                    Write-Host "OK       $Label $Destination"
                } catch {
                    Write-Error "ERROR    $Label $Destination marker refresh failed" -ErrorAction Continue
                    $script:Conflicts++
                }
                return
            }
        }
        $result = Install-DirectorySwap $staging $Destination
        switch ($result.Status) {
            "success" {
                if ($existed) { Write-Host "UPDATED  $Label $Destination" }
                else { Write-Host "CREATED  $Label $Destination" }
            }
            "cleanup-failed" {
                if ($existed) { Write-Host "UPDATED  $Label $Destination" }
                else { Write-Host "CREATED  $Label $Destination" }
                Write-Host "WARNING  $Label $Destination holder cleanup failed: $($result.Holder)"
            }
            "create-failed" {
                Write-Error "ERROR    $Label $Destination create failed" -ErrorAction Continue
                $script:Conflicts++
            }
            "restored" {
                Write-Error "ERROR    $Label $Destination swap failed; restored original" -ErrorAction Continue
                $script:Conflicts++
            }
            "recovery-failure" {
                Write-Error "ERROR    $Label $Destination recovery failure: original retained in holder $($result.Holder)" -ErrorAction Continue
                $script:Conflicts++
            }
        }
    } catch {
        if ($staging -and (Test-Path $staging)) { Remove-Item -Recurse -Force $staging -ErrorAction SilentlyContinue }
        Write-Error "ERROR    $Label $Destination : $_" -ErrorAction Continue
        $script:Conflicts++
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
        Install-CopyRoot $Label $_.FullName $Path
    }
}

function Install-CommandSkills([string]$Label, [string]$Destination) {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    foreach ($Name in @("agent-build", "bughunt", "elite-build", "grade", "parallel-work", "secure-delivery", "tribunal", "web-build")) {
        $Source = Join-Path $Root "skills/$Name"
        $Path = Join-Path $Destination $Name
        Install-CopyRoot $Label $Source $Path
    }
}

function Install-Runtime {
    $Destination = Split-Path -Parent $Runtime
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Install-PackCopy "runtime" $Runtime
}

function Install-Commands([string]$Label, [string]$Destination) {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -File (Join-Path $Root "command-adapters/*.md") | ForEach-Object {
        $Path = Join-Path $Destination $_.Name
        $Tmp = New-UniqueSibling $Path "tmp"
        $Rendered = Get-Content -Raw $_.FullName
        $Rendered = $Rendered.Replace('${CLAUDE_PLUGIN_ROOT}', $Runtime)
        $Rendered = $Rendered.Replace('${CURSOR_PLUGIN_ROOT}', $Runtime)
        $Rendered = $Rendered.TrimEnd() + "`n`n<!-- $ManagedCommandMarker -->`n"
        Set-Content -NoNewline -Encoding utf8 -Path $Tmp -Value $Rendered
        if (Test-Path $Path) {
            $Existing = Get-Content -Raw $Path -ErrorAction SilentlyContinue
            if (-not $Existing.Contains($ManagedCommandMarker)) {
                Write-Error "CONFLICT $Label $Path already exists" -ErrorAction Continue
                $script:Conflicts++
                Remove-Item -Force $Tmp -ErrorAction SilentlyContinue
                return
            }
            if ($Existing -eq $Rendered) {
                Remove-Item -Force $Tmp
                Write-Host "OK       $Label $Path"
            } else {
                try {
                    Move-Item -Path $Tmp -Destination $Path -Force
                    Write-Host "UPDATED  $Label $Path"
                } catch {
                    Remove-Item -Force $Tmp -ErrorAction SilentlyContinue
                    Write-Error "ERROR    $Label $Path update failed" -ErrorAction Continue
                    $script:Conflicts++
                }
            }
        } else {
            try {
                Move-Item -Path $Tmp -Destination $Path
                Write-Host "CREATED  $Label $Path"
            } catch {
                Remove-Item -Force $Tmp -ErrorAction SilentlyContinue
                Write-Error "ERROR    $Label $Path create failed" -ErrorAction Continue
                $script:Conflicts++
            }
        }
    }
}

function Install-OpencodePlugin {
    $Source = Join-Path $Runtime "hooks/opencode-plugin.js"
    $DestDir = Join-Path $HOME ".config/opencode/plugins"
    $Dest = Join-Path $DestDir "backs-aios.js"
    $Marker = "$Dest.backs-aios-managed"
    $TmpDest = $null
    $BackupDest = $null
    if (-not (Test-Path $Source -PathType Leaf)) {
        Write-Error "ERROR opencode-plugin source missing: $Source" -ErrorAction Continue
        $script:Conflicts++
        return
    }
    New-Item -ItemType Directory -Force -Path $DestDir | Out-Null
    if (Test-Path $Dest -PathType Container) {
        Write-Error "CONFLICT opencode-plugin $Dest is a directory" -ErrorAction Continue
        $script:Conflicts++
        return
    }
    if ((Test-Path $Dest) -or (Test-Path $Marker)) {
        if (-not (Test-Path $Marker -PathType Leaf)) {
            Write-Error "CONFLICT opencode-plugin $Dest already exists (not managed)" -ErrorAction Continue
            $script:Conflicts++
            return
        }
        $markerContent = (Get-Content -Raw $Marker -ErrorAction SilentlyContinue).Trim()
        if ($markerContent -notmatch '^backs-aios-managed \d+\.\d+\.\d+$') {
            Write-Error "CONFLICT opencode-plugin $Dest already exists (not managed)" -ErrorAction Continue
            $script:Conflicts++
            return
        }
    }
    try {
        $TmpDest = New-UniqueSibling $Dest "tmp"
        Copy-Item -Path $Source -Destination $TmpDest
        if (Test-Path $Dest) {
            $existing = Get-Content -Raw $Dest -ErrorAction SilentlyContinue
            $newContent = Get-Content -Raw $TmpDest -ErrorAction SilentlyContinue
            if ($existing -eq $newContent) {
                Remove-Item -Force $TmpDest
                try {
                    Write-ManagedMarker $Marker
                    Write-Host "OK       opencode-plugin $Dest"
                } catch {
                    Write-Error "ERROR    opencode-plugin $Dest marker refresh failed" -ErrorAction Continue
                    $script:Conflicts++
                }
                return
            }
            $BackupDest = New-UniqueSibling $Dest "backs-aios-backup"
            Copy-Item -Path $Dest -Destination $BackupDest
            Move-Item -Path $TmpDest -Destination $Dest -Force
            try {
                Write-ManagedMarker $Marker
                Remove-Item -Force $BackupDest -ErrorAction SilentlyContinue
                $BackupDest = $null
                Write-Host "UPDATED  opencode-plugin $Dest"
            } catch {
                if ($BackupDest -and (Test-Path $BackupDest)) {
                    Move-Item -Path $BackupDest -Destination $Dest -Force
                    if (Test-Path $Dest) {
                        Write-Error "ERROR    opencode-plugin $Dest marker replace failed; restored adapter" -ErrorAction Continue
                    } else {
                        Write-Error "ERROR    opencode-plugin $Dest recovery failure: adapter backup retained at $BackupDest" -ErrorAction Continue
                    }
                } else {
                    Write-Error "ERROR    opencode-plugin $Dest marker replace failed; no backup available" -ErrorAction Continue
                }
                $script:Conflicts++
            }
        } else {
            Move-Item -Path $TmpDest -Destination $Dest
            try {
                Write-ManagedMarker $Marker
                Write-Host "CREATED  opencode-plugin $Dest"
            } catch {
                Remove-Item -Force $Dest -ErrorAction SilentlyContinue
                Write-Error "ERROR    opencode-plugin $Dest marker create failed; removed adapter" -ErrorAction Continue
                $script:Conflicts++
            }
        }
    } catch {
        if ($BackupDest -and (Test-Path $BackupDest)) {
            Move-Item -Path $BackupDest -Destination $Dest -Force
            if (-not (Test-Path $Dest)) {
                Write-Error "ERROR    opencode-plugin $Dest recovery failure: adapter backup retained at $BackupDest" -ErrorAction Continue
                $script:Conflicts++
                return
            }
        } elseif ((Test-Path $Dest) -and -not (Test-Path $Marker)) {
            Remove-Item -Force $Dest -ErrorAction SilentlyContinue
        }
        if ($TmpDest -and (Test-Path $TmpDest)) { Remove-Item -Force $TmpDest -ErrorAction SilentlyContinue }
        Write-Error "ERROR    opencode-plugin $Dest : $_" -ErrorAction Continue
        $script:Conflicts++
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
    Install-OpencodePlugin
}

function Install-Claude {
    Install-Skills "claude" (Join-Path $HOME ".claude/skills")
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
    Install-PackCopy "cursor" $Path
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
