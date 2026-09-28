# -*- coding: utf-8 -*-
"""Portada del KIT a partir de la portada real del PDF (mismo arte).

La original dice «200+ modelli… e molto altro · bonus inclusi gratis», que es
la colección entera. El kit de la landing son 10 modelos sin bonus, así que:
  «200+»                        -> «10»
  «…PORTAFOGLI E MOLTO ALTRO»   -> «…PORTAFOGLI E CINTURE»
  cinta «BONUS INCLUSI GRATIS»  -> «KIT DI PARTENZA»
El texto viejo se borra con inpaint y se escribe encima con fuentes parecidas
(Alfa Slab One para el número, Poppins para el resto).

    python -u copertina_kit.py   -> img/copertina-kit.png (alta) y -s.webp
"""
import io, os
import cv2
import fitz
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

QUI = os.path.dirname(os.path.abspath(__file__))
FONTI = os.path.join(QUI, "_fonti")
PDF = os.path.join(QUI, "..", "Ebooks", "Pelletteria Facile - Borse e Zaini.pdf")

d = fitz.open(PDF)
pix = fitz.Pixmap(d, d[0].get_image_info(xrefs=True)[0]["xref"])
cov = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
W, H = cov.size                      # 2480 x 3504
k = W / 774                          # coordenadas medidas sobre la vista de 774 px
R = lambda x0, y0, x1, y1: (int(x0 * k), int(y0 * k), int(x1 * k), int(y1 * k))


def cancella(img, box, cond, dil=9, raggio=9):
    """Borra con inpaint los píxeles de `box` que cumplen `cond(arr)`."""
    a = np.array(img)
    x0, y0, x1, y1 = box
    zona = a[y0:y1, x0:x1]
    m = cond(zona).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((dil, dil), np.uint8))
    maschera = np.zeros(a.shape[:2], np.uint8)
    maschera[y0:y1, x0:x1] = m
    bgr = cv2.cvtColor(a, cv2.COLOR_RGB2BGR)
    out = cv2.inpaint(bgr, maschera, raggio, cv2.INPAINT_TELEA)
    out = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    # grano del pergamino sobre lo reconstruido, para que no quede liso
    rumore = np.random.default_rng(7).normal(0, 3.2, out.shape)
    sel = maschera > 0
    out = out.astype(np.float32)
    out[sel] = np.clip(out[sel] + rumore[sel], 0, 255)
    return Image.fromarray(out.astype(np.uint8)), maschera


lum = lambda z: 0.3 * z[..., 0] + 0.59 * z[..., 1] + 0.11 * z[..., 2]

# 1. «200+»: todo lo oscuro de esa franja (con su sombra)
cov, _ = cancella(cov, R(70, 140, 610, 338), lambda z: lum(z) < 205, dil=31, raggio=15)
# 2. la línea «BORSE, ZAINI, PORTAFOGLI E MOLTO ALTRO» (sin tocar las dos rayas)
cov, _ = cancella(cov, R(66, 422, 708, 462), lambda z: lum(z) < 190, dil=15, raggio=9)


