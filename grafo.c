#include "grafo.h"
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define MIN(a,b) ((a)<(b)?(a):(b))

Grafo *grafo_criar(int n, Representation rep, int direcionado){
    if(n <= 0) return NULL;
    Grafo *g = calloc(1, sizeof(Grafo));
    if(!g) return NULL;
    g->n = n;
    g->m = 0;
    g->direcionado = direcionado ? 1 : 0;
    g->rep = rep;

    g->deg = calloc(n, sizeof(int));
    g->adj = NULL;
    g->cap = NULL;
    g->mat = NULL;

    if(rep == REP_LIST){
        g->adj = calloc(n, sizeof(int*));
        g->cap = calloc(n, sizeof(int));
        if(!g->adj || !g->cap) { grafo_destruir(g); return NULL; }
        /* initially no neighbors allocated */
    } else {
        /* allocate n*n bytes (0 or 1) */
        size_t sz = (size_t)n * (size_t)n;
        g->mat = calloc(sz, sizeof(uint8_t));
        if(!g->mat){ grafo_destruir(g); return NULL; }
    }
    return g;
}

void grafo_destruir(Grafo *g){
    if(!g) return;
    if(g->deg) free(g->deg);
    if(g->cap){
        for(int i=0;i<g->n;i++) if(g->adj && g->adj[i]) free(g->adj[i]);
        free(g->cap);
    }
    if(g->adj) free(g->adj);
    if(g->mat) free(g->mat);
    free(g);
}

static int ensure_capacity(Grafo *g, int v0){
    int v = v0 - 1;
    int cap = g->cap[v];
    if(cap == 0){
        int newcap = 4;
        int *arr = malloc(newcap * sizeof(int));
        if(!arr) return -1;
        g->adj[v] = arr;
        g->cap[v] = newcap;
        return 0;
    }
    if(g->deg[v] >= cap){
        int newcap = cap * 2;
        int *arr = realloc(g->adj[v], newcap * sizeof(int));
        if(!arr) return -1;
        g->adj[v] = arr;
        g->cap[v] = newcap;
    }
    return 0;
}

int grafo_adicionar_aresta(Grafo *g, int u, int v){
    if(!g) return -1;
    if(u < 1 || u > g->n || v < 1 || v > g->n) return -1;
    int ui = u-1, vi = v-1;
    int added_edge = 0;
    if(g->rep == REP_LIST){
        /* avoid duplicate neighbors */
        int exists = 0;
        for(int i=0;i<g->deg[ui];i++){
            if(g->adj[ui][i] == v){ exists = 1; break; }
        }
        if(!exists){
            if(ensure_capacity(g, u) != 0) return -1;
            g->adj[ui][g->deg[ui]++] = v;
            added_edge = 1; /* count one undirected edge once below */
        }
        if(!g->direcionado){
            int exists2 = 0;
            for(int i=0;i<g->deg[vi];i++){
                if(g->adj[vi][i] == u){ exists2 = 1; break; }
            }
            if(!exists2){
                if(ensure_capacity(g, v) != 0) return -1;
                g->adj[vi][g->deg[vi]++] = u;
            }
        }
    } else {
        /* matrix */
        size_t idx = (size_t)ui * g->n + (size_t)vi;
        if(g->mat[idx] == 0){
            g->mat[idx] = 1;
            g->deg[ui]++;
            added_edge = 1;
            if(!g->direcionado){
                size_t idx2 = (size_t)vi * g->n + (size_t)ui;
                if(g->mat[idx2] == 0){
                    g->mat[idx2] = 1;
                    g->deg[vi]++;
                }
            }
        }
    }
    if(added_edge) g->m++;
    return 0;
}

Grafo *grafo_carregar(const char *path, Representation rep, int direcionado){
    FILE *f = fopen(path, "r");
    if(!f) return NULL;
    int n;
    if(fscanf(f, "%d", &n) != 1){ fclose(f); return NULL; }
    Grafo *g = grafo_criar(n, rep, direcionado);
    if(!g){ fclose(f); return NULL; }
    int u,v;
    while(fscanf(f, "%d %d", &u, &v) == 2){
        if(u < 1 || u > n || v < 1 || v > n) continue;
        if(grafo_adicionar_aresta(g, u, v) != 0){ /* if adding fails, ignore */ }
    }
    fclose(f);
    return g;
}

int grafo_escrever_resumo(Grafo *g, const char *path){
    if(!g) return -1;
    FILE *f = fopen(path, "w");
    if(!f) return -1;
    fprintf(f, "# n = %d\n", g->n);
    fprintf(f, "# m = %d\n", g->m);
    for(int i=0;i<g->n;i++){
        fprintf(f, "%d %d\n", i+1, g->deg[i]);
    }
    fclose(f);
    return 0;
}

int grafo_grau(Grafo *g, int v){
    if(!g) return -1;
    if(v < 1 || v > g->n) return -1;
    return g->deg[v-1];
}

int grafo_num_arestas(Grafo *g){
    if(!g) return 0;
    return g->m;
}

