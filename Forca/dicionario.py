import requests
from random import choice
from time import sleep
from dicio import Dicio
from rich.progress import Progress
from bs4 import BeautifulSoup


class Dicionario:
    def __init__(self):
        self.dicio = Dicio()
        self.progress = Progress()
        self.url = 'https://www.dicio.com.br/lista-de-palavras/'
        self.palavras = self.pega_palavras()
        self.palavra = choice(self.palavras)
        self.resultado = self.dicio.search(self.palavra)
        self.significado = self.pega_significado(self.resultado)
        self.sinonimo = self.pega_sinonimo(self.resultado)

    def pega_palavras(self):
        barra = self.progress.add_task('Carrega palavras')
        with self.progress:
            self.progress.console.print('Fazendo download das palavras...')
            self.progress.advance(barra, advance=25)
            response = requests.get(self.url).text
            self.progress.console.print('Extraindo palavras...')
            self.progress.advance(barra, advance=25)
            soup = BeautifulSoup(response, 'html.parser')
            sleep(0.5)
            self.progress.advance(barra, advance=25)
            lista = [
                palavra.text
                for palavra in soup.select('.words-list--links > a')
            ]
            self.progress.advance(barra, advance=25)
            sleep(0.5)
            self.progress.console.print(
                f'Foram encontradas {len(lista)} palavras!')

        return [palavra for palavra in lista if len(palavra) > 5]

    def pega_significado(self, palavra):
        barra = self.progress.add_task('Pega significado da palavra')
        with self.progress:
            sleep(1)
            self.progress.advance(barra, advance=50)
            try:
                return palavra.meaning.split(';')[0]
            except IndexError:
                self.progress.advance(barra, advance=25)
                return palavra.meaning[0] if isinstance(
                    palavra.meaning, list) else palavra.meaning

    def pega_sinonimo(self, palavra):
        barra = self.progress.add_task('Pega sinonimo da palavra')
        with self.progress:
            sleep(1)
            self.progress.advance(barra, advance=50)
            try:
                return palavra.synonyms[0]
            except IndexError:
                self.progress.advance(barra, advance=25)
                return palavra.synonyms[0] if isinstance(
                    palavra.synonyms, list) else palavra.synonyms


if __name__ == '__main__':
    D = Dicionario()
