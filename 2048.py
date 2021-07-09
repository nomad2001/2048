import bottle
import model
from pynput import keyboard

igreRazred = model.IgreRazred()
uporabnikiRazred = model.UporabnikiRazred()
prijavaPoRegistraciji = False
prijavaPoOdjavi = False

with open('sifra.txt') as datoteka:
    COOKIE_SECRET = datoteka.read()

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=COOKIE_SECRET
    )

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
    global prijavaPoRegistraciji
    global prijavaPoOdjavi
    if prijavaPoRegistraciji:
        prijavaPoRegistraciji = False
        return bottle.template("prijava.html", napaka = 0)
    elif prijavaPoOdjavi:
        prijavaPoOdjavi = False
        return bottle.template("prijava.html", napaka = 2)
    else:
        return bottle.template("prijava.html", napaka = 3)

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
        return bottle.template("prijava.html", napaka = 1)

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
        uporabnikiRazred = model.UporabnikiRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
        uporabnikiRazred.uporabniki[uporabnik.uporabnisko_ime] = uporabnik
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        global prijavaPoRegistraciji
        prijavaPoRegistraciji = True
        bottle.redirect("/prijava/")
    except ValueError:
        return bottle.template("registracija.html", napaka = 2)

@bottle.post("/odjava/")
def odjava():
    global prijavaPoOdjavi
    prijavaPoOdjavi = True
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")

@bottle.get("/igra/")
def pred_igro():
    uporabnisko_ime = trenutni_uporabnik()
    igreRazred = model.IgreRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)

    if uporabnisko_ime in igreRazred.igre.keys():
        return bottle.template("index.html", obstaja = True)
    else:
        return bottle.template("index.html", obstaja = False)

@bottle.post("/igra/")
def nova_igra():
    uporabnisko_ime = trenutni_uporabnik()
    igreRazred = model.IgreRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.UporabnikiRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
    velikost = int(bottle.request.forms.get("velikost"))
    igreRazred.nova_igra(uporabnikiRazred.uporabniki[uporabnisko_ime], velikost)
    igreRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/igraj/")

@bottle.get("/igra/izbira_velikosti/")
def izbira_velikosti():
    return bottle.template("izbira_velikosti.html")

def on_press(key):
    try:
        k = key.char
    except:
        k = key.name
    
    if k in ['left', 'right', 'up', 'down', 'enter']:
        return False  

def dobi_smer():
    listener = keyboard.Listener(on_press = on_press)
    listener.start()
    listener.join()
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.left:
                return model.LEVO
            elif event.key == keyboard.Key.right:
                return model.DESNO   
            elif event.key == keyboard.Key.up:
                return model.GOR      
            elif event.key == keyboard.Key.down:
                return model.DOL
            elif event.key == keyboard.Key.enter:
                return model.NEOBSTOJECA_SMER

@bottle.get("/igraj/")
def pokazi_igro():
    uporabnisko_ime = trenutni_uporabnik()
    igreRazred = model.IgreRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.UporabnikiRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)

    if igreRazred.igre[uporabnisko_ime].konecIgre():
        return bottle.redirect("/konec/")
    else:
        return bottle.template("igra.html", tabela = igreRazred.igre[uporabnisko_ime].tabela, \
                        stTock = igreRazred.igre[uporabnisko_ime].steviloTock, \
maxStTock = uporabnikiRazred.uporabniki[uporabnisko_ime].najboljsi_rezultati[str(igreRazred.igre[uporabnisko_ime].velikost)], \
                                velikost = igreRazred.igre[uporabnisko_ime].velikost)

@bottle.post("/igraj/")
def igraj():
    uporabnisko_ime = trenutni_uporabnik()
    igreRazred = model.IgreRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.UporabnikiRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)

    smer = dobi_smer()

    if igreRazred.premakni(uporabnikiRazred.uporabniki[uporabnisko_ime], smer):
        igreRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/konec/")
    else:
        igreRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
        uporabnikiRazred.zapisi_v_datoteko(model.DATOTEKA_ZA_UPORABNIKE)
        bottle.redirect("/igraj/")
    
@bottle.get("/konec/")
def konec_izgled():
    uporabnisko_ime = trenutni_uporabnik()
    igreRazred = model.IgreRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_SHRANJEVANJE)
    uporabnikiRazred = model.UporabnikiRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
    
    return bottle.template("konec.html", tabela = igreRazred.igre[uporabnisko_ime].tabela, \
                    stTock = igreRazred.igre[uporabnisko_ime].steviloTock, \
                        maxStTock = uporabnikiRazred.uporabniki[uporabnisko_ime].najboljsi_rezultati[str(igreRazred.igre[uporabnisko_ime].velikost)], \
                                velikost = igreRazred.igre[uporabnisko_ime].velikost)

@bottle.get("/lestvica/")
def izberi_velikost_lestvice():
    return bottle.template("izberi_velikost_lestvice.html")

@bottle.get("/lestvica/<velikost>/<zacetek:int>-<konec:int>/")
def lestvica(velikost, zacetek, konec):
    uporabnisko_ime = trenutni_uporabnik()
    uporabnikiRazred = model.UporabnikiRazred.preberi_iz_datoteke(model.DATOTEKA_ZA_UPORABNIKE)
    lestvica = uporabnikiRazred.dobi_lestvico(velikost)
    trenutnoMesto = lestvica.index((uporabnisko_ime, 
                        uporabnikiRazred.uporabniki[uporabnisko_ime].najboljsi_rezultati[str(velikost)]))
    return bottle.template(
        "lestvica.html", zacetek = zacetek, konec = konec, lestvica = lestvica, mesto = trenutnoMesto + 1,
                        velikost = velikost
        )

bottle.run(reloader=True, debug=True)