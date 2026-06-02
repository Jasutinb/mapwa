$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$buildDir = Join-Path $projectRoot "build"
$oldBuildDir = Join-Path $buildDir "old"
$webZip = Join-Path $buildDir "web.zip"

Set-Location $projectRoot

if (Test-Path -LiteralPath $webZip) {
    New-Item -ItemType Directory -Path $oldBuildDir -Force | Out-Null

    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $archivedZip = Join-Path $oldBuildDir "web-$timestamp.zip"
    Move-Item -LiteralPath $webZip -Destination $archivedZip

    Write-Host "Moved old web.zip to $archivedZip"
}

uv run python -m pygbag --app_name mapwa --title Mapwa --build --archive --disable-sound-format-error main.py
