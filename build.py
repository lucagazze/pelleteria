# -*- coding: utf-8 -*-
"""Landing de Pelletteria Facile: index.html + páginas legales.

Misma estructura que la landing de Chimica (studiofacile/chimica.html) con
estética propia de taller de cuero. Todo sale de la configuración de abajo:
cambiar el kit, el precio o el checkout es editar CONFIG y volver a correr.

Reglas de contenido:
- Toast de compras recientes (social proof toast) copiado de studiofacile.
- El kit son los 3 volúmenes PDF (Borse e Zaini, Portafogli, Cinture): 81 modelos.
  Solo se describe lo que está en los PDF. Todos los proyectos traen foto del
  modelo terminado y tavole; misure/materiali/minuteria/strumenti solo los más
  completos: no prometerlos «per ogni modello».
- Sin checkout la página sale con noindex y los botones van a #offerta.

    python -u build.py
"""
import html, json, math, os

QUI = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ CONFIG
SITO = "https://pelletteria.studiofacilebook.com"
# 17,00 desde el 02/10/2026, decision de Luca. Estaba en 19,90.
#
# EL NUMERO VIVE EN UN SOLO LUGAR y de aqui sale a las once partes de la
# pagina donde aparece: los cuatro botones, el bloque de la oferta, el
# resumen, el FAQ, el precio por modelo, el JSON-LD y el evento del
# pixel. Cambiarlo a mano en el HTML dejaria alguno viejo, y el que se
# queda viejo es siempre el que mira el comprador.
#
# TIENE QUE COINCIDIR CON EL CHECKOUT. El 02/10 la pagina decia 19,90 €
# y el checkout cobraba US$ 27: un 25 % mas, en el momento de pagar. Si
# el producto de Impultienda no se pasa a 17 €, este numero vuelve a
# mentir — y ahora miente mas barato, que es peor, porque el comprador
# descubre la diferencia recien con la tarjeta en la mano.
# 17,99 € desde el 02/10/2026. Paso por 19,90 → 17 → 17,99 el mismo dia:
# si vuelve a cambiar, se toca SOLO esta linea.
#
# La coma es la decimal italiana y asi se imprime en la pagina. Los usos
# que necesitan un numero la convierten solos: float("17,99") para el
# precio por modelo y value:17.99 para el evento del pixel.
# 19,90 € desde el 03/10/2026, pedido de Luca (antes 17,99).
PREZZO = "19,90"
CHECKOUT = "https://pelletteria.studiofacilebook.com/cassa"   # checkout propio (app), rewrite en vercel.json (10/10). Antes Impultienda.
PIXEL = "2855836794801494"   # pixel de Meta de Pelletteria Facile (28/09)
CLARITY = "ypv295hl4t"   # Microsoft Clarity (29/09)
EMAIL = "info@studiofacilebook.com"   # buzón de soporte (confirmar)
SOCIETA = "QUILLSTONE DIGITAL LLC"
INDIRIZZO = "1057 NW 136th Ave, Miami, FL 33182, Stati Uniti"
AGG = "27 settembre 2026"

# Los 3 volúmenes del kit (PDF en ../Ebooks). assets.py genera las portadas
# (img/copertine/<slug>.webp), las miniaturas (img/miniature/<slug>-NN.webp) y
# _modelli.json con el nombre de cada modelo. La numeración salta del 2 al 4: así vienen los PDF.
VOLUMI = [
    {"slug": "v1", "num": "1", "titolo": "Borse e Zaini", "breve": "borse e zaini",
     "sotto": "Borse, zaini e cartelle", "modelli": 39, "pagine": 671},
    {"slug": "v2", "num": "2", "titolo": "Portafogli", "breve": "portafogli, portacarte e portamonete",
     "sotto": "Portafogli, portacarte e portamonete", "modelli": 38, "pagine": 137},
    {"slug": "v4", "num": "4", "titolo": "Cinture", "breve": "cinture",
     "sotto": "Cinture in pelle", "modelli": 4, "pagine": 22},
]
with open(os.path.join(QUI, "_modelli.json"), encoding="utf-8") as _f:
    NOMI = json.load(_f)
for _v in VOLUMI:
    assert len(NOMI[_v["num"]]) == _v["modelli"], _v["titolo"]

# Galería con pestañas: páginas reales de algunos modelos
# (img/sfoglia/<slug>/<k>.webp, las genera assets.py). "n" = proyecto del Vol. 1; "mini" = miniatura de otro volumen.
SFOGLIA = [
    {"slug": "rosaleen", "breve": "Rosaleen", "tipo": "Zaino", "n": 1, "nome": "Zaino Rosaleen", "cat": "Zaini", "info": "29 pagine · 28 × 25 × 16 cm", "pagine": [
        ("Il modello finito", "Un modello, due colori: corallo e verde a contrasto."),
        ("Le misure", "28 × 25 × 16 cm, a zaino montato."),
        ("I materiali", "Pelle rigida da 1,6 mm, contrasto da 1,4–1,6 mm, cinghie da 2,8 mm."),
        ("La minuteria", "3 fibbie e 2 anelli a D da 20 mm."),
        ("Lo schema dei pezzi", "Tutti i pezzi in un colpo d'occhio, con le lettere di raccordo."),
        ("Tavola 1:1", "A grandezza naturale, con i fori di cucitura segnati.")]},
    {"slug": "bifold", "breve": "Bifold", "tipo": "Portafoglio", "mini": "img/miniature/v2-27.webp", "nome": "Portafoglio bifold classico", "cat": "Portafogli", "info": "volume Portafogli · 5 pagine", "pagine": [
        ("Il modello finito", "Bifold con tasche per carte, banconote e monete."),
        ("Tavola 1:1", "I pezzi grandi, con i fori di cucitura segnati."),
        ("Tavola 1:1", "Le tasche, pezzo per pezzo."),
        ("Tavola 1:1", "Gli ultimi pezzi, con il segno del bottone.")]},
    {"slug": "cintura-donna", "breve": "Cintura", "tipo": "Da donna", "mini": "img/miniature/v4-04.webp", "nome": "Cintura da donna", "cat": "Cinture", "info": "volume Cinture · larghezza 4 cm", "pagine": [
        ("La scheda del modello", "Larghezza 4 cm, lunghezza 103 cm: pelle da 2 mm e fibbia a rullo da 40 mm."),
        ("Tavola 1:1 · 40 mm", "Le estremità della cintura, con i fori di cucitura."),
        ("Tavola 1:1 · 38 mm", "La variante da 1,5 pollici (circa 3,8 cm).")]},
    {"slug": "aria", "breve": "Aria", "tipo": "Borsa a secchiello", "n": 16, "nome": "Secchiello Aria", "cat": "Borse", "info": "23 pagine · 26 × 20,5 × 14 cm", "pagine": [
        ("Il modello finito", "Secchiello in pelle bianca con dettagli a contrasto."),
        ("Le misure", "26 × 20,5 × 14 cm."),
        ("I materiali", "Circa 0,5 m² di pelle da 1,8 mm e contrasto da 1 mm."),
        ("La minuteria", "2 bottoni Sam Browne e 4 anelli a D da 20 mm."),
        ("Lo schema dei pezzi", "Ogni pezzo della borsa, prima di tagliare."),
        ("Tavola 1:1", "Corpo e cinghie, con i fori già segnati.")]},
    {"slug": "borsone", "breve": "Borsone", "tipo": "Da viaggio", "n": 15, "nome": "Borsone da viaggio", "cat": "Tracolle e borsoni", "info": "48 pagine · 25 × 55 × 25 cm", "pagine": [
        ("Il modello finito", "Il borsone da viaggio, in due pelli."),
        ("Le misure", "25 × 55 × 25 cm, manico alto 16 cm."),
        ("I materiali", "Circa 1,4 m² di pelle da 2,4 mm e contrasto in concia vegetale."),
        ("La minuteria", "Cerniera da 52 cm, 4 anelli a D, 2 fibbie e 2 bottoni automatici."),
        ("Lo schema dei pezzi", "Tutti i pezzi del borsone su una pagina."),
        ("Tavola 1:1", "Una delle tavole, con i fori di cucitura.")]},
    {"slug": "drew", "breve": "Drew", "tipo": "Tracolla", "n": 21, "nome": "Tracolla Drew", "cat": "Tracolle e borsoni", "info": "23 pagine · 21 × 30 × 9 cm", "pagine": [
        ("Il modello finito", "Tracolla con fibbie e pelle a contrasto."),
        ("Le misure", "21 × 30 × 9 cm."),
        ("I materiali", "Corpo da 2 mm, contrasto da 2,4 mm, cinghie da 2,8 mm."),
        ("La minuteria", "2 fibbie, 4 anelli a D e 2 bottoni Sam Browne."),
        ("Lo schema dei pezzi", "Corpo, patta e cinghie, pezzo per pezzo."),
        ("Tavola 1:1", "A grandezza naturale, con i fori di cucitura.")]},
    {"slug": "gufo", "breve": "Gufo", "tipo": "Zaino", "n": 4, "nome": "Zaino Gufo", "cat": "Zaini", "info": "15 pagine · 19 × 18 × 10 cm", "pagine": [
        ("Il modello finito", "Lo zaino a forma di gufo, con ali e dettagli decorativi."),
        ("Materiali e misure", "19 × 18 × 10 cm, con pelle, minuteria e strumenti."),
        ("Il controllo di stampa", "I due quadrati da misurare prima delle tavole."),
        ("Lo schema dei pezzi", "Orecchie, ali e occhi: ogni pezzo al suo posto."),
        ("Tavola 1:1 · le ali", "Ali e occhi, con i fori di cucitura."),
        ("Tavola 1:1", "Con i segni di raccordo tra i pezzi.")]},
    {"slug": "street-chic", "breve": "Street Chic", "tipo": "Borsa a spalla", "n": 2, "nome": "Borsa Street Chic", "cat": "Borse", "info": "15 pagine · borsa a spalla", "pagine": [
        ("Il modello finito", "Borsa a spalla con tasche laterali."),
        ("Materiali e strumenti", "Pelle da 1,6–1,8 mm, cerniera, chiusura magnetica e il resto."),
        ("Lo schema dei pezzi", "I numeri indicano quali fori unire tra loro."),
        ("La pelle necessaria", "Circa 0,4 m²: tutti i pezzi su un foglio da 40 × 100 cm."),
        ("Tavola 1:1", "Con il righello di scala su ogni tavola."),
        ("Tavola 1:1", "I numeri dei fori da unire, già segnati.")]},
]

# Testimonianze: SOLO clienti reali e con il loro consenso (foto dei loro lavori).
# {"nome": "Giulia", "citta": "Milano", "modello": "Zaino Rosaleen", "testo": "...", "foto": "img/clienti/giulia.webp"}
# Con la lista vuota la sezione non esce.
TESTIMONIANZE = []

# Messaggi WhatsApp di allievi del corso di Luca (negozio fisico): originali in spagnolo, tradotti in italiano (lo dice la sezione).
# (N, alt): img/clienti/wa-N.webp (grande) e wa-N-s.webp (carosello), nell'ordine in cui escono.
CHAT = [
    (2, "Zaino cucito a mano: «Ho iniziato da zero e non riesco a credere a questo risultato»"),
    (3, "Portafoglio rosso: «Pensavo di non riuscirci, ma seguendo il corso passo dopo passo è venuto così»"),
    (4, "Zaino per l'università: «Non ho avuto bisogno di una macchina»"),
    (5, "Tracolla blu: «È venuta bellissima, grazie per tutto ciò che insegnate nel corso»"),
    (6, "Cintura in cuoio: «Ho finito la mia prima cintura!!»"),
    (7, "Portafoglio con punto croce: «Mi sono piaciute tantissimo le 3 tecniche di cucitura»"),
    (8, "Borsa shopper: «Non avevo mai lavorato la pelle ed è venuta così»"),
    (9, "Cintura blu: «Ho già realizzato la mia prima cintura, tutte le lezioni sono facili da seguire»"),
    (1, "Zaino roll-top in pelle: «Ho iniziato da zero e grazie alle lezioni sono riuscito a realizzare qualcosa del genere passo dopo passo»"),
]
# ---------------------------------------------------------------- /CONFIG

e = lambda s: html.escape(s, quote=True)


def wh(rel):
    """width/height reales de img/<rel>, para que el navegador reserve el lugar."""
    from PIL import Image
    w, h = Image.open(os.path.join(QUI, "img", rel)).size
    return f'width="{w}" height="{h}"'
ANTEPRIMA = not CHECKOUT
N = sum(v["modelli"] for v in VOLUMI)
PAGINE = sum(v["pagine"] for v in VOLUMI)
CTA = CHECKOUT or "#offerta"


def elenco_kit():
    """«39 borse e zaini · 38 portafogli, … · 4 cinture» para el resumen."""
    return " · ".join(f"{v['modelli']} {v['breve']}" for v in VOLUMI)


ICO = {
    "lock": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/></svg>',
    "ok": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
    "no": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    "forbici": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/></svg>',
    "griglia": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    "righello": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 17 17 3l4 4L7 21z"/><path d="m7 13 2 2M10 10l2 2M13 7l2 2"/></svg>',
    "libro": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h7"/></svg>',
    "ago": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20 17.5 6.5"/><ellipse cx="18.8" cy="5.2" rx="2.1" ry="1" transform="rotate(-45 18.8 5.2)"/><path d="M19.5 6.5c1.5 3 .5 6-2.5 7s-5 3.5-4 6.5"/></svg>',
    "regalo": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="9" width="18" height="12" rx="1"/><path d="M3 13h18M12 9v12M12 9C10 5 6 5 7 8s5 1 5 1 4 2 5-1-3-3-5 1"/></svg>',
    "monete": '<svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v4c0 1.7 3.1 3 7 3s7-1.3 7-3V6"/><path d="M5 10v4c0 1.7 3.1 3 7 3s7-1.3 7-3v-4"/><path d="M5 14v4c0 1.7 3.1 3 7 3s7-1.3 7-3v-4"/></svg>',
    "tocco": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5"/><path d="M22 9v6"/></svg>',
    "razzo": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2"/><path d="M9 15l-3-3c1-4 4.5-8 12-9-1 7.5-5 11-9 12z"/><circle cx="14.5" cy="9.5" r="1.8"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9z"/><circle cx="8" cy="8" r="1.6"/></svg>',
}

