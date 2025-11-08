# PowerShell build script for the C project
# Requires a working gcc in PATH (MinGW-w64 recommended)
param()

$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Set-Location $scriptDir
if (-not (Test-Path -Path "main.c")){
    Write-Error "main.c not found in $PWD"
    exit 1
}

Write-Host "Compiling with gcc..."
$proc = Start-Process gcc -ArgumentList '-std=c11','-O2','-Wall','-o','graph.exe','main.c','grafo.c' -NoNewWindow -Wait -PassThru
if ($proc.ExitCode -ne 0) {
    Write-Error "Build failed (exit code $($proc.ExitCode))"
    exit $proc.ExitCode
}
Write-Host "Build succeeded: graph.exe" -ForegroundColor Green
