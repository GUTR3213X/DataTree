# Projeto de Gerenciamento de Nodes

Este projeto implementa um sistema de gerenciamento de nós (nodes) em uma estrutura de árvore, permitindo criação, remoção e manipulação de nós de forma interativa no terminal.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

- `main.py`: Arquivo principal que executa a aplicação e gerencia as interações com o usuário.
- `Nodes.py`: Define a classe `BaseNode`, que representa um nó na estrutura de árvore e fornece funcionalidades para manipulação dos nós.
- `TerminalActions.py`: Implementa um sistema de ações interativas no terminal.

## Instalação

### Pré-requisitos

Este projeto requer Python 3. Para instalar as dependências, utilize:

```sh
pip install colorama
```

## Como Usar

Execute o arquivo principal:

```sh
python main.py
```

O programa apresentará uma interface interativa para gerenciar os nós.

## Funcionalidades

### Principais Comandos

- `1`: Criar um novo nó.
- `2`: Criar um novo nó raiz.
- `3`: Remover um nó.
- `4`: Remover um nó raiz.
- `5`: Editar ou adicionar um campo ao nó.
- `e`: Expandir ou recolher um nó.
- `v`: Visualizar dados do nó.
- `w`: Mover para cima.
- `s`: Mover para baixo.
- `q`: Sair do programa.
- `f`: Acessar opções de arquivo (Salvar/Carregar).

### Salvamento e Carregamento de Dados

O programa permite salvar e carregar a estrutura de nós usando arquivos `.pkl`.

- Para salvar, selecione a opção de arquivo e informe um nome.
- Para carregar, informe o nome do arquivo salvo anteriormente.

## Estrutura de Classes

### `BaseNode` (Nodes.py)

Representa um nó na árvore, armazenando dados e permitindo a manipulação de filhos e pais.

- `append(node)`: Adiciona um nó filho.
- `remove(checks)`: Remove nós que atendem a certos critérios.
- `prettystr()`: Retorna uma string formatada da árvore.

### `Action` e `Actions` (TerminalActions.py)

- `Action`: Representa uma ação acionável no terminal.
- `Actions`: Conjunto de ações interativas exibidas no terminal.