SCHIZZO = ('<svg viewBox="0 0 200 150" fill="none" stroke-linecap="round" stroke-linejoin="round">'
           '<ellipse cx="104" cy="96" rx="58" ry="30" fill="rgba(60,40,20,.05)" stroke="none"/>'
           '<path d="M50 60c-2 30 2 58 6 64 34 4 64 3 90-2 4-22 6-42 2-64-28-3-68-1-98 2z"/>'
           '<path d="M53 64c-1 27 3 52 6 58M144 62c3 20 2 41-1 58M58 121c30 3 58 2 84-3" stroke-dasharray="3 5"/>'
           '<path d="M78 58c2-28 44-28 46-2M83 57c3-21 35-23 37-2"/>'
           '<path d="M92 76h18v14H92z" stroke-dasharray="2 3"/>'
           '<path d="M56 144h90M56 140v8M146 140v8" stroke="#b9ab98"/>'
           '<text x="101" y="139" font-family="Oswald,sans-serif" font-size="11" fill="#a3372d" stroke="none" text-anchor="middle">? cm</text>'
           '<text x="166" y="52" font-family="Oswald,sans-serif" font-size="34" font-weight="700" fill="#a3372d" stroke="none">?</text>'
           '<path d="M160 70l14 14M174 70l-14 14" stroke="#c9a08f"/></svg>')

FAVICON = ("data:image/svg+xml,"
           "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect x='4' y='4' width='56' height='56' rx='14' fill='%23a5561f'/%3E"
           "%3Crect x='11' y='11' width='42' height='42' rx='9' fill='none' stroke='%23f3e2c4' "
           "stroke-width='3' stroke-dasharray='5 4'/%3E"
           "%3Ctext x='32' y='42' font-family='Georgia,serif' font-weight='700' font-size='28' "
           "text-anchor='middle' fill='%23fff'%3EPF%3C/text%3E%3C/svg%3E")

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
         '&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">')

