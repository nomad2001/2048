# 2048

## Avtor

* Matija Kocbek
* Gabriele Cirulli (avtor originalne igre 2048, od katere je vzeta osnovna predloga v HTML in CSS)

## Kratek opis

Igra 2048 je preplavila svet leta 2014. Igra se igra tako, da se po tabeli
premikajo ploščice številk v različnih smereh. Enaki številki, če ni nobene 
druge številke med njima, se seštejeta v svojega dvakratnika in združita v 
eno ploščico. Če uspeš sestaviti blok s številko 2048 si zmagal. Tudi po zmagi 
pa lahko igro nadaljuješ in poskusiš sestaviti bloke s čim večjimi številkami 
(večjimi od 2048).

## Navodila za namestitev Pythona

Preden lahko začnete igrati igro 2048, morate imeti nameščen Python na svojem
računalniku. Pojdite na spletno stran https://www.python.org/downloads/ in 
sledite navodilom. V Python ni ob naložitvi vgrajena nobena knjižnica, ki zna 
spremljati, kaj vnašate s tipkovnico, zato morate dodato naložiti Pythonovo
knjižnico pynput. Odprite ukazni poziv (navodila za odpiranje glejte spodaj) in
vtipkajte ukaz "pip install pynput". S tem boste naložili potrebno knjižnico.

## Navodila za namestitev in zagon igre

Na vrhu github repozitorija je zeleni gumb z napisom "Code". Pritisnite nanj
in izberite "Download ZIP". Naložila se bo ZIP datoteka z imenom "2048-main".
Ekstrahirajte vse datoteke iz te ZIP datoteke v neko novo mapo. Ko odprete
novo mapo z ekstrahiranimi podatki, se bo pojavila mapa z imenom "2048-main".
Odprite tudi to mapo in kopirajte pot, do datotek, ki jih vidite (pot je
navadno prikazana pri vrhu okna z datotekami). Nato odprite ukazni poziv 
(navodila za odpiranje glejte spodaj) in vtipkajte ukaz "cd pot" (brez 
narekovajev), kjer je pot tista, ki ste jo pred tem kopirali. Pot, ki ste jo 
kopirali, lahko prilepite z zaporednim stiskom na tipke "CTRL" in "V". Nato 
pritisnite "ENTER". Ko ste s tem končali, vtipkajte še ukaz "2048.py" in pritisnite "ENTER". Povezavo, ki se prikaže (podobna mora biti http://127.0.0.1:8080/), prepišite v okence 
za iskanje v svojem spletnem brskalniku. Odprlo se bo okno s prijavo.

## Navodila za uporabo spletnega vmesnika

Za uporabo spletnega vmesnika računalniške igre 2048 je potrebna predhodna
registracija. Ko ste registrirani, se lahko prijavite in igrate igro.

Ko se prijavite, lahko izbirate, ali boste začeli novo igro ali pa nadaljevali
zadnjo, ki ste jo igrali (nadaljevanje igre je možno le, če ste že kdaj prej
igrali to igro). Ob vsakem začetku nove igre morate tudi izbrati velikost tabele,
na kateri želite igrati.

Ko začnete igrati, poskusite zbrati čim več točk. Dobite jih tako, da s puščicami
na tipkovnici izberete smer, v katero želite, da se vse ploščice na tabeli
premaknejo. Če v izbrani smeri med dvema ploščicama z enakima številkama ni nobene
druge ploščice, se ploščici združita v eno ploščico z dvakrat večjo številko. 
Vrednost nove ploščice se pribije k vašemu skupnemu številu točk.

V vsakem trenutku lahko trenutno igro prekinete in začnete novo igro. Prav tako
lahko dostopate do lestvice uspešnosti in se primerjate z drugimi uporabniki.

## Opomba

Takoj, ko naložite igro, so že dodani nekateri izmišljeni uporabniki in njihovi
rezultati, da bi lahko videli, kako deluje lestvica. Če želite pobrisati te 
uporabnike in rezultate, odprite datoteki "uporabniki.json" in "podatki.json" 
v mapi, ki ste jo dobili z ekstrahiranjem. Iz teh datotek pobrišite vse podatke 
in pustite v njiju le niz "{}" (brez narekovajev).

## Navodila za odpiranje ukaznega poziva

* Če uporabljate Windows, ga zaženete tako, da pritisnete skupaj Windows tipko 
in tipko "R", nato pa v okencu, ki se pojavi, vtipkate "cmd" in stisnete tipko "ENTER".
* Če uporabljate MacOS, pritisnite skupaj "command" tipko in tipko za presledek. V okencu,
ki se pojavi, vtipkajte "terminal" in izberite možnost "Terminal".
* Če uporabljate Linux, lahko odprete ukazni poziv s hitrim zaporednim pritiskom na
tipke "CTRL", "ALT" in  "T".