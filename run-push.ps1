param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$webZip = Join-Path $projectRoot "build/web.zip"

Set-Location $projectRoot
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