CSS = r"""
:root{
  --espresso:#1c130c;--espresso-2:#271a11;--leather:#6b3a1d;--cognac:#b8662c;--cognac-d:#8f4b1c;
  --tan:#e0b57b;--gold:#dcaa55;--parchment:#efe4cf;--cream:#f7f0e3;--paper:#fcf9f3;
  --ink:#2a1c13;--ink-2:#4b3627;--muted:#6b5645;--line:#d9c6a6;--ok:#2e6a46;--no:#a3372d;
  --it-g:#1f8a4c;--it-r:#c73a2f;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;overflow-x:clip}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
body{margin:0;background:var(--parchment);color:var(--ink);font:400 17px/1.62 Inter,system-ui,-apple-system,Segoe UI,sans-serif;overflow-x:clip}
img{max-width:100%;height:auto;display:block}
a{color:var(--cognac-d)}
h1,h2,h3{font-family:Oswald,Impact,"Arial Narrow",sans-serif;font-weight:700;line-height:1.08;letter-spacing:.005em;margin:0;text-wrap:balance}
p{margin:0 0 1em}
strong{font-weight:700}
.wrap{width:100%;max-width:1080px;margin:0 auto;padding:0 16px}
.stretta{max-width:760px}
svg{width:1em;height:1em;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}

/* superficies */
.cuoio{position:relative;color:var(--cream);background-color:var(--espresso);
  background-image:radial-gradient(900px 520px at 10% -10%,rgba(184,102,44,.30),transparent 62%),
  radial-gradient(700px 480px at 110% 15%,rgba(220,170,85,.14),transparent 60%),
  url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 .9 0 0 0 0 .8 0 0 0 .07 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.sez{padding:64px 0}
.sez-alt{background:var(--cream)}
.sez+.sez-alt,.sez-alt+.sez{border-top:2px dashed var(--line)}
@media (min-width:900px){.sez{padding:92px 0}}

/* tipografia de sección */
.occhiello{display:inline-flex;align-items:center;gap:8px;font:600 12.5px/1 Inter,sans-serif;letter-spacing:.16em;text-transform:uppercase;
  color:var(--cognac-d);padding:8px 13px;border:1.5px dashed currentColor;border-radius:999px;margin-bottom:18px}
.cuoio .occhiello{color:var(--tan)}
.titolo{text-align:center;margin:0 auto 34px;max-width:780px}
.titolo h2{font-size:clamp(30px,6vw,46px);text-transform:uppercase;color:var(--ink)}
.cuoio .titolo h2{color:#fff}
.titolo p{margin:14px auto 0;color:var(--muted);font-size:18px;max-width:640px}
.cuoio .titolo p{color:rgba(247,240,227,.8)}
.accento{color:var(--cognac)}
.cuoio .accento{color:var(--tan)}

/* botón: etiqueta de cuero con costura */
.btn{position:relative;display:flex;align-items:center;justify-content:center;gap:10px;width:100%;max-width:540px;margin:0 auto;
  padding:19px 24px 20px;border-radius:14px;background:linear-gradient(180deg,#c26c2d 0%,#99501e 100%);color:#fff;text-decoration:none;
  font:700 clamp(18px,4.6vw,21px)/1.15 Oswald,Impact,sans-serif;letter-spacing:.05em;text-transform:uppercase;text-align:center;
  box-shadow:0 5px 0 #5c3016,0 16px 30px rgba(28,19,12,.34);transition:transform .12s ease,box-shadow .12s ease}
.btn::before{content:"";position:absolute;inset:5px;border:1.5px dashed rgba(255,255,255,.62);border-radius:10px;pointer-events:none}
.btn:hover{transform:translateY(2px);box-shadow:0 3px 0 #5c3016,0 10px 22px rgba(28,19,12,.3)}
.btn:focus-visible{outline:3px solid var(--gold);outline-offset:4px}
.fiducia{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 16px;margin:16px 0 0;font-size:14px;color:var(--muted)}
.fiducia span{display:inline-flex;align-items:center;gap:6px}
.fiducia svg{color:var(--cognac)}
.cuoio .fiducia{color:rgba(247,240,227,.78)}
.cuoio .fiducia svg{color:var(--tan)}

/* marco de página (como el libro) */
.cornice{position:relative;padding:9px;border-radius:12px;background:linear-gradient(160deg,#7c4424,#56301a);box-shadow:0 18px 36px rgba(28,19,12,.28)}
.cornice::after{content:"";position:absolute;inset:4px;border:1.5px dashed rgba(247,227,196,.55);border-radius:9px;pointer-events:none}
.cornice img{border-radius:5px}

/* anteprima */
.anteprima{background:#fff3c4;color:#5b4300;font:600 13.5px/1.4 Inter,sans-serif;text-align:center;padding:10px 16px;border-bottom:1px solid #e6d27a}

/* promo */
.promo{position:sticky;top:0;z-index:999;width:100%;background:linear-gradient(180deg,#2b1c12 0%,#1e130b 100%);border-bottom:1px solid rgba(224,181,123,.38);box-shadow:0 3px 16px rgba(18,12,7,.38);padding:8px 16px}
.promo-in{max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:center;gap:10px 18px;flex-wrap:wrap;line-height:1.3}
.promo-txt{display:inline-flex;align-items:center;gap:9px;font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#fff}
.promo-txt::before{content:"";flex:0 0 auto;width:7px;height:7px;border-radius:50%;background:var(--gold);animation:promoPulse 2.6s ease-out infinite}
@keyframes promoPulse{0%{box-shadow:0 0 0 0 rgba(220,170,85,.65)}70%{box-shadow:0 0 0 9px rgba(220,170,85,0)}100%{box-shadow:0 0 0 0 rgba(220,170,85,0)}}
.promo-time{display:inline-flex;align-items:center;gap:8px;font-size:13.5px;font-weight:500;color:rgba(247,240,227,.82)}
.promo-clock{font-size:14px;font-weight:700;letter-spacing:.25px;line-height:1.2;color:#ffe082;background:rgba(0,0,0,.38);border:1px solid rgba(224,181,123,.45);border-radius:7px;padding:4px 10px;box-shadow:inset 0 1px 2px rgba(0,0,0,.35),0 1px 4px rgba(0,0,0,.25);white-space:nowrap}
.promo-clock:empty{display:none}
@media (max-width:560px){
  .promo{padding:8px 12px}
  .promo-in{gap:6px 10px}
  .promo-txt{font-size:12px;letter-spacing:.06em}
  .promo-time{font-size:12px}
  .promo-clock{font-size:12.5px;padding:3px 8px}
}
@media (prefers-reduced-motion:reduce){.promo-txt::before{animation:none}}
section[id]{scroll-margin-top:60px}

/* hero */
.hero{padding:26px 0 56px;overflow:hidden}
.marchio{display:flex;flex-direction:column;align-items:center;gap:7px;margin-bottom:18px}
.marchio span{font:600 15px/1 Oswald,sans-serif;letter-spacing:.3em;text-transform:uppercase;color:var(--tan)}
.tricolore{display:flex;width:54px;height:4px;border-radius:2px;overflow:hidden}
.tricolore i{flex:1}.tricolore i:nth-child(1){background:var(--it-g)}.tricolore i:nth-child(2){background:#fff}.tricolore i:nth-child(3){background:var(--it-r)}
.hero-in{display:grid;gap:26px;align-items:center}
.hero-img{max-width:520px;margin:0 auto;width:100%}
.hero-txt{text-align:center}
.hero h1{font-size:clamp(34px,8.6vw,58px);text-transform:uppercase;color:#fff}
.hero h1 em{font-style:normal;color:var(--tan);display:block}
.hero .sub{font-size:18.5px;color:rgba(247,240,227,.86);margin:18px auto 26px;max-width:600px}
@media (min-width:900px){
  .hero{padding:34px 0 84px}
  .hero-in{grid-template-columns:1fr 1fr;gap:48px}
  .hero-txt{text-align:left;order:-1}
  .marchio{align-items:flex-start}
  .hero .sub{margin-left:0}
  .hero .btn{margin-left:0}
  .hero .fiducia{justify-content:flex-start}
  .hero-img{max-width:none}
  .hero-img img{transform:scale(1.14)}
}

.vantaggi{list-style:none;margin:22px auto 26px;padding:0;display:grid;gap:12px;max-width:580px;text-align:left}
.vantaggi li{display:flex;gap:14px;align-items:flex-start;padding:14px 16px;border-radius:14px;background:rgba(255,255,255,.05);
  border:1.5px dashed rgba(224,181,123,.35)}
.vantaggi svg{width:42px;height:42px;padding:9px;border-radius:12px;background:var(--tan);color:var(--espresso);stroke-width:2.1}
.vantaggi b{display:block;font:600 19px/1.2 Oswald,sans-serif;text-transform:uppercase;color:#fff;letter-spacing:.01em}
.vantaggi span{display:block;font-size:15px;line-height:1.5;color:rgba(247,240,227,.84);margin-top:4px}
.vantaggi.chiari{margin:0 auto;max-width:620px}
.vantaggi.chiari li{background:var(--paper);border:1px solid var(--line);padding:20px 18px;box-shadow:0 10px 24px rgba(28,19,12,.07)}
.vantaggi.chiari svg{background:var(--espresso);color:var(--tan)}
.vantaggi.chiari b{color:var(--ink);font-size:20px}
.vantaggi.chiari span{color:var(--muted);font-size:15.5px}
@media (min-width:900px){.vantaggi.chiari{grid-template-columns:repeat(3,1fr);max-width:none;gap:20px}.vantaggi.chiari li{flex-direction:column;padding:26px 24px}}

/* barra de datos */
.dati{position:relative;margin-top:-26px;z-index:2}
.dati ul{list-style:none;margin:0;padding:18px;display:grid;grid-template-columns:1fr 1fr;gap:16px 14px;background:var(--paper);
  border-radius:16px;box-shadow:0 14px 34px rgba(28,19,12,.16);border:1px solid var(--line)}
.dati li{display:flex;flex-direction:column;gap:3px;padding:6px 4px;text-align:center;align-items:center}
.dati svg{width:26px;height:26px;color:var(--cognac);margin-bottom:4px}
.dati strong{font:700 23px/1.05 Oswald,sans-serif;text-transform:uppercase;color:var(--ink)}
.dati small{font-size:13.5px;line-height:1.35;color:var(--muted)}
@media (min-width:900px){.dati ul{grid-template-columns:repeat(4,1fr);padding:22px 12px}.dati li+li{border-left:2px dashed var(--line)}}

/* galería */
/* galería con pestañas y paginación */
.scorri-schede{margin-bottom:18px}
.schede{gap:10px}
.scheda{all:unset;box-sizing:border-box;cursor:pointer;flex:none;display:flex;align-items:center;gap:10px;padding:6px 16px 6px 6px;border-radius:999px;
  background:var(--paper);border:1.5px solid var(--line);scroll-snap-align:start;transition:background .15s,border-color .15s,box-shadow .15s}
.scheda img{width:40px;height:40px;border-radius:50%;object-fit:cover;flex:none}
.scheda b{display:block;font:600 15px/1.1 Oswald,sans-serif;text-transform:uppercase;color:var(--ink);white-space:nowrap}
.scheda small{display:block;font-size:12px;line-height:1.3;color:var(--muted);white-space:nowrap}
.scheda:hover{border-color:var(--cognac)}
.scheda[aria-selected="true"]{background:var(--espresso);border-color:var(--espresso);box-shadow:0 8px 18px rgba(28,19,12,.22)}
.scheda[aria-selected="true"] b{color:#fff}.scheda[aria-selected="true"] small{color:var(--tan)}
.scheda:focus-visible{outline:3px solid var(--cognac);outline-offset:2px}
@media (min-width:900px){.scorri-schede{margin-bottom:28px}.scorri-schede .scorri-box{margin:0}.schede{flex-wrap:wrap;justify-content:center;overflow:visible;padding:4px 0}}
.pannello[hidden]{display:none}
.giostra-testa{text-align:center;font-size:14.5px;color:var(--muted);margin:0 0 14px}
.giostra-testa b{font:600 16px/1.2 Oswald,sans-serif;text-transform:uppercase;color:var(--ink);letter-spacing:.02em}
.giostra{position:relative}
.giostra::before,.giostra::after{content:"";position:absolute;top:0;bottom:0;width:44px;z-index:1;pointer-events:none;opacity:0;transition:opacity .25s}
.giostra::before{left:-16px;background:linear-gradient(90deg,var(--parchment) 12%,transparent)}
.giostra::after{right:-16px;background:linear-gradient(270deg,var(--parchment) 12%,transparent)}
.pannello.puo-sx .giostra::before,.pannello.puo-dx .giostra::after{opacity:1}
@media (min-width:900px){.giostra::before{left:-2px}.giostra::after{right:-2px}}
.binario{display:grid;grid-auto-flow:column;grid-auto-columns:80%;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;
  margin:0 -16px;padding:4px 16px 8px;scroll-padding-inline:16px;scrollbar-width:none;overscroll-behavior-x:contain}
.binario::-webkit-scrollbar{display:none}
@media (min-width:600px){.binario{grid-auto-columns:calc((100% - 46px)/2.35)}}
@media (min-width:900px){.binario{grid-auto-columns:calc((100% - 60px)/3.35);gap:20px;margin:0;padding:4px 0 8px;scroll-padding-inline:0}}
.foglio{margin:0;scroll-snap-align:start}
.foglio button{all:unset;cursor:zoom-in;display:block;width:100%;border-radius:12px}
.foglio button:focus-visible{outline:3px solid var(--cognac);outline-offset:3px}
.foglio .cornice{padding:6px}
.foglio img{aspect-ratio:3/4;object-fit:cover;object-position:top;width:100%;background:#fff}
.foglio figcaption{padding:12px 4px 0}
.foglio figcaption b{display:flex;align-items:center;gap:8px;font:600 17px/1.2 Oswald,sans-serif;text-transform:uppercase;color:var(--ink)}
.foglio figcaption b i{font-style:normal;display:inline-grid;place-items:center;flex:none;width:24px;height:24px;border-radius:50%;background:var(--cognac);color:#fff;font:600 13px/1 Inter,sans-serif}
.foglio figcaption span{display:block;font-size:14.5px;color:var(--muted);margin-top:5px;line-height:1.45}
.freccia{position:absolute;top:38%;transform:translateY(-50%);z-index:2;width:46px;height:46px;border-radius:50%;border:1.5px dashed var(--tan);
  background:rgba(28,19,12,.88);color:#fff;font:500 26px/1 Inter,sans-serif;display:grid;place-items:center;cursor:pointer;
  box-shadow:0 8px 18px rgba(0,0,0,.28);transition:opacity .2s}
.freccia.prev{left:-4px}.freccia.next{right:-4px}
.freccia:disabled{opacity:0;pointer-events:none}
.freccia:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
@media (min-width:900px){.freccia.prev{left:-24px}.freccia.next{right:-24px}}
.paginazione{display:flex;align-items:center;justify-content:center;gap:16px;margin-top:16px}
.punti{display:flex;gap:8px;align-items:center}
.punti button{all:unset;cursor:pointer;width:10px;height:10px;border-radius:999px;background:#ccb690;transition:width .25s,background .25s}
.punti button[aria-current="true"]{width:28px;background:var(--cognac)}
.punti button:focus-visible{outline:2px solid var(--cognac);outline-offset:3px}
.conta{font:600 14px/1 Oswald,sans-serif;letter-spacing:.08em;color:var(--muted);min-width:44px;text-align:right}
.cta-mezzo{margin-top:40px;text-align:center}
.cta-mezzo .al-modello{margin:12px 0 0;font-size:14.5px;color:var(--muted)}

/* deslizables: borde que asoma, degradé donde sigue, flechas, aviso y empujón */
.scorri{position:relative}
.scorri-box{position:relative;margin:0 -16px}
.scorri-traccia{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-inline:16px;padding:6px 16px 12px;
  scrollbar-width:none;overscroll-behavior-x:contain}
.scorri-traccia::-webkit-scrollbar{display:none}
.scorri-traccia>*{scroll-snap-align:start;flex:none}
.scorri-box::before,.scorri-box::after{content:"";position:absolute;top:0;bottom:0;width:52px;z-index:1;pointer-events:none;opacity:0;transition:opacity .25s}
.scorri-box::before{left:0;background:linear-gradient(90deg,var(--parchment) 14%,transparent)}
.scorri-box::after{right:0;background:linear-gradient(270deg,var(--parchment) 14%,transparent)}
.scorri.puo-sx .scorri-box::before,.scorri.puo-dx .scorri-box::after{opacity:1}
.scorri-freccia{position:absolute;top:calc(50% - 20px);transform:translateY(-50%);z-index:2;width:44px;height:44px;border-radius:50%;
  border:1.5px dashed var(--tan);background:rgba(28,19,12,.88);color:#fff;font:500 25px/1 Inter,sans-serif;display:grid;place-items:center;
  cursor:pointer;box-shadow:0 8px 18px rgba(0,0,0,.28);transition:opacity .2s}
.scorri-freccia.prev{left:8px}.scorri-freccia.next{right:8px}
.scorri-freccia:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.scorri:not(.puo-sx) .scorri-freccia.prev,.scorri:not(.puo-dx) .scorri-freccia.next{opacity:0;pointer-events:none}
.scorri.fermo .scorri-traccia{justify-content:center}
.scorri-piede{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:6px}
.scorri.fermo .scorri-piede{display:none}
.scorri-hint{display:inline-flex;align-items:center;font:600 12px/1 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;
  color:var(--cognac-d);white-space:nowrap;transition:opacity .4s}
.scorri-hint i{font-style:normal;font-size:18px;line-height:0;margin-left:1px}
.scorri-hint i:first-of-type{margin-left:6px;opacity:.35}
.scorri-hint i:nth-of-type(2){opacity:.65}
.toccato .scorri-hint{opacity:0}
.scorri-barra{position:relative;width:120px;height:4px;border-radius:4px;background:rgba(107,58,29,.16);overflow:hidden}
.scorri-barra i{position:absolute;top:0;bottom:0;left:0;width:30%;border-radius:4px;background:var(--cognac);transition:left .15s linear}

/* cosa crei: cinta de modelos terminados */
.crei{padding:40px 0 4px}
.crei-tit{text-align:center;font:600 13px/1 Inter,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--cognac-d);margin:0 0 14px}
.nastro figure{margin:0;width:148px}
.nastro img{width:148px;height:185px;object-fit:cover;border-radius:14px;box-shadow:0 10px 22px rgba(28,19,12,.18);border:3px solid var(--paper)}
.nastro figcaption{font:600 13.5px/1.2 Oswald,sans-serif;text-transform:uppercase;text-align:center;margin-top:9px;color:var(--ink)}
@media (min-width:900px){.nastro figure{width:178px}.nastro img{width:178px;height:222px}.crei .scorri-box{margin:0}}
/* i 3 volumi: portada, datos y deslizable de modelos */
.volumi{display:grid;gap:20px}
.volume{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:18px 16px 12px;display:grid;
  grid-template-columns:92px minmax(0,1fr);gap:14px 16px;align-items:center;box-shadow:0 12px 28px rgba(28,19,12,.08)}
.vol-cop{width:92px;height:auto;border-radius:6px;box-shadow:0 8px 18px rgba(28,19,12,.25)}
.vol-testa h3{font:600 22px/1.1 Oswald,sans-serif;text-transform:uppercase;margin:0 0 6px;color:var(--ink)}
.vol-testa p{margin:0;font-size:14.5px;line-height:1.4;color:var(--muted)}
.vol-testa .vol-num{margin:0 0 3px;font-size:15px;color:var(--cognac-d)}
.volume .scorri{grid-column:1/-1;min-width:0}
.volume .scorri-box{margin:0 -16px}
.volume .scorri-box::before{background:linear-gradient(90deg,var(--paper) 14%,transparent)}
.volume .scorri-box::after{background:linear-gradient(270deg,var(--paper) 14%,transparent)}
.mini figure{margin:0;width:112px}
.mini img{width:112px;height:112px;object-fit:cover;border-radius:12px;border:2px solid var(--paper);box-shadow:0 6px 14px rgba(28,19,12,.16)}
.mini figcaption{font-size:12.5px;line-height:1.25;margin-top:6px;color:var(--ink-2);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
@media (min-width:900px){.volume{grid-template-columns:150px minmax(0,1fr);padding:24px 24px 14px}.vol-cop{width:150px}
  .volume .scorri-box{margin:0 -24px}.mini figure{width:132px}.mini img{width:132px;height:132px}}
.chat-nota{max-width:520px;margin:10px auto 0;text-align:center;font-size:12.5px;line-height:1.4;color:var(--muted)}
.chat{align-items:flex-start}
.chat figure{margin:0;width:250px}
.chat button{display:block;width:100%;padding:0;border:0;background:none;cursor:zoom-in;border-radius:16px}
.chat button:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.chat img{display:block;width:100%;height:auto;border-radius:16px;box-shadow:0 10px 22px rgba(28,19,12,.18);border:3px solid var(--paper)}
@media (min-width:900px){.chat figure{width:280px}}

/* aviso de deslizar dentro de la paginación (solo móvil y tablet) */
.paginazione .scorri-hint{margin-right:2px}
@media (min-width:900px){.paginazione .scorri-hint{display:none}}

/* plan de 15 días */
.piano{list-style:none;margin:0;padding:0;display:grid;gap:14px}
.piano li{background:rgba(255,255,255,.04);border:1.5px dashed rgba(224,181,123,.42);border-radius:16px;padding:18px 18px 16px}
.piano .giorni{display:inline-block;font:700 12px/1 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--espresso);
  background:var(--tan);padding:7px 11px;border-radius:999px;margin-bottom:12px}
.piano b{display:block;font:600 21px/1.15 Oswald,sans-serif;text-transform:uppercase;color:#fff;margin-bottom:6px}
.piano p{margin:0;font-size:15.5px;line-height:1.55;color:rgba(247,240,227,.84)}
.nota-piano{text-align:center;font-size:13.5px;color:rgba(247,240,227,.62);margin:20px auto 0;max-width:620px}
@media (min-width:900px){.piano{grid-template-columns:repeat(4,1fr);gap:18px}}

/* testimonianze reali */
.testimonianze{display:grid;gap:18px}
.testim{margin:0;background:var(--paper);border:1px solid var(--line);border-radius:16px;overflow:hidden}
.testim img{aspect-ratio:4/3;object-fit:cover;width:100%}
.testim blockquote{margin:0;padding:16px 18px 6px;font-size:16px;color:var(--ink-2)}
.testim figcaption{padding:0 18px 18px;font-size:14px;color:var(--muted)}
@media (min-width:900px){.testimonianze{grid-template-columns:repeat(3,1fr)}}

/* dos columnas texto + imagen */
.due{display:grid;gap:34px;align-items:center}
.due .testo h2{font-size:clamp(30px,6vw,44px);text-transform:uppercase;margin-bottom:20px}
.due .testo p{font-size:17.5px;color:var(--ink-2)}
.due .immagine{max-width:420px;margin:0 auto;width:100%}
.immagine.libera{margin:0 auto}
.immagine.libera figcaption{text-align:center;font-size:14px;color:var(--muted);margin-top:10px;line-height:1.45}
@media (min-width:900px){.due .immagine.libera{max-width:500px}}
.nota{display:flex;gap:12px;align-items:center;margin-top:22px;padding:14px 16px;border-radius:12px;background:var(--paper);border:1.5px dashed var(--cognac);
  font:600 17px/1.35 Oswald,sans-serif;letter-spacing:.02em;text-transform:uppercase;color:var(--cognac-d)}
.nota svg{width:26px;height:26px}
@media (min-width:900px){.due{grid-template-columns:1.1fr .9fr;gap:60px}.due.inversa .immagine{order:-1}}

/* comparación */
.confronto{display:grid;gap:18px}
.lato{border-radius:16px;padding:24px 20px}
.lato h3{font-size:22px;text-transform:uppercase;margin-bottom:16px;display:flex;align-items:center;gap:10px}
.lato ul{list-style:none;margin:0;padding:0;display:grid;gap:13px}
.lato li{display:flex;gap:11px;align-items:flex-start;font-size:16.5px;line-height:1.45}
.lato li svg{width:22px;height:22px;margin-top:1px;padding:3px;border-radius:50%;stroke-width:3}
.lato.senza{background:#ece3d4;border:1.5px solid #d8cbb5;color:#5e4d40}
.lato.senza li svg{background:#e3cdc6;color:var(--no)}
.lato.con{background:var(--espresso);color:var(--cream);box-shadow:0 18px 36px rgba(28,19,12,.25)}
.lato.con h3{color:var(--tan)}
.lato.con li svg{background:rgba(46,106,70,.3);color:#8fd0a6}
.lato .cornice,.schizzo{margin-top:22px}
.lato .cornice img{aspect-ratio:4/3;object-fit:cover;object-position:top}
.schizzo{aspect-ratio:4/3;background:#fbf8f1;border:1px solid #d8cbb5;border-radius:10px;display:grid;place-items:center;transform:rotate(-1.2deg);box-shadow:0 8px 18px rgba(28,19,12,.08)}
.schizzo svg{width:88%;height:auto;stroke:#8d8378;stroke-width:1.6}
@media (max-width:899px){.lato .cornice,.schizzo{max-width:420px;margin-left:auto;margin-right:auto}}
@media (min-width:900px){.confronto{grid-template-columns:1fr 1fr;gap:26px;align-items:start}.lato{padding:32px 30px}}

/* modelos del kit */
.kit{display:grid;gap:34px}
.cat h3{display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:23px;text-transform:uppercase;color:var(--ink);
  padding-bottom:10px;margin-bottom:14px;border-bottom:2px dashed var(--line)}
.cat h3 small{font:600 12.5px/1 Inter,sans-serif;letter-spacing:.1em;color:var(--cognac-d)}
.cat-cards{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.mod{background:var(--paper);border-radius:14px;overflow:hidden;border:1px solid var(--line);box-shadow:0 10px 24px rgba(28,19,12,.1);display:flex;flex-direction:column}
.mod img{aspect-ratio:4/5;object-fit:cover;width:100%;background:#e8dcc6}
.mod div{padding:12px 12px 14px;display:flex;flex-direction:column;gap:6px;flex:1}
.mod b{font:600 17px/1.15 Oswald,sans-serif;text-transform:uppercase;color:var(--ink)}
.mod span{font-size:13.5px;line-height:1.45;color:var(--muted)}
.mod em{margin-top:auto;font-style:normal;font-size:12.5px;font-weight:600;color:var(--cognac-d)}
.mod.manca{background:repeating-linear-gradient(135deg,#f6eedd 0 12px,#f1e6d1 12px 24px);border:2px dashed #c9a877;box-shadow:none;
  align-items:center;justify-content:center;text-align:center;min-height:230px;padding:18px}
.mod.manca svg{width:30px;height:30px;color:#b08a55}
.mod.manca b{margin-top:8px;color:#8a6a3f}
@media (min-width:640px){.kit{grid-template-columns:1fr 1fr}}
@media (min-width:980px){.kit{grid-template-columns:repeat(5,1fr);gap:18px}.cat-cards{grid-template-columns:1fr}.cat h3{font-size:20px;flex-direction:column;align-items:flex-start;justify-content:flex-end;gap:6px;min-height:74px}}

/* modo más simple */
.immagina{font:700 22px/1.2 Oswald,sans-serif;text-transform:uppercase;color:var(--cognac-d);margin-bottom:10px}
.contrario{padding:16px 18px;border-left:4px solid #c9b18d;background:rgba(255,255,255,.45);border-radius:0 12px 12px 0;color:var(--muted);font-style:italic}
.meglio{padding:16px 18px;border-left:4px solid var(--cognac);background:var(--paper);border-radius:0 12px 12px 0;font-weight:500}
.passi{list-style:none;margin:20px 0 22px;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.passi li{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:12px;font-size:15px;line-height:1.35}
.passi li b{display:block;font:700 26px/1 Oswald,sans-serif;color:var(--cognac);margin-bottom:4px}

/* qué recibís */
.ricevi{display:grid;gap:22px}
.blocco{background:var(--paper);border-radius:16px;border:1px solid var(--line);padding:22px 20px;box-shadow:0 10px 26px rgba(28,19,12,.08)}
.blocco h3{font-size:21px;text-transform:uppercase;margin-bottom:14px;color:var(--ink)}
.righe{list-style:none;margin:0;padding:0}
.righe li{display:grid;grid-template-columns:auto 1fr;gap:4px 14px;padding:12px 0;border-bottom:1.5px dashed var(--line)}
.righe li:last-child{border-bottom:0}
.righe .c{font:700 15px/1.3 Oswald,sans-serif;text-transform:uppercase;color:var(--cognac-d);min-width:108px}
.righe .m{font-size:15.5px;line-height:1.45}
.righe .m i{color:#9a7a4f}
.spunte{list-style:none;margin:0;padding:0;display:grid;gap:11px}
.spunte li{display:flex;gap:10px;align-items:flex-start;font-size:16px;line-height:1.45}
.spunte svg{width:21px;height:21px;padding:3px;border-radius:50%;background:rgba(46,106,70,.14);color:var(--ok);stroke-width:3;margin-top:1px}
@media (min-width:900px){.ricevi{grid-template-columns:1.1fr .9fr;align-items:start}}

/* licencia */
.licenza{display:grid;gap:14px}
.voce{display:flex;gap:14px;align-items:flex-start;background:var(--paper);border-radius:14px;padding:18px;border:1px solid var(--line)}
.voce>svg{width:34px;height:34px;padding:7px;border-radius:50%;stroke-width:3}
.voce.si>svg{background:rgba(46,106,70,.14);color:var(--ok)}
.voce.no>svg{background:rgba(163,55,45,.12);color:var(--no)}
.voce b{display:block;font:600 19px/1.2 Oswald,sans-serif;text-transform:uppercase;margin-bottom:4px}
.voce span{font-size:15.5px;color:var(--muted);line-height:1.5}
@media (min-width:900px){.licenza{grid-template-columns:repeat(3,1fr);gap:20px}}

/* para quién */
.profili{display:grid;gap:16px}
.profilo{background:var(--paper);border-radius:16px;padding:24px 22px;border:1px solid var(--line);position:relative}
.profilo::before{content:"";position:absolute;inset:6px;border:1.5px dashed rgba(184,102,44,.28);border-radius:11px;pointer-events:none}
.profilo svg{width:40px;height:40px;padding:9px;border-radius:12px;background:var(--espresso);color:var(--tan);margin-bottom:14px}
.profilo h3{font-size:22px;text-transform:uppercase;margin-bottom:10px}
.profilo p{font-size:16px;color:var(--ink-2);margin:0}
@media (min-width:900px){.profili{grid-template-columns:repeat(3,1fr);gap:22px}}

/* oferta */
.offerta{max-width:680px;margin:0 auto;background:var(--paper);border-radius:20px;padding:28px 20px 30px;border:1px solid var(--line);
  box-shadow:0 22px 50px rgba(28,19,12,.16);position:relative}
.offerta::before{content:"";position:absolute;inset:8px;border:2px dashed rgba(184,102,44,.35);border-radius:14px;pointer-events:none}
.offerta .spunte{margin-bottom:26px}
.offerta-img{position:relative;max-width:460px;margin:-4px auto 22px}
.prezzo{text-align:center;margin:0 0 22px}
.prezzo small{display:block;font:600 13px/1 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.prezzo strong{display:block;font:700 66px/1 Oswald,sans-serif;color:var(--cognac-d);margin:10px 0 6px}
.prezzo span{font-size:14.5px;color:var(--muted)}
@media (min-width:900px){.offerta{padding:40px 44px}}

/* garantía */
.garanzia{display:grid;gap:26px;align-items:center;justify-items:center;text-align:center;max-width:860px;margin:0 auto}
.sigillo{width:168px;height:168px;border-radius:50%;display:grid;place-items:center;text-align:center;color:#fff;
  background:radial-gradient(circle at 35% 30%,#c47436,#8a4619 70%);box-shadow:0 14px 30px rgba(28,19,12,.3),inset 0 0 0 7px rgba(255,255,255,.08);position:relative}
.sigillo::after{content:"";position:absolute;inset:9px;border-radius:50%;border:2px dashed rgba(255,241,220,.7)}
.sigillo b{display:block;font:700 54px/.9 Oswald,sans-serif}
.sigillo span{display:block;font:600 13px/1.2 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase}
.garanzia h2{font-size:clamp(28px,5.6vw,40px);text-transform:uppercase}
.garanzia p{font-size:17px;color:var(--ink-2);max-width:640px;margin:12px auto 0}
.garanzia .tre{font:600 16px/1.5 Oswald,sans-serif;letter-spacing:.04em;text-transform:uppercase;color:var(--cognac-d)}
@media (min-width:900px){.garanzia{grid-template-columns:auto 1fr;text-align:left;justify-items:start;gap:44px}.garanzia p{margin-left:0}}

/* FAQ */
.faq{max-width:780px;margin:0 auto;display:grid;gap:12px}
.faq details{background:var(--paper);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.faq summary{list-style:none;cursor:pointer;padding:18px 54px 18px 18px;position:relative;font:600 18px/1.3 Oswald,sans-serif;letter-spacing:.01em;color:var(--ink)}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:16px;top:50%;transform:translateY(-50%);width:28px;height:28px;border-radius:50%;
  display:grid;place-items:center;background:var(--cream);border:1.5px dashed var(--cognac);color:var(--cognac-d);font:600 20px/1 Inter,sans-serif}
.faq details[open] summary::after{content:"−"}
.faq summary:focus-visible{outline:3px solid var(--cognac);outline-offset:-3px}
.faq details p{padding:0 18px 18px;margin:0;color:var(--ink-2);font-size:16px}

/* cierre */
.finale{text-align:center}
.finale h2{font-size:clamp(30px,6.4vw,48px);text-transform:uppercase;color:#fff;margin-bottom:22px}
.finale p{font-size:18px;color:rgba(247,240,227,.86);max-width:640px;margin:0 auto 1em}
.finale .grande{font:600 clamp(22px,5vw,28px)/1.25 Oswald,sans-serif;color:var(--tan);text-transform:uppercase;letter-spacing:.02em}
.riassunto{list-style:none;padding:0;margin:26px auto 30px;display:flex;flex-wrap:wrap;justify-content:center;gap:10px}
.riassunto li{padding:9px 14px;border-radius:999px;border:1.5px dashed rgba(224,181,123,.55);font-size:14.5px;color:var(--cream)}
.riassunto b{color:#fff}
.dopo{margin-top:14px;font-size:14px;color:rgba(247,240,227,.66)}

/* footer */
footer{background:#140d08;color:rgba(247,240,227,.6);padding:34px 0 40px;font-size:13.5px;text-align:center}
footer .marchio{margin-bottom:14px}
footer nav{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 16px;margin:10px 0 12px}
footer a{color:rgba(247,240,227,.78)}

/* visor */
.visore{border:0;padding:0;background:transparent;max-width:min(92vw,720px);max-height:94vh;overflow:visible}
.visore::backdrop{background:rgba(18,11,6,.9)}
.visore img{max-height:82vh;width:auto;margin:0 auto;border-radius:6px;box-shadow:0 20px 60px rgba(0,0,0,.5)}
.visore p{color:var(--cream);text-align:center;margin:12px 0 0;font:600 16px/1.3 Oswald,sans-serif;text-transform:uppercase;letter-spacing:.04em}
.visore .ctrl{position:fixed;top:50%;transform:translateY(-50%);width:46px;height:46px;border-radius:50%;border:1.5px dashed rgba(224,181,123,.7);
  background:rgba(28,19,12,.8);color:#fff;font:600 22px/1 Inter,sans-serif;cursor:pointer}
.visore .prev{left:10px}.visore .next{right:10px}
.visore .chiudi{position:fixed;top:12px;right:12px;width:44px;height:44px;border-radius:50%;border:0;background:rgba(247,240,227,.14);color:#fff;font:400 26px/1 Inter,sans-serif;cursor:pointer}

/* cartel de compra reciente */
.sp-toast{
  position:fixed;left:14px;top:14px;z-index:99999;
  display:flex;align-items:center;gap:12px;
  background:#fff;border:1px solid #e4e9ee;border-radius:12px;
  padding:10px 14px 10px 10px;max-width:330px;
  box-shadow:0 10px 30px rgba(18,25,31,.22);
  opacity:0;visibility:hidden;transform:translateY(-16px) scale(.97);
  transition:opacity .45s ease, transform .45s cubic-bezier(.2,.8,.3,1), visibility .45s;
}
.sp-toast.show{opacity:1;visibility:visible;transform:translateY(0) scale(1)}
.sp-mini{
  position:relative;flex:0 0 auto;width:66px;height:42px;border-radius:6px;overflow:hidden;
  background:#0f1516;box-shadow:0 2px 8px rgba(18,25,31,.22);
}
.sp-mini img{width:100%;height:100%;object-fit:cover;border-radius:0;margin:0;display:block}
.sp-txt{min-width:0;line-height:1.4}
.sp-name{font-size:13.5px;font-weight:700;color:#12191f;display:block}
.sp-name b{font-weight:700}
.sp-prod{
  font-size:12px;color:#5b6874;display:block;margin-top:1px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.sp-meta{
  font-size:10.5px;color:#98a3ad;display:flex;align-items:center;gap:5px;margin-top:3px;
}
.sp-meta .ok{color:#28a745;font-weight:700}
.sp-close{
  position:absolute;top:-10px;right:-10px;
  width:26px;height:26px;padding:0;line-height:1;
  display:flex;align-items:center;justify-content:center;
  border:1px solid #e0e6eb;border-radius:50%;
  background:#fff;color:#8a949e;font-size:16px;font-weight:600;
  font-family:inherit;cursor:pointer;
  box-shadow:0 2px 8px rgba(18,25,31,.14);
  transition:background .18s ease, color .18s ease, transform .18s ease, border-color .18s ease;
}
.sp-close:hover{background:#ffffff;border-color:#cbd5e1;color:#12191f;transform:scale(1.08);box-shadow:0 4px 12px rgba(18,25,31,.2)}
.sp-close:active{transform:scale(.96)}
@media (max-width:560px){
  .sp-toast{left:8px;right:8px;top:10px;max-width:none}
}
"""

