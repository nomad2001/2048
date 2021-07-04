import random
import json
import copy
import hashlib

GOR = 'U'
DOL = 'D'
LEVO = 'L'
DESNO = 'R'
KONEC_IGRE = 'E'
NEOBSTOJECA_SMER = 'N'

DATOTEKA_ZA_SHRANJEVANJE = "podatki.json"
DATOTEKA_ZA_UPORABNIKE = "uporabniki.json"

class Uporabniki:
    def __init__(self, uporabniki = None):
        self.uporabniki = uporabniki or {}

    def zapisi_v_datoteko(self, datoteka):
        json_slovar = {}

        for ime, uporabnik in self.uporabniki.items():
            json_slovar[ime] = uporabnik.v_slovar()

        with open(datoteka, "w") as out_file:
            json.dump(json_slovar, out_file)
    
    @staticmethod
    def preberi_iz_datoteke(datoteka):
        with open(datoteka, "r") as in_file:
            json_slovar = json.load(in_file)

        uporabniki = {}
        
        for ime, slovar in json_slovar.items():
            uporabniki[ime] = Uporabnik.iz_slovarja(slovar)
        
        return Uporabniki(uporabniki)

class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, najboljsi_rezultat):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.najboljsi_rezultat = najboljsi_rezultat
    
    @staticmethod
    def prijava(uporabnisko_ime, geslo_v_cistopisu):
        uporabniki = Uporabniki.preberi_iz_datoteke(DATOTEKA_ZA_UPORABNIKE).uporabniki
        if uporabniki[uporabnisko_ime] is None:
            raise ValueError("Uporabniško ime ne obstaja")
        elif uporabniki[uporabnisko_ime].preveri_geslo(geslo_v_cistopisu):
            return uporabniki[uporabnisko_ime]        
        else:
            raise ValueError("Geslo je napačno")

    @staticmethod
    def registracija(uporabnisko_ime, geslo_v_cistopisu):
        if Uporabniki.preberi_iz_datoteke(DATOTEKA_ZA_UPORABNIKE)[uporabnisko_ime] is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            zasifrirano_geslo = Uporabnik._zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, 0)
            return uporabnik

    def _zasifriraj_geslo(geslo_v_cistopisu, sol = None):
        if sol is None:
            sol = str(random.getrandbits(32))
        posoljeno_geslo = sol + geslo_v_cistopisu
        h = hashlib.blake2b()
        h.update(posoljeno_geslo.encode(encoding="utf-8"))
        return f"{sol}${h.hexdigest()}"

    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "najboljsi_rezultat": self.najboljsi_rezultat,
        }

    def preveri_geslo(self, geslo_v_cistopisu):
        sol, _ = self.zasifrirano_geslo.split("$")
        return self.zasifrirano_geslo == Uporabnik._zasifriraj_geslo(geslo_v_cistopisu, sol)

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        najboljsi_rezultat = slovar["najboljsi_rezultat"]
        return Uporabnik(uporabnisko_ime, zasifrirano_geslo, najboljsi_rezultat)

def generirarajNakljucnoPozicijoInStevilo(velikost, tabela):
    stProstihMest = 0

    for i in range(velikost):
        for j in range(velikost):
            if tabela[i][j] == 0:
                stProstihMest += 1
    
    if stProstihMest == 0:
        return
    
    poVrstiProst = random.randrange(stProstihMest) + 1

    for i in range(velikost):
        for j in range(velikost):
            if tabela[i][j] == 0:
                poVrstiProst -= 1
                if poVrstiProst == 0:
                    x = i
                    y = j
                    break
        
    kateroNovoStevilo = random.randrange(10)

    if kateroNovoStevilo % 5 == 0:
        tabela[x][y] = 4
    else:
        tabela[x][y] = 2

class Glavno:
    def __init__(self, zacetne_igre = None):
        self.igre = zacetne_igre or {}

    def nova_igra(self, uporabnik, velikost):
        sveza_igra = nova_igra(velikost)
        self.igre[uporabnik.uporabnisko_ime] = sveza_igra
        return uporabnik
    
    def premakni(self, uporabnik, smer):
        igra = self.igre[uporabnik.uporabnisko_ime]
        igra.premakni(smer)

        if igra.steviloTock > uporabnik.najboljsi_rezultat:
            uporabnik.najboljsi_rezultat = igra.steviloTock

        self.igre[uporabnik.uporabnisko_ime] = igra
    
    def pretvor_v_json_slovar(self):
        slovar_iger = {}

        for uporabnisko_ime, igra in self.igre.items():
            slovar_iger[uporabnisko_ime] = igra.pretvor_v_json_slovar()

        return slovar_iger
    
    def zapisi_v_datoteko(self, datoteka):
        with open(datoteka, "w") as out_file:
            json_slovar = self.pretvor_v_json_slovar()
            json.dump(json_slovar, out_file)
    
    @classmethod
    def dobi_iz_json_slovarja(cls, slovar):
        slovar_iger = {}

    #    if len(slovar) == 0:
     #       return Glavno(slovar_iger, 0)

        for uporabnisko_ime, igra_slovar in slovar.items():
            slovar_iger[uporabnisko_ime] = Igra.dobi_iz_json_slovarja(igra_slovar)

        return Glavno(slovar_iger)
    
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
                        self.steviloTock += 2 * self.tabela[i][j - 1]
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
                        self.steviloTock += 2 * self.tabela[j - 1][i]
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
                        self.steviloTock += 2 * self.tabela[i][j + 1]
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
                        self.steviloTock += 2 * self.tabela[j + 1][i]
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
        return Igra(slovar["velikost"], slovar["tabela"], slovar["tocke"])
    
def nova_igra(velikost):
    return Igra(velikost)