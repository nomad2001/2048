import model

def izpis_igre(igra):
    izpis = igra.velikost * '-' + '\n'

    for i in range(igra.velikost):
        for j in range(igra.velikost):
            izpis += '|' + str(igra.tabela[i][j])
        izpis += '|\n'
    
    izpis += igra.velikost * '-' + '\n'
    return izpis