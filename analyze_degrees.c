#include <stdio.h>
#include <stdlib.h>
#include "grafo.h"

int main() {
    // Carregar o grafo do arquivo
    Grafo *g = grafo_carregar("as_graph.txt", REP_LIST, 0);
    if (!g) {
        printf("Erro ao carregar o grafo\n");
        return 1;
    }

    // Encontrar o menor e maior grau
    int menor_grau = grafo_grau(g, 1);  // Começamos com o grau do vértice 1
    int maior_grau = menor_grau;
    int maior_grau_possivel = g->n - 1;  // n-1 é o maior grau possível em um grafo simples

    // Criar array para contar frequência dos graus
    int *freq_graus = calloc(g->n, sizeof(int));
    if (!freq_graus) {
        printf("Erro de alocação de memória\n");
        grafo_destruir(g);
        return 1;
    }

    // Analisar os graus de todos os vértices
    for (int v = 1; v <= g->n; v++) {
        int grau = grafo_grau(g, v);
        freq_graus[grau]++;
        
        if (grau < menor_grau) menor_grau = grau;
        if (grau > maior_grau) maior_grau = grau;
    }

    
    printf("Análise do AS Graph:\n");
    printf("Número de vértices (n): %d\n", g->n);
    printf("Menor grau: %d\n", menor_grau);
    printf("Maior grau: %d\n", maior_grau);
    printf("Maior grau possível (n-1): %d\n", maior_grau_possivel);
    printf("Porcentagem do maior grau em relação ao máximo possível: %.2f%%\n", 
           (float)maior_grau * 100 / maior_grau_possivel);

    // Salvar distribuição de graus para plotagem
    FILE *fp = fopen("degree_distribution.txt", "w");
    if (fp) {
        for (int i = 0; i <= maior_grau; i++) {
            if (freq_graus[i] > 0) {
                fprintf(fp, "%d %d\n", i, freq_graus[i]);
            }
        }
        fclose(fp);
    }

    free(freq_graus);
    grafo_destruir(g);
    return 0;
}