JS = r"""
(function(){
  // fecha de hoy en la barra de la oferta (como en las otras landing)
  var el=document.getElementById('oggi');
  if(el){try{var s=new Date().toLocaleDateString('it-IT',{timeZone:'Europe/Rome',weekday:'long',day:'numeric',month:'long'});
    el.textContent=(s?s.replace(/(^\w|\s\w)/g,function(m){return m.toUpperCase();}):'Oggi');}catch(e){el.textContent='Oggi';}}

  // utm_* y click ids de la visita → links al checkout, para que la venta quede atribuida al anuncio
  function conParametri(h){try{var u=new URL(h,location.href);
    new URLSearchParams(location.search).forEach(function(v,k){if(/^(utm_|fbclid$|gclid$|ttclid$)/.test(k)&&!u.searchParams.has(k))u.searchParams.set(k,v);});
    return u.toString();}catch(e){return h;}}
  document.querySelectorAll('a[data-co]').forEach(function(a){a.href=conParametri(a.href);});
  // visor de páginas: navega dentro del modelo abierto
  var dlg=document.getElementById('visore'), img=dlg&&dlg.querySelector('img'), cap=dlg&&dlg.querySelector('p'), lista=[], i=0;
  function mostra(k){i=(k+lista.length)%lista.length;var b=lista[i];img.src=b.getAttribute('data-grande');img.alt=b.getAttribute('data-titolo');cap.textContent=b.getAttribute('data-titolo');}
  document.addEventListener('click',function(ev){var b=ev.target.closest&&ev.target.closest('[data-grande]');if(!b||!dlg)return;
    var g=b.closest('[data-gruppo]')||document;lista=[].slice.call(g.querySelectorAll('[data-grande]'));mostra(lista.indexOf(b));if(dlg.showModal)dlg.showModal();});
  if(dlg){
    dlg.querySelector('.prev').onclick=function(){mostra(i-1);};
    dlg.querySelector('.next').onclick=function(){mostra(i+1);};
    dlg.querySelector('.chiudi').onclick=function(){dlg.close();};
    dlg.addEventListener('click',function(ev){if(ev.target===dlg)dlg.close();});
    document.addEventListener('keydown',function(ev){if(!dlg.open)return;if(ev.key==='ArrowLeft')mostra(i-1);if(ev.key==='ArrowRight')mostra(i+1);});
  }

  // carrusel de páginas con puntos, contador y flechas
  document.querySelectorAll('.pannello').forEach(function(pan){
    var bin=pan.querySelector('.binario'), fogli=[].slice.call(bin.children), punti=[].slice.call(pan.querySelectorAll('.punti button')),
        conta=pan.querySelector('.conta'), prev=pan.querySelector('.prev'), next=pan.querySelector('.next'), attesa=false, voluto=null;
    function passo(){return fogli.length>1?fogli[1].offsetLeft-fogli[0].offsetLeft:bin.clientWidth;}
    function aggiorna(){attesa=false;var fine=bin.scrollLeft+bin.clientWidth>=bin.scrollWidth-4;
      var k=fine?(voluto!==null?voluto:fogli.length-1):Math.max(0,Math.min(fogli.length-1,Math.round(bin.scrollLeft/passo())));
      punti.forEach(function(p,n){p.setAttribute('aria-current',n===k?'true':'false');});
      conta.textContent=(k+1)+' / '+fogli.length;prev.disabled=bin.scrollLeft<=4;next.disabled=fine;}
    bin.addEventListener('scroll',function(){if(!attesa){attesa=true;requestAnimationFrame(aggiorna);}},{passive:true});
    ['pointerdown','wheel','touchstart'].forEach(function(t){bin.addEventListener(t,function(){voluto=null;},{passive:true});});
    prev.onclick=function(){voluto=null;bin.scrollBy({left:-passo(),behavior:'smooth'});};
    next.onclick=function(){bin.scrollBy({left:passo(),behavior:'smooth'});};
    punti.forEach(function(p,n){p.onclick=function(){voluto=n;bin.scrollTo({left:n*passo(),behavior:'smooth'});aggiorna();};});
    window.addEventListener('resize',aggiorna);
    pan._aggiorna=aggiorna;aggiorna();
  });

  // pestañas de modelos
  var schede=[].slice.call(document.querySelectorAll('.scheda'));
  function apri(t,focus){schede.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;
      document.getElementById(x.getAttribute('aria-controls')).hidden=!on;});
    var pan=document.getElementById(t.getAttribute('aria-controls'));pan.querySelector('.binario').scrollLeft=0;pan._aggiorna&&pan._aggiorna();
    if(focus)t.focus();}
  schede.forEach(function(t,n){t.addEventListener('click',function(){apri(t);});
    t.addEventListener('keydown',function(ev){var d=ev.key==='ArrowRight'?1:ev.key==='ArrowLeft'?-1:0;if(d){ev.preventDefault();apri(schede[(n+d+schede.length)%schede.length],true);}});});

  // deslizables: estado de bordes, barra, flechas y aviso
  document.querySelectorAll('[data-scorri]').forEach(function(box){
    var tr=box.querySelector('.scorri-traccia, .binario'), barra=box.querySelector('.scorri-barra i'),
        prev=box.querySelector('.scorri-freccia.prev'), next=box.querySelector('.scorri-freccia.next'), toccato=false, ultimo=0, attesa=false;
    if(!tr)return;
    function stato(){attesa=false;var max=tr.scrollWidth-tr.clientWidth, x=tr.scrollLeft;
      box.classList.toggle('fermo',max<=4);box.classList.toggle('puo-sx',x>4);box.classList.toggle('puo-dx',x<max-4);
      if(barra&&max>4){var vis=tr.clientWidth/tr.scrollWidth;barra.style.width=(vis*100)+'%';barra.style.left=((x/max)*(1-vis)*100)+'%';}}
    function passo(){var a=tr.children[0], b=tr.children[1];return a&&b?b.offsetLeft-a.offsetLeft:tr.clientWidth*.8;}
    function tocca(){toccato=true;ultimo=Date.now();box.classList.add('toccato');}
    tr.addEventListener('scroll',function(){if(!attesa){attesa=true;requestAnimationFrame(stato);}},{passive:true});
    ['pointerdown','touchstart','wheel'].forEach(function(t){tr.addEventListener(t,tocca,{passive:true});});
    if(prev)prev.onclick=function(){tocca();tr.scrollBy({left:-passo(),behavior:'smooth'});};
    if(next)next.onclick=function(){tocca();tr.scrollBy({left:passo(),behavior:'smooth'});};
    box.querySelectorAll('.freccia, .punti button').forEach(function(b){b.addEventListener('click',tocca);});
    window.addEventListener('resize',stato);stato();
  });

  // cartel de compra reciente (social proof toast)
  (function(){
    var buyers = [
      { name: "Chiara da Milano", prod: "Ha acquistato il Kit Pelletteria Facile", time: "fa 4 minuti" },
      { name: "Marco da Firenze", prod: "Kit Completo · 3 Volumi (81 Modelli)", time: "fa 12 minuti" },
      { name: "Martina da Bologna", prod: "Ha acquistato il Kit Completo", time: "fa 18 minuti" },
      { name: "Lorenzo da Roma", prod: "Kit Completo · 3 Volumi (81 Modelli)", time: "fa 25 minuti" },
      { name: "Sofia da Torino", prod: "Ha sbloccato il Kit Pelletteria Facile", time: "fa 31 minuti" },
      { name: "Matteo da Vicenza", prod: "Kit Completo · 3 Volumi (81 Modelli)", time: "fa 39 minuti" },
      { name: "Camilla da Padova", prod: "Ha acquistato il Kit Completo", time: "fa 44 minuti" },
      { name: "Alessandro da Napoli", prod: "Kit Completo · 3 Volumi (81 Modelli)", time: "fa 52 minuti" }
    ];
    var idx = 0;
    var toast = document.getElementById('spToast');
    var spName = document.getElementById('spName');
    var spProd = document.getElementById('spProd');
    var spTime = document.getElementById('spTime');
    var spClose = document.getElementById('spClose');

    if (!toast) return;

    function showNext() {
      var b = buyers[idx];
      if (spName) spName.textContent = b.name;
      if (spProd) spProd.textContent = b.prod;
      if (spTime) spTime.textContent = b.time;
      toast.classList.add('show');

      setTimeout(function() {
        toast.classList.remove('show');
      }, 6000);

      idx = (idx + 1) % buyers.length;
    }

    if (spClose) {
      spClose.addEventListener('click', function(e) {
        e.stopPropagation();
        toast.classList.remove('show');
      });
    }

    setTimeout(function() {
      showNext();
      setInterval(showNext, 18000);
    }, 6000);
  })();
})();
"""


