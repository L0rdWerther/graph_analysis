#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "grafo.h"

static double now_seconds(void){
    struct timespec ts;
    if(clock_gettime(CLOCK_MONOTONIC, &ts) == 0){
        return ts.tv_sec + ts.tv_nsec / 1e9;
    }
    return (double)time(NULL);
}

int main(void){
    Grafo *g = grafo_carregar("as_graph.txt", REP_LIST, 0);
    if(!g){
        fprintf(stderr, "Erro ao carregar o grafo\n");
        return 1;
    }

    int n = g->n;
    int diameter = 0;
    int diam_u = 0, diam_v = 0;

    double t0 = now_seconds();

    for(int s = 1; s <= n; ++s){
        int *levels = NULL;
        int *parents = grafo_bfs(g, s, &levels);
        if(!parents || !levels){
            fprintf(stderr, "Erro ao executar BFS a partir de %d\n", s);
            free(parents);
            free(levels);
            grafo_destruir(g);
            return 1;
        }

        int max_level = -1;
        int far = s;
        for(int v = 1; v <= n; ++v){
            if(levels[v] > max_level){
                max_level = levels[v];
                far = v;
            }
        }

        if(max_level > diameter){
            diameter = max_level;
            diam_u = s;
            diam_v = far;
        }

        free(parents);
        free(levels);
    }

    double t1 = now_seconds();

    printf("Diâmetro (distância máxima mínima): %d\n", diameter);
    printf("Exemplo de par com distância = diâmetro: %d -> %d\n", diam_u, diam_v);
    printf("Número de vértices: %d\n", n);
    printf("Tempo gasto: %.3f segundos\n", t1 - t0);

    grafo_destruir(g);
    return 0;
}
