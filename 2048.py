import bottle
import model
import pygame #ali lahko uporabim pygame?

glavno = model.Glavno()
COOKIE_SECRET="bnupičgtfhg9rp8gret934t57thzergurg48thfrhreh8"

@bottle.route("/views/<file_path:path>")
def return_static(file_path):
    return bottle.static_file(file_path,"views")

@bottle.get("/")
def index():
    return bottle.template("index.html")

@bottle.get("/igra/")
def pred_novo_igro():
    id_igre = glavno.nova_igra(4)
    bottle.redirect("/igraj/")

#@bottle.post("/igra/")
#def nova_igra():
 #   id_igre = glavno.nova_igra(4)
  #  bottle.redirect("/igraj/")

@bottle.get("/igraj/")
def igra():
    id_igre = 1
    return bottle.template("igra.html", tabela = glavno.igre[id_igre].tabela, \
                    stTock = glavno.igre[id_igre].steviloTock)

@bottle.post("/igraj/")
def igraj():
    pritiski = pygame.event.get()    
    id_igre = 1

    for smer in pritiski:
        if smer.type == pygame.KEYDOWN:
            if smer.key == pygame.K_LEFT:
                glavno.premakni(id_igre, 'L')
            elif smer.key == pygame.K_RIGHT:
                glavno.premakni(id_igre, 'R')
            elif smer.key == pygame.K_UP:
                glavno.premakni(id_igre, 'U')
            elif smer.key == pygame.K_DOWN:
                glavno.premakni(id_igre, 'D')
            else:
                glavno.premakni(id_igre) #tu dodaj opozorilo za neveljaven ukaz

    bottle.redirect("/igraj/")

bottle.run(reloader=True, debug=True)