def pixel_head(principale=True):
    """Pixel de Meta: PageView en todas las páginas; en la landing también ViewContent y el clic al checkout.
    Con CHECKOUT el clic manda InitiateCheckout; sin checkout el botón solo baja a #offerta y va como ClickCTA."""
    if not PIXEL:
        return ""
    clic = "fbq('track','InitiateCheckout',FB)" if CHECKOUT else "fbq('trackCustom','ClickCTA',FB)"
    eventi = (f"""var FB={{content_ids:['kit-pelletteria-facile'],content_name:'Kit Pelletteria Facile · 3 volumi',content_type:'product',value:{PREZZO.replace(',', '.')},currency:'EUR',num_items:1}};
fbq('track','ViewContent',FB);
document.addEventListener('click',function(ev){{var a=ev.target.closest&&ev.target.closest('a.btn[data-co]');if(a){clic};}},true);""" if principale else "")
    return f"""<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;
s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','{PIXEL}');fbq('track','PageView');
{eventi}
</script>
<noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={PIXEL}&ev=PageView&noscript=1" alt=""></noscript>"""


def clarity_head():
    if not CLARITY:
        return ""
    return f"""<script type="text/javascript">
(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","{CLARITY}");
</script>"""


def head(title, desc, path, extra=""):
    robots = "noindex, nofollow" if ANTEPRIMA else "index, follow"
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#1c130c">
<link rel="canonical" href="{SITO}{path}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="icon" href="{FAVICON}" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Pelletteria Facile">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITO}{path}">
<meta property="og:image" content="{SITO}/img/og.jpg">
{FONTS}
<style>{CSS}</style>
{extra}
{clarity_head()}
</head>"""


def marchio():
    return '<div class="marchio"><span>Pelletteria Facile</span><i class="tricolore"><i></i><i></i><i></i></i></div>'


def bottone(testo, grande=True, href=None):
    """Botón de etiqueta. Sin href va al checkout (data-co: el pixel cuenta ese clic); con href es un ancla de la página."""
    cls = "btn btn-grande" if grande else "btn"
    co = "" if href else " data-co"
    return f'<a class="{cls}" href="{e(href or CTA)}"{co}>{ICO["tag"]}<span>{testo}</span></a>'


FIDUCIA = (f'<p class="fiducia"><span>{ICO["lock"]}Pagamento sicuro</span>'
           f'<span>{ICO["bolt"]}Accesso immediato</span><span>{ICO["shield"]}Garanzia 30 giorni</span></p>')


def sezione_volumi():
    """Una caja por volumen: portada, datos y todos sus modelos en un deslizable."""
    out = []
    for v in VOLUMI:
        cop = f'copertine/{v["slug"]}.webp'
        items = "".join(f'<figure><img src="img/miniature/{v["slug"]}-{k:02d}.webp" alt="{e(n)}" width="300" height="300" '
                        f'loading="lazy" decoding="async"><figcaption>{e(n)}</figcaption></figure>'
                        for k, n in enumerate(NOMI[v["num"]], 1))
        out.append(f'<article class="volume"><img class="vol-cop" src="img/{cop}" alt="La copertina del volume {e(v["titolo"])}" '
                   f'{wh(cop)} loading="lazy" decoding="async">'
                   f'<div class="vol-testa"><h3>{e(v["titolo"])}</h3><p class="vol-num"><b>{v["modelli"]} modelli</b> · {v["pagine"]} pagine</p>'
                   f'<p>{e(v["sotto"])}</p></div>'
                   f'<div class="scorri" data-scorri><div class="scorri-box">'
                   f'<button type="button" class="scorri-freccia prev" aria-label="Modelli precedenti">‹</button>'
                   f'<div class="scorri-traccia mini">{items}</div>'
                   f'<button type="button" class="scorri-freccia next" aria-label="Modelli successivi">›</button></div>'
                   f'<div class="scorri-piede">{AVVISO}<span class="scorri-barra" aria-hidden="true"><i></i></span></div></div></article>')
    return "".join(out)


def righe_volumi():
    return "".join(f'<li><span class="c">{e(v["titolo"])}</span><span class="m">{v["modelli"]} modelli · {v["pagine"]} pagine '
                   f'<i>({e(v["breve"])})</i></span></li>' for v in VOLUMI)


AVVISO = '<span class="scorri-hint" aria-hidden="true">Scorri<i>›</i><i>›</i><i>›</i></span>'


def sfoglia():
    """Pestañas de modelos + carrusel de páginas con puntos y contador."""
    schede, pannelli = [], []
    for k, m in enumerate(SFOGLIA):
        on = k == 0
        sel = "true" if on else "false"
        schede.append(f'<button type="button" role="tab" class="scheda" id="tab-{m["slug"]}" aria-controls="pan-{m["slug"]}" '
                      f'aria-selected="{sel}" tabindex="{0 if on else -1}"><img src="{m.get("mini") or f"img/modelli/{m['n']:02d}.webp"}" alt="" '
                      f'width="40" height="40" decoding="async"><span><b>{e(m["breve"])}</b><small>{e(m["tipo"])}</small></span></button>')
        fogli, punti = [], []
        for n, (tit, dida) in enumerate(m["pagine"], 1):
            rel = f'sfoglia/{m["slug"]}/{n}'
            titolo = f'{m["nome"]} · {tit}'
            fogli.append(f'<figure class="foglio"><button type="button" data-grande="img/{rel}.webp" data-titolo="{e(titolo)}" '
                         f'aria-label="Apri la pagina: {e(titolo)}"><div class="cornice"><img src="img/{rel}-s.webp" '
                         f'alt="{e(m["nome"])}, pagina vera: {e(tit)}" {wh(rel + "-s.webp")} loading="lazy" decoding="async"></div></button>'
                         f'<figcaption><b><i>{n}</i>{e(tit)}</b><span>{e(dida)}</span></figcaption></figure>')
            cur = ' aria-current="true"' if n == 1 else ' aria-current="false"'
            punti.append(f'<button type="button" aria-label="Vai alla pagina {n}"{cur}></button>')
        nasc = "" if on else " hidden"
        pannelli.append(f'<div class="pannello" role="tabpanel" id="pan-{m["slug"]}" aria-labelledby="tab-{m["slug"]}" data-gruppo data-scorri{nasc}>'
                        f'<p class="giostra-testa"><b>{e(m["nome"])}</b> · {e(m["info"])}</p><div class="giostra">'
                        f'<button type="button" class="freccia prev" aria-label="Pagina precedente">‹</button>'
                        f'<div class="binario">{"".join(fogli)}</div>'
                        f'<button type="button" class="freccia next" aria-label="Pagina successiva">›</button></div>'
                        f'<div class="paginazione">{AVVISO}<div class="punti">{"".join(punti)}</div>'
                        f'<span class="conta" aria-live="polite">1 / {len(fogli)}</span></div></div>')
    return (f'<div class="scorri scorri-schede" data-scorri><div class="scorri-box">'
            f'<div class="scorri-traccia schede" role="tablist" aria-label="Scegli il modello">{"".join(schede)}</div></div>'
            f'<div class="scorri-piede"><span class="scorri-hint" aria-hidden="true">Scorri: ci sono altri modelli'
            f'<i>›</i><i>›</i><i>›</i></span></div></div>' + "".join(pannelli))


def chat():
    """Carrusel de mensajes de alumnos (traducidos): se desliza a mano o con las flechas; toque = ampliar."""
    if not CHAT:
        return ""
    items = "".join(f'<figure><button type="button" data-grande="img/clienti/wa-{n}.webp" '
                    f'data-titolo="Messaggio di un allievo" aria-label="Ingrandisci il messaggio {k}">'
                    f'<img src="img/clienti/wa-{n}-s.webp" alt="Messaggio WhatsApp tradotto dallo spagnolo. {e(alt)}" '
                    f'{wh(f"clienti/wa-{n}-s.webp")} loading="lazy" decoding="async"></button></figure>'
                    for k, (n, alt) in enumerate(CHAT, 1))
    return (f'<section class="crei" aria-label="Messaggi degli allievi" data-gruppo><div class="wrap"><p class="crei-tit">Cosa hanno creato i nostri allievi</p>'
            f'<div class="scorri" data-scorri><div class="scorri-box">'
            f'<button type="button" class="scorri-freccia prev" aria-label="Messaggio precedente">‹</button>'
            f'<div class="scorri-traccia chat">{items}</div>'
            f'<button type="button" class="scorri-freccia next" aria-label="Messaggio successivo">›</button></div>'
            f'<div class="scorri-piede">{AVVISO}<span class="scorri-barra" aria-hidden="true"><i></i></span></div>'
            f'</div><p class="chat-nota">Messaggi WhatsApp di allievi del nostro corso, tradotti dallo spagnolo.</p></div></section>')


def per_modello():
    v = float(PREZZO.replace(",", ".")) / N
    if v < 1:
        return f"meno di {math.ceil(v * 100)} centesimi a modello"
    return "meno di 2€ a modello" if v < 2 else f"{v:.2f}€ a modello".replace(".", ",")


def testimonianze():
    if not TESTIMONIANZE:
        return ""
    cards = "".join(f'<figure class="testim"><img src="{e(t["foto"])}" alt="Il lavoro di {e(t["nome"])}: {e(t["modello"])}" '
                    f'loading="lazy" decoding="async"><blockquote>{e(t["testo"])}</blockquote>'
                    f'<figcaption><b>{e(t["nome"])}</b> · {e(t["citta"])} · {e(t["modello"])}</figcaption></figure>'
                    for t in TESTIMONIANZE)
    return (f'<section class="sez" aria-label="Lavori dei clienti"><div class="wrap"><div class="titolo">'
            f'<span class="occhiello">Dai clienti</span><h2>Cosa Hanno <span class="accento">Creato</span></h2></div>'
            f'<div class="testimonianze">{cards}</div></div></section>')


FAQ = [
    ("Come riceverò il kit?",
     "Subito dopo l'acquisto ricevi un'email con i 3 volumi in PDF: li scarichi e li stampi, oppure li consulti da telefono, tablet o computer."),
    ("Cosa c'è nei 3 volumi?",
     f"Borse e Zaini (39 modelli), Portafogli, portacarte e portamonete (38 modelli) e Cinture (4 modelli): {N} modelli e {PAGINE} pagine in tutto. "
     "Ogni modello ha la foto del pezzo finito e le sue tavole da stampare; i progetti più completi riportano anche misure, pelle, minuteria e strumenti."),
    ("Il pagamento è unico?",
     f"Sì: {PREZZO}€ una volta sola. Nessun abbonamento, nessun addebito ricorrente."),
    ("Posso stampare le tavole a casa?",
     "Sì. Quasi tutte le tavole sono in formato A4 (nel volume Borse e Zaini anche US Letter) e si stampano con una stampante normale, al 100%, senza «adatta alla pagina». "
     "La prima tavola delle cinture è in A3. Prima di stampare misuri il riferimento di scala: se coincide con il righello, la stampa è giusta."),
    ("Serve una macchina da cucire?",
     "Gli strumenti indicati nei progetti sono quelli da banco: cutter, tappetino da taglio, aghi e filo cerato, fustelle e mazzuolo. "
     "I progetti più completi elencano quelli che servono."),
    ("La pelle e la minuteria sono incluse?",
     "No, il kit è in PDF. I progetti più completi ti dicono che pelle usare, di che spessore e quanta, e quali fibbie, anelli e chiusure comprare: così prendi solo quello che serve."),
    ("Sono alle prime armi: fa per me?",
     "Sì, se hai un minimo di manualità. Il kit non è un corso video: ti dà i cartamodelli pronti, "
     "e le pagine «Prima di iniziare» di ogni volume spiegano come stampare e preparare il lavoro. Per il primo lavoro scegli il modello con meno pezzi."),
    ("In quanto tempo realizzo il primo pezzo?",
     "Dipende dal modello e dalla tua manualità: un pezzo con pochi elementi si fa in pochi giorni, una borsa strutturata richiede più tempo. "
     "Se parti da un progetto completo trovi prima materiali, minuteria e strumenti, così prepari tutto e non ti fermi a metà."),
    ("Posso vendere quello che realizzo?",
     "Sì. La licenza ti permette di realizzare e vendere i pezzi in pelle che crei con questi modelli. Non puoi invece condividere o rivendere i file."),
    ("Le misure sono in centimetri?",
     "Sì. In alcune tavole trovi anche i pollici, accanto ai centimetri."),
    ("E se il kit non fa per me?",
     f"Hai 30 giorni per chiedere il rimborso: scrivi a {EMAIL} e ti restituiamo il 100%, senza domande."),
]


def faq_html():
    return "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQ)


def faq_schema():
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)


def pagina_principale():
    titolo = "Pelletteria Facile · Impara a Creare Prodotti in Pelle e Inizia a Venderli in Meno di 15 Giorni"
    desc = (f"Il kit Pelletteria Facile: 3 volumi in PDF con {N} modelli di borse, zaini, portafogli e cinture in pelle, "
            f"con le tavole da stampare a casa e la licenza per vendere i pezzi che crei. {PREZZO}€, garanzia 30 giorni.")
    return head(titolo, desc, "/", pixel_head() + f'\n<script type="application/ld+json">{faq_schema()}</script>') + f"""
