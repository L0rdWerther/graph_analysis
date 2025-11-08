C Graph Analysis

This project mirrors the Python `graph_analysis` runner but in C.

Features:
- Read a graph from a text file: first line = number of vertices n, subsequent lines are edges `u v` (1-based).
- Support two representations selectable at runtime: adjacency list (`list`) and adjacency matrix (`matrix`).
- Write a summary file with n, m, and degree per vertex.
- Provide BFS, DFS, and connected components routines.

Build

Make sure you have a C compiler (gcc/clang). From the `graph_analysis_c` directory run:

    make

Run

    ./graph -i ../graph_analysis/entrada.txt -o saida.txt -r list

Flags

  -i <file>    input graph file (default: stdin)
  -o <file>    output summary file (default: saida.txt)
  -r <type>    representation: list or matrix (default: list)
  -b <v>       run BFS from vertex v (1-based)
  -d <v>       run DFS from vertex v (1-based)
  -c           compute connected components
  --directed   treat graph as directed

Notes

- The adjacency-matrix implementation uses a contiguous byte array (n*n bytes). For very large n this may be impractical.
- The adjacency-list uses dynamic arrays per vertex and is suitable for sparse graphs.

Windows notes

If you are on Windows, you can build with MinGW-w64 (gcc) or another compiler. This repository includes simple build scripts:

  - `build.bat` — batch file for cmd.exe
  - `build.ps1` — PowerShell script

Example (cmd.exe):

  cd "c:\Users\Tony\Documents\IFB DOCUMENTS\teoria_dos_grafos\Trabalho1\graph_analysis_c"
  build.bat

Example (PowerShell):

  cd "c:\Users\Tony\Documents\IFB DOCUMENTS\teoria_dos_grafos\Trabalho1\graph_analysis_c"
  .\build.ps1

After building you will have `graph.exe`. Run it like:

  .\graph.exe -i ..\graph_analysis\collaboration_graph.txt -o saida.txt -r list

Be careful with the `matrix` representation on very large graphs (`n*n` bytes): it can require several gigabytes of RAM.

