#include <stdio.h>
#include <stdlib.h>
#include "grafo.h"

// Função para encontrar o maior nível na árvore BFS
int encontrar_maior_nivel(int *levels, int n) {
    int max_level = 0;
    for (int i = 1; i <= n; i++) {
        if (levels[i] > max_level) {
            max_level = levels[i];
        }
    }
    return max_level;
}

int main() {
    // Carregar o grafo do arquivo
    Grafo *g = grafo_carregar("as_graph.txt", REP_LIST, 0);
    if (!g) {
        printf("Erro ao carregar o grafo\n");
        return 1;
    }

    // Vértices de teste para BFS
    int vertices_teste[] = {1, 2, 10, 100, 1000, 5000, 10000};
    int num_testes = sizeof(vertices_teste) / sizeof(vertices_teste[0]);

    printf("Análise de BFS no AS Graph:\n");
    printf("Vértice\tMaior Nível\n");
    printf("-------------------\n");

    // Realizar BFS a partir de cada vértice de teste
    for (int i = 0; i < num_testes; i++) {
        int start = vertices_teste[i];
        if (start > g->n) continue;  // Pular se o vértice não existe

        int *levels = NULL;
        int *parents = grafo_bfs(g, start, &levels);

        if (parents && levels) {
            int max_level = encontrar_maior_nivel(levels, g->n);
            printf("%d\t%d\n", start, max_level);

            free(parents);
            free(levels);
        }
    }

    grafo_destruir(g);
    return 0;
}