#!/usr/bin/env python3
"""Runner completo para a biblioteca de grafos.

Uso:
  python main.py                           # modo interativo
  python main.py -i entrada.txt            # lê grafo de arquivo
  python main.py -i entrada.txt -b 0       # lê de arquivo e executa BFS a partir do vértice 0
  python main.py -i entrada.txt -d 0       # lê de arquivo e executa DFS a partir do vértice 0
  python main.py -i entrada.txt -c         # lê de arquivo e encontra componentes conexos
  python main.py -i entrada.txt -a 0       # lê de arquivo e executa todas as operações

Opções:
  -i/--input    arquivo de entrada (se não fornecido, usa modo interativo)
  -o/--output   arquivo de saída para o resumo (padrão: saida.txt)
  -r/--rep      representação usada para graus: list|matrix|both (padrão: list)
  -b/--bfs      vértice inicial para BFS
  -d/--dfs      vértice inicial para DFS
  -c/--comp     encontrar componentes conexos
  -a/--all      executar todas as operações (BFS, DFS e componentes) a partir do vértice fornecido
"""

import argparse
import sys
from grafo import Grafo


def parse_args():
    parser = argparse.ArgumentParser(description="Biblioteca de grafos com BFS, DFS e componentes conexos")
    parser.add_argument('-i', '--input', dest='input', help='Arquivo de entrada do grafo')
    parser.add_argument('-o', '--output', dest='output', default='saida.txt', help='Arquivo de saída com o resumo')
    parser.add_argument('-r', '--rep', default='list', choices=['list', 'matrix', 'both'],
                        help='Representação para calcular graus')
    parser.add_argument('-b', '--bfs', type=int, metavar='V', help='Executar BFS a partir do vértice V')
    parser.add_argument('-d', '--dfs', type=int, metavar='V', help='Executar DFS a partir do vértice V')
    parser.add_argument('-c', '--comp', action='store_true', help='Encontrar componentes conexos')
    parser.add_argument('-a', '--all', type=int, metavar='V', help='Executar todas as operações a partir do vértice V')
    parser.add_argument('pos_input', nargs='?', help='(posicional) arquivo de entrada')
    parser.add_argument('pos_output', nargs='?', help='(posicional) arquivo de saída')
    args = parser.parse_args()

    if getattr(args, 'pos_input', None):
        args.input = args.pos_input
    if getattr(args, 'pos_output', None):
        args.output = args.pos_output

    return args


def modo_interativo():
    """Executa o programa em modo interativo"""
    print("=" * 60)
    print("BIBLIOTECA DE BUSCA EM GRAFOS - Modo Interativo")
    print("=" * 60)

    n = int(input("\nNúmero de vértices: "))

    tipo = input("Grafo direcionado? (s/n): ").strip().lower()
    direcionado = (tipo == 's')

    g = Grafo(n, direcionado)

    print(f"\nAdicione as arestas (vértices de 1 a {n})")
    print("Digite 'fim' quando terminar")

    while True:
        entrada = input("Aresta (u v): ").strip()
        if entrada.lower() == 'fim':
            break

        try:
            u, v = map(int, entrada.split())
            if 1 <= u <= n and 1 <= v <= n:
                g.adicionar_aresta(u, v)
                print(f"  Aresta {u} -> {v} adicionada")
            else:
                print(f"  Erro: vértices devem estar entre 1 e {n}")
        except:
            print("  Formato inválido. Use: u v")

    while True:
        try:
            inicio = int(input(f"\nVértice inicial para busca (1 a {n}): "))
            if 1 <= inicio <= n:
                break
            else:
                print(f"Vértice deve estar entre 1 e {n}")
        except:
            print("Entrada inválida")

    print("\n" + "=" * 60)
    print("MENU DE OPERAÇÕES")
    print("=" * 60)
    print("1 - BFS (Busca em Largura)")
    print("2 - DFS (Busca em Profundidade)")
    print("3 - Ambas (BFS e DFS)")
    print("4 - Componentes Conexos")
    print("5 - Todas as operações")

    opcao = input("\nEscolha uma opção: ").strip()

    executar_operacoes(g, inicio, opcao)

    print("\n" + "=" * 60)
    print("Execução concluída!")
    print("=" * 60)


