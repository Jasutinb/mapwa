$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$buildDir = Join-Path $projectRoot "build"
$oldBuildDir = Join-Path $buildDir "old"
$webZip = Join-Path $buildDir "web.zip"
$webDir = Join-Path $buildDir "web"
$stageDir = Join-Path $buildDir "mapwa"
$stageMain = Join-Path $stageDir "main.py"
$stageWebDir = Join-Path $stageDir "build/web"
$stageWebZip = Join-Path $stageDir "build/web.zip"

Set-Location $projectRoot

$resolvedBuildDir = [System.IO.Path]::GetFullPath($buildDir)
$resolvedStageDir = [System.IO.Path]::GetFullPath($stageDir)
$resolvedWebDir = [System.IO.Path]::GetFullPath($webDir)
if (-not $resolvedStageDir.StartsWith($resolvedBuildDir)) {
    throw "Refusing to clean staging directory outside build: $resolvedStageDir"
}
if (-not $resolvedWebDir.StartsWith($resolvedBuildDir)) {
    throw "Refusing to clean web output outside build: $resolvedWebDir"
}

if (Test-Path -LiteralPath $webZip) {
    New-Item -ItemType Directory -Path $oldBuildDir -Force | Out-Null

    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $archivedZip = Join-Path $oldBuildDir "web-$timestamp.zip"
    Move-Item -LiteralPath $webZip -Destination $archivedZip

    Write-Host "Moved old web.zip to $archivedZip"
}

if (Test-Path -LiteralPath $stageDir) {
    Remove-Item -LiteralPath $stageDir -Recurse -Force
}
if (Test-Path -LiteralPath $webDir) {
    Remove-Item -LiteralPath $webDir -Recurse -Force
}

New-Item -ItemType Directory -Path $stageDir -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $projectRoot "main.py") -Destination $stageMain

robocopy (Join-Path $projectRoot "src") (Join-Path $stageDir "src") *.py /E /XD __pycache__ | Out-Host
if ($LASTEXITCODE -gt 7) {
    throw "Failed to stage src files. robocopy exit code: $LASTEXITCODE"
}

robocopy (Join-Path $projectRoot "assets") (Join-Path $stageDir "assets") *.* /E /XD __pycache__ | Out-Host
if ($LASTEXITCODE -gt 7) {
    throw "Failed to stage asset files. robocopy exit code: $LASTEXITCODE"
}

$staticDir = Join-Path $projectRoot "static"
if (Test-Path -LiteralPath $staticDir) {
    robocopy $staticDir (Join-Path $stageDir "static") *.* /E /XD __pycache__ | Out-Host
    if ($LASTEXITCODE -gt 7) {
        throw "Failed to stage static files. robocopy exit code: $LASTEXITCODE"
    }
}

uv run python -m pygbag --app_name mapwa --title Mapwa --build --archive --disable-sound-format-error $stageMain
if ($LASTEXITCODE -ne 0) {
    throw "pygbag build failed. Exit code: $LASTEXITCODE"
}

if (-not (Test-Path -LiteralPath $stageWebZip)) {
    throw "pygbag did not create $stageWebZip"
}

Copy-Item -LiteralPath $stageWebDir -Destination $webDir -Recurse -Force
Copy-Item -LiteralPath $stageWebZip -Destination $webZip -Force

Write-Host "Created $webZip"
