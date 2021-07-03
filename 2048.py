import bottle
import model
import pygame #ali lahko uporabim pygame?

glavno = model.Glavno()

with open('sifra.txt') as datoteka:
    COOKIE_SECRET = datoteka.read()

@bottle.route("/views/<file_path:path>")
def return_static(file_path):
    return bottle.static_file(file_path,"views")

@bottle.get("/")
def index():
    return bottle.template("index.html")

#@bottle.get("/igra/")
#def pred_novo_igro():
 #   return bottle.template("index.html")

@bottle.post("/igra/")
def nova_igra():
    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    id_igre = glavno.nova_igra(4)
    glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    bottle.response.set_cookie("ID_IGRE",str(id_igre),path="/",
        secret=COOKIE_SECRET)
    bottle.redirect("/igraj/")

@bottle.get("/igraj/")
def pokazi_igro():
    id_igre=int(
        bottle.request.get_cookie("ID_IGRE",secret=COOKIE_SECRET)
    )

    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)

    return bottle.template("igra.html", tabela = glavno.igre[id_igre].tabela, \
                    stTock = glavno.igre[id_igre].steviloTock)

def dobi_smer():
    pygame.init()
    while True:
        pygame.event.wait()
        for dogodek in pygame.event.get():
            if dogodek.type == pygame.KEYDOWN:
                return dogodek

#@bottle.post("/igraj/")
#def igraj():
#    id_igre=int(
#        bottle.request.get_cookie("ID_IGRE",secret=COOKIE_SECRET)
#    )

#    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
#    #pygame.init()
#    #pritiski = pygame.event.get()    
#    smer = dobi_smer()
#    
#    if smer.key == pygame.K_LEFT:
#        glavno.premakni(id_igre, 'L')
#    elif smer.key == pygame.K_RIGHT:
#        glavno.premakni(id_igre, 'R')
#    elif smer.key == pygame.K_UP:
#        glavno.premakni(id_igre, 'U')
#    elif smer.key == pygame.K_DOWN:
#        glavno.premakni(id_igre, 'D')
#    else:
#        glavno.premakni(id_igre) #tu dodaj opozorilo za neveljaven ukaz

    #for smer in pritiski:
        #if smer.type == pygame.KEYDOWN:
         #   if smer.key == pygame.K_LEFT:
          #      glavno.premakni(id_igre, 'L')
           # elif smer.key == pygame.K_RIGHT:
            #    glavno.premakni(id_igre, 'R')
        #    elif smer.key == pygame.K_UP:
         #       glavno.premakni(id_igre, 'U')
          #  elif smer.key == pygame.K_DOWN:
           #     glavno.premakni(id_igre, 'D')
           # else:
            #    glavno.premakni(id_igre) #tu dodaj opozorilo za neveljaven ukaz
    
#    glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
#    bottle.redirect("/igraj/")

@bottle.post("/igraj/levo")
def igraj():
    id_igre=int(
        bottle.request.get_cookie("ID_IGRE",secret=COOKIE_SECRET)
    )

    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    glavno.premakni(id_igre, 'L')
    glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/igraj/")

@bottle.post("/igraj/desno")
def igraj():
    id_igre=int(
        bottle.request.get_cookie("ID_IGRE",secret=COOKIE_SECRET)
    )

    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    glavno.premakni(id_igre, 'R')
    glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/igraj/")

@bottle.post("/igraj/dol")
def igraj():
    id_igre=int(
        bottle.request.get_cookie("ID_IGRE",secret=COOKIE_SECRET)
    )

    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    glavno.premakni(id_igre, 'D')
    glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/igraj/")

@bottle.post("/igraj/gor")
def igraj():
    id_igre=int(
        bottle.request.get_cookie("ID_IGRE",secret=COOKIE_SECRET)
    )

    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    glavno.premakni(id_igre, 'U')
    glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/igraj/")

bottle.run(reloader=True, debug=True)