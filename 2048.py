import bottle
import model
#import pygame #ali lahko uporabim pygame?
from pynput import keyboard

glavno = model.Glavno()
uporabnikiRazred = model.Uporabniki()

with open('sifra.txt') as datoteka:
    COOKIE_SECRET = datoteka.read()

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME,secret=COOKIE_SECRET
    )
    if not uporabnisko_ime:
        bottle.redirect("/prijava/")
    if uporabnisko_ime:
        return uporabnisko_ime
    else:
        bottle.redirect("/prijava/")


@bottle.route("/views/<file_path:path>")
def return_static(file_path):
    return bottle.static_file(file_path,"views")

@bottle.get("/")
def index():
    bottle.redirect("/prijava/")

@bottle.get("/prijava/")
def prijava_izgled():
    return bottle.template("prijava.html", napaka = False)

@bottle.post("/prijava/")
def prijava():
    uporabnisko_ime = bottle.request.forms.getunicode("ime")
    geslo = bottle.request.forms.getunicode("geslo")

    try:
        model.Uporabnik.prijava(uporabnisko_ime, geslo)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=COOKIE_SECRET
        )
        bottle.redirect("/igra/")
    except ValueError:
        return bottle.template("prijava.html", napaka = True)

@bottle.get("/registracija/")
def registracija_izgled():
    return bottle.template("registracija.html", napaka = 0)

@bottle.post("/registracija/")
def registracija():
    uporabnisko_ime = bottle.request.forms.getunicode("ime")
    geslo1 = bottle.request.forms.getunicode("geslo")
    geslo2 = bottle.request.forms.getunicode("ponovno_geslo")

    if geslo1 != geslo2:
        return bottle.template("registracija.html", napaka = 1)
    
    try:
        uporabnik = model.Uporabnik.registracija(uporabnisko_ime, geslo1)
        uporabnikiRazred = model.Uporabniki.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
        uporabnikiRazred.uporabniki[uporabnik.uporabnisko_ime] = uporabnik
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/prijava/")
    except ValueError:
        return bottle.template("registracija.html", napaka = 2)

@bottle.get("/igra/")
def pred_igro():
    uporabnisko_ime = trenutni_uporabnik()
    uporabnikiRazred = model.Uporabniki.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
    return bottle.template(
        "index.html", maxTocke = uporabnikiRazred.uporabniki[uporabnisko_ime].najboljsi_rezultat
        )

@bottle.post("/igra/")
def nova_igra():
    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.Uporabniki.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
    uporabnisko_ime = trenutni_uporabnik()
    glavno.nova_igra(uporabnikiRazred.uporabniki[uporabnisko_ime], 4)
    glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/igraj/")

#def dobi_smer():
 #   pygame.init()
  #  while True:
   #     pygame.event.wait()
    #    for dogodek in pygame.event.get():
     #       if dogodek.type == pygame.KEYDOWN:
      #          return dogodek

def on_press(key):
    try:
        k = key.char
    except:
        k = key.name
    if k in ['left', 'right', 'up', 'down']:
        print('Key pressed: ' + k)
        return False  

def dobi_smer():
    listener = keyboard.Listener(on_press = on_press)
    listener.start()
    #listener.join()
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.left:
                return 'L'
            elif event.key == keyboard.Key.right:
                return 'R'    
            elif event.key == keyboard.Key.up:
                return 'U'        
            elif event.key == keyboard.Key.down:
                return 'D'

@bottle.get("/igraj/")
def pokazi_igro():
    uporabnisko_ime = trenutni_uporabnik()
    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.Uporabniki.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
   # glavno.premakni(uporabnikiRazred.uporabniki[uporabnisko_ime], dobi_smer())
   # glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)

    return bottle.template("igra.html", tabela = glavno.igre[uporabnisko_ime].tabela, \
                    stTock = glavno.igre[uporabnisko_ime].steviloTock, \
                        maxStTock = uporabnikiRazred.uporabniki[uporabnisko_ime].najboljsi_rezultat)

@bottle.post("/igraj/splosno/")
def igraj_splosno():
    uporabnisko_ime = trenutni_uporabnik()
    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.Uporabniki.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)

    if glavno.premakni(uporabnikiRazred.uporabniki[uporabnisko_ime], dobi_smer()):
        glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/konec/")
    else:
        glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/igraj/")
    
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

@bottle.post("/igraj/levo/")
def igrajLevo():
    uporabnisko_ime = trenutni_uporabnik()
    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.Uporabniki.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)

    if glavno.premakni(uporabnikiRazred.uporabniki[uporabnisko_ime], 'L'):
        glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/konec/")
    else:
        glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/igraj/")

@bottle.post("/igraj/desno/")
def igrajDesno():
    uporabnisko_ime = trenutni_uporabnik()
    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.Uporabniki.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
    if glavno.premakni(uporabnikiRazred.uporabniki[uporabnisko_ime], 'R'):
        glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/konec/")
    else:
        glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/igraj/")

@bottle.post("/igraj/dol/")
def igrajDol():
    uporabnisko_ime = trenutni_uporabnik()
    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.Uporabniki.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)

    if glavno.premakni(uporabnikiRazred.uporabniki[uporabnisko_ime], 'D'):
        glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/konec/")
    else:
        glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/igraj/")

@bottle.post("/igraj/gor/")
def igrajGor():
    uporabnisko_ime = trenutni_uporabnik()
    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.Uporabniki.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
    if glavno.premakni(uporabnikiRazred.uporabniki[uporabnisko_ime], 'U'):
        glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/konec/")
    else:
        glavno.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/igraj/")

@bottle.get("/konec/")
def konec_izgled():
    uporabnisko_ime = trenutni_uporabnik()
    glavno = model.Glavno.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.Uporabniki.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
    
    return bottle.template("konec.html", tabela = glavno.igre[uporabnisko_ime].tabela, \
                    stTock = glavno.igre[uporabnisko_ime].steviloTock, \
                        maxStTock = uporabnikiRazred.uporabniki[uporabnisko_ime].najboljsi_rezultat)

bottle.run(reloader=True, debug=True)