#ifndef GRAFO_H
#define GRAFO_H

#include <stdio.h>
#include <stdint.h>

typedef enum { REP_LIST, REP_MATRIX } Representation;

typedef struct {
    int n;              // número de vértices
    int m;              // número de arestas
    int direcionado;    // 0 = não, 1 = sim
    Representation rep; // representação atual

    /* lista de adjacência */
    int *deg;       // grau de cada vértice
    int **adj;      // adj[v] é array de vizinhos
    int *cap;       // capacidade de cada lista

    /* matriz de adjacência (compacta: n*n bytes) */
    uint8_t *mat;   // mat[i*n + j] == 1 se aresta existe
} Grafo;

/* inicializa grafo vazio */
Grafo *grafo_criar(int n, Representation rep, int direcionado);
void grafo_destruir(Grafo *g);

/* adicionar aresta (u,v) onde u,v são 1-based */
int grafo_adicionar_aresta(Grafo *g, int u, int v);

/* ler grafo de arquivo (formato: primeira linha n, depois arestas `u v`) */
Grafo *grafo_carregar(const char *path, Representation rep, int direcionado);

/* escrever resumo (n, m, grau por vértice) */
int grafo_escrever_resumo(Grafo *g, const char *path);

/* consultas */
int grafo_grau(Grafo *g, int v); /* v 1-based */
int grafo_num_arestas(Grafo *g);

/* BFS, DFS e componentes */
int *grafo_bfs(Grafo *g, int inicio, int **out_level); /* retorna pai[] (1-based vertices or 0 for nil). out_level receives pointer to array of levels (-1 unreachable) */
int *grafo_dfs(Grafo *g, int inicio, int **out_level);
int grafo_componentes(Grafo *g, int ***out_components, int **out_sizes);

/* utilitários */
void grafo_imprimir(Grafo *g);

#endif
