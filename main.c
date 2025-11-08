#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "grafo.h"
#include <time.h>
#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#else
#include <sys/resource.h>
#include <unistd.h>
#include <sys/time.h>
#endif

/* Return current RSS in MB, or -1.0 on error */
static double get_rss_mb(void){
#ifdef _WIN32
    PROCESS_MEMORY_COUNTERS pmc;
    if(GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))){
        return (double)pmc.WorkingSetSize / 1024.0 / 1024.0;
    }
    return -1.0;
#else
    struct rusage ru;
    if(getrusage(RUSAGE_SELF, &ru) == 0){
#if defined(__APPLE__)
        /* ru_maxrss is in bytes on macOS */
        return (double)ru.ru_maxrss / 1024.0 / 1024.0;
#else
        /* ru_maxrss is in kilobytes on Linux */
        return (double)ru.ru_maxrss / 1024.0;
#endif
    }
    return -1.0;
#endif
}

/* Portable wall-clock time in seconds */
static double now_seconds(void){
#ifdef _WIN32
    LARGE_INTEGER freq, counter;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&counter);
    return (double)counter.QuadPart / (double)freq.QuadPart;
#else
    struct timespec ts;
    if(clock_gettime(CLOCK_MONOTONIC, &ts) == 0){
        return ts.tv_sec + ts.tv_nsec / 1e9;
    }
    /* fallback */
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec / 1e6;
#endif
}

void usage(const char *prog){
    fprintf(stderr, "Usage: %s -i input -o output -r list|matrix [-b start] [-d start] [-c] [--directed]\n", prog);
}

