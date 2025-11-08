## Teoria dos Grafos — Graph_Analysis

### Parte 1

O objetivo deste trabalho é projetar e desenvolver uma **biblioteca para manipulação de grafos**.
A biblioteca deve ser capaz de:

* Representar **grafos simples e não dirigidos**;
* Implementar um conjunto básico de **algoritmos e operações sobre grafos**.

*Para esta primeira parte, o foco está na representação do grafo e na leitura de arquivos de entrada.*

---

### Estrutura do Projeto

```
projeto-grafos/
│
├── algoritmos.py
├── grafo.py
├── main.py
│
├── entrada.txt
├── as_graph.txt
├── collaboration_graph.txt
│
├── bfs_resultado.txt
├── componentes_resultado.txt
│
├── .gitignore
└── README.md
```

---

###  Como Executar

#### Pré-requisitos

* **Python 3.8** ou superior instalado no sistema;
* **Editor de código** ou **terminal** configurado para executar scripts Python.

---

####  No Windows

1. **Baixe o repositório:**

   * Clique em **Code → Download ZIP** no GitHub e extraia os arquivos,
     **ou** use o Git:

     ```bash
     git clone https://github.com/seuusuario/graph_analysis.git
     cd graph_analysis
     ```

2. **Abra o terminal** (Prompt de Comando ou PowerShell) na pasta do projeto.

3. **Execute o programa:**

   ```bash
   python main.py
   ```

4. **Verifique os resultados:**

   * Os arquivos de saída serão gerados na mesma pasta:

     ```
     bfs_resultado.txt
     dfs_resultado.txt
     componentes_resultado.txt
     saida.txt
     ```

---

#### No Linux

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seuusuario/graph_analysis.git
   cd graph_analysis
   ```

2. **Execute o programa:**

   ```bash
   python3 main.py
   ```

3. **Verifique os resultados:**

   * Os arquivos de saída serão gerados na mesma pasta:

     ```
     bfs_resultado.txt
     dfs_resultado.txt
     componentes_resultado.txt
     saida.txt
     ```

---






