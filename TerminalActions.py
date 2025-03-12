from typing import Callable, Any
from colorama import Cursor, Fore

class Action:
    def __init__(self, key: str, name: str, *functions: Callable[..., Any]):
        self.name = name
        self.key = key
        self.functions = functions
    def __str__(self):
        return f'{self.key} : {self.name}'
    def run(self):
        result: list[Any] = []
        for function in self.functions:
            result.append(function())
        return result
def Actions(*actions: Action):
    def wrapper():
        print('\n'.join(map(str, actions)))
        while True:
            response = input('Resposta: ')
            for action in actions:
                if action.key == response:
                    return action.run()
            print(f'{Fore.RED}Resposta inválida{Fore.RESET}')
            print(Cursor.UP(2), end='')
    return wrapper
