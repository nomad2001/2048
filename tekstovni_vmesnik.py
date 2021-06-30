import model

def izpis_igre(igra):
    izpis = igra.velikost * '-' + '\n'

    for i in range(igra.velikost):
        for j in range(igra.velikost):
            izpis += '|' + str(igra.tabela[i][j])
        izpis += '|\n'
    
    izpis += igra.velikost * '-' + '\n'
    return izpis

def izpis_konca_igre(igra):
    return f'Igra je končana. Ne moreš več narediti nobene poteze. Dosegel si {igra.steviloTock} točk.'

def zahtevaj_vnos():
    return input("Smer: ")