from collections import deque


class Grafo:
    """Classe para representar um grafo"""

    def __init__(self, n, direcionado=False):
        """
        Inicializa o grafo

        Args:
            n: número de vértices
            direcionado: se o grafo é direcionado ou não
        """
        self.n = n
        self.direcionado = direcionado
        self.lista_adj = [[] for _ in range(n)]

    def adicionar_aresta(self, u, v):
        """
        Adiciona uma aresta entre os vértices u e v (0-indexed)

        Args:
            u: vértice origem
            v: vértice destino
        """
        self.lista_adj[u].append(v)
        if not self.direcionado:
            self.lista_adj[v].append(u)

    def bfs(self, inicio, arquivo_saida="bfs_resultado.txt"):
        """
        Executa busca em largura (BFS) a partir do vértice inicial

        Args:
            inicio: vértice inicial (0-indexed)
            arquivo_saida: nome do arquivo para salvar os resultados

        Returns:
            tuple: (pai, nivel) - vetores com o pai e nível de cada vértice
        """
        visitado = [False] * self.n
        nivel = [-1] * self.n
        pai = [-1] * self.n

        fila = deque([inicio])
        visitado[inicio] = True
        nivel[inicio] = 0

        while fila:
            u = fila.popleft()
            for v in self.lista_adj[u]:
                if not visitado[v]:
                    visitado[v] = True
                    pai[v] = u
                    nivel[v] = nivel[u] + 1
                    fila.append(v)

        # Salvar resultados em arquivo
        self._salvar_resultado(pai, nivel, "BFS", arquivo_saida)

        return pai, nivel

    def dfs(self, inicio, arquivo_saida="dfs_resultado.txt"):
        """
        Executa busca em profundidade (DFS) a partir do vértice inicial

        Args:
            inicio: vértice inicial (0-indexed)
            arquivo_saida: nome do arquivo para salvar os resultados

        Returns:
            tuple: (pai, nivel) - vetores com o pai e nível de cada vértice
        """
        visitado = [False] * self.n
        nivel = [-1] * self.n
        pai = [-1] * self.n

        nivel[inicio] = 0
        self._dfs_recursivo(inicio, visitado, nivel, pai)

        # Salvar resultados em arquivo
        self._salvar_resultado(pai, nivel, "DFS", arquivo_saida)

        return pai, nivel

    def _dfs_recursivo(self, u, visitado, nivel, pai):
        """Função auxiliar recursiva para DFS"""
        visitado[u] = True

        for v in self.lista_adj[u]:
            if not visitado[v]:
                pai[v] = u
                nivel[v] = nivel[u] + 1
                self._dfs_recursivo(v, visitado, nivel, pai)

    def _salvar_resultado(self, pai, nivel, tipo_busca, arquivo_saida):
        """
        Salva os resultados da busca em arquivo

        Args:
            pai: vetor de pais
            nivel: vetor de níveis
            tipo_busca: "BFS" ou "DFS"
            arquivo_saida: nome do arquivo
        """
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(f"Resultado da busca {tipo_busca}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"{'Vértice':<10} {'Pai':<10} {'Nível':<10}\n")
            f.write("-" * 50 + "\n")

            for v in range(self.n):
                pai_str = str(pai[v]) if pai[v] != -1 else "raiz"
                nivel_str = str(nivel[v]) if nivel[v] != -1 else "não visitado"
                f.write(f"{v:<10} {pai_str:<10} {nivel_str:<10}\n")

        print(f"Resultados salvos em '{arquivo_saida}'")