<body>
<div class="sp-toast" id="spToast" role="status" aria-live="polite">
  <button class="sp-close" id="spClose" aria-label="Chiudi">×</button>
  <span class="sp-mini"><img id="spShot" src="img/hero.webp" alt="Kit Pelletteria Facile"></span>
  <div class="sp-txt">
    <span class="sp-name" id="spName">Chiara da Milano</span>
    <span class="sp-prod" id="spProd">Kit Completo · 3 Volumi (81 Modelli)</span>
    <span class="sp-meta"><span class="ok">✔ Accesso confermato</span> · <span id="spTime">fa 4 minuti</span></span>
  </div>
</div>
<div class="promo" role="status" aria-live="off">
  <div class="promo-in">
    <span class="promo-txt">Offerta di lancio</span>
    <span class="promo-time">Valida fino a oggi, <span class="promo-clock" id="oggi"></span></span>
  </div>
</div>

<header class="hero cuoio">
  <div class="wrap hero-in">
    <div class="hero-txt">
      {marchio()}
      <span class="occhiello">3 volumi in PDF · {N} modelli</span>
      <h1>Impara a Creare Prodotti in Pelle <em>e Inizia a Venderli in Meno di 15 Giorni</em></h1>
      <p class="sub">{N} cartamodelli di borse, zaini, portafogli e cinture, pronti da stampare a casa.</p>
      {bottone("Voglio iniziare a creare", href="#offerta")}
      {FIDUCIA}
    </div>
    <div class="hero-img">
      <img src="img/hero.webp" alt="Le copertine dei 3 volumi del kit: 39 modelli di borse e zaini, 38 modelli di portafogli, portacarte e portamonete, 4 modelli di cinture"
           {wh("hero.webp")} fetchpriority="high" decoding="async">
    </div>
  </div>
</header>

<section class="dati" aria-label="Il kit in breve">
  <div class="wrap">
    <ul>
      <li>{ICO["forbici"]}<strong>{N} modelli</strong><small>borse, zaini, portafogli e cinture</small></li>
      <li>{ICO["libro"]}<strong>3 volumi PDF</strong><small>{PAGINE} pagine in tutto</small></li>
      <li>{ICO["righello"]}<strong>Scala 1:1</strong><small>tavole da stampare a casa, al 100%</small></li>
      <li>{ICO["tag"]}<strong>Puoi venderli</strong><small>la licenza copre i pezzi che crei</small></li>
    </ul>
  </div>
</section>

{chat()}

<section class="sez sez-alt" id="sfoglia" aria-label="Sfoglia i progetti del kit">
  <div class="wrap">
    <div class="titolo">
      <span class="occhiello">Dentro il kit</span>
      <h2>Sfoglia i <span class="accento">Progetti</span> del Kit</h2>
      <p>Pagine vere dei 3 volumi, modello per modello. Scegli un modello, scorri le pagine e toccane una per vederla in grande.</p>
    </div>
    {sfoglia()}
    <div class="cta-mezzo">{bottone(f"Voglio questi cartamodelli · {PREZZO}€", href="#offerta")}{FIDUCIA}</div>
  </div>
</section>

<section class="sez" id="perche" aria-label="Perché il kit">
  <div class="wrap">
    <div class="titolo">
      <span class="occhiello">In meno di 15 giorni</span>
      <h2>Crea Prodotti in Pelle <span class="accento">e Inizia a Venderli</span></h2>
    </div>
      <ul class="vantaggi chiari">
        <li>{ICO["monete"]}<div><b>Prodotti da vendere, fatti con le tue mani</b>
          <span>Borse, portafogli e cinture in pelle: pezzi che si comprano volentieri fatti a mano, e la licenza ti permette di venderli.</span></div></li>
        <li>{ICO["tocco"]}<div><b>Anche da zero, 100% pratico</b>
          <span>Parti dalla guida «Prima di iniziare» e da un modello con pochi pezzi: già dal primo lavoro hai qualcosa da mostrare.</span></div></li>
        <li>{ICO["razzo"]}<div><b>Pronto a vendere prima di finire</b>
          <span>Non aspetti di aver fatto tutto il kit: ogni pezzo finito è già un prodotto da mettere in vendita.</span></div></li>
      </ul>
  </div>
</section>

