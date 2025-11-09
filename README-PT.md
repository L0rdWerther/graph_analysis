Graph Analysis — instruções de uso (português)

Este repositório contém duas implementações para análise de grafos usadas nas atividades: uma em Python (`graph_analysis`) e uma em C (no mesmo diretório). Ambas suportam:

- leitura de grafos em arquivo (primeira linha = n, depois arestas `u v` 1-based)
- duas representações escolhíveis em tempo de execução: lista de adjacência (`list`) e matriz de adjacência (`matrix`)
- rotinas de BFS, DFS e componentes conexos
- escrita de um arquivo resumo com `n`, `m` e grau por vértice

Objetivo deste README

Aqui estão comandos e instruções para reproduzir as três consultas/medições pedidas no Estudo de Caso 1:

1) medir memória usada por cada representação (lista vs matriz)
2) medir tempo de execução de BFS (pior caso amostrado) nas duas representações
3) obter componentes conexos e seus tamanhos (maior/menor)

Pré-requisitos

- Python 3.8+ (para os scripts Python opcionalmente usados)
- um compilador C (gcc/clang via MSYS2/MinGW no Windows ou gcc/clang no Linux/macOS)
- (Windows) MinGW-w64 com `gcc` ou Visual Studio toolchain; quando usar `GetProcessMemoryInfo` a ligação `-lpsapi` pode ser necessária
- (opcional para Python) `psutil` para medir RSS: `pip install psutil`

Arquivos importantes

- `as_graph.txt`, `collaboration_graph.txt` — conjuntos de dados usados
- `main.c`, `grafo.c`, `grafo.h` — implementação C (binário: `graph.exe` após compilação)
- `grafo.py`, `main.py` — implementação Python (script runner)
- `saida.txt`, `saida_bfs_measure.txt`, `saida_components.txt` — nomes de exemplo onde o programa grava resultados

Como executar (C)

1) Compilar (bash/WSL / MSYS2 / Git Bash):

```bash
cd "/c/Users/Tony/Documents/IFB DOCUMENTS/teoria_dos_grafos/Trabalho1/graph_analysis"
gcc -O2 -o graph.exe main.c grafo.c -lm -lpsapi
```

Observação: no Windows o `-lpsapi` é necessário para resolver a chamada a `GetProcessMemoryInfo`. Se usar o `Makefile` ou os scripts (`build.bat`, `build.ps1`) prefira esses wrappers.

2) Medir memória e tempo de construção das representações (lista vs matriz):

```bash
./graph.exe -i ./collaboration_graph.txt --measure
```

Saída esperada: a execução imprime uma tabela com as duas representações e as métricas:
- Time(s): tempo de construção
- RSS before / RSS after: uso de memória do processo antes/depois da construção (MB)
- Peak: pico observado (platform-specific)

Os dados também serão salvos se você fornecer `-o <arquivo>` para o resumo (grau por vértice).

3) Medir tempo (BFS pior caso amostrado)

```bash
./graph.exe -i ./as_graph.txt --bfs-measure -r list -o ./saida_bfs_measure.txt
```

Isso carrega cada representação (lista e matriz), amostra vértices (máx grau, mín grau e alguns pontos espaçados) e imprime o pior tempo de BFS medido por representação. `saida_bfs_measure.txt` recebe o resumo padrão.

Se você solicitar `-r matrix` ao chamar o binário, o programa agora detecta e reutiliza a representação já carregada para evitar tentativas de alocar duas matrizes grandes ao mesmo tempo (isso evita falhas por falta de memória).

4) Componentes conexos (usar a representação em lista para ser mais econômico em memória):

```bash
./graph.exe -i ./as_graph.txt -r list -c -o ./saida_components.txt
```

Saída: o programa imprimirá quantas componentes foram encontradas e escreverá em `saida_components.txt` a lista de vértices por componente. Use esse arquivo para extrair o tamanho do maior e do menor componente.

Exemplo de extração rápida (Unix/bashtools) — tamanhos por componente:

```bash
# o formato em saida_components.txt é: "k componentes encontrados:" seguido por linhas "Componente i (tamanho T): v1 v2 ..."
grep "Componente" saida_components.txt | sed -E 's/.*\(tamanho ([0-9]+)\).*/\1/' | sort -n
```

Isso imprime os tamanhos ordenados (o primeiro é o menor, o último é o maior).

Como executar (Python)

Se preferir usar os scripts Python (úteis para análise/plotagem):

1) criar um virtualenv e instalar dependências opcionais:

```bash
python -m venv .venv
source .venv/bin/activate    # ou .\.venv\Scripts\activate on Windows (PowerShell/CMD)
pip install --upgrade pip
pip install psutil matplotlib numpy
```

2) medir memória (Python tem `--measure` que usa tracemalloc + psutil quando disponível):

```bash
python main.py -i collaboration_graph.txt --measure
```

Aviso: a implementação "matriz" em Python usa listas aninhadas e é extremamente ineficiente em memória (muitos objetos Python). Use os resultados apenas como comparação didática, e não como implementação prática (para matrizes grandes prefira NumPy, bitsets ou estruturas esparsas).

Respostas exemplares (executadas durante testes neste repositório)

- Para `as_graph.txt` (AS graph): n = 32385, m = 46736
- Componentes conexos: 1 (tamanho único = 32385)
- Exemplo de tempos BFS (amostrados) observados nesta máquina de teste: list ≈ 0.003 s, matrix ≈ 2.06 s

Essas medidas variam conforme CPU e memória da sua máquina — repita as medições no seu ambiente para obter valores comparáveis.

Boas práticas e notas finais

- Sempre use a representação em lista (`-r list`) para grafos esparsos (a maioria dos grafos reais).
- A representação `matrix` consome O(n^2) bytes: cuidado em grafos grandes (n grande).
- No Windows, lembre-se de linkar `psapi` ao compilar ou use os scripts `build.bat`/`build.ps1` providos.
- Se desejar, eu posso adicionar um modo que exporte resultados (memória/tempo/componentes) em CSV/JSON automaticamente para facilitar relatórios.
