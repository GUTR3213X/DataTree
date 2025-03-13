from Nodes import BaseNode, get
from typing import Any, Callable, Optional
from TerminalActions import Action, Actions
from colorama import Fore
import os
import pickle as pkl

def do_nothing():
    return None
def red(s: str) -> str:
    return f'{Fore.RED}{s}{Fore.RESET}'
def Lgreen(s: str) -> str:
    return f'{Fore.LIGHTGREEN_EX}{s}{Fore.RESET}'
def PARENT_IS_CLOSED(node: BaseNode) -> bool:
    if node.parent is not None:
        return node.parent['closed'] == True
    return False
def IS_SELECTED(node: BaseNode) -> str:
    if node['selected']:
        return f'{Fore.LIGHTGREEN_EX}◉{Fore.RESET} '
    return f'{Fore.LIGHTGREEN_EX}○{Fore.RESET} '
def EQ_ID(node1: BaseNode, node2: BaseNode):
    return node1.id == node2.id
def NAME(node: BaseNode) -> str:
    return f'{node["name"]}'
def STATE(node: BaseNode) -> str:
    match node['closed']:
        case True:
            return red('⯈ ')
        case False: 
            return Lgreen('⯆ ')
        case _:
            return '  '
def IS_ACTIVATED(node: BaseNode) -> bool:
    return node.activated
def STR_ID(node: BaseNode) -> str:
    return f'{node.id:0>2} '
def func_print(s: str) -> Callable[..., None]:
    def wrapper():
        return print(s)
    return wrapper
def IDENTATION(node: BaseNode, lvl: int) -> str:
    return '  │ ' * lvl
class MyNode(BaseNode):
    def __init__(self, name: str, closed: Optional[bool], data: dict[Any, Any]):
        super().__init__(data)
        self['name'] = name
        self['closed'] = closed
        self['selected'] = False
        self.hidden_conditions      = [PARENT_IS_CLOSED   ]
        self.equal_conditions       = [EQ_ID              ]
        self.representations        = [STATE, NAME        ]
        self.include_conditions     = [IS_ACTIVATED       ]
        self.show_before_identation = [IS_SELECTED, STR_ID]
        self.identation = IDENTATION

class Main:
    def __init__(self):
        self.hud = Actions(
            Action('1', 'Criar node', self.criar_node),
            Action('2', 'Criar root', self.criar_root),
            Action('3', 'Remover node', 
                func_print('Tem certeza?'), Actions(
                    Action('s', 'Sim', self.remover_node),
                    Action('', 'Ignorar', do_nothing)
                )
            ),
            Action('4', 'Remover root',
                func_print('Tem certeza?'), Actions(
                   Action('s', 'Sim', self.remover_root),
                   Action('', 'Ignorar', do_nothing)
               )
            ),
            Action('5', 'Editar/adicionar um campo ao node', self.editar_campo),
            Action('e', 'Des/encolher node', self.enc_desenc_node),
            Action('v', 'Visualizar dados do node', self.vis_dados),
            Action('w', 'Mover para cima', self.cima),
            Action('s', 'Mover para baixo', self.baixo),
            Action('q', 'Parar', self.parar),
            Action('f', 'Arquivo', Actions(
                Action('1', 'Salvar', self.salvar),
                Action('2', 'Carregar', self.carregar)
            ))
        )
        self.super = BaseNode({})
        self.index = 0
        self.running: bool = True
    
    # Acoes
    def criar_node(self):
        nome = input('Nome do novo node: ')
        self.selecionado().append(MyNode(nome, None, {}))
        if self.selecionado()['closed'] is None:
            self.selecionado()['closed'] = False
    def criar_root(self):
        nome = input('Nome do novo root: ')
        self.super.append(MyNode(nome, None, {}))
        if self.super['closed'] is None:
            self.super['closed'] = False
    def remover_node(self):
        node = self.selecionado()
        if node.parent is not None and node.parent != self.super:
            if len(node.parent.children) <= 1:
                node.parent['closed'] = None
        node.deactivate()
    def remover_root(self):
        x = self.selecionado()
        while x.parent != self.super:
            x = x.parent
        x.deactivate()
    def editar_campo(self):
        chave = input('Chave: ')
        valor = input('Valor: ')
        self.selecionado()[chave] = valor
    def enc_desenc_node(self):
        node = self.selecionado()
        match node['closed']:
            case False:
                node['closed'] = True
            case True:
                node['closed'] = False
            case _:
                pass
    def vis_dados(self):
        r = ''
        print(f'Lendo dados de "{self.selecionado()["name"]}"...', end='')
        for k, v in self.selecionado().data.items():
            r += f'\n{repr(k):.<20}{repr(v):.>20} ({type(v).__name__})'
        print(r)
        input('Precione <ENTER> para continuar.')
    def cima(self, n: int=1):
        self.desselecionar()
        self.index -= n
        self.normalizar()
        self.selecionar()
        while get([self.selecionado()]+self.selecionado().parents, PARENT_IS_CLOSED):
            self.cima(1)
    def baixo(self, n: int=1):
        self.desselecionar()
        self.index += n
        self.normalizar()
        self.selecionar()
        while get([self.selecionado()]+self.selecionado().parents, PARENT_IS_CLOSED):
            self.baixo(1)
    def parar(self):
        self.running = False

    # Cursor
    def limite(self):
        return len(self.super.all) - 1
    def normalizar(self):
        self.index = min(max(self.index, 1), self.limite())
    def desselecionar(self):
        for node in self.super.all[1:]:
            node['selected'] = False
    def selecionar(self):
        self.selecionado()['selected'] = True
    def selecionado(self):
        for root in self.super.all[1:]:
            for node in root.all:
                if node.id == self.index:
                    return node
        raise IndexError(f'Não existe node com o id {self.index}')
    
    # Arquivo
    def salvar(self):
        filename = input('Nome do arquivo: ')
        with open(filename + '.pkl', 'wb') as file:
            pkl.dump(self.super, file)
    def carregar(self):
        filename = input('Nome do arquivo: ')
        with open(filename + '.pkl', 'rb') as file:
            self.super = pkl.load(file)
    
    # Rodando
    def run(self):
        self.running = True
        while self.running:
            os.system('clear')
            print(self.super.root_show())
            try:
                self.hud()
                self.baixo(0)
            except Exception as e:
                input(red(f'{type(e).__name__}: {e} '))

if __name__ == '__main__':
    Main().run()