<section class="sez sez-alt">
  <div class="wrap due">
    <div class="testo">
      <span class="occhiello">Prima di tagliare</span>
      <h2>Perché le Misure Tornano <span class="accento">Prima Ancora di Tagliare</span></h2>
      <p>Un cartamodello sbagliato di pochi millimetri lo scopri solo alla fine: quando i pezzi non combaciano e la pelle ormai è tagliata.</p>
      <p>Per questo ogni volume ha il suo <strong>controllo di stampa</strong>. Stampi la pagina al 100%, senza «adatta alla pagina»,
        misuri il quadrato di controllo (o il righello stampato sulla tavola, dove c'è) e sai subito se la stampa è giusta. Se non coincide, correggi le impostazioni della stampante —
        <strong>prima di toccare la pelle</strong>.</p>
      <p>Poi unisci le tavole seguendo lettere, numeri e frecce di raccordo. I fori di cucitura sono già segnati sul cartamodello: non devi tracciarli tu.</p>
      <div class="nota">{ICO["righello"]}Prima controlli la scala. Poi tagli.</div>
    </div>
    <figure class="immagine libera">
      <img src="img/misure.webp" alt="Due tavole vere del kit: le ali dello Zaino Gufo e una tavola della Borsa Street Chic, con i fori di cucitura segnati e il righello di scala ingrandito"
           {wh("misure.webp")} loading="lazy" decoding="async">
      <figcaption>Tavole vere del kit: fori di cucitura già segnati e righello di scala stampato sulla tavola.</figcaption>
    </figure>
  </div>
</section>

<section class="sez" aria-label="Confronto">
  <div class="wrap">
    <div class="titolo">
      <span class="occhiello">La differenza</span>
      <h2>La Differenza Si Vede <span class="accento">al Primo Taglio</span></h2>
    </div>
    <div class="confronto">
      <div class="lato senza">
        <h3>Senza cartamodello</h3>
        <ul>
          <li>{ICO["no"]}Disegni il modello a occhio, partendo da una foto</li>
          <li>{ICO["no"]}Metti in pausa un video ogni dieci secondi</li>
          <li>{ICO["no"]}Sprechi pelle per un pezzo che non combacia</li>
        </ul>
        <div class="schizzo" aria-hidden="true">{SCHIZZO}</div>
      </div>
      <div class="lato con">
        <h3>Con Pelletteria Facile</h3>
        <ul>
          <li>{ICO["ok"]}Le tavole sono già disegnate, in scala 1:1</li>
          <li>{ICO["ok"]}Nei progetti completi pelle, spessori e minuteria sono già scritti</li>
          <li>{ICO["ok"]}Controlli la scala prima di tagliare</li>
        </ul>
        <div class="cornice"><img src="img/pagine/tavola-1-1.webp" alt="Una tavola del cartamodello in scala 1:1 con i fori di cucitura segnati"
             {wh("pagine/tavola-1-1.webp")} loading="lazy" decoding="async"></div>
      </div>
    </div>
  </div>
</section>

<section class="sez sez-alt" id="modelli" aria-label="I modelli del kit">
  <div class="wrap">
    <div class="titolo">
      <span class="occhiello">Il kit</span>
      <h2>I 3 Volumi <span class="accento">del Kit</span></h2>
      <p>{N} modelli in tutto. Ogni modello ha la foto del pezzo finito e le sue tavole da stampare; i progetti più completi riportano anche misure, pelle, minuteria e strumenti.</p>
    </div>
    <div class="volumi">{sezione_volumi()}</div>
    <div class="cta-mezzo">{bottone(f"Voglio il kit a {PREZZO}€", href="#offerta")}<p class="al-modello">3 volumi, {N} modelli: {per_modello()}.</p></div>
  </div>
</section>

<section class="sez">
  <div class="wrap due inversa">
    <div class="testo">
      <span class="occhiello">Il metodo</span>
      <h2>E Se Esistesse un Modo <span class="accento">Più Semplice?</span></h2>
      <p class="immagina">Immagina questo:</p>
      <p class="contrario">Invece di passare la serata a ricopiare un modello da una foto, ritagliarlo, provarlo sulla pelle e ricominciare perché i pezzi non tornano...</p>
      <p class="meglio">...apri il progetto, stampi le tavole, misuri il quadrato di controllo e sei pronto a tagliare.</p>
      <p>Nei progetti completi pelle, spessori, minuteria e strumenti sono già scritti. E la sequenza è sempre la stessa:</p>
      <ol class="passi">
        <li><b>1</b>Prepara il cartamodello</li>
        <li><b>2</b>Riporta e taglia</li>
        <li><b>3</b>Prepara fori e minuteria</li>
        <li><b>4</b>Assembla e rifinisci</li>
      </ol>
      <p>È esattamente questo che fa Pelletteria Facile. Non è una raccolta di foto da copiare: <strong>ogni modello ha le sue tavole già disegnate</strong>,
        da stampare e tagliare.</p>
    </div>
    <div class="immagine cornice">
      <img src="img/pagine/tecniche-base.webp" alt="La pagina «Tecniche di base»: prepara, riporta e taglia, prepara fori e minuteria, assembla e rifinisci"
           {wh("pagine/tecniche-base.webp")} loading="lazy" decoding="async">
    </div>
  </div>
</section>

<section class="sez sez-alt" aria-label="Cosa riceverai">
  <div class="wrap">
    <div class="titolo">
      <span class="occhiello">Cosa riceverai</span>
      <h2>Ecco Cosa Riceverai <span class="accento">con il Kit</span></h2>
    </div>
    <div class="ricevi">
      <div class="blocco">
        <h3>I 3 volumi · {N} modelli</h3>
        <ul class="righe">{righe_volumi()}</ul>
      </div>
      <div class="blocco">
        <h3>Nei volumi trovi</h3>
        <ul class="spunte">
          <li>{ICO["ok"]}La foto del modello finito, per ogni progetto</li>
          <li>{ICO["ok"]}Le tavole del cartamodello da stampare a casa, al 100%</li>
          <li>{ICO["ok"]}Il controllo di stampa da misurare prima di tagliare</li>
          <li>{ICO["ok"]}L'indice dei progetti e la guida «Prima di iniziare» in ogni volume</li>
          <li>{ICO["ok"]}Nei progetti completi: misure, pelle e spessori</li>
          <li>{ICO["ok"]}Nei progetti completi: minuteria e strumenti</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sez" aria-label="Per chi è">
  <div class="wrap">
    <div class="titolo">
      <span class="occhiello">Per chi è</span>
      <h2>Questo Kit <span class="accento">Fa per Te?</span></h2>
    </div>
    <div class="profili">
      <div class="profilo">{ICO["ago"]}<h3>Sai cucire, ma la pelle ti blocca</h3>
        <p>Ago e filo li sai usare, ma davanti a una pelle intera non sai da dove partire. Qui il cartamodello c'è già: stampi, controlli la scala e tagli.</p></div>
      <div class="profilo">{ICO["forbici"]}<h3>Lavori già la pelle e cerchi modelli nuovi</h3>
        <p>Borse, zaini, portafogli e cinture con le tavole pronte: meno ore al tavolo da disegno, più ore al banco.</p></div>
      <div class="profilo">{ICO["tag"]}<h3>Vuoi vendere le tue creazioni</h3>
        <p>Borse, portafogli e cinture fatti a mano si vendono ai mercatini dell'artigianato, su Etsy e su Instagram. Con il kit parti da cartamodelli già disegnati, e i pezzi che crei puoi venderli.</p></div>
    </div>
  </div>
</section>

<section class="sez cuoio" id="piano" aria-label="Il piano di 15 giorni">
  <div class="wrap">
    <div class="titolo">
      <span class="occhiello">Dal kit alla vendita</span>
      <h2>Il Tuo Piano di <span class="accento">15 Giorni</span></h2>
      <p>Un modo semplice per organizzarti: dai pezzi più facili a quelli più impegnativi, fino ai primi annunci.</p>
    </div>
    <ol class="piano">
      <li><span class="giorni">Giorni 1–2</span><b>Prepari il banco</b>
        <p>Scegli il modello, stampi le tavole, controlli la scala e prepari pelle, minuteria e strumenti.</p></li>
      <li><span class="giorni">Giorni 3–6</span><b>Il primo pezzo</b>
        <p>Parti da un modello con pochi pezzi, come un portafoglio o una cintura, e segui la sequenza: prepara, riporta, taglia, assembla.</p></li>
      <li><span class="giorni">Giorni 7–12</span><b>Una borsa o uno zaino</b>
        <p>Passi a un modello più ricco del kit, con misure, materiali e tavole 1:1 già pronti.</p></li>
      <li><span class="giorni">Giorni 13–15</span><b>I primi annunci</b>
        <p>Fotografi i pezzi finiti e li metti in vendita: mercatini dell'artigianato, Etsy, Instagram. La licenza te lo permette.</p></li>
    </ol>
    <p class="nota-piano">È un piano indicativo: i tempi dipendono dal modello che scegli, dai materiali e dalla tua manualità.</p>
    <div class="cta-mezzo">{bottone(f"Voglio iniziare · {PREZZO}€", href="#offerta")}</div>
  </div>
</section>

{testimonianze()}

<section class="sez" id="offerta" aria-label="L'offerta">
  <div class="wrap">
    <div class="titolo">
      <span class="occhiello">Ricapitolando</span>
      <h2>Ricapitolando: Ecco <span class="accento">Cosa Ricevi</span></h2>
    </div>
    <div class="offerta">
      <div class="offerta-img"><img src="img/hero.webp" alt="Le copertine dei 3 volumi del kit: Borse e Zaini, Portafogli e Cinture"
        {wh("hero.webp")} loading="lazy" decoding="async"></div>
      <ul class="spunte">
        <li>{ICO["ok"]}<span><strong>3 volumi in PDF, {N} modelli:</strong> {e(elenco_kit())}</span></li>
        <li>{ICO["ok"]}<span>Per ogni modello la foto del pezzo finito e le tavole da stampare; nei progetti completi anche misure, materiali, minuteria e strumenti</span></li>
        <li>{ICO["ok"]}<span><strong>La licenza per vendere</strong> i pezzi in pelle che crei con questi modelli</span></li>
        <li>{ICO["ok"]}<span>La guida «Prima di iniziare» e il controllo di stampa in ogni volume</span></li>
        <li>{ICO["ok"]}<span>PDF in alta risoluzione: stampi le tavole tutte le volte che vuoi</span></li>
        <li>{ICO["ok"]}<span>Consegna via email: accesso immediato, senza spedizioni né attese</span></li>
        <li>{ICO["ok"]}<span>Garanzia di 30 giorni senza domande: provi senza rischio</span></li>
      </ul>
      <div class="prezzo"><small>Offerta di lancio</small><strong>{PREZZO}€</strong><span>Pagamento unico · 3 volumi, {N} modelli: {per_modello()}</span></div>
      {bottone("Sì, voglio il kit")}
      {FIDUCIA}
    </div>
  </div>
</section>

<section class="sez sez-alt" aria-label="Garanzia">
  <div class="wrap">
    <div class="garanzia">
      <div class="sigillo"><div><b>30</b><span>Giorni<br>garanzia</span></div></div>
      <div>
        <h2>Garanzia «Prova Senza Rischio»: <span class="accento">30 Giorni</span></h2>
        <p>Hai 30 giorni interi per provare il kit. Se entro quel periodo senti che non ti è servito, o semplicemente non era quello che ti aspettavi,
          <strong>ti restituiamo il 100% della spesa</strong>.</p>
        <p class="tre">Senza domande · Senza clausole in piccolo · Senza complicazioni</p>
        <p>Il rischio è zero. La decisione è tua.</p>
      </div>
    </div>
  </div>
</section>

<section class="sez" aria-label="Domande frequenti">
  <div class="wrap">
    <div class="titolo">
      <span class="occhiello">Domande</span>
      <h2>Domande <span class="accento">Frequenti</span></h2>
    </div>
    <div class="faq">{faq_html()}</div>
  </div>
</section>

<section class="sez cuoio finale" aria-label="Ultima cosa">
  <div class="wrap stretta">
    <h2>Un'Ultima Cosa Prima Che Tu Decida...</h2>
    <p class="grande">Il tuo primo prodotto in pelle da vendere non deve partire da un foglio bianco. E può essere in vendita in meno di 15 giorni.</p>
    <p>Non devi ricopiare un modello da una foto, né sprecare pelle per un pezzo che non combacia.
      E di sicuro non devi rinunciare perché «la pelle è difficile».</p>
    <p>C'è un modo più semplice, ed è a un clic di distanza: {N} cartamodelli già disegnati, da stampare in scala 1:1. Ora tocca a te.</p>
    <ul class="riassunto">
      <li>Spesa unica: <b>{PREZZO}€</b></li>
      <li><b>{N} modelli</b>: {per_modello()}</li>
      <li>Garanzia: <b>30 giorni</b> senza domande</li>
      <li>Accesso <b>immediato</b> via email</li>
    </ul>
    {bottone(f"Voglio il kit a {PREZZO}€")}
    <p class="dopo">Il kit arriva via email, subito dopo il pagamento.</p>
  </div>
</section>

{footer()}

<dialog class="visore" id="visore" aria-label="Pagina ingrandita">
  <button class="chiudi" type="button" aria-label="Chiudi">×</button>
  <button class="ctrl prev" type="button" aria-label="Pagina precedente">‹</button>
  <img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="">
  <p></p>
  <button class="ctrl next" type="button" aria-label="Pagina successiva">›</button>
</dialog>

<script>{JS}</script>
</body>
</html>
"""


def footer():
    return f"""<footer>
  <div class="wrap">
    {marchio()}
    <p>© 2026 Pelletteria Facile · Tutti i diritti riservati</p>
    <nav aria-label="Pagine legali"><a href="/rimborso">Politica di Rimborso</a><a href="/privacy">Privacy</a><a href="/termini">Termini</a><a href="/assistenza">Assistenza</a><a href="https://cartamodelli.studiofacilebook.com/" target="_blank" rel="noopener">Tutti i prodotti</a></nav>
    <p>{e(SOCIETA)} · {e(INDIRIZZO)}</p>
  </div>
</footer>"""


# ------------------------------------------------------------ páginas legales
LEGALI_CSS = """
.legale{padding:40px 0 70px}
.legale .carta{max-width:780px;margin:0 auto;background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:30px 22px;box-shadow:0 14px 34px rgba(28,19,12,.1)}
.legale h1{font-size:clamp(28px,6vw,40px);text-transform:uppercase;margin-bottom:8px}
.legale h2{font-size:21px;text-transform:uppercase;margin:28px 0 10px;color:var(--cognac-d)}
.legale p,.legale li{font-size:16px;color:var(--ink-2)}
.legale ul,.legale ol{padding-left:22px}
.legale .agg{display:block;font-size:13.5px;color:var(--muted);margin-bottom:22px}
.legale .box{margin-top:26px;padding:18px;border-radius:12px;border:1.5px dashed var(--cognac);background:var(--cream)}
.testata{padding:22px 0 18px}.testata a{text-decoration:none}
@media (min-width:900px){.legale .carta{padding:44px 48px}}
"""

LEGALI = {
    "assistenza": ("Assistenza Clienti", f"""
<h1>Assistenza Clienti</h1><span class="agg">Ultimo aggiornamento: {AGG}</span>
<p>Hai una domanda su un acquisto, non hai ricevuto l'email con i PDF o vuoi richiedere un rimborso? Scrivici: rispondiamo entro <strong>24-48 ore lavorative</strong>.</p>
<div class="box"><p><strong>Scrivici via email</strong><br>Indica l'email usata per l'acquisto e, se lo hai, il numero d'ordine.</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<h2>Domande frequenti</h2>
<p><strong>Non ho ricevuto l'email con i PDF.</strong><br>Controlla la cartella spam o promozioni. Se non la trovi, scrivici dall'indirizzo usato per l'acquisto e te la inviamo di nuovo.</p>
<p><strong>Voglio un rimborso.</strong><br>Hai 30 giorni dall'acquisto. Leggi la <a href="/rimborso">Politica di Rimborso</a> oppure scrivici direttamente.</p>
<p><strong>Posso scaricare e stampare i file più volte?</strong><br>Sì. Puoi scaricare i PDF e stampare i cartamodelli tutte le volte che vuoi, su qualsiasi dispositivo.</p>
<h2>Chi siamo</h2>
<p>Pelletteria Facile è un marchio di <strong>{SOCIETA}</strong>, {INDIRIZZO}.</p>
"""),
    "rimborso": ("Politica di Rimborso e Garanzia", f"""
<h1>Politica di Rimborso e Garanzia</h1><span class="agg">Ultimo aggiornamento: {AGG}</span>
<p>Vogliamo che tu possa provare i cartamodelli di <strong>Pelletteria Facile</strong> in totale tranquillità.</p>
<h2>1. Natura del prodotto digitale</h2>
<p>I nostri prodotti sono <strong>beni digitali</strong> (cartamodelli e indicazioni in PDF) ad accesso immediato: dopo il pagamento ricevi via email i link per scaricarli.</p>
<h2>2. Garanzia di rimborso di 30 giorni</h2>
<p>Offriamo una <strong>garanzia di rimborso al 100% valida per 30 giorni</strong> dalla data di acquisto: se il materiale non soddisfa le tue aspettative, o per qualsiasi altro motivo, senza alcuna giustificazione richiesta.</p>
<h2>3. Come richiedere un rimborso</h2>
<ol><li>Invia un'email a <a href="mailto:{EMAIL}">{EMAIL}</a> con l'oggetto <em>«Richiesta di rimborso»</em>.</li>
<li>Indica l'indirizzo email usato per l'acquisto e, se lo hai, il numero d'ordine.</li></ol>
<p>Elaboriamo la richiesta entro <strong>24-48 ore lavorative</strong>.</p>
<h2>4. Tempi e metodo di rimborso</h2>
<p>Il rimborso viene emesso sullo <strong>stesso metodo di pagamento</strong> usato per l'ordine. I tempi di accredito dipendono dal circuito bancario, di solito tra <strong>5 e 10 giorni lavorativi</strong>.</p>
<h2>5. Resi fisici</h2>
<p>Trattandosi di materiale esclusivamente digitale, non è richiesta alcuna restituzione fisica.</p>
"""),
    "privacy": ("Informativa sulla Privacy", f"""
<h1>Informativa sulla Privacy</h1><span class="agg">Ultimo aggiornamento: {AGG}</span>
<p>Questa informativa spiega quali dati personali raccogliamo quando visiti il sito di Pelletteria Facile o acquisti i nostri prodotti digitali, perché li usiamo e quali diritti hai, anche ai sensi del Regolamento (UE) 2016/679 (GDPR).</p>
<h2>1. Titolare del trattamento</h2>
<p><strong>{SOCIETA}</strong> (marchio Pelletteria Facile), {INDIRIZZO}. Contatto: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>2. Quali dati raccogliamo</h2>
<ul><li><strong>Dati dell'ordine:</strong> nome, cognome, indirizzo email, paese e dettagli dell'acquisto.</li>
<li><strong>Dati di pagamento:</strong> sono trattati direttamente dal fornitore dei pagamenti. Non vediamo né conserviamo il numero completo della tua carta.</li>
<li><strong>Dati di navigazione:</strong> pagine visitate, dispositivo, indirizzo IP approssimativo e interazioni con il sito, raccolti tramite cookie e strumenti simili.</li>
<li><strong>Comunicazioni:</strong> i messaggi che ci invii via email.</li></ul>
<h2>3. Perché usiamo i dati e su quale base</h2>
<ul><li><strong>Consegnare i prodotti acquistati</strong> e fornire assistenza (esecuzione del contratto).</li>
<li><strong>Gestire pagamenti, rimborsi e prevenzione delle frodi</strong> (esecuzione del contratto e legittimo interesse).</li>
<li><strong>Adempiere a obblighi fiscali e contabili</strong> (obbligo di legge).</li>
<li><strong>Misurare e migliorare il sito e le nostre pubblicità</strong> (consenso, dove richiesto).</li>
<li><strong>Inviarti email sui nostri prodotti</strong>, da cui puoi disiscriverti in qualsiasi momento (legittimo interesse o consenso).</li></ul>
<h2>4. Con chi condividiamo i dati</h2>
<p>Non vendiamo i tuoi dati. Li condividiamo solo con i fornitori che ci aiutano a far funzionare il servizio: la piattaforma di checkout e il fornitore dei pagamenti, il servizio di invio delle email, Meta (Facebook/Instagram) per misurare le campagne pubblicitarie, Microsoft Clarity per capire come viene usato il sito (mappe di calore e registrazioni anonime delle sessioni), e Vercel per l'hosting del sito.</p>
<p>Alcuni di questi fornitori si trovano negli Stati Uniti. I trasferimenti avvengono con le garanzie previste dal GDPR, come le Clausole Contrattuali Standard o il Data Privacy Framework UE-USA.</p>
<h2>5. Per quanto tempo conserviamo i dati</h2>
<p>I dati degli ordini sono conservati per il tempo richiesto dagli obblighi fiscali e contabili. I dati di navigazione e marketing sono conservati per il tempo necessario alle finalità indicate o fino alla revoca del consenso.</p>
<h2>6. Sicurezza</h2>
<p>Il sito usa connessioni cifrate (HTTPS). L'accesso ai dati è limitato alle persone e ai fornitori che ne hanno bisogno per fornire il servizio.</p>
<h2>7. I tuoi diritti</h2>
<p>Puoi chiedere in qualsiasi momento l'accesso, la rettifica, la cancellazione o la portabilità dei tuoi dati, opporti al trattamento o revocare il consenso, scrivendo a <a href="mailto:{EMAIL}">{EMAIL}</a>. Hai anche il diritto di presentare un reclamo all'autorità di controllo del tuo paese (in Italia, il Garante per la protezione dei dati personali).</p>
<h2>8. Minori</h2>
<p>I nostri prodotti sono destinati a persone maggiorenni. Non raccogliamo consapevolmente dati di minori.</p>
<h2>9. Modifiche</h2>
<p>Possiamo aggiornare questa informativa. La data dell'ultimo aggiornamento è indicata in alto.</p>
"""),
    "termini": ("Termini e Condizioni", f"""
<h1>Termini e Condizioni</h1><span class="agg">Ultimo aggiornamento: {AGG}</span>
<p>Questi termini regolano l'uso del sito e l'acquisto dei prodotti digitali Pelletteria Facile, offerti da <strong>{SOCIETA}</strong>, {INDIRIZZO} («noi»). Effettuando un acquisto accetti questi termini.</p>
<h2>1. Prodotti</h2>
<p>Vendiamo cartamodelli e indicazioni di pelletteria in formato digitale (PDF). I modelli inclusi e il numero di pagine sono descritti nella pagina di ogni offerta.</p>
<h2>2. Prezzi e pagamento</h2>
<p>I prezzi sono indicati nella pagina dell'offerta e al checkout. Il pagamento è unico, senza abbonamenti né addebiti ricorrenti.</p>
<h2>3. Consegna</h2>
<p>I prodotti vengono consegnati via email all'indirizzo indicato al momento dell'acquisto, di norma entro pochi minuti.</p>
<h2>4. Garanzia e rimborsi</h2>
<p>Offriamo una garanzia di rimborso di <strong>30 giorni</strong> dalla data di acquisto, alle condizioni descritte nella <a href="/rimborso">Politica di Rimborso</a>.</p>
<h2>5. Licenza d'uso</h2>
<p>Con l'acquisto ricevi una licenza <strong>personale e non trasferibile</strong>. Puoi stampare i cartamodelli tutte le volte che vuoi e <strong>realizzare e vendere i pezzi in pelle</strong> che crei con questi modelli. Non puoi cedere, condividere, rivendere o pubblicare online i file o le pagine.</p>
<h2>6. Uso degli strumenti</h2>
<p>La lavorazione della pelle richiede strumenti taglienti e da percussione. Usali con attenzione e seguendo le indicazioni del produttore. I risultati dipendono dai materiali scelti e dalla manualità di ciascuno.</p>
<h2>7. Responsabilità</h2>
<p>Curiamo con attenzione i contenuti, ma non garantiamo che siano privi di errori o adatti a ogni situazione. Nei limiti consentiti dalla legge, non siamo responsabili per danni derivanti dall'uso del materiale. Restano salvi i diritti inderogabili del consumatore previsti dalla legge applicabile.</p>
<h2>8. Contatti</h2>
<p>Per qualsiasi domanda scrivi a <a href="mailto:{EMAIL}">{EMAIL}</a> oppure visita la pagina <a href="/assistenza">Assistenza</a><a href="https://cartamodelli.studiofacilebook.com/" target="_blank" rel="noopener">Tutti i prodotti</a>.</p>
"""),
}


def pagina_legale(slug, titolo, corpo):
    h = head(f"{titolo} — Pelletteria Facile", f"{titolo} di Pelletteria Facile.", f"/{slug}", pixel_head(principale=False))
    h = h.replace("</style>", LEGALI_CSS + "</style>")
    return h + f"""
<body>
<header class="cuoio testata"><div class="wrap"><a href="/" aria-label="Torna alla pagina principale">{marchio()}</a></div></header>
<main class="legale"><div class="wrap"><div class="carta">{corpo}</div></div></main>
{footer()}
</body>
</html>
"""


def versiona(testo):
    """img/x.webp -> img/x.webp?v=<md5>: las imágenes se cachean 7 días (vercel.json)
    y sin versión el navegador sigue mostrando la vieja cuando se reemplaza."""
    import hashlib, re

    def rep(m):
        path = os.path.join(QUI, "img", m.group(2))
        if not os.path.exists(path):
            return m.group(0)
        return f'{m.group(1)}="img/{m.group(2)}?v={hashlib.md5(open(path, "rb").read()).hexdigest()[:8]}"'
    return re.sub(r'(src|data-grande)="img/([^"?]+)"', rep, testo)


def scrivi(nome, testo):
    with open(os.path.join(QUI, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)


scrivi("index.html", versiona(pagina_principale()))
for slug, (titolo, corpo) in LEGALI.items():
    scrivi(f"{slug}.html", pagina_legale(slug, titolo, corpo))
# /cassa y lo que necesita el checkout propio (assets, api, gracias, post-pago, entrega, tracking) van a la app,
# igual que studiofacile/phlebotomy/vercel.json con /checkout (10/10).
APP = "https://checkout-propio-sepia.vercel.app"
RISCRITTURE = ["/cassa", "/_next/:path*", "/api/:path*", "/gracias", "/oferta/:path*", "/d/:path*", "/t.js"]
scrivi("vercel.json", json.dumps({"cleanUrls": True, "trailingSlash": False,
    "rewrites": [{"source": r, "destination": APP + r} for r in RISCRITTURE],
    "headers": [{"source": "/img/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]}]},
    indent=2) + "\n")
scrivi("robots.txt", "User-agent: *\nDisallow: /\n" if ANTEPRIMA else f"User-agent: *\nAllow: /\nSitemap: {SITO}/sitemap.xml\n")
scrivi("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + "".join(f"  <url><loc>{SITO}/{p}</loc></url>\n" for p in [""] + list(LEGALI)) + "</urlset>\n")

# Favicon como archivo (Google no usa el data: URI del <link>): sale del ícono de la marca.
ICONA = os.path.join(QUI, "..", "Marca", "pelletteria-icon.png")
if os.path.exists(ICONA):
    from PIL import Image
    ic = Image.open(ICONA).convert("RGBA")
    ic.save(os.path.join(QUI, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    ic.resize((192, 192), Image.LANCZOS).save(os.path.join(QUI, "icon-192.png"))
    ic.resize((180, 180), Image.LANCZOS).save(os.path.join(QUI, "apple-touch-icon.png"))
print(f"ok · {N} modelli · {PAGINE} pagine · noindex={ANTEPRIMA} · checkout={CHECKOUT}")
