"""Generates farm-themed illustrations into assets/ (already run; included for reference)."""
from PIL import Image, ImageDraw
import random, math
random.seed(7)
W, H = 1200, 600

def gradient(d, top, bottom, h0, h1):
    for y in range(h0, h1):
        t = (y - h0) / max(1, h1 - h0)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)

def sun(d, x, y, r, col=(255, 224, 130)):
    for k in range(6, 0, -1):
        d.ellipse([x-r-k*14, y-r-k*14, x+r+k*14, y+r+k*14], fill=col + (22,))
    d.ellipse([x-r, y-r, x+r, y+r], fill=col)

def hills(d, base, col, amp, ph):
    pts = [(0, H)]
    for x in range(0, W+10, 10):
        pts.append((x, base + math.sin(x/170 + ph) * amp + math.sin(x/60 + ph) * amp/4))
    pts.append((W, H)); d.polygon(pts, fill=col)

def rows(d, y0, col1, col2):
    for i in range(14):
        y = y0 + i*i*1.6 + i*6
        if y > H: break
        d.line([(0, y), (W, y)], fill=col1 if i % 2 else col2, width=max(2, int(i*1.6)))

def wheat(d, x, y, s, col=(222, 176, 60)):
    d.line([(x, y), (x, y-60*s)], fill=(120, 150, 60), width=max(1, int(2*s)))
    for k in range(7):
        yy = y-60*s + k*7*s
        d.ellipse([x-6*s, yy-4*s, x, yy+5*s], fill=col)
        d.ellipse([x, yy-8*s, x+6*s, yy+1*s], fill=col)

def farmer(d, x, y, s=1.0, shirt=(200, 70, 50), tool="hoe"):
    d.ellipse([x-18*s, y-120*s, x+18*s, y-84*s], fill=(150, 98, 64))
    d.ellipse([x-34*s, y-112*s, x+34*s, y-98*s], fill=(238, 205, 120))
    d.pieslice([x-22*s, y-132*s, x+22*s, y-92*s], 180, 360, fill=(238, 205, 120))
    d.rounded_rectangle([x-22*s, y-84*s, x+22*s, y-20*s], 10, fill=shirt)
    d.rectangle([x-20*s, y-22*s, x-4*s, y+40*s], fill=(54, 84, 130))
    d.rectangle([x+4*s, y-22*s, x+20*s, y+40*s], fill=(54, 84, 130))
    d.line([(x+20*s, y-70*s), (x+55*s, y-10*s)], fill=shirt, width=int(12*s))
    if tool == "hoe":
        d.line([(x+55*s, y-10*s), (x+80*s, y-140*s)], fill=(110, 78, 40), width=int(6*s))
        d.polygon([(x+50*s, y-14*s), (x+75*s, y-8*s), (x+60*s, y+8*s)], fill=(150, 150, 160))
    else:
        d.ellipse([x+40*s, y-6*s, x+80*s, y+20*s], fill=(200, 150, 80))

def save(img, name):
    img.convert("RGB").save(f"assets/{name}.jpg", quality=90)

# 1 hero sunrise
img = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(img, "RGBA")
d.rectangle([0, 0, W, H], fill=(255, 236, 179)); gradient(d, (255, 183, 94), (255, 236, 179), 0, 330)
sun(d, 880, 250, 62)
hills(d, 330, (126, 170, 90), 40, 0.4); hills(d, 380, (88, 140, 62), 35, 2.0)
gradient(d, (70, 120, 50), (30, 80, 40), 420, H); rows(d, 420, (52, 100, 44), (92, 150, 60))
for _ in range(90): wheat(d, random.randint(0, W), random.randint(430, 590), random.uniform(.7, 1.6))
farmer(d, 300, 520, 1.5)
save(img, "hero_sunrise")

# 2 farmer harvesting
img = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(img, "RGBA")
d.rectangle([0, 0, W, H], fill=(225, 244, 252)); gradient(d, (135, 196, 235), (225, 244, 252), 0, 360)
for cx, cy in [(200, 120), (640, 80), (980, 150)]:
    for dx, dy, r in [(0, 0, 44), (40, 10, 36), (-40, 12, 34)]:
        d.ellipse([cx+dx-r, cy+dy-r*.6, cx+dx+r, cy+dy+r*.6], fill=(255, 255, 255, 235))
