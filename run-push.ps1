param(
    [switch]$DryRun,
    [string]$UserVersion
)

$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$webZip = Join-Path $projectRoot "build/web.zip"

Set-Location $projectRoot
if (-not $env:UV_CACHE_DIR) {
    $env:UV_CACHE_DIR = Join-Path $projectRoot ".uv-cache"
}
if (-not $env:UV_PYTHON_INSTALL_DIR) {
    $env:UV_PYTHON_INSTALL_DIR = Join-Path $projectRoot ".uv-python"
}
& (Join-Path $projectRoot "run-build.ps1")

if (-not (Test-Path -LiteralPath $webZip)) {
    throw "Build did not create $webZip"
}

function Get-DeployUserVersion {
    if ($UserVersion) {
        return $UserVersion
    }

    if ($env:GITHUB_SHA) {
        return $env:GITHUB_SHA.Substring(0, [Math]::Min(12, $env:GITHUB_SHA.Length))
    }

    $gitVersion = (& git rev-parse --short=12 HEAD 2>$null)
    if ($LASTEXITCODE -eq 0 -and $gitVersion) {
        return $gitVersion.Trim()
    }

    return Get-Date -Format "yyyyMMdd-HHmmss"
}

$resolvedUserVersion = Get-DeployUserVersion

$butlerArgs = @("push")
if ($DryRun) {
    $butlerArgs += "--dry-run"
}
$butlerArgs += @($webZip, "jbautista/mapwa:web", "--userversion", $resolvedUserVersion)

Write-Host "Deploying itch.io user version: $resolvedUserVersion"

& butler @butlerArgs
if ($LASTEXITCODE -ne 0) {
    throw "butler push failed. Exit code: $LASTEXITCODE"
}
