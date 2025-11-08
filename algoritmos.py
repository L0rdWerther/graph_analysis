from collections import deque

def bfs(grafo, inicio):
    visitado = [False]*grafo.n
    nivel = [-1]*grafo.n
    pai = [-1]*grafo.n

    fila = deque([inicio])
    visitado[inicio] = True
    nivel[inicio] = 0

    while fila:
        u = fila.popleft()
        for v in grafo.lista_adj[u]:
            if not visitado[v-1]:
                visitado[v-1] = True
                pai[v-1] = u
                nivel[v-1] = nivel[u-1] + 1
                fila.append(v)
    return pai, nivel
