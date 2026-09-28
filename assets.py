# -*- coding: utf-8 -*-
"""Imágenes de la landing, sacadas del PDF real (nada generado con IA).

- img/modelli/NN.webp : la foto del modelo terminado de cada uno de los 39
  proyectos (la imagen más grande de su página de apertura), recorte 4:5.
- img/pagine/*.webp   : páginas del proyecto Rosaleen para la galería, más
  «Tecniche di base» y «Controllo di stampa».
- img/hero.webp       : abanico de tres páginas reales (modelo terminado,
  esquema de piezas, tabla 1:1).
- img/og.jpg          : imagen para compartir (1200x630).

    python -u assets.py
"""
import json, os, re, sys
import fitz
from PIL import Image, ImageDraw, ImageFilter

QUI = os.path.dirname(os.path.abspath(__file__))
EB = os.path.join(QUI, "..", "Ebooks")
IMG = os.path.join(QUI, "img")
# Los 3 volúmenes del kit. El Vol. 1 nuevo es igual al viejo salvo la portada.
d = fitz.open(os.path.join(EB, "Pelletteria Facile - Vol 1 - Borse e Zaini.pdf"))
d2 = fitz.open(os.path.join(EB, "Pelletteria Facile - Vol 2 - Portafogli.pdf"))
d4 = fitz.open(os.path.join(EB, "Pelletteria Facile - Vol 4 - Cinture.pdf"))


def pagina(n, larghezza, doc=None):
    """Página n (1-based) de `doc` (Vol. 1 por defecto) rasterizada a `larghezza` px."""
    p = (doc or d)[n - 1]
    zoom = larghezza / p.rect.width
    pm = p.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)


FORZA = "--forza" in sys.argv


def salva(im, rel, q=80):
    """Guarda en img/<rel>. Lo que ya existe no se vuelve a codificar (webp method=6 es lento) salvo con --forza."""
    path = os.path.join(IMG, rel)
    if os.path.exists(path) and not FORZA:
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if rel.endswith(".jpg"):
        im.convert("RGB").save(path, quality=q, optimize=True, progressive=True)
    else:
        im.save(path, "WEBP", quality=q, method=6)
    return path


