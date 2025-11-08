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
    """

    def __init__(self, n: int):
        self.n = int(n)
        # lista de adjacência: cada entrada armazena vértices em base 1
        self.lista_adj = [[] for _ in range(self.n)]
        # matriz de adjacência (0/1)
        self.matriz_adj = [[0] * self.n for _ in range(self.n)]

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
        if u not in self.lista_adj[v - 1]:
            self.lista_adj[v - 1].append(u)

        # matriz é 0/1
        self.matriz_adj[u - 1][v - 1] = 1
        self.matriz_adj[v - 1][u - 1] = 1

    def grau(self, v: int, rep: str = 'list') -> int:
        """Retorna o grau do vértice v (1-based).

        rep escolhe a representação usada para calcular o grau: 'list' ou
        'matrix'. Por padrão usa a lista de adjacência.
        """
        if v < 1 or v > self.n:
            raise ValueError(f"Vértice fora do intervalo: {v}")
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
        return total_grau // 2

    @classmethod
    def from_file(cls, path: str) -> 'Grafo':
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

            grafo = cls(n)

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