int main(int argc, char **argv){
    const char *input = NULL;
    const char *output = "saida.txt";
    char rep_str[16] = "list";
    int bfs_start = 0;
    int dfs_start = 0;
    int do_comp = 0;
    int directed = 0;
    int do_measure = 0;

    for(int i=1;i<argc;i++){
        if(strcmp(argv[i], "-i") == 0 && i+1<argc) { input = argv[++i]; }
        else if(strcmp(argv[i], "-o") == 0 && i+1<argc) { output = argv[++i]; }
        else if(strcmp(argv[i], "-r") == 0 && i+1<argc) { strncpy(rep_str, argv[++i], 15); rep_str[15]='\0'; }
        else if(strcmp(argv[i], "-b") == 0 && i+1<argc) { bfs_start = atoi(argv[++i]); }
        else if(strcmp(argv[i], "-d") == 0 && i+1<argc) { dfs_start = atoi(argv[++i]); }
        else if(strcmp(argv[i], "-c") == 0) { do_comp = 1; }
        else if(strcmp(argv[i], "--directed") == 0) { directed = 1; }
        else if(strcmp(argv[i], "--measure") == 0) { do_measure = 1; }
        else { usage(argv[0]); return 1; }
    }

    Representation rep = REP_LIST;
    if(strcmp(rep_str, "matrix") == 0) rep = REP_MATRIX;

    Grafo *g = NULL;
    if(!input){ fprintf(stderr, "No input provided\n"); usage(argv[0]); return 1; }

    /* use get_rss_mb() and now_seconds() defined above */

    if(do_measure){
        /* Measure for list and matrix separately and print a compact table */
        struct {
            const char *name;
            int rep_type;
            double time_s;
            double rss_before;
            double rss_after;
            double rss_peak;
            int success;
        } results[2] = {
            {"list", REP_LIST, 0, 0, 0, 0, 0},
            {"matrix", REP_MATRIX, 0, 0, 0, 0, 0}
        };

    /* helper to get peak memory (peak working set / ru_maxrss) */

        for(int i=0;i<2;i++){
            int rep_t = results[i].rep_type;
            double t0 = now_seconds();
            double before = get_rss_mb();
            Grafo *g_local = grafo_carregar(input, rep_t, directed);
            double t1 = now_seconds();
            double after = get_rss_mb();

            results[i].time_s = t1 - t0;
            results[i].rss_before = before < 0 ? 0.0 : before;
            results[i].rss_after = after < 0 ? 0.0 : after;
            /* peak: read peak after build (platform-provided peak metric)
               on Windows PeakWorkingSetSize; on POSIX getrusage.ru_maxrss */
#ifdef _WIN32
            {
                PROCESS_MEMORY_COUNTERS pmc;
                if(GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc)))
                    results[i].rss_peak = (double)pmc.PeakWorkingSetSize / 1024.0 / 1024.0;
                else results[i].rss_peak = results[i].rss_after;
            }
#else
            {
                struct rusage ru;
                if(getrusage(RUSAGE_SELF, &ru) == 0){
#if defined(__APPLE__)
                    results[i].rss_peak = (double)ru.ru_maxrss / 1024.0 / 1024.0;
#else
                    results[i].rss_peak = (double)ru.ru_maxrss / 1024.0;
#endif
                } else {
                    results[i].rss_peak = results[i].rss_after;
                }
            }
#endif

            results[i].success = (g_local != NULL);
            if(g_local) grafo_destruir(g_local);
        }

        /* Print a neat table */
        printf("\n=== Memory / Time comparison ===\n");
        printf("%-12s | %10s | %12s | %12s | %8s | %10s\n",
               "Representation", "Time(s)", "RSS before", "RSS after", "Delta", "Peak");
        printf("-------------+------------+--------------+--------------+----------+------------\n");
        for(int i=0;i<2;i++){
            double delta = results[i].rss_after - results[i].rss_before;
            if(!results[i].success){
                printf("%-12s | %10s | %12s | %12s | %8s | %10s\n",
                    results[i].name, "FAILED", "-", "-", "-", "-");
            } else {
                printf("%-12s | %10.2f | %12.2f | %12.2f | %8.2f | %10.2f\n",
                    results[i].name, results[i].time_s,
                    results[i].rss_before, results[i].rss_after,
                    delta, results[i].rss_peak);
            }
        }
        printf("================================\n\n");

        /* Rebuild list for normal operation */
        g = grafo_carregar(input, REP_LIST, directed);
        if(!g){ fprintf(stderr, "Erro ao carregar grafo (list) após medições\n"); return 2; }

    } else {
        g = grafo_carregar(input, rep, directed);
        if(!g){ fprintf(stderr, "Erro ao carregar grafo de '%s'\n", input); return 2; }
    }

    printf("Grafo carregado. n=%d m=%d rep=%s\n", g->n, g->m, rep==REP_LIST?"list":"matrix");

    if(grafo_escrever_resumo(g, output) != 0){ fprintf(stderr, "Erro ao escrever resumo em '%s'\n", output); }
    else printf("Resumo escrito em '%s'\n", output);

    if(bfs_start > 0){
        int *level = NULL;
        int *pai = grafo_bfs(g, bfs_start, &level);
        if(pai){
            printf("BFS iniciando em %d:\n", bfs_start);
            for(int i=0;i<g->n;i++){
                if(level[i] != -1) printf("%d: pai=%d nivel=%d\n", i+1, pai[i], level[i]);
            }
            free(pai); free(level);
        }
    }

    if(dfs_start > 0){
        int *level = NULL;
        int *pai = grafo_dfs(g, dfs_start, &level);
        if(pai){
            printf("DFS iniciando em %d:\n", dfs_start);
            for(int i=0;i<g->n;i++){
                if(level[i] != -1) printf("%d: pai=%d nivel=%d\n", i+1, pai[i], level[i]);
            }
            free(pai); free(level);
        }
    }

    if(do_comp){
        int **comps = NULL; int *sizes = NULL;
        int k = grafo_componentes(g, &comps, &sizes);
        printf("%d componentes encontrados:\n", k);
        for(int i=0;i<k;i++){
            printf("Componente %d (tamanho %d):", i+1, sizes[i]);
            for(int j=0;j<sizes[i]; j++) printf(" %d", comps[i][j]);
            printf("\n");
            free(comps[i]);
        }
        free(comps); free(sizes);
    }

    grafo_destruir(g);
    return 0;
}
