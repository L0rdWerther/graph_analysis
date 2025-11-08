@echo off
REM Build script for Windows (uses gcc from MinGW or similar)
SETLOCAL
if not exist main.c (
  echo main.c not found in %CD%
  exit /b 1
)

echo Compiling C project...
gcc -std=c11 -O2 -Wall -o graph.exe main.c grafo.c
nif errorlevel 1 (
  echo Build failed
  exit /b 1
)
echo Build succeeded: graph.exe
ENDLOCAL