def ritaglio(im, rw, rh):
    """Recorte centrado a la proporción rw:rh."""
    w, h = im.size
    if w / h > rw / rh:
        nw = int(h * rw / rh); x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w * rh / rw); y = max(0, (h - nh) // 2)
    return im.crop((0, y, w, y + nh))


def foto_apertura(doc, pg):
    """Foto del modelo terminado en la página de apertura pg (1-based)."""
    # Descarto el fondo de pergamino (ocupa la página entera) y los píxeles
    # sueltos de 1x1; la foto es la imagen con más píxeles de las que quedan.
    # Su caja puede salirse de la página (la recorta un trazado), por eso la
    # saco del xref y no rasterizando la zona.
    pag = doc[pg - 1].rect
    info = [i for i in doc[pg - 1].get_image_info(xrefs=True)
            if i["xref"] and min(i["width"], i["height"]) > 50
            and not (i["bbox"][0] <= 1 and i["bbox"][1] <= 1
                     and i["bbox"][2] >= pag.width - 1 and i["bbox"][3] >= pag.height - 1)]
    x = max(info, key=lambda i: i["width"] * i["height"])["xref"]
    pix = fitz.Pixmap(doc, x)
    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    smask = doc.extract_image(x).get("smask")
    if smask:   # la 32 tiene la transparencia aparte: sin aplicarla sale negra
        pix = fitz.Pixmap(fitz.Pixmap(pix, 0) if pix.alpha else pix, fitz.Pixmap(doc, smask))
    rgba = Image.frombytes("RGBA" if pix.alpha else "RGB", (pix.width, pix.height), pix.samples)
    foto = Image.new("RGB", rgba.size, "white")
    foto.paste(rgba, (0, 0), rgba if pix.alpha else None)
    return foto


# ------------------------------------------------ 1. foto de cada modelo
toc = [t for t in d.get_toc() if t[2] >= 9]
for k, (_, nome, pg) in enumerate(toc, 1):
    foto = foto_apertura(d, pg)
    if k == 2:   # Street Chic es una página entera rasterizada: recorto la foto a mano
        pm = d[pg - 1].get_pixmap(matrix=fitz.Matrix(4, 4), clip=fitz.Rect(150, 250, 505, 639))
        foto = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    foto = ritaglio(foto, 4, 5).resize((600, 750), Image.LANCZOS)
    salva(foto, f"modelli/{k:02d}.webp", 78)
print("modelli", len(toc))

# ------------------------------------------------ 1b. los 3 volúmenes: miniaturas cuadradas y nombres
# img/miniature/v<vol>-NN.webp (300x300) + _modelli.json con el nombre de cada modelo, en orden.
NOMI = {"1": [re.sub(r"^\d+\s*[·.\-–]?\s*", "", t[1]).strip() for t in toc]}
for k in range(1, len(toc) + 1):
    im = Image.open(os.path.join(IMG, "modelli", f"{k:02d}.webp")).convert("RGB")
    salva(ritaglio(im, 1, 1).resize((300, 300), Image.LANCZOS), f"miniature/v1-{k:02d}.webp", 76)

# Vol. 2: el índice (pág. 3) trae «NN / Nombre / página»; la apertura de cada modelo es esa página.
righe = [r.strip() for r in d2[2].get_text().splitlines() if r.strip()]
v2 = []
for i in range(len(righe) - 2):
    if re.fullmatch(r"\d\d", righe[i]) and not re.fullmatch(r"\d+", righe[i + 1]):
        unita = re.fullmatch(r"(.+?)\s+(\d+)", righe[i + 1])   # a veces nombre y página vienen en la misma línea
        if unita:
            v2.append((int(righe[i]), unita[1], int(unita[2])))
        elif re.fullmatch(r"\d+", righe[i + 2]):
            v2.append((int(righe[i]), righe[i + 1], int(righe[i + 2])))
v2 = sorted(set(v2))
assert len(v2) == 38, len(v2)
NOMI["2"] = [n for _, n, _ in v2]


def foto_visibile(doc, pg):
    """La foto tal como se ve en la página: rasterizo la caja visible de la imagen más grande
    (en el Vol. 2 algunas fotos traen texto o un dibujo fuera del recorte)."""
    p = doc[pg - 1]
    boxes = [fitz.Rect(i["bbox"]) & p.rect for i in p.get_image_info()
             if min(i["width"], i["height"]) > 50 and not fitz.Rect(i["bbox"]).contains(p.rect)]
    box = max(boxes, key=lambda r: r.get_area())
    pm = p.get_pixmap(matrix=fitz.Matrix(3, 3), clip=box, alpha=False)
    return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)


def quadrato(im, x=0.5):
    """Recorte cuadrado; x = posición horizontal del centro (0 izquierda, 1 derecha)."""
    w, h = im.size
    if w <= h:
        return ritaglio(im, 1, 1)
    left = int((w - h) * x)
    return im.crop((left, 0, left + h, h))


SPOSTA = {("2", 11): 0.0}   # la pochette está a la izquierda de la foto
for k, _, pg in v2:
    salva(quadrato(foto_visibile(d2, pg), SPOSTA.get(("2", k), 0.5)).resize((300, 300), Image.LANCZOS), f"miniature/v2-{k:02d}.webp", 76)

# Vol. 4: un modelo por entrada de nivel 1 que empieza con «Cintura».
v4 = [(t[1], t[2]) for t in d4.get_toc() if t[0] == 1 and t[1].startswith("Cintura")]
NOMI["4"] = [n for n, _ in v4]
for k, (_, pg) in enumerate(v4, 1):
    salva(quadrato(foto_visibile(d4, pg)).resize((300, 300), Image.LANCZOS), f"miniature/v4-{k:02d}.webp", 76)
with open(os.path.join(QUI, "_modelli.json"), "w", encoding="utf-8") as f:
    json.dump(NOMI, f, ensure_ascii=False, indent=1)
print("miniature", {v: len(n) for v, n in NOMI.items()})

# Portadas de los 3 volúmenes (caja de cada volumen en la landing)
COPERTINE = {"v1": d, "v2": d2, "v4": d4}
for slug, doc in COPERTINE.items():
    salva(pagina(1, 480, doc), f"copertine/{slug}.webp", 80)

# ------------------------------------------------ 2. páginas de la galería
GALLERIA = {10: "modello-finito", 11: "misure", 12: "materiali", 13: "minuteria",
            14: "strumenti", 15: "controllo-stampa", 16: "schema-pezzi", 17: "tavola-1-1",
            5: "tecniche-base", 3: "indice"}