def executar_operacoes(g, inicio, opcao):
    """Executa as operações selecionadas no grafo"""

    if opcao in ['1', '3', '5']:
        print("\n--- Executando BFS ---")
        pai_bfs, nivel_bfs = g.bfs(inicio, "bfs_resultado.txt")
        print("\nÁrvore BFS:")
        for v_idx in range(g.n):
            v = v_idx + 1  # Converter para base-1
            if nivel_bfs[v_idx] != -1:
                pai_str = "raiz" if pai_bfs[v_idx] == -1 else pai_bfs[v_idx]
                print(f"  Vértice {v}: pai = {pai_str}, nível = {nivel_bfs[v_idx]}")

    if opcao in ['2', '3', '5']:
        print("\n--- Executando DFS ---")
        pai_dfs, nivel_dfs = g.dfs(inicio, "dfs_resultado.txt")
        print("\nÁrvore DFS:")
        for v_idx in range(g.n):
            v = v_idx + 1  # Converter para base-1
            if nivel_dfs[v_idx] != -1:
                pai_str = "raiz" if pai_dfs[v_idx] == -1 else pai_dfs[v_idx]
                print(f"  Vértice {v}: pai = {pai_str}, nível = {nivel_dfs[v_idx]}")

    if opcao in ['4', '5']:
        print("\n--- Encontrando Componentes Conexos ---")
        componentes = g.componentes_conexos("componentes_resultado.txt")
        print(f"\nNúmero de componentes: {len(componentes)}")
        for i, comp in enumerate(componentes, 1):
            print(f"\nComponente {i}:")
            print(f"  Tamanho: {len(comp)} vértices")
            print(f"  Vértices: {comp}")


