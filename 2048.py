import bottle
import model
import pygame #ali lahko uporabim pygame?

glavno = model.Glavno()
COOKIE_SECRET="bnupičgtfhg9rp8gret934t57thzergurg48thfrhreh8"

@bottle.route('/views/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root = '/views')

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
    return bottle.template("igra.html", tabela = glavno.igre[id_igre].tabela)

@bottle.post("/igraj/")
def igraj():
    smer = pygame.key.get_pressed()
    id_igre = 1

    if smer[pygame.K_LEFT]:
        glavno.premakni(id_igre, 'L')
    elif smer[pygame.K_RIGHT]:
        glavno.premakni(id_igre, 'R')
    elif smer[pygame.K_UP]:
        glavno.premakni(id_igre, 'U')
    elif smer[pygame.K_DOWN]:
        glavno.premakni(id_igre, 'D')
    else:
        glavno.premakni(id_igre) #tu dodaj opozorilo za neveljaven ukaz

    bottle.redirect("/igraj/")

bottle.run(reloader=True, debug=True)