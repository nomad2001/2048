import model

def izpis_igre(igra):
    izpis = igra.velikost * ' -' + '\n'

    for i in range(igra.velikost):
        for j in range(igra.velikost):
            izpis += '|' + str(igra.tabela[i][j])
        izpis += '|\n'
    
    izpis += igra.velikost * ' -' + '\n'
    return izpis

def izpis_konca_igre(igra):
    return f'Igra je končana. Ne moreš več narediti nobene poteze. Dosegel si {igra.steviloTock} točk.'

def zahtevaj_smer():
    return input("Smer: ")

def zahtevaj_velikost():
    return int(input("Velikost tabele: "))

def izpis_neobstojece_smeri(smer):
    return f'Ukaz {smer} je neveljaven, saj ne obstaja smer {smer}. Ponovno vnesite smer.'

def pozeni_vmesnik():
    igra = model.nova_igra(zahtevaj_velikost())

    while True:
        print(izpis_igre(igra))
        smer = zahtevaj_smer()
        stanje = igra.premakni(smer)

        if stanje == model.KONEC_IGRE:
            print(izpis_konca_igre(igra))
            break
        elif stanje == model.NEOBSTOJECA_SMER:
            print(izpis_neobstojece_smeri(smer))

pozeni_vmesnik()