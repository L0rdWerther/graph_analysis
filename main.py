#!/usr/bin/env python3
"""Runner simples para testar a biblioteca de grafos.

Uso padrão (no diretório do projeto):
  python main.py

Opções:
  -i/--input   arquivo de entrada (padrão: entrada.txt)
  -o/--output  arquivo de saída para o resumo (padrão: saida.txt)
  -r/--rep     representação usada para graus: list|matrix|both (padrão: list)
"""

import argparse
import sys
from grafo import Grafo


def parse_args():
	parser = argparse.ArgumentParser(description="Lê um grafo e escreve um resumo (vértices, arestas, graus)")
	# opções nomeadas
	parser.add_argument('-i', '--input', dest='input', default='entrada.txt', help='Arquivo de entrada do grafo')
	parser.add_argument('-o', '--output', dest='output', default='saida.txt', help='Arquivo de saída com o resumo')
	parser.add_argument('-r', '--rep', default='list', choices=['list', 'matrix', 'both'], help='Representação para calcular graus')
	# argumentos posicionais opcionais (permitir: python main.py entrada.txt saida.txt)
	parser.add_argument('pos_input', nargs='?', help='(posicional) arquivo de entrada')
	parser.add_argument('pos_output', nargs='?', help='(posicional) arquivo de saída')
	args = parser.parse_args()

	# se o usuário passou posicionais, estes sobrescrevem as opções
	if getattr(args, 'pos_input', None):
		args.input = args.pos_input
	if getattr(args, 'pos_output', None):
		args.output = args.pos_output

	return args


def main():
	args = parse_args()

	try:
		g = Grafo.from_file(args.input)
	except Exception as e:
		print(f"Erro ao ler '{args.input}': {e}")
		return 1

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
	return 0


if __name__ == '__main__':
	sys.exit(main())