hills(d, 340, (140, 190, 100), 30, 1.0)
gradient(d, (190, 150, 60), (120, 90, 30), 380, H); rows(d, 380, (170, 130, 50), (214, 176, 80))
for _ in range(160): wheat(d, random.randint(0, W), random.randint(390, 590), random.uniform(.8, 1.8))
farmer(d, 620, 540, 1.7, shirt=(70, 130, 90), tool="basket")
save(img, "farmer_harvest")

# 3 green paddy
img = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(img, "RGBA")
d.rectangle([0, 0, W, H], fill=(240, 250, 235)); gradient(d, (170, 220, 240), (240, 250, 235), 0, 300)
hills(d, 290, (90, 150, 110), 50, 0.2); hills(d, 340, (60, 120, 80), 30, 1.4)
gradient(d, (110, 170, 190), (60, 120, 130), 380, H)
for i in range(7):
    y = 400 + i*30
    d.rectangle([0, y, W, y+16], fill=(80, 150, 60))
    for x in range(0, W, 14): d.line([(x, y+16), (x+random.randint(-4, 4), y-12-i*2)], fill=(110, 190, 70), width=3)
farmer(d, 880, 560, 1.4, shirt=(230, 150, 40))
save(img, "paddy_field")

# 4 harvest basket
img = Image.new("RGBA", (W, H), (250, 240, 215, 255)); d = ImageDraw.Draw(img, "RGBA")
d.rectangle([0, 400, W, H], fill=(190, 140, 90))
for x in range(0, W, 90): d.line([(x, 400), (x, H)], fill=(160, 110, 66), width=3)
d.pieslice([300, 300, 900, 620], 0, 180, fill=(170, 112, 60)); d.ellipse([300, 300, 900, 360], fill=(140, 90, 46))
def veg(x, y, col, r, leaf=(70, 150, 60)):
    d.ellipse([x-r, y-r, x+r, y+r], fill=col); d.polygon([(x-8, y-r), (x+8, y-r), (x, y-r-28)], fill=leaf)
for x, y, c, r in [(400, 330, (225, 60, 50), 46), (500, 300, (250, 160, 40), 50), (610, 320, (230, 70, 55), 48),
                   (710, 300, (255, 200, 60), 46), (800, 335, (200, 50, 50), 40), (560, 270, (120, 180, 60), 40)]:
    veg(x, y, c, r)
for x in range(80, 300, 36): wheat(d, x, 500, 1.6)
for x in range(920, 1140, 36): wheat(d, x, 500, 1.6)
save(img, "harvest_basket")

# 5 tractor
img = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(img, "RGBA")
d.rectangle([0, 0, W, H], fill=(255, 244, 214)); gradient(d, (255, 214, 150), (255, 244, 214), 0, 340)
sun(d, 220, 200, 50); hills(d, 330, (150, 185, 90), 30, 0.8)
gradient(d, (140, 100, 50), (90, 60, 30), 380, H); rows(d, 380, (120, 84, 40), (160, 116, 60))
d.rectangle([520, 330, 800, 430], fill=(60, 140, 70)); d.rectangle([700, 270, 810, 360], fill=(40, 110, 55))
d.rectangle([715, 285, 795, 345], fill=(190, 225, 240)); d.rectangle([520, 300, 540, 330], fill=(60, 60, 60))
d.ellipse([480, 380, 600, 500], fill=(30, 30, 30)); d.ellipse([510, 410, 570, 470], fill=(180, 180, 90))
d.ellipse([690, 340, 870, 520], fill=(30, 30, 30)); d.ellipse([745, 395, 815, 465], fill=(180, 180, 90))
save(img, "tractor_field")

# 6 sprout banner
img = Image.new("RGBA", (W, 300), (232, 245, 220, 255)); d = ImageDraw.Draw(img, "RGBA")
for x in range(60, W, 120):
    h = random.randint(80, 170)
    d.line([(x, 300), (x, 300-h)], fill=(80, 140, 60), width=6)
    d.ellipse([x-46, 300-h-14, x, 300-h+22], fill=(110, 180, 70)); d.ellipse([x, 300-h-34, x+46, 300-h+2], fill=(90, 160, 60))
img.convert("RGB").save("assets/sprout_banner.jpg", quality=90)
print("images done")
