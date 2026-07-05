param(
    [switch]$Fix
)

$ErrorActionPreference = "Stop"

$env:SDL_VIDEODRIVER = "dummy"
$env:SDL_AUDIODRIVER = "dummy"
if (-not $env:UV_CACHE_DIR) {
    $env:UV_CACHE_DIR = Join-Path $PSScriptRoot ".uv-cache"
}
if (-not $env:UV_PYTHON_INSTALL_DIR) {
    $env:UV_PYTHON_INSTALL_DIR = Join-Path $PSScriptRoot ".uv-python"
}

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,
        [string[]]$Arguments = @()
    )

    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Command $($Arguments -join ' ') failed. Exit code: $LASTEXITCODE"
    }
}

Invoke-CheckedCommand "uv" @("run", "pytest", "-n", "auto")

$ruffArgs = @("run", "ruff", "check", ".")
if ($Fix) {
    $ruffArgs += "--fix"
}

Invoke-CheckedCommand "uv" $ruffArgs
