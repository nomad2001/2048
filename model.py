from random import randrange
import json
import copy

GOR = 'U'
DOL = 'D'
LEVO = 'L'
DESNO = 'R'
KONEC_IGRE = 'E'
NEOBSTOJECA_SMER = 'N'

DATOTEKA_ZA_SHRANJEVANJE = "podatki.json"

def generirarajNakljucnoPozicijoInStevilo(velikost, tabela):
    obstajaProstoMesto = False

    for i in range(velikost):
        for j in range(velikost):
            if tabela[i][j] == 0:
                obstajaProstoMesto = True
                break
    
    if not obstajaProstoMesto:
        return
    
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

class Glavno:
    def __init__(self, zacetne_igre=None, zacetni_id=0):
        self.igre = zacetne_igre or {}
        self.max_id = zacetni_id
    
    def prost_id_igre(self):
        self.max_id += 1
        return self.max_id

    def nova_igra(self, velikost):
        nov_id = self.prost_id_igre()
        sveza_igra = nova_igra(velikost)

        self.igre[nov_id] = sveza_igra
        return nov_id
    
    def premakni(self, id_igre, smer):
        igra = self.igre[id_igre]
        igra.premakni(smer)
        self.igre[id_igre] = igra
    
    def pretvor_v_json_slovar(self):
        slovar_iger = {}

        for id_igre, igra in self.igre.items():
            slovar_iger[id_igre] = igra.pretvor_v_json_slovar()

        return {
            "max_id": self.max_id,
            "igre": slovar_iger
        }
    
    def zapisi_v_datoteko(self, datoteka):
        with open(datoteka, "w") as out_file:
            json_slovar = self.pretvor_v_json_slovar()
            json.dump(json_slovar, out_file)
    
    @classmethod
    def dobi_iz_json_slovarja(cls, slovar):
        slovar_iger = {}

        for id_igre, igra_slovar in slovar["igre"].items():
            slovar_iger[int(id_igre)] = Igra.dobi_iz_json_slovarja(igra_slovar)

        return Glavno(slovar_iger,slovar["max_id"])
    
    @staticmethod
    def preberi_iz_datoteke(datoteka):
        with open(datoteka, "r") as in_file:
            json_slovar = json.load(in_file)
        return Glavno.dobi_iz_json_slovarja(json_slovar)

