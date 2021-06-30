from random import randrange

GOR = 'U'
DOL = 'D'
LEVO = 'L'
DESNO = 'R'
KONEC_IGRE = 'E'

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
        else:
            self.tabela = tabela
    
    def premakniLevo(self):
        aliSeJeKateriPremaknil = False
        for i in range(self.velikost):
            prostaMesta = []
            prvoSeVednoProstoMesto = 0
            for j in range(self.velikost):
                if self.tabela[i][j] == 0:
                    prostaMesta.append(j)
                elif len(prostaMesta) != 0:
                    if prostaMesta[prvoSeVednoProstoMesto] == 0:
                        self.tabela[i][0] = self.tabela[i][j]
                        self.tabela[i][j] = 0
                        prostaMesta.append(j)
                        prvoSeVednoProstoMesto += 1
                    else:
                        if self.tabela[i][prostaMesta[prvoSeVednoProstoMesto ] - 1] == self.tabela[i][j]:
                            self.tabela[i][prostaMesta[prvoSeVednoProstoMesto] - 1] *= 2
                            self.tabela[i][j] = 0
                            prostaMesta.append(j)
                        else:
                            self.tabela[i][prostaMesta[prvoSeVednoProstoMesto]] = self.tabela[i][j]
                            self.tabela[i][j] = 0
                            prostaMesta.append(j)
                            prvoSeVednoProstoMesto += 1
                aliSeJeKateriPremaknil = True
        return aliSeJeKateriPremaknil
        
    def premakniGor(self):
        aliSeJeKateriPremaknil = False
        for i in range(self.velikost):
            prostaMesta = []
            prvoSeVednoProstoMesto = 0
            for j in range(self.velikost):
                if self.tabela[j][i] == 0:
                    prostaMesta.append(j)
                elif len(prostaMesta) != 0:
                    if prostaMesta[prvoSeVednoProstoMesto] == 0:
                        self.tabela[0][i] = self.tabela[j][i]
                        self.tabela[j][i] = 0
                        prostaMesta.append(j)
                        prvoSeVednoProstoMesto += 1
                    else:
                        if self.tabela[prostaMesta[prvoSeVednoProstoMesto] - 1][i] == self.tabela[j][i]:
                            self.tabela[prostaMesta[prvoSeVednoProstoMesto] - 1][i] *= 2
                            self.tabela[j][i] = 0
                            prostaMesta.append(j)
                        else:
                            self.tabela[prostaMesta[prvoSeVednoProstoMesto]][i] = self.tabela[j][i]
                            self.tabela[j][i] = 0
                            prostaMesta.append(j)
                            prvoSeVednoProstoMesto += 1
                    aliSeJeKateriPremaknil = True
        return aliSeJeKateriPremaknil
    
    def premakniDesno(self):
        aliSeJeKateriPremaknil = False
        for i in range(self.velikost):
            prostaMesta = []
            prvoSeVednoProstoMesto = 0
            for j in range(self.velikost - 1, -1, -1):
                if self.tabela[i][j] == 0:
                    prostaMesta.append(j)
                elif len(prostaMesta) != 0:
                    if prostaMesta[prvoSeVednoProstoMesto] == self.velikost - 1:
                        self.tabela[i][self.velikost - 1] = self.tabela[i][j]
                        self.tabela[i][j] = 0
                        prostaMesta.append(j)
                        prvoSeVednoProstoMesto += 1
                    else:
                        if self.tabela[i][prostaMesta[prvoSeVednoProstoMesto] + 1] == self.tabela[i][j]:
                            self.tabela[i][prostaMesta[prvoSeVednoProstoMesto] + 1] *= 2
                            self.tabela[i][j] = 0
                            prostaMesta.append(j)
                        else:
                            self.tabela[i][prostaMesta[prvoSeVednoProstoMesto]] = self.tabela[i][j]
                            self.tabela[i][j] = 0
                            prostaMesta.append(j)
                            prvoSeVednoProstoMesto += 1
                aliSeJeKateriPremaknil = True
        return aliSeJeKateriPremaknil
    
    def premakniDol(self):
        aliSeJeKateriPremaknil = False
        for i in range(self.velikost):
            prostaMesta = []
            prvoSeVednoProstoMesto = 0
            for j in range(self.velikost - 1, -1, -1):
                if self.tabela[j][i] == 0:
                    prostaMesta.append(j)
                elif len(prostaMesta) != 0:
                    if prostaMesta[prvoSeVednoProstoMesto] == self.velikost - 1:
                        self.tabela[self.velikost - 1][i] = self.tabela[j][i]
                        self.tabela[j][i] = 0
                        prostaMesta.append(j)
                        prvoSeVednoProstoMesto += 1
                    else:
                        if self.tabela[prostaMesta[prvoSeVednoProstoMesto] + 1][i] == self.tabela[j][i]:
                            self.tabela[prostaMesta[prvoSeVednoProstoMesto] + 1][i] *= 2
                            self.tabela[j][i] = 0
                            prostaMesta.append(j)
                        else:
                            self.tabela[prostaMesta[prvoSeVednoProstoMesto]][i] = self.tabela[j][i]
                            self.tabela[j][i] = 0
                            prostaMesta.append(j)
                            prvoSeVednoProstoMesto += 1
                aliSeJeKateriPremaknil = True
        return aliSeJeKateriPremaknil

    def konecIgre(self):
        kopija = Igra(self.velikost, self.tabela)

        if kopija.premakniDesno() == False and kopija.premakniLevo() == False \
            and kopija.premakniGor() == False and kopija.premakniDol() == False:
            return True
    
    def premakni(self, smer):
        if smer == GOR:
            self.premakniGor()
        elif smer == DOL:
            self.premakniDol()
        elif smer == DESNO:
            self.premakniDesno()
        elif smer == LEVO:
            self.premakniLevo()
        
        if self.konecIgre():
            return KONEC_IGRE

def nova_igra(velikost):
    return Igra(velikost)