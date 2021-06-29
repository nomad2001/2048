from random import randrange

def generirarajNakljucnoPozicijoInStevilo(velikost, tabela):
    x = randrange(velikost)
    y = randrange(velikost)

    while tabela[x][y] != 0:
        x = randrange(velikost)
        y = randrange(velikost)
        
    kateroNovoStevilo = randrange(10)

    if kateroNovoStevilo % 5 == 0:
        tabela[x][y] = 4
    else:
        tabela[x][y] = 2

class Igra:
    def __init__(self, velikost = 4, tabela = None):
        self.velikost = velikost

        if tabela == None:
            self.tabela = [[0 for i in range(velikost)] for i in range(velikost)]
            generirarajNakljucnoPozicijoInStevilo(self.velikost,self.tabela)
            generirarajNakljucnoPozicijoInStevilo(self.velikost,self.tabela)


