from collections import deque


class Grafo:
    """Representação de grafo com escolha de representação (lista ou matriz).

    O usuário escolhe a representação a ser utilizada no construtor.
    Os vértices no arquivo de entrada são esperados como 1..n (base 1).
    Internamente as estruturas usam índices 0..n-1, mas os métodos públicos
    aceitam vértices em base 1.

    A classe fornece:
    - adicionar_aresta(u, v)
    - grau(v)
    - num_arestas()
    - from_file(path, rep='list'|'matrix') -> Grafo (classmethod)
    - write_summary(path)
    - bfs(inicio, arquivo_saida) - Busca em largura
    - dfs(inicio, arquivo_saida) - Busca em profundidade
    - componentes_conexos(arquivo_saida) - Encontra componentes conexos
    - get_vizinhos(v) - Retorna lista de vizinhos do vértice v
    """

    def __init__(self, n: int, representacao: str = 'list', direcionado: bool = False):
        """Inicializa o grafo com a representação escolhida.

        Args:
            n: número de vértices
            representacao: 'list' para lista de adjacência, 'matrix' para matriz
            direcionado: True para grafo direcionado, False para não direcionado
        """
        if representacao not in ('list', 'matrix'):
            raise ValueError("representacao deve ser 'list' ou 'matrix'")

        self.n = int(n)
        self.direcionado = bool(direcionado)
        self.representacao = representacao

        if self.representacao == 'list':
            # Lista de adjacência: cada entrada armazena vértices em base 1
            self.lista_adj = [[] for _ in range(self.n)]
        else:  # matriz
            # Matriz de adjacência (0/1)
            self.matriz_adj = [[0] * self.n for _ in range(self.n)]

    def adicionar_aresta(self, u: int, v: int) -> None:
        """Adiciona aresta entre u e v. u/v são 1-based.

        Permite múltiplas chamadas para a mesma aresta; mantém a representação
        como se fosse um grafo simples (sem arestas paralelas).
        """
        if u < 1 or v < 1 or u > self.n or v > self.n:
            raise ValueError(f"Vértice fora do intervalo: {u}, {v}")

        if self.representacao == 'list':
            # Lista armazena vértices em base 1
            if v not in self.lista_adj[u - 1]:
                self.lista_adj[u - 1].append(v)
            if not self.direcionado and u not in self.lista_adj[v - 1]:
                self.lista_adj[v - 1].append(u)
        else:  # matriz
            self.matriz_adj[u - 1][v - 1] = 1
            if not self.direcionado:
                self.matriz_adj[v - 1][u - 1] = 1

    def get_vizinhos(self, v: int) -> list:
        """Retorna lista de vizinhos do vértice v (1-based).

        Args:
            v: vértice (1-based)

        Returns:
            Lista de vizinhos em base 1
        """
        if v < 1 or v > self.n:
            raise ValueError(f"Vértice fora do intervalo: {v}")

        if self.representacao == 'list':
            return self.lista_adj[v - 1].copy()
        else:  # matriz
            vizinhos = []
            for i in range(self.n):
                if self.matriz_adj[v - 1][i] == 1:
                    vizinhos.append(i + 1)  # retorna em base 1
            return vizinhos

    def grau(self, v: int) -> int:
        """Retorna o grau do vértice v (1-based).

        Args:
            v: vértice (1-based)

        Returns:
            Grau do vértice
        """
        if v < 1 or v > self.n:
            raise ValueError(f"Vértice fora do intervalo: {v}")

        if self.representacao == 'list':
            return len(self.lista_adj[v - 1])
        else:  # matriz
            return sum(self.matriz_adj[v - 1])

    def num_arestas(self) -> int:
        """Retorna número de arestas."""
        if self.representacao == 'list':
            total_grau = sum(len(adj) for adj in self.lista_adj)
        else:  # matriz
            total_grau = sum(sum(linha) for linha in self.matriz_adj)

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

        inicio_idx = inicio - 1

        visitado = [False] * self.n
        nivel = [-1] * self.n
        pai = [-1] * self.n

        fila = deque([inicio_idx])
        visitado[inicio_idx] = True
        nivel[inicio_idx] = 0

        while fila:
            u_idx = fila.popleft()
            u = u_idx + 1  # converte para base 1

            # Obtém vizinhos usando o método get_vizinhos
            for v in self.get_vizinhos(u):
                v_idx = v - 1
                if not visitado[v_idx]:
                    visitado[v_idx] = True
                    pai[v_idx] = u  # armazena pai em base 1
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
        u = u_idx + 1  # converte para base 1

        # Obtém vizinhos usando o método get_vizinhos
        for v in self.get_vizinhos(u):
            v_idx = v - 1
            if not visitado[v_idx]:
                pai[v_idx] = u  # armazena pai em base 1
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
        u = u_idx + 1  # converte para base 1

        # Obtém vizinhos usando o método get_vizinhos
        for v in self.get_vizinhos(u):
            v_idx = v - 1
            if not visitado[v_idx]:
                self._dfs_componente(v_idx, visitado, componente)

    def _salvar_componentes(self, componentes: list, arquivo_saida: str):
        """Salva os componentes conexos em arquivo."""
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("COMPONENTES CONEXOS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Representação utilizada: {self.representacao}\n")
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
            f.write(f"Representação utilizada: {self.representacao}\n\n")
            f.write(f"{'Vértice':<10} {'Pai':<10} {'Nível':<10}\n")
            f.write("-" * 50 + "\n")

            for v_idx in range(self.n):
                v = v_idx + 1  # converte para base 1
                pai_str = str(pai[v_idx]) if pai[v_idx] != -1 else "raiz"
                nivel_str = str(nivel[v_idx]) if nivel[v_idx] != -1 else "não visitado"
                f.write(f"{v:<10} {pai_str:<10} {nivel_str:<10}\n")

        print(f"Resultados salvos em '{arquivo_saida}'")

    @classmethod
    def from_file(cls, path: str, representacao: str = 'list') -> 'Grafo':
        """Lê um grafo de um arquivo texto.

        Args:
            path: caminho do arquivo
            representacao: 'list' para lista de adjacência, 'matrix' para matriz

        Formato esperado:
        - primeira linha: número de vértices (inteiro)
        - segunda linha (opcional): 'direcionado' ou 'nao-direcionado' (padrão: nao-direcionado)
        - linhas subsequentes: arestas, cada linha com dois inteiros u v
          (u e v em base 1). Linhas vazias e comentários (começando com '#')
          são ignoradas.
        """
        with open(path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

            if not lines:
                raise ValueError("Arquivo vazio ou sem número de vértices")

            # Primeira linha: número de vértices
            try:
                n = int(lines[0].split()[0])
            except ValueError as e:
                raise ValueError(f"Formato inválido na primeira linha: {lines[0]}") from e

            # Segunda linha opcional: tipo do grafo
            direcionado = False
            start_idx = 1
            if len(lines) > 1 and lines[1].lower() in ('direcionado', 'nao-direcionado', 'não-direcionado'):
                direcionado = (lines[1].lower() == 'direcionado')
                start_idx = 2

            grafo = cls(n, representacao=representacao, direcionado=direcionado)

            # Ler arestas
            for raw in lines[start_idx:]:
                parts = raw.split()
                if len(parts) < 2:
                    continue
                try:
                    u = int(parts[0])
                    v = int(parts[1])
                except ValueError:
                    continue
                grafo.adicionar_aresta(u, v)

        return grafo

    def write_summary(self, path: str) -> None:
        """Escreve um arquivo texto com:
        - representação utilizada
        - número de vértices
        - número de arestas
        - grau de cada vértice (uma linha por vértice)
        """
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"Representação: {self.representacao}\n")
            f.write(f"Tipo: {'direcionado' if self.direcionado else 'não direcionado'}\n")
            f.write(f"Número de vértices: {self.n}\n")
            f.write(f"Número de arestas: {self.num_arestas()}\n\n")

            f.write("Grau dos vértices:\n")
            for i in range(1, self.n + 1):
                f.write(f"{i}: {self.grau(i)}\n")

    def imprimir_representacao(self):
        """Imprime a representação do grafo (para debug)."""
        print(f"\nRepresentação: {self.representacao}")
        print(f"Tipo: {'direcionado' if self.direcionado else 'não direcionado'}")
        print(f"Vértices: {self.n}, Arestas: {self.num_arestas()}\n")

        if self.representacao == 'list':
            print("Lista de Adjacência:")
            for i in range(self.n):
                print(f"  {i + 1}: {self.lista_adj[i]}")
        else:
            print("Matriz de Adjacência:")
            print("     " + "  ".join(str(i + 1) for i in range(self.n)))
            print("   ┌" + "─" * (3 * self.n + 1) + "┐")
            for i in range(self.n):
                linha = "  ".join(str(self.matriz_adj[i][j]) for j in range(self.n))
                print(f"{i + 1}  │ {linha} │")
            print("   └" + "─" * (3 * self.n + 1) + "┘")

    def __repr__(self) -> str:
        return f"Grafo(n={self.n}, edges={self.num_arestas()}, rep={self.representacao})"