/* BFS */
int *grafo_bfs(Grafo *g, int inicio, int **out_level){
    if(!g) return NULL;
    int n = g->n;
    int *pai = malloc(n * sizeof(int));
    int *nivel = malloc(n * sizeof(int));
    if(!pai || !nivel){ free(pai); free(nivel); return NULL; }
    for(int i=0;i<n;i++){ pai[i] = 0; nivel[i] = -1; }
    int s = inicio - 1;
    int *q = malloc(n * sizeof(int)); if(!q){ free(pai); free(nivel); return NULL; }
    int qt=0,qh=0;
    q[qt++] = s; nivel[s] = 0; pai[s] = -1;
    while(qh < qt){
        int u = q[qh++];
        if(g->rep == REP_LIST){
            for(int i=0;i<g->deg[u];i++){
                int v = g->adj[u][i]-1;
                if(nivel[v] == -1){ nivel[v] = nivel[u] + 1; pai[v] = u+1; q[qt++] = v; }
            }
        } else {
            for(int v=0; v<n; v++){
                if(g->mat[(size_t)u * n + v]){
                    if(nivel[v] == -1){ nivel[v] = nivel[u] + 1; pai[v] = u+1; q[qt++] = v; }
                }
            }
        }
    }
    free(q);
    if(out_level) *out_level = nivel; else free(nivel);
    return pai;
}

/* DFS (iterative using stack) */
int *grafo_dfs(Grafo *g, int inicio, int **out_level){
    if(!g) return NULL;
    int n = g->n;
    int *pai = malloc(n * sizeof(int));
    int *nivel = malloc(n * sizeof(int));
    int *vis = calloc(n, sizeof(int));
    if(!pai || !nivel || !vis){ free(pai); free(nivel); free(vis); return NULL; }
    for(int i=0;i<n;i++){ pai[i] = 0; nivel[i] = -1; }
    int s = inicio - 1;
    int *stack = malloc(n * sizeof(int)); if(!stack){ free(pai); free(nivel); free(vis); return NULL; }
    int sp = 0;
    stack[sp++] = s; nivel[s] = 0; pai[s] = -1;
    while(sp > 0){
        int u = stack[--sp];
        if(vis[u]) continue;
        vis[u] = 1;
        if(g->rep == REP_LIST){
            for(int i=0;i<g->deg[u];i++){
                int v = g->adj[u][i]-1;
                if(!vis[v]){ pai[v] = u+1; nivel[v] = nivel[u] + 1; stack[sp++] = v; }
            }
        } else {
            for(int v=0; v<n; v++){
                if(g->mat[(size_t)u * n + v]){
                    if(!vis[v]){ pai[v] = u+1; nivel[v] = nivel[u] + 1; stack[sp++] = v; }
                }
            }
        }
    }
    free(stack); free(vis);
    if(out_level) *out_level = nivel; else free(nivel);
    return pai;
}

/* componentes conexos: retorna número de componentes, out_components aponta para array de int* (each component is list of vertices 1-based), out_sizes gives sizes. Caller must free components and sizes. */
int grafo_componentes(Grafo *g, int ***out_components, int **out_sizes){
    if(!g) return 0;
    int n = g->n;
    int *vis = calloc(n, sizeof(int));
    if(!vis) return 0;
    int **comps = malloc(n * sizeof(int*));
    int *sizes = malloc(n * sizeof(int));
    if(!comps || !sizes){ free(vis); free(comps); free(sizes); return 0; }
    int comp_count = 0;
    int *stack = malloc(n * sizeof(int)); if(!stack){ free(vis); free(comps); free(sizes); return 0; }

    for(int i=0;i<n;i++){
        if(vis[i]) continue;
        /* start DFS to collect component */
        int sp=0;
        stack[sp++] = i; vis[i]=1;
        int *members = malloc(n * sizeof(int)); if(!members) { /* cleanup */ }
        int mem_sz = 0;
        while(sp>0){
            int u = stack[--sp];
            members[mem_sz++] = u+1;
            if(g->rep == REP_LIST){
                for(int j=0;j<g->deg[u];j++){
                    int v = g->adj[u][j]-1;
                    if(!vis[v]){ vis[v]=1; stack[sp++]=v; }
                }
            } else {
                for(int v=0; v<n; v++){
                    if(g->mat[(size_t)u * n + v]){
                        if(!vis[v]){ vis[v]=1; stack[sp++]=v; }
                    }
                }
            }
        }
        /* shrink members to actual size */
        int *m_shr = realloc(members, mem_sz * sizeof(int));
        comps[comp_count] = m_shr ? m_shr : members;
        sizes[comp_count] = mem_sz;
        comp_count++;
    }
    free(stack); free(vis);
    *out_components = comps; *out_sizes = sizes;
    return comp_count;
}

void grafo_imprimir(Grafo *g){
    if(!g) return;
    printf("Grafo n=%d m=%d rep=%s direcionado=%d\n", g->n, g->m,
           g->rep==REP_LIST?"list":"matrix", g->direcionado);
    if(g->rep == REP_LIST){
        for(int i=0;i<g->n;i++){
            printf("%d:", i+1);
            for(int j=0;j<g->deg[i];j++) printf(" %d", g->adj[i][j]);
            printf("\n");
        }
    } else {
        for(int i=0;i<g->n;i++){
            printf("%d:", i+1);
            for(int j=0;j<g->n;j++) if(g->mat[(size_t)i * g->n + j]) printf(" %d", j+1);
            printf("\n");
        }
    }
}