for n, slug in GALLERIA.items():
    im = pagina(n, 1100)
    salva(im.resize((900, int(im.height * 900 / im.width)), Image.LANCZOS), f"pagine/{slug}.webp", 80)
    salva(im.resize((440, int(im.height * 440 / im.width)), Image.LANCZOS), f"pagine/{slug}-s.webp", 76)
print("pagine", len(GALLERIA))


# ------------------------------------------------ 2b. páginas de cada modelo del kit
# Seis páginas por modelo para la galería con pestañas: terminado, medidas,
# materiales, minuteria, esquema y una tabla 1:1 (Gufo y Street Chic ordenan
# distinto su proyecto). img/sfoglia/<modelo>/<k>.webp y <k>-s.webp
SFOGLIA = {
    "rosaleen": [9, 11, 12, 13, 16, 17],
    "aria": [304, 306, 307, 308, 311, 312],
    "borsone": [256, 258, 259, 260, 263, 292],
    "drew": [414, 416, 417, 418, 421, 422],
    "gufo": [61, 62, 63, 64, 69, 71],
    "street-chic": [38, 39, 40, 41, 45, 46],
}
SFOGLIA_ALTRI = {   # modelos de los otros volúmenes: (documento, páginas)
    "bifold": (d2, [97, 99, 100, 101]),
    "cintura-donna": (d4, [17, 18, 20]),
}
for slug, (doc, pagine) in SFOGLIA_ALTRI.items():
    for k, n in enumerate(pagine, 1):
        im = pagina(n, 1100, doc)
        salva(im.resize((900, int(im.height * 900 / im.width)), Image.LANCZOS), f"sfoglia/{slug}/{k}.webp", 80)
        salva(im.resize((480, int(im.height * 480 / im.width)), Image.LANCZOS), f"sfoglia/{slug}/{k}-s.webp", 76)
for slug, pagine in SFOGLIA.items():
    for k, n in enumerate(pagine, 1):
        im = pagina(n, 1100)
        salva(im.resize((900, int(im.height * 900 / im.width)), Image.LANCZOS), f"sfoglia/{slug}/{k}.webp", 80)
        salva(im.resize((480, int(im.height * 480 / im.width)), Image.LANCZOS), f"sfoglia/{slug}/{k}-s.webp", 76)
print("sfoglia", sum(len(v) for v in SFOGLIA.values()))


# ------------------------------------------------ 3. hero: abanico de páginas
def con_ombra(im, angolo):
    """Página con borde fino y sombra suave, rotada. Devuelve RGBA."""
    pad = 60
    base = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    ombra = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ombra.paste((20, 10, 4, 150), (pad + 10, pad + 22, pad + im.width + 10, pad + im.height + 22))
    ombra = ombra.filter(ImageFilter.GaussianBlur(22))
    base.alpha_composite(ombra)
    base.paste(im.convert("RGBA"), (pad, pad))
    return base.rotate(angolo, resample=Image.BICUBIC, expand=True)


def tablet(im, w, bordo=18, r=34, pad=70):
    """Portada derecha dentro de un marco tipo tablet, con sombra. Devuelve (RGBA, pad)."""
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS).convert("RGBA")
    W, H = w + bordo * 2, im.height + bordo * 2
    out = Image.new("RGBA", (W + pad * 2, H + pad * 2), (0, 0, 0, 0))
    ombra = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(ombra).rounded_rectangle((pad + 6, pad + 24, pad + W + 6, pad + H + 24), r, fill=(6, 3, 1, 190))
    out.alpha_composite(ombra.filter(ImageFilter.GaussianBlur(24)))
    ImageDraw.Draw(out).rounded_rectangle((pad, pad, pad + W - 1, pad + H - 1), r, fill=(26, 20, 16, 255),
                                          outline=(96, 78, 62, 255), width=3)
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r - bordo + 6, fill=255)
    im.putalpha(m)
    out.alpha_composite(im, (pad + bordo, pad + bordo))
    return out, pad


# Las portadas reales de los 3 volúmenes del kit, derechas como tablets:
# Borse e Zaini al frente y más grande, Portafogli a la izquierda y Cinture a la derecha.
# Se tapan solo ~50 px para que se lea el título de cada una.
sin, p1 = tablet(pagina(1, 1000, d2), 500)    # Vol. 2 · Portafogli
des, _ = tablet(pagina(1, 1000, d4), 500)     # Vol. 4 · Cinture
cen, p2 = tablet(pagina(1, 1200, d), 600)     # Vol. 1 · Borse e Zaini
ws, hs = sin.width - 2 * p1, sin.height - 2 * p1    # caja del marco, sin la sombra
wc, hc = cen.width - 2 * p2, cen.height - 2 * p2
SOVRAPP = 50
xc = ws - SOVRAPP
xd = xc + wc - SOVRAPP
ys = (hc - hs) // 2
M = 90
tela = Image.new("RGBA", (xd + ws + 2 * M, hc + 2 * M), (0, 0, 0, 0))
tela.alpha_composite(sin, (M - p1, M + ys - p1))
tela.alpha_composite(des, (M + xd - p1, M + ys - p1))
tela.alpha_composite(cen, (M + xc - p2, M - p2))
box = tela.getbbox()
hero = tela.crop(box)
hero = hero.resize((1200, int(hero.height * 1200 / hero.width)), Image.LANCZOS)
salva(hero, "hero.webp", 82)
print("hero", hero.size)

# ------------------------------------------------ 3b. sección «le misure tornano»
# Dos tavole punteadas reales en abanico (las alas del Gufo y una tavola de
# Street Chic) y una lupa sobre el righello di scala impreso en la tavola.
def lente(im, r):
    """Recorte circular con anillo de cuero y costura, listo para superponer."""
    lato = r * 2
    im = im.resize((lato, lato), Image.LANCZOS).convert("RGBA")
    maschera = Image.new("L", (lato, lato), 0)
    ImageDraw.Draw(maschera).ellipse((0, 0, lato - 1, lato - 1), fill=255)
    im.putalpha(maschera)
    pad = 40
    out = Image.new("RGBA", (lato + pad * 2, lato + pad * 2), (0, 0, 0, 0))
    ombra = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(ombra).ellipse((pad + 6, pad + 14, pad + lato + 6, pad + lato + 14), fill=(20, 10, 4, 150))
    out.alpha_composite(ombra.filter(ImageFilter.GaussianBlur(16)))
    dr = ImageDraw.Draw(out)
    dr.ellipse((pad - 14, pad - 14, pad + lato + 14, pad + lato + 14), fill=(107, 58, 29, 255))
    out.alpha_composite(im, (pad, pad))
    # costura punteada sobre el anillo
    import math
    rr = r + 7
    for k in range(64):
        a = 2 * math.pi * k / 64
        cx, cy = pad + r + rr * math.cos(a), pad + r + rr * math.sin(a)
        dr.line((cx - 2 * math.sin(a), cy + 2 * math.cos(a), cx + 2 * math.sin(a), cy - 2 * math.cos(a)), fill=(240, 222, 190, 255), width=2)
    return out


W2 = 640
ali = con_ombra(pagina(69, W2), -7)          # Zaino Gufo · le ali
street = con_ombra(pagina(45, W2), 4)        # Street Chic · tavola 04 con righello
pm = d[44].get_pixmap(matrix=fitz.Matrix(7, 7), clip=fitz.Rect(26, 744, 256, 796), alpha=False)
righello = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
# encuadre cuadrado centrado en el righello, con fondo blanco de la tavola
q = Image.new("RGB", (righello.width, righello.width), "white")
q.paste(righello, (0, (righello.width - righello.height) // 2))
tela = Image.new("RGBA", (1500, 1400), (0, 0, 0, 0))
tela.alpha_composite(ali, (0, 40))
tela.alpha_composite(street, (560, 150))
tela.alpha_composite(lente(q, 190), (60, 820))
box = tela.getbbox()
mis = tela.crop(box)
mis = mis.resize((1000, int(mis.height * 1000 / mis.width)), Image.LANCZOS)
salva(mis, "misure.webp", 82)
print("misure", mis.size)

# ------------------------------------------------ 4. og:image 1200x630
og = Image.new("RGB", (1200, 630), (34, 22, 15))
foto = hero.copy()
foto.thumbnail((760, 600), Image.LANCZOS)
og.paste(foto, (1200 - foto.width - 20, (630 - foto.height) // 2), foto)
salva(og, "og.jpg", 84)
print("ok")