class Igra:
    def __init__(self, velikost = 4, tabela = None, steviloTock = 0):
        self.velikost = velikost
        self.steviloTock = steviloTock

        if tabela == None:
            self.tabela = [[0 for i in range(velikost)] for i in range(velikost)]
            generirarajNakljucnoPozicijoInStevilo(self.velikost,self.tabela)
            generirarajNakljucnoPozicijoInStevilo(self.velikost,self.tabela)
        else:
            self.tabela = tabela
    
    def premakniLevo(self):
        zeSestet = [[False for i in range(self.velikost)] for i in range(self.velikost)]
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
                        if self.tabela[i][prostaMesta[prvoSeVednoProstoMesto] - 1] == self.tabela[i][j] \
                            and not zeSestet[i][prostaMesta[prvoSeVednoProstoMesto] - 1]:
                            self.steviloTock += 2 * self.tabela[i][j]
                            self.tabela[i][prostaMesta[prvoSeVednoProstoMesto] - 1] *= 2
                            self.tabela[i][j] = 0
                            zeSestet[i][prostaMesta[prvoSeVednoProstoMesto] - 1] = True
                            prostaMesta.append(j)
                        else:
                            self.tabela[i][prostaMesta[prvoSeVednoProstoMesto]] = self.tabela[i][j]
                            self.tabela[i][j] = 0
                            prostaMesta.append(j)
                            prvoSeVednoProstoMesto += 1
                    aliSeJeKateriPremaknil = True
                elif j != 0:
                    if self.tabela[i][j] == self.tabela[i][j - 1]:
                        self.tabela[i][j - 1] *= 2
                        self.tabela[i][j] = 0
                        zeSestet[i][j - 1] = True
                        prostaMesta.append(j)
                        aliSeJeKateriPremaknil = True
        return aliSeJeKateriPremaknil
        
    def premakniGor(self):
        zeSestet = [[False for i in range(self.velikost)] for i in range(self.velikost)]
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
                        if self.tabela[prostaMesta[prvoSeVednoProstoMesto] - 1][i] == self.tabela[j][i] \
                            and not zeSestet[prostaMesta[prvoSeVednoProstoMesto] - 1][i]:
                            self.steviloTock += 2 * self.tabela[j][i]
                            self.tabela[prostaMesta[prvoSeVednoProstoMesto] - 1][i] *= 2
                            self.tabela[j][i] = 0
                            zeSestet[prostaMesta[prvoSeVednoProstoMesto] - 1][i] = True
                            prostaMesta.append(j)
                        else:
                            self.tabela[prostaMesta[prvoSeVednoProstoMesto]][i] = self.tabela[j][i]
                            self.tabela[j][i] = 0
                            prostaMesta.append(j)
                            prvoSeVednoProstoMesto += 1
                    aliSeJeKateriPremaknil = True
                elif j != 0:
                    if self.tabela[j][i] == self.tabela[j - 1][i]:
                        self.tabela[j - 1][i] *= 2
                        self.tabela[j][i] = 0
                        zeSestet[j - 1][i] = True
                        prostaMesta.append(j)
                        aliSeJeKateriPremaknil = True
        return aliSeJeKateriPremaknil
    
    def premakniDesno(self):
        zeSestet = [[False for i in range(self.velikost)] for i in range(self.velikost)]
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
                        if self.tabela[i][prostaMesta[prvoSeVednoProstoMesto] + 1] == self.tabela[i][j] \
                            and not zeSestet[i][prostaMesta[prvoSeVednoProstoMesto] + 1]:
                            self.steviloTock += 2 * self.tabela[i][j]
                            self.tabela[i][prostaMesta[prvoSeVednoProstoMesto] + 1] *= 2
                            self.tabela[i][j] = 0
                            zeSestet[i][prostaMesta[prvoSeVednoProstoMesto] + 1] = True
                            prostaMesta.append(j)
                        else:
                            self.tabela[i][prostaMesta[prvoSeVednoProstoMesto]] = self.tabela[i][j]
                            self.tabela[i][j] = 0
                            prostaMesta.append(j)
                            prvoSeVednoProstoMesto += 1
                    aliSeJeKateriPremaknil = True
                elif j != self.velikost - 1:
                    if self.tabela[i][j] == self.tabela[i][j + 1]:
                        self.tabela[i][j + 1] *= 2
                        self.tabela[i][j] = 0
                        zeSestet[i][j + 1] = True
                        prostaMesta.append(j)
                        aliSeJeKateriPremaknil = True
        return aliSeJeKateriPremaknil
    
    def premakniDol(self):
        zeSestet = [[False for i in range(self.velikost)] for i in range(self.velikost)]
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
                        if self.tabela[prostaMesta[prvoSeVednoProstoMesto] + 1][i] == self.tabela[j][i] \
                            and not zeSestet[prostaMesta[prvoSeVednoProstoMesto] + 1][i]:
                            self.steviloTock += 2 * self.tabela[j][i]
                            self.tabela[prostaMesta[prvoSeVednoProstoMesto] + 1][i] *= 2
                            self.tabela[j][i] = 0
                            zeSestet[prostaMesta[prvoSeVednoProstoMesto] + 1][i] = True
                            prostaMesta.append(j)
                        else:
                            self.tabela[prostaMesta[prvoSeVednoProstoMesto]][i] = self.tabela[j][i]
                            self.tabela[j][i] = 0
                            prostaMesta.append(j)
                            prvoSeVednoProstoMesto += 1
                    aliSeJeKateriPremaknil = True
                elif j != self.velikost - 1:
                    if self.tabela[j][i] == self.tabela[j + 1][i]:
                        self.tabela[j + 1][i] *= 2
                        self.tabela[j][i] = 0
                        zeSestet[j + 1][i] = True
                        prostaMesta.append(j)
                        aliSeJeKateriPremaknil = True
        return aliSeJeKateriPremaknil

    def konecIgre(self):
        kopija = copy.deepcopy(self)

        if kopija.premakniDesno() == False and kopija.premakniLevo() == False \
            and kopija.premakniGor() == False and kopija.premakniDol() == False:
            return True
        
        return False
    
    def premakni(self, smer):
        if smer == GOR:
            if self.premakniGor():
                generirarajNakljucnoPozicijoInStevilo(self.velikost, self.tabela)
        elif smer == DOL:
            if self.premakniDol():
                generirarajNakljucnoPozicijoInStevilo(self.velikost, self.tabela)
        elif smer == DESNO:
            if self.premakniDesno():
                generirarajNakljucnoPozicijoInStevilo(self.velikost, self.tabela)
        elif smer == LEVO:
            if self.premakniLevo():
                generirarajNakljucnoPozicijoInStevilo(self.velikost, self.tabela)
        else:
            return NEOBSTOJECA_SMER
        
        if self.konecIgre():
            return KONEC_IGRE
    
    def pretvor_v_json_slovar(self):
        return {
            "tocke": self.steviloTock,
            "velikost": self.velikost,
            "tabela": self.tabela
        }

    @staticmethod
    def dobi_iz_json_slovarja(slovar):
        return Igra(slovar["tocke"], slovar["velikost"], slovar["tabela"])
    
def nova_igra(velikost):
    return Igra(velikost)