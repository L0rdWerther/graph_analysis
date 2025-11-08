from collections import deque


class Grafo:
    """Representação de grafo que mantém simultaneamente lista de adjacência
    e matriz de adjacência. Os vértices no arquivo de entrada são esperados
    como 1..n (base 1). Internamente as estruturas usam índices 0..n-1, mas
    os métodos públicos aceitam vértices em base 1.

    A classe fornece:
    - adicionar_aresta(u, v)
    - grau(v, rep='list'|'matrix')
    - num_arestas()
    - from_file(path) -> Grafo (classmethod)
    - write_summary(path, rep='list'|'matrix'|'both')
    - bfs(inicio, arquivo_saida) - Busca em largura
    - dfs(inicio, arquivo_saida) - Busca em profundidade
    - componentes_conexos(arquivo_saida) - Encontra componentes conexos
    """

    def __init__(self, n: int, direcionado: bool = False, default_rep: str = 'list'):
        self.n = int(n)
        self.direcionado = bool(direcionado)
        # lista de adjacência: cada entrada armazena vértices em base 1
        self.lista_adj = [[] for _ in range(self.n)]
        # matriz de adjacência (0/1)
        self.matriz_adj = [[0] * self.n for _ in range(self.n)]
        if default_rep not in ('list', 'matrix'):
            raise ValueError("default_rep deve ser 'list' ou 'matrix'")
        self.default_rep = default_rep

    def adicionar_aresta(self, u: int, v: int) -> None:
        """Adiciona aresta não direcionada entre u e v. u/v são 1-based.

        Permite múltiplas chamadas para a mesma aresta; se já existir, mantém
        a representação como se fosse um grafo simples (sem paralelas) na
        matriz, e na lista pode duplicar se o usuário inserir várias vezes.
        """
        if u < 1 or v < 1 or u > self.n or v > self.n:
            raise ValueError(f"Vértice fora do intervalo: {u}, {v}")

        # lista armazena vértices em base 1 (para facilitar leitura/escrita)
        if v not in self.lista_adj[u - 1]:
            self.lista_adj[u - 1].append(v)
        # matriz é 0/1 para aresta u->v
        self.matriz_adj[u - 1][v - 1] = 1

        if not self.direcionado:
            # se não direcionado, adicionar também v->u
            if u not in self.lista_adj[v - 1]:
                self.lista_adj[v - 1].append(u)
            self.matriz_adj[v - 1][u - 1] = 1

    def grau(self, v: int, rep: str = 'list') -> int:
        """Retorna o grau do vértice v (1-based).

        rep escolhe a representação usada para calcular o grau: 'list' ou
        'matrix'. Por padrão usa a lista de adjacência.
        """
        if v < 1 or v > self.n:
            raise ValueError(f"Vértice fora do intervalo: {v}")
        if rep is None:
            rep = self.default_rep

        if rep == 'list':
            return len(self.lista_adj[v - 1])
        elif rep == 'matrix':
            return sum(self.matriz_adj[v - 1])
        else:
            raise ValueError("rep deve ser 'list' ou 'matrix'")

    def num_arestas(self) -> int:
        """Retorna número de arestas (grafo não direcionado)."""
        # soma dos graus / 2
        total_grau = sum(len(adj) for adj in self.lista_adj)
        return total_grau // 2 if not self.direcionado else total_grau

    def bfs(self, inicio: int, arquivo_saida: str = "bfs_resultado.txt"):
        """Executa busca em largura (BFS) a partir do vértice inicial (1-based).

        Args:
            inicio: vértice inicial (1-based)
            arquivo_saida: nome do arquivo para salvar os resultados

        Returns:
            tuple: (pai, nivel) - vetores com o pai e nível de cada vértice (1-based)
        """
        if inicio < 1 or inicio > self.n:
            raise ValueError(f"Vértice inicial fora do intervalo: {inicio}")

        # Trabalha internamente com índices 0-based
        inicio_idx = inicio - 1

        visitado = [False] * self.n
        nivel = [-1] * self.n
        pai = [-1] * self.n

        fila = deque([inicio_idx])
        visitado[inicio_idx] = True
        nivel[inicio_idx] = 0

        while fila:
            u_idx = fila.popleft()
            # lista_adj armazena vértices em base 1
            for v in self.lista_adj[u_idx]:
                v_idx = v - 1
                if not visitado[v_idx]:
                    visitado[v_idx] = True
                    pai[v_idx] = u_idx + 1  # armazena pai em base 1
                    nivel[v_idx] = nivel[u_idx] + 1
                    fila.append(v_idx)

        # Salvar resultados em arquivo
        self._salvar_resultado(pai, nivel, "BFS", arquivo_saida)

        return pai, nivel

    def dfs(self, inicio: int, arquivo_saida: str = "dfs_resultado.txt"):
        """Executa busca em profundidade (DFS) a partir do vértice inicial (1-based).

        Args:
            inicio: vértice inicial (1-based)
            arquivo_saida: nome do arquivo para salvar os resultados

        Returns:
            tuple: (pai, nivel) - vetores com o pai e nível de cada vértice (1-based)
        """
        if inicio < 1 or inicio > self.n:
            raise ValueError(f"Vértice inicial fora do intervalo: {inicio}")

        inicio_idx = inicio - 1

        visitado = [False] * self.n
        nivel = [-1] * self.n
        pai = [-1] * self.n

        nivel[inicio_idx] = 0
        self._dfs_recursivo(inicio_idx, visitado, nivel, pai)

        # Salvar resultados em arquivo
        self._salvar_resultado(pai, nivel, "DFS", arquivo_saida)

        return pai, nivel

    def _dfs_recursivo(self, u_idx: int, visitado: list, nivel: list, pai: list):
        """Função auxiliar recursiva para DFS (trabalha com índices 0-based)"""
        visitado[u_idx] = True

        # lista_adj armazena vértices em base 1
        for v in self.lista_adj[u_idx]:
            v_idx = v - 1
            if not visitado[v_idx]:
                pai[v_idx] = u_idx + 1  # armazena pai em base 1
                nivel[v_idx] = nivel[u_idx] + 1
                self._dfs_recursivo(v_idx, visitado, nivel, pai)

    def componentes_conexos(self, arquivo_saida: str = "componentes_resultado.txt"):
        """Encontra os componentes conexos do grafo.

        Args:
            arquivo_saida: nome do arquivo para salvar os resultados

        Returns:
            list: lista de componentes, onde cada componente é uma lista de vértices (1-based)
        """
        visitado = [False] * self.n
        componentes = []

        for v_idx in range(self.n):
            if not visitado[v_idx]:
                componente = []
                self._dfs_componente(v_idx, visitado, componente)
                # Converte para base 1 e ordena
                componente_base1 = sorted([v + 1 for v in componente])
                componentes.append(componente_base1)

        # Salvar resultados em arquivo
        self._salvar_componentes(componentes, arquivo_saida)

        return componentes

    def _dfs_componente(self, u_idx: int, visitado: list, componente: list):
        """Função auxiliar DFS para encontrar componentes conexos (trabalha com índices 0-based)"""
        visitado[u_idx] = True
        componente.append(u_idx)

        # lista_adj armazena vértices em base 1
        for v in self.lista_adj[u_idx]:
            v_idx = v - 1
            if not visitado[v_idx]:
                self._dfs_componente(v_idx, visitado, componente)

    def _salvar_componentes(self, componentes: list, arquivo_saida: str):
        """Salva os componentes conexos em arquivo."""
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("COMPONENTES CONEXOS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Número de componentes: {len(componentes)}\n\n")

            for i, comp in enumerate(componentes, 1):
                f.write(f"Componente {i}:\n")
                f.write(f"  Tamanho: {len(comp)} vértices\n")
                f.write(f"  Vértices: {comp}\n\n")

        print(f"Resultados salvos em '{arquivo_saida}'")

    def _salvar_resultado(self, pai: list, nivel: list, tipo_busca: str, arquivo_saida: str):
        """Salva os resultados da busca em arquivo."""
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(f"Resultado da busca {tipo_busca}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"{'Vértice':<10} {'Pai':<10} {'Nível':<10}\n")
            f.write("-" * 50 + "\n")

            for v_idx in range(self.n):
                v = v_idx + 1  # converte para base 1
                pai_str = str(pai[v_idx]) if pai[v_idx] != -1 else "raiz"
                nivel_str = str(nivel[v_idx]) if nivel[v_idx] != -1 else "não visitado"
                f.write(f"{v:<10} {pai_str:<10} {nivel_str:<10}\n")

        print(f"Resultados salvos em '{arquivo_saida}'")

    @classmethod
    def from_file(cls, path: str, default_rep: str = 'list') -> 'Grafo':
        """Lê um grafo de um arquivo texto.

        Formato esperado:
        - primeira linha: número de vértices (inteiro)
        - linhas subsequentes: arestas, cada linha com dois inteiros u v
          (u e v em base 1). Linhas vazias e comentários (começando com '#')
          são ignoradas.
        """
        with open(path, 'r', encoding='utf-8') as f:
            # pular linhas em branco até achar um número
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # primeira linha útil: número de vértices
                try:
                    n = int(line.split()[0])
                except ValueError as e:
                    raise ValueError(f"Formato inválido na primeira linha: {line}") from e
                break
            else:
                raise ValueError("Arquivo vazio ou sem número de vértices")

            grafo = cls(n, default_rep=default_rep)

            for raw in f:
                raw = raw.strip()
                if not raw or raw.startswith('#'):
                    continue
                parts = raw.split()
                if len(parts) < 2:
                    # ignora linhas que não tenham ao menos dois números
                    continue
                try:
                    u = int(parts[0])
                    v = int(parts[1])
                except ValueError:
                    # ignora linhas malformadas
                    continue
                grafo.adicionar_aresta(u, v)

        return grafo

    def write_summary(self, path: str, rep: str = 'list') -> None:
        """Escreve um arquivo texto com:
        - número de vértices
        - número de arestas
        - grau de cada vértice (uma linha por vértice)

        rep pode ser 'list', 'matrix' ou 'both'.
        """
        if rep not in ('list', 'matrix', 'both'):
            raise ValueError("rep deve ser 'list', 'matrix' ou 'both'")

        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"Número de vértices: {self.n}\n")
            f.write(f"Número de arestas: {self.num_arestas()}\n")
            f.write("Grau dos vértices:\n")
            for i in range(1, self.n + 1):
                if rep == 'both':
                    g_list = self.grau(i, 'list')
                    g_mat = self.grau(i, 'matrix')
                    f.write(f"{i}: lista={g_list}, matriz={g_mat}\n")
                else:
                    g = self.grau(i, rep)
                    f.write(f"{i}: {g}\n")

    def __repr__(self) -> str:
        return f"Grafo(n={self.n}, edges={self.num_arestas()})"