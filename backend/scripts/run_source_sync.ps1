# Run the legal source sync locally (Windows). Intended for Task Scheduler; safe to run by hand.
#   powershell -NoProfile -ExecutionPolicy Bypass -File backend\scripts\run_source_sync.ps1 [-Ingest]
#
# Register a weekly task (Mondays 06:30) - run once in an elevated or normal PowerShell:
#   schtasks /Create /SC WEEKLY /D MON /ST 06:30 /TN "PJN legal sources sync" `
#     /TR "powershell -NoProfile -ExecutionPolicy Bypass -File `"$PWD\backend\scripts\run_source_sync.ps1`" -Ingest"
param([switch]$Ingest)

$ErrorActionPreference = "Stop"
$backend = Split-Path -Parent $PSScriptRoot
$python = Join-Path $backend ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) { $python = "python" }
$logDir = Join-Path $backend "logs"
New-Item -ItemType Directory -Force $logDir | Out-Null
$log = Join-Path $logDir ("source_sync_{0}.log" -f (Get-Date -Format "yyyy-MM-dd_HHmm"))

$syncArgs = @("scripts\sync_sources.py")
if ($Ingest) { $syncArgs += "--ingest" }

Push-Location $backend
try {
    & $python @syncArgs *>&1 | Tee-Object -FilePath $log
    $code = $LASTEXITCODE
} finally {
    Pop-Location
}
Write-Output "Exit code $code. Log: $log. Summary: frontend\data\sources\last_run_summary.md"
exit $code