def toppa(img, box, raggio):
    """Parche de cuero cosido encima de la cinta (el texto viejo va de borde a
    borde y el inpaint deja manchas): degradé, grano, viñeta, borde, costura y sombra."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    top, bot = np.array([112, 58, 30], np.float32), np.array([74, 36, 16], np.float32)
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    base = np.repeat(top[None, None, :] + (bot - top)[None, None, :] * t, w, axis=1)
    g = cv2.GaussianBlur(np.random.default_rng(11).normal(0, 10, (h, w)).astype(np.float32), (0, 0), 1.4)
    base += g[..., None]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    vig = np.clip(np.minimum(np.minimum(xx, w - 1 - xx) / (0.18 * w), np.minimum(yy, h - 1 - yy) / (0.12 * h)), 0, 1) * .25 + .75
    base *= vig[..., None]
    pezza = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    maschera = Image.new("L", (w, h), 0)
    ImageDraw.Draw(maschera).rounded_rectangle((0, 0, w - 1, h - 1), raggio, fill=255)
    ombra = Image.new("L", img.size, 0)
    ImageDraw.Draw(ombra).rounded_rectangle((x0 + 6, y0 + 12, x1 + 6, y1 + 12), raggio, fill=150)
    img.paste((30, 14, 6), (0, 0), ombra.filter(ImageFilter.GaussianBlur(14)))
    img.paste(pezza, (x0, y0), maschera)
    d2 = ImageDraw.Draw(img)
    d2.rounded_rectangle((x0, y0, x1, y1), raggio, outline=(44, 20, 8), width=5)
    ins, L, G, crema = 24, 26, 16, (236, 212, 170)

    def tratteggio(ax, ay, bx, by):
        lun = ((bx - ax) ** 2 + (by - ay) ** 2) ** .5
        for i in range(int(lun // (L + G)) + 1):
            s0, s1 = i * (L + G) / lun, min(1, (i * (L + G) + L) / lun)
            d2.line((ax + (bx - ax) * s0, ay + (by - ay) * s0, ax + (bx - ax) * s1, ay + (by - ay) * s1), fill=crema, width=6)
    r = raggio * .4
    tratteggio(x0 + ins + r, y0 + ins, x1 - ins - r, y0 + ins)
    tratteggio(x1 - ins, y0 + ins + r, x1 - ins, y1 - ins - r)
    tratteggio(x1 - ins - r, y1 - ins, x0 + ins + r, y1 - ins)
    tratteggio(x0 + ins, y1 - ins - r, x0 + ins, y0 + ins + r)


# 3. la cinta: parche nuevo encima del texto «BONUS INCLUSI GRATIS» y del regalo
toppa(cov, R(593, 64, 720, 248), int(9 * k))

dr = ImageDraw.Draw(cov)
MARRONE = (74, 36, 16)


def centro(testo, font, cx, y, fill, **kw):
    w = dr.textlength(testo, font=font)
    dr.text((cx - w / 2, y), testo, font=font, fill=fill, **kw)


# «10» en relieve: sombra, cuerpo con degradé y luz arriba a la izquierda
f10 = ImageFont.truetype(os.path.join(FONTI, "AlfaSlabOne-Regular.ttf"), int(215 * k))
cx = int(340 * k)
bbox = dr.textbbox((0, 0), "10", font=f10)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x, y = cx - tw / 2 - bbox[0], int(150 * k) - bbox[1]
m = Image.new("L", cov.size, 0)
ImageDraw.Draw(m).text((x, y), "10", font=f10, fill=255)
ombra = m.filter(ImageFilter.GaussianBlur(18))
cov.paste((50, 25, 10), (14, 22), Image.eval(ombra, lambda v: int(v * .55)))
grad = Image.new("RGB", cov.size)
gd = ImageDraw.Draw(grad)
for yy in range(int(y + bbox[1]), int(y + bbox[3]) + 1):
    t = (yy - (y + bbox[1])) / max(1, th)
    c = tuple(int(a + (b - a) * t) for a, b in zip((128, 66, 30), (78, 36, 15)))
    gd.line((0, yy, W, yy), fill=c)
cov.paste(grad, (0, 0), m)
luce = ImageChops_sub = None
from PIL import ImageChops
bordo = ImageChops.subtract(m, m.transform(m.size, Image.AFFINE, (1, 0, 5, 0, 1, 5)))
cov.paste((196, 132, 88), (0, 0), bordo.filter(ImageFilter.GaussianBlur(2)))

# línea de categorías
fcat = ImageFont.truetype(os.path.join(FONTI, "Poppins-SemiBold.ttf"), int(23.5 * k))
centro("BORSE, ZAINI, PORTAFOGLI E CINTURE", fcat, int(388 * k), int(426 * k), (58, 34, 20))

# cinta: «KIT DI PARTENZA»
fkit = ImageFont.truetype(os.path.join(FONTI, "Poppins-ExtraBold.ttf"), int(25 * k))
fk2 = ImageFont.truetype(os.path.join(FONTI, "Poppins-ExtraBold.ttf"), int(21 * k))
crema = (246, 226, 190)
centro("KIT", fkit, int(657 * k), int(92 * k), crema)
centro("DI", fkit, int(657 * k), int(121 * k), crema)
centro("PARTENZA", fk2, int(657 * k), int(152 * k), crema)
# forbici semplici al posto del regalo
fx, fy, s = int(657 * k), int(212 * k), k
oro = (214, 168, 92)
for dx in (-1, 1):
    dr.ellipse((fx + dx * 9 * s - 6 * s, fy + 8 * s - 6 * s, fx + dx * 9 * s + 6 * s, fy + 8 * s + 6 * s), outline=oro, width=int(2.4 * s))
dr.line((fx - 5 * s, fy + 3 * s, fx + 12 * s, fy - 16 * s), fill=oro, width=int(2.6 * s))
dr.line((fx + 5 * s, fy + 3 * s, fx - 12 * s, fy - 16 * s), fill=oro, width=int(2.6 * s))

os.makedirs(os.path.join(QUI, "img"), exist_ok=True)
cov.save(os.path.join(QUI, "img", "copertina-kit.png"), optimize=True)
cov.resize((774, 1094), Image.LANCZOS).save(os.path.join(QUI, "img", "copertina-kit-s.webp"), "WEBP", quality=84, method=6)
print("copertina", cov.size)
