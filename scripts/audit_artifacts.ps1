$ErrorActionPreference = "Stop"

$RootDir = Resolve-Path (Join-Path $PSScriptRoot "..")
$Failures = 0
$Warnings = 0

function Section($Title) {
    ""
    $Title
    "-" * $Title.Length
}

function Ok($Message) {
    "ok: $Message"
}

function Warn($Message) {
    $script:Warnings += 1
    "warn: $Message"
}

function Fail($Message) {
    $script:Failures += 1
    "fail: $Message"
}

function Check-Path($Path) {
    if (Test-Path (Join-Path $RootDir $Path)) {
        Ok "$Path exists"
    } else {
        Fail "$Path is missing"
    }
}

function Check-GitignorePattern($Pattern) {
    $Gitignore = Join-Path $RootDir ".gitignore"
    if ((Test-Path $Gitignore) -and ((Get-Content $Gitignore) -contains $Pattern)) {
        Ok ".gitignore excludes $Pattern"
    } else {
        Fail ".gitignore does not exclude $Pattern"
    }
}

function Show-Inventory($Path, $Label) {
    $FullPath = Join-Path $RootDir $Path
    $Files = @()

    if (Test-Path $FullPath) {
        $Files = @(Get-ChildItem $FullPath -Recurse -File | Sort-Object FullName)
    }

    "${Label}: $($Files.Count)"
    foreach ($File in $Files) {
        $File.FullName.Substring($RootDir.Path.Length + 1).Replace("\", "/")
    }
    ""
}

"Artifact audit"
"=============="
""
"Root: $RootDir"

Section "Required files"
@(
    ".gitignore",
    "README.md",
    "ARTIFACT_INDEX.md",
    "PROJECT_STATUS.md",
    "AGENTS.md",
    "cases",
    "benchmarks",
    "evals",
    "protocols",
    "scripts"
) | ForEach-Object { Check-Path $_ }

Section "Artifact inventory"
Show-Inventory "evals" "Evals"
Show-Inventory "benchmarks" "Benchmarks"
Show-Inventory "protocols" "Protocols"
Show-Inventory "cases" "Cases"

Section "AGENTS.md checks"
$AgentsPath = Join-Path $RootDir "AGENTS.md"
if (Test-Path $AgentsPath) {
    $AgentsText = Get-Content -Raw $AgentsPath
    if ($AgentsText -match "Slippery Stone Protocol") {
        Ok "Slippery Stone Protocol is logged"
    } else {
        Fail "Slippery Stone Protocol is missing"
    }

    if ($AgentsText -match "Track dumpsite automation") {
        Ok "Track dumpsite automation is logged"
    } else {
        Warn "Track dumpsite automation is missing"
    }
} else {
    Fail "AGENTS.md is missing"
}

Section "Anonymity scan"
$MarkerPattern = "halil|mayor|codex|chatgpt\.com|github\.dev|samsung|android|mx keys|cafe|phone app|ritual timing|hallelujah|found and explained|tremor|adhd|health|medical|accessibility"
$MarkdownFiles = @(
    Get-ChildItem $RootDir -Recurse -File -Include "*.md" |
        Where-Object { $_.FullName -notlike (Join-Path $RootDir "private") + "*" }
)
$MarkerHits = @($MarkdownFiles | Select-String -Pattern $MarkerPattern -CaseSensitive:$false)

if ($MarkerHits.Count -gt 0) {
    Fail "public anonymity markers found"
    foreach ($Hit in $MarkerHits) {
        $RelativePath = $Hit.Path.Substring($RootDir.Path.Length + 1).Replace("\", "/")
        "${RelativePath}:$($Hit.LineNumber): $($Hit.Line.Trim())"
    }
} else {
    Ok "no obvious public anonymity markers found"
}

Section "Upload hazards"
Check-GitignorePattern "ffmpeg.exe"
Check-GitignorePattern "ffprobe.exe"
Check-GitignorePattern "delivery/"
Check-GitignorePattern "*.zip"
Check-GitignorePattern "private/"

if ((Test-Path (Join-Path $RootDir "ffmpeg.exe")) -or (Test-Path (Join-Path $RootDir "ffprobe.exe"))) {
    Warn "local media binaries exist; do not manually upload the whole folder"
} else {
    Ok "no local media binaries found"
}

if (Test-Path (Join-Path $RootDir "delivery")) {
    Ok "delivery bundle folder exists locally and is ignored"
} else {
    Ok "no local delivery folder found"
}

Section "Delivery bundle"
$ZipPath = Join-Path $RootDir "delivery/AS-010-03.07.2026-00-37-artifacts-github-bundle.zip"
if (Test-Path $ZipPath) {
    Ok "delivery zip exists"
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $Zip = [System.IO.Compression.ZipFile]::OpenRead($ZipPath)
    try {
        $Entries = @($Zip.Entries | ForEach-Object { $_.FullName })
        $Entries
        if ($Entries | Where-Object { $_ -match "\.exe$|^delivery/|\.zip$" }) {
            Fail "delivery zip contains excluded files"
        } else {
            Ok "delivery zip excludes binaries, nested zips, and delivery folder"
        }

        $ExpectedEntries = @(
            Get-ChildItem $RootDir -Recurse -File |
                Where-Object {
                    $_.FullName -notlike (Join-Path $RootDir "delivery") + "*" -and
                    $_.FullName -notlike (Join-Path $RootDir "private") + "*" -and
                    $_.Extension -ne ".zip" -and
                    $_.Name -notin @("ffmpeg.exe", "ffprobe.exe")
                } |
                ForEach-Object { $_.FullName.Substring($RootDir.Path.Length + 1).Replace("\", "/") } |
                Sort-Object
        )

        $MissingEntries = @($ExpectedEntries | Where-Object { $Entries -notcontains $_ })
        $ExtraEntries = @($Entries | Where-Object { $ExpectedEntries -notcontains $_ })

        if ($MissingEntries.Count -gt 0) {
            Warn "delivery zip is missing current artifact files; manual upload mode treats this as non-blocking"
            $MissingEntries
        }

        if ($ExtraEntries.Count -gt 0) {
            Warn "delivery zip contains stale or unexpected files; manual upload mode treats this as non-blocking"
            $ExtraEntries
        }

        if (($MissingEntries.Count -eq 0) -and ($ExtraEntries.Count -eq 0)) {
            Ok "delivery zip matches current artifact files"
        }
    } finally {
        $Zip.Dispose()
    }
} else {
    Warn "delivery zip not found"
}

Section "Focused AS-010 update bundle"
$UpdateZipPath = Join-Path $RootDir "delivery/AS-010-03.07.2026-00-37-boundary-drift-contextual-fog-update.zip"
if (Test-Path $UpdateZipPath) {
    Ok "AS-010 focused update zip exists"
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $UpdateZip = [System.IO.Compression.ZipFile]::OpenRead($UpdateZipPath)
    try {
        $UpdateEntries = @($UpdateZip.Entries | ForEach-Object { $_.FullName })
        $UpdateEntries
        $RequiredUpdateEntries = @(
            "evals/AS-010-03.07.2026-00-00-boundary-drift-contextual-fog.md",
            "ARTIFACT_INDEX.md",
            "PROJECT_STATUS.md",
            "README.md",
            "scripts/audit_artifacts.ps1",
            "scripts/audit_artifacts.sh"
        )
        $MissingUpdateEntries = @($RequiredUpdateEntries | Where-Object { $UpdateEntries -notcontains $_ })
        if ($MissingUpdateEntries.Count -gt 0) {
            Fail "AS-010 focused update zip is missing required files"
            $MissingUpdateEntries
        } else {
            Ok "AS-010 focused update zip contains required files"
        }
    } finally {
        $UpdateZip.Dispose()
    }
} else {
    Fail "AS-010 focused update zip is missing"
}

Section "Git state"
if (Test-Path (Join-Path $RootDir ".git")) {
    Ok "git repository is initialized"
    if (Get-Command git -ErrorAction SilentlyContinue) {
        git -C $RootDir status --short
    } else {
        Warn "git command is unavailable"
    }
} else {
    Ok "this folder is not initialized as a git repository"
}

""
"Summary"
"-------"
"Failures: $Failures"
"Warnings: $Warnings"

if ($Failures -gt 0) {
    exit 1
}
