#include <stdio.h>
#include <stdlib.h>
#include "grafo.h"

int main() {
    // Carregar o grafo do arquivo
    Grafo *g = grafo_carregar("collaboration_graph.txt", REP_LIST, 0);
    if (!g) {
        printf("Erro ao carregar o grafo\n");
        return 1;
    }

    int **components;  // Array com os vértices de cada componente
    int *sizes;       // Array com os tamanhos dos componentes
    int num_components = grafo_componentes(g, &components, &sizes);

    if (num_components < 0) {
        printf("Erro ao encontrar componentes\n");
        grafo_destruir(g);
        return 1;
    }

    // Encontrar o maior e menor componente
    int maior = sizes[0];
    int menor = sizes[0];
    for (int i = 1; i < num_components; i++) {
        if (sizes[i] > maior) maior = sizes[i];
        if (sizes[i] < menor) menor = sizes[i];
    }

    printf("Número de componentes conexos: %d\n", num_components);
    printf("Tamanho do maior componente: %d\n", maior);
    printf("Tamanho do menor componente: %d\n", menor);

   
    for (int i = 0; i < num_components; i++)
        free(components[i]);
    free(components);
    free(sizes);
    grafo_destruir(g);

    return 0;
}