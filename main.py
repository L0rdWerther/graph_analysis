#!/usr/bin/env python3
"""Runner completo para a biblioteca de grafos.

Uso:
  python main.py                           # modo interativo
  python main.py -i entrada.txt            # lê grafo de arquivo (padrão: lista)
  python main.py -i entrada.txt -r matrix  # lê de arquivo usando matriz
  python main.py -i entrada.txt -b 1       # lê de arquivo e executa BFS a partir do vértice 1
  python main.py -i entrada.txt -d 1       # lê de arquivo e executa DFS a partir do vértice 1
  python main.py -i entrada.txt -c         # lê de arquivo e encontra componentes conexos
  python main.py -i entrada.txt -a 1       # lê de arquivo e executa todas as operações

NOTA: Os vértices são numerados de 1 a n (base-1).

Opções:
  -i/--input      arquivo de entrada (se não fornecido, usa modo interativo)
  -o/--output     arquivo de saída para o resumo (padrão: saida.txt)
  -r/--rep        representação: list (lista de adjacência) ou matrix (matriz) (padrão: list)
  -b/--bfs        vértice inicial para BFS (1 a n)
  -d/--dfs        vértice inicial para DFS (1 a n)
  -c/--comp       encontrar componentes conexos
  -a/--all        executar todas as operações (BFS, DFS e componentes) a partir do vértice fornecido (1 a n)
  -p/--print      imprimir a representação do grafo no console
  --directed      forçar interpretação como grafo direcionado
"""

import argparse
import sys
from grafo import Grafo


def parse_args():
    parser = argparse.ArgumentParser(
        description="Biblioteca de grafos com BFS, DFS e componentes conexos",
        epilog="NOTA: Os vértices são numerados de 1 a n (indexação base-1)"
    )
    parser.add_argument('-i', '--input', dest='input', help='Arquivo de entrada do grafo')
    parser.add_argument('-o', '--output', dest='output', default='saida.txt', help='Arquivo de saída com o resumo')
    parser.add_argument('-r', '--rep', default='list', choices=['list', 'matrix'],
                        help='Representação: list (lista de adjacência) ou matrix (matriz de adjacência)')
    parser.add_argument('-b', '--bfs', type=int, metavar='V', help='Executar BFS a partir do vértice V (1 a n)')
    parser.add_argument('-d', '--dfs', type=int, metavar='V', help='Executar DFS a partir do vértice V (1 a n)')
    parser.add_argument('-c', '--comp', action='store_true', help='Encontrar componentes conexos')
    parser.add_argument('-a', '--all', type=int, metavar='V', help='Executar todas as operações a partir do vértice V (1 a n)')
    parser.add_argument('-p', '--print', action='store_true', dest='print_rep', help='Imprimir a representação do grafo')
    parser.add_argument('--directed', action='store_true', help='Forçar interpretação como grafo direcionado')
    parser.add_argument('--measure', action='store_true', help='Medir memória usada ao construir o grafo (list vs matrix)')
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

    rep = input("Representação (list/matrix): ").strip().lower()
    if rep not in ('list', 'matrix'):
        print("Representação inválida. Usando 'list'.")
        rep = 'list'

    g = Grafo(n, representacao=rep, direcionado=direcionado)

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

    # Mostrar representação
    g.imprimir_representacao()

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
    # If measurement requested, perform two separate constructions and report memory
    if args.measure:
        import tracemalloc, time
        try:
            import psutil
            psutil_available = True
            proc = psutil.Process()
        except Exception:
            psutil_available = False

        def measure_build(repr_name: str):
            print(f"\nMedindo construção com representação: {repr_name}")
            tracemalloc.start()
            t0 = time.time()
            rss_before = proc.memory_info().rss if psutil_available else None
            try:
                g_local = Grafo.from_file(args.input, representacao=repr_name)
                if args.directed:
                    g_local.direcionado = True
            except MemoryError:
                tracemalloc.stop()
                print("Construção falhou por falta de memória (MemoryError)")
                return None
            except Exception as e:
                tracemalloc.stop()
                print(f"Erro durante construção: {e}")
                return None
            t1 = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            rss_after = proc.memory_info().rss if psutil_available else None
            result = {
                'repr': repr_name,
                'time_s': t1 - t0,
                'tracemalloc_current_mb': current / 1024 / 1024,
                'tracemalloc_peak_mb': peak / 1024 / 1024,
                'rss_before_mb': (rss_before / 1024 / 1024) if rss_before is not None else None,
                'rss_after_mb': (rss_after / 1024 / 1024) if rss_after is not None else None,
                'graph': g_local,
            }
            return result

        # measure list
        res_list = measure_build('list')
        # measure matrix
        res_matrix = measure_build('matrix')

        print("\nResultado da medição:")
        for res in (res_list, res_matrix):
            if res is None:
                print("  - Falha ao medir representação (possível falta de memória)")
                continue
            print(f"  Representação: {res['repr']}")
            print(f"    Tempo de construção: {res['time_s']:.2f} s")
            print(f"    tracemalloc pico: {res['tracemalloc_peak_mb']:.2f} MB")
            if psutil_available:
                print(f"    RSS antes: {res['rss_before_mb']:.2f} MB, depois: {res['rss_after_mb']:.2f} MB")
            print("")

        # If list build succeeded, continue using that graph instance for further ops
        if res_list and res_list.get('graph'):
            g = res_list['graph']
        elif res_matrix and res_matrix.get('graph'):
            g = res_matrix['graph']
        else:
            print("Nenhum grafo válido foi construído; abortando.")
            return 1

    else:
        try:
            g = Grafo.from_file(args.input, representacao=args.rep)
            # Sobrescrever se usuário especificou --directed
            if args.directed:
                g.direcionado = True
        except Exception as e:
            print(f"Erro ao ler '{args.input}': {e}")
            return 1

    # Informar tipo do grafo
    tipo_grafo = "direcionado" if g.direcionado else "não direcionado"
    print(f"Grafo {tipo_grafo} carregado.")
    print(f"Representação: {g.representacao}")

    # Imprimir representação se solicitado
    if args.print_rep:
        g.imprimir_representacao()

    # Escrever resumo básico
    try:
        g.write_summary(args.output)
    except Exception as e:
        print(f"Erro ao escrever '{args.output}': {e}")
        return 1

    # Relatório curto no console (resumo apenas)
    print(f"\n# n = {g.n}")
    print(f"# m = {g.num_arestas()}")
    # Os graus completos são gravados em arquivo pelo método write_summary()
    print(f"\nGrau dos vértices gravados em '{args.output}'")

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