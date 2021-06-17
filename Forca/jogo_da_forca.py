from abc import ABC, abstractmethod
import os
from random import choice
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel


class Membro(ABC):
    @classmethod
    @abstractmethod
    def cria_parte(cls):
        raise NotImplementedError


class Cabeca(Membro):
    @classmethod
    def cria_parte(cls):
        return 'O'


class Tronco(Membro):
    @classmethod
    def cria_parte(cls):
        return '|'


class Esquerdo(Membro):
    @classmethod
    def cria_parte(cls):
        return '\t|\t       /'


class Direito(Membro):
    @classmethod
    def cria_parte(cls):
        return '\\'


class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.corpo = Boneco()


class Boneco:
    def __init__(self):
        self.partes = self.cria_partes()
        self.linhas = self.cria_linhas()
        self.vivo = True

    def __str__(self):
        return ''.join(self.renderiza_boneco()) + '\t|'

    def cria_partes(self):
        self.cabeca = Cabeca.cria_parte()
        self.tronco = Tronco.cria_parte()
        self.braco_esquerdo, self.perna_esquerda = Esquerdo.cria_parte(
        ), Esquerdo.cria_parte()
        self.braco_direito, self.perna_direita = Direito.cria_parte(
        ), Direito.cria_parte()
        return [
            self.cabeca, self.braco_esquerdo, self.tronco, self.braco_direito,
            self.perna_esquerda, self.perna_direita
        ]

    def cria_linhas(self):
        return [
            self.partes[0], ''.join(self.partes[1:4]),
            ' '.join(self.partes[4:])
        ]

    def renderiza_boneco(self):
        return [
            f'{linha:^3}\n' if len(linha) > 1 or i == 0 else f'{linha:<3}\n'
            for i, linha in enumerate(self.linhas)
        ]

    def retira_parte(self):
        try:
            self.partes.pop()
            self.linhas = self.cria_linhas()
        except IndexError:
            self.linhas = 'X'
            self.vivo = False


class Palavra:
    def __init__(self):
        self.palavras = [
            'familia', 'açougue', 'psicopata', 'pandemia', 'ensolarado',
            'endividamento', 'verdejante', 'celeuma', 'apicultor',
            'rastejante', 'ventilador', 'submarino', 'helicoptero',
            'planejamento', 'receptivo', 'visionario'
        ]
        self.adivinha = choice(self.palavras)
        self.segredo = '_' * len(self.adivinha)

    def __str__(self):
        return self.segredo

    def adiciona_letra(self, letra):
        indices = [i for i, l in enumerate(self.adivinha) if letra == l]
        self.segredo = ''.join([
            l if i in indices else l if l == self.segredo[i] else '_'
            for i, l in enumerate(self.adivinha)
        ])


class Forca:
    def __init__(self, boneco: Boneco):
        self.boneco = boneco
        self.palavra = Palavra()
        self.forca = self.renderiza_forca()

    def renderiza_forca(self, titulo=None):
        return Panel(f'''
        -----------------             
        |               |            
        |               |            
        |              {self.boneco}
        |                       
        |                       
        |                      
        |                      


  --->  {self.palavra}   letras = {len(self.palavra.segredo)}
        ''',
                     title=titulo,
                     padding=(0, 5),
                     expand=False)


class Controle:
    def __init__(self):
        self.painel = Panel('JOGO DA FORCA')
        self.console = Console()
        self.letras_erradas = []

    def pega_resposta(self):
        self.resposta = Prompt.ask(
            'Tente uma letra(ou arrisque a palavra toda)').lower()
        if len(self.resposta) > 1:
            arriscar = Prompt.ask(
                f'Você quer arriscar chutando a palavra {self.resposta}?(s/n)'
            ).lower()
            if arriscar == 's' and self.resposta.lower(
            ) == self.forca.palavra.adivinha:
                self.forca.palavra.segredo = self.forca.palavra.adivinha
                return
            elif arriscar.lower(
            ) == 's' and self.resposta.lower() != self.forca.palavra.adivinha:
                self.console.print('Infelizmente você errou a palavra')
                self.forca.boneco.vivo = False
                return
            elif arriscar == 'n':
                self.console.print(
                    'Melhor ter certeza antes de arriscar mesmo!')
                return
            else:
                self.console.print(
                    'Aparentemente você não escolheu nenhuma das alternativas. Segue o baile.'
                )
                return

        if self.resposta in self.forca.palavra.adivinha:
            self.forca.palavra.adiciona_letra(self.resposta)
            return self.console.print('Parabéns! Você acertou a letra')
        self.forca.boneco.retira_parte()
        self.letras_erradas.append(self.resposta)
        return self.console.print('Infelizmente você errou e perdeu uma vida')

    def palavra_incompleta(self):
        return True if self.forca.palavra.segredo != self.forca.palavra.adivinha else False

    def inicia_jogo(self):
        self.console.print(self.painel,
                           justify='center',
                           style='bold blue on black')
        self.jogador = Jogador(Prompt.ask('Diga seu nome'))
        self.forca = Forca(self.jogador.corpo)
        while self.forca.boneco.vivo and self.palavra_incompleta():
            if os.sys.platform == 'windows':
                os.system('cls')
            else:
                os.system('clear')
            self.console.print(
                self.forca.renderiza_forca(self.jogador.nome),
                Panel.fit('-'.join(self.letras_erradas),
                          title='Letras erradas'))
            self.pega_resposta()
        if self.forca.boneco.vivo:
            return self.console.print(
                'Parabéns, você acertou a palavra e ganhou o jogo!')
        return self.console.print(
            f'Você não conseguiu acertar a palavra a tempo e foi enforcado! A palavra era {self.forca.palavra.adivinha}'
        )


if __name__ == '__main__':
    jogo = Controle()
    jogo.inicia_jogo()
