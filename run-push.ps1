param(
    [switch]$DryRun
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

$butlerArgs = @("push")
if ($DryRun) {
    $butlerArgs += "--dry-run"
}
$butlerArgs += @($webZip, "jbautista/mapwa:web")

& butler @butlerArgs
if ($LASTEXITCODE -ne 0) {
    throw "butler push failed. Exit code: $LASTEXITCODE"
}
