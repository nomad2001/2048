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
    return bottle.template("index.html")

@bottle.post("/igra/")
def nova_igra():
    id_igre = glavno.nova_igra()
    bottle.redirect("/igra/<id_igre>/")

@bottle.get("/igra/<id_igre>/")
def igra(id_igre):
    return bottle.template("igra.html", tabela = glavno[id_igre].tabela)

@bottle.post("/igra/<id_igre>/")
def igra(id_igre):
    smer = pygame.key.get_pressed()

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

    bottle.redirect("/igra/<id_igre>/")

bottle.run(reloader=True, debug=True)