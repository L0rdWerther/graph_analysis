class Grafo:
    def __init__(self, n):
        self.n = n
        self.lista_adj = [[] for _ in range(n)]
        self.matriz_adj = [[0]*n for _ in range(n)]

    def adicionar_aresta(self, u, v):
        self.lista_adj[u-1].append(v)
        self.lista_adj[v-1].append(u)
        self.matriz_adj[u-1][v-1] = 1
        self.matriz_adj[v-1][u-1] = 1

    def grau(self, v):
        return len(self.lista_adj[v-1])