def main():
    args = parse_args()

    # Modo interativo se não forneceu arquivo de entrada
    if not args.input:
        modo_interativo()
        return 0

    # Modo de arquivo
    try:
        g = Grafo.from_file(args.input)
    except Exception as e:
        print(f"Erro ao ler '{args.input}': {e}")
        return 1

    # Escrever resumo(s) básico(s)
    try:
        if args.rep == 'both':
            # quando o usuário pede 'both', geramos dois arquivos separados
            # - o arquivo principal (args.output) conterá a versão por lista
            # - um arquivo adicional com sufixo _matrix conterá a versão por matriz
            import os
            g.write_summary(args.output, rep='list')
            base, ext = os.path.splitext(args.output)
            matrix_output = f"{base}_matrix{ext}" if ext else f"{args.output}_matrix"
            g.write_summary(matrix_output, rep='matrix')
        else:
            g.write_summary(args.output, rep=args.rep)
    except Exception as e:
        print(f"Erro ao escrever '{args.output}': {e}")
        return 1

    # Relatório curto no console (formato simples: '# n', '# m', then 'v grau')
    print(f"# n = {g.n}")
    print(f"# m = {g.num_arestas()}")
    # escolha qual representação mostrar no console (mantemos formato: 'v grau')
    display_rep = 'list' if args.rep == 'both' else args.rep
    for i in range(1, g.n + 1):
        print(f"{i} {g.grau(i, display_rep)}")

    print('\nResumo escrito com sucesso.')

    # Executar operações de busca/componentes se solicitado
    if args.all is not None:
        inicio = args.all
        if 1 <= inicio <= g.n:
            print("\n" + "=" * 60)
            print("EXECUTANDO TODAS AS OPERAÇÕES")
            print("=" * 60)
            executar_operacoes(g, inicio, '5')
        else:
            print(f"Erro: vértice {inicio} fora do intervalo [1, {g.n}]")
            return 1
    else:
        if args.bfs is not None:
            inicio = args.bfs
            if 1 <= inicio <= g.n:
                print("\n--- Executando BFS ---")
                g.bfs(inicio, "bfs_resultado.txt")
            else:
                print(f"Erro: vértice {inicio} fora do intervalo [1, {g.n}]")
                return 1

        if args.dfs is not None:
            inicio = args.dfs
            if 1 <= inicio <= g.n:
                print("\n--- Executando DFS ---")
                g.dfs(inicio, "dfs_resultado.txt")
            else:
                print(f"Erro: vértice {inicio} fora do intervalo [1, {g.n}]")
                return 1

        if args.comp:
            print("\n--- Encontrando Componentes Conexos ---")
            componentes = g.componentes_conexos("componentes_resultado.txt")
            print(f"Número de componentes: {len(componentes)}")
            for i, comp in enumerate(componentes, 1):
                print(f"Componente {i}: {len(comp)} vértices - {comp}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
#!/usr/bin/env python3
"""Runner completo para a biblioteca de grafos.

Uso:
  python main.py                           # modo interativo
  python main.py -i entrada.txt            # lê grafo de arquivo
  python main.py -i entrada.txt -b 0       # lê de arquivo e executa BFS a partir do vértice 0
  python main.py -i entrada.txt -d 0       # lê de arquivo e executa DFS a partir do vértice 0
  python main.py -i entrada.txt -c         # lê de arquivo e encontra componentes conexos
  python main.py -i entrada.txt -a 0       # lê de arquivo e executa todas as operações

Opções:
  -i/--input    arquivo de entrada (se não fornecido, usa modo interativo)
  -o/--output   arquivo de saída para o resumo (padrão: saida.txt)
  -r/--rep      representação usada para graus: list|matrix|both (padrão: list)
  -b/--bfs      vértice inicial para BFS
  -d/--dfs      vértice inicial para DFS
  -c/--comp     encontrar componentes conexos
  -a/--all      executar todas as operações (BFS, DFS e componentes) a partir do vértice fornecido
"""

import argparse
import sys
from grafo import Grafo


def parse_args():
    parser = argparse.ArgumentParser(description="Biblioteca de grafos com BFS, DFS e componentes conexos")
    parser.add_argument('-i', '--input', dest='input', help='Arquivo de entrada do grafo')
    parser.add_argument('-o', '--output', dest='output', default='saida.txt', help='Arquivo de saída com o resumo')
    parser.add_argument('-r', '--rep', default='list', choices=['list', 'matrix', 'both'],
                        help='Representação para calcular graus')
    parser.add_argument('-b', '--bfs', type=int, metavar='V', help='Executar BFS a partir do vértice V')
    parser.add_argument('-d', '--dfs', type=int, metavar='V', help='Executar DFS a partir do vértice V')
    parser.add_argument('-c', '--comp', action='store_true', help='Encontrar componentes conexos')
    parser.add_argument('-a', '--all', type=int, metavar='V', help='Executar todas as operações a partir do vértice V')
    parser.add_argument('pos_input', nargs='?', help='(posicional) arquivo de entrada')
    parser.add_argument('pos_output', nargs='?', help='(posicional) arquivo de saída')
    args = parser.parse_args()

    if getattr(args, 'pos_input', None):
        args.input = args.pos_input
    if getattr(args, 'pos_output', None):
        args.output = args.pos_output

    return args


def modo_interativo():
    """Executa o programa em modo interativo"""
    print("=" * 60)
    print("BIBLIOTECA DE BUSCA EM GRAFOS - Modo Interativo")
    print("=" * 60)

    n = int(input("\nNúmero de vértices: "))

    tipo = input("Grafo direcionado? (s/n): ").strip().lower()
    direcionado = (tipo == 's')

    g = Grafo(n, direcionado)

    print(f"\nAdicione as arestas (vértices de 1 a {n})")
    print("Digite 'fim' quando terminar")

    while True:
        entrada = input("Aresta (u v): ").strip()
        if entrada.lower() == 'fim':
            break

        try:
            u, v = map(int, entrada.split())
            if 1 <= u <= n and 1 <= v <= n:
                g.adicionar_aresta(u, v)
                print(f"  Aresta {u} -> {v} adicionada")
            else:
                print(f"  Erro: vértices devem estar entre 1 e {n}")
        except:
            print("  Formato inválido. Use: u v")

    while True:
        try:
            inicio = int(input(f"\nVértice inicial para busca (1 a {n}): "))
            if 1 <= inicio <= n:
                break
            else:
                print(f"Vértice deve estar entre 1 e {n}")
        except:
            print("Entrada inválida")

    print("\n" + "=" * 60)
    print("MENU DE OPERAÇÕES")
    print("=" * 60)
    print("1 - BFS (Busca em Largura)")
    print("2 - DFS (Busca em Profundidade)")
    print("3 - Ambas (BFS e DFS)")
    print("4 - Componentes Conexos")
    print("5 - Todas as operações")

    opcao = input("\nEscolha uma opção: ").strip()

    executar_operacoes(g, inicio, opcao)

    print("\n" + "=" * 60)
    print("Execução concluída!")
    print("=" * 60)


def executar_operacoes(g, inicio, opcao):
    """Executa as operações selecionadas no grafo"""

    if opcao in ['1', '3', '5']:
        print("\n--- Executando BFS ---")
        pai_bfs, nivel_bfs = g.bfs(inicio, "bfs_resultado.txt")
        print("\nÁrvore BFS:")
        for v_idx in range(g.n):
            v = v_idx + 1  # Converter para base-1
            if nivel_bfs[v_idx] != -1:
                pai_str = "raiz" if pai_bfs[v_idx] == -1 else pai_bfs[v_idx]
                print(f"  Vértice {v}: pai = {pai_str}, nível = {nivel_bfs[v_idx]}")

    if opcao in ['2', '3', '5']:
        print("\n--- Executando DFS ---")
        pai_dfs, nivel_dfs = g.dfs(inicio, "dfs_resultado.txt")
        print("\nÁrvore DFS:")
        for v_idx in range(g.n):
            v = v_idx + 1  # Converter para base-1
            if nivel_dfs[v_idx] != -1:
                pai_str = "raiz" if pai_dfs[v_idx] == -1 else pai_dfs[v_idx]
                print(f"  Vértice {v}: pai = {pai_str}, nível = {nivel_dfs[v_idx]}")

    if opcao in ['4', '5']:
        print("\n--- Encontrando Componentes Conexos ---")
        componentes = g.componentes_conexos("componentes_resultado.txt")
        print(f"\nNúmero de componentes: {len(componentes)}")
        for i, comp in enumerate(componentes, 1):
            print(f"\nComponente {i}:")
            print(f"  Tamanho: {len(comp)} vértices")
            print(f"  Vértices: {comp}")


def main():
    args = parse_args()

    # se não há arquivo de entrada, abrir modo interativo
    if not args.input:
        modo_interativo()
        return 0

    # Ler grafo do arquivo, passando preferência de representação
    default_rep = args.rep if args.rep in ('list', 'matrix') else 'list'
    try:
        g = Grafo.from_file(args.input, default_rep=default_rep)
    except Exception as e:
        print(f"Erro ao ler '{args.input}': {e}")
        return 1

    # Escrever resumo básico
    try:
        g.write_summary(args.output, rep=args.rep)
    except Exception as e:
        print(f"Erro ao escrever '{args.output}': {e}")
        return 1

    # Relatório curto no console
    print(f"# n = {g.n}")
    print(f"# m = {g.num_arestas()}")
    for i in range(1, g.n + 1):
        if args.rep == 'both':
            gl = g.grau(i, 'list')
            gm = g.grau(i, 'matrix')
            print(f"{i} lista={gl}, matriz={gm}")
        else:
            print(f"{i} {g.grau(i, args.rep)}")

    print('\nResumo escrito com sucesso.')

    # Executar operações de busca/componentes se solicitado
    if args.all is not None:
        inicio = args.all
        if 1 <= inicio <= g.n:
            print("\n" + "=" * 60)
            print("EXECUTANDO TODAS AS OPERAÇÕES")
            print("=" * 60)
            executar_operacoes(g, inicio, '5')
        else:
            print(f"Erro: vértice {inicio} fora do intervalo [1, {g.n}]")
            return 1
    else:
        if args.bfs is not None:
            inicio = args.bfs
            if 1 <= inicio <= g.n:
                print("\n--- Executando BFS ---")
                g.bfs(inicio, "bfs_resultado.txt")
            else:
                print(f"Erro: vértice {inicio} fora do intervalo [1, {g.n}]")
                return 1

        if args.dfs is not None:
            inicio = args.dfs
            if 1 <= inicio <= g.n:
                print("\n--- Executando DFS ---")
                g.dfs(inicio, "dfs_resultado.txt")
            else:
                print(f"Erro: vértice {inicio} fora do intervalo [1, {g.n}]")
                return 1

        if args.comp:
            print("\n--- Encontrando Componentes Conexos ---")
            componentes = g.componentes_conexos("componentes_resultado.txt")
            print(f"Número de componentes: {len(componentes)}")
            for i, comp in enumerate(componentes, 1):
                print(f"Componente {i}: {len(comp)} vértices - {comp}")

    return 0


if __name__ == '__main__':
    sys.exit(main())