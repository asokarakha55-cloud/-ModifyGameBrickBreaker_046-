import pygame
import random
import math
import array
import json
import os

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# --- KONSTANTA ---
WIDTH, HEIGHT = 760, 600
FPS = 60
HUD_H = 48

BG_BASE = (10, 14, 24)
HUD_BG = (18, 24, 38)
TEXT_COLOR = (241, 245, 249)
MUTED_TEXT = (148, 163, 184)
STEEL = (100, 116, 139)
BOMB_COL = (239, 68, 68)

BLOCK_COLORS = {
    3: (244, 63, 94),
    2: (251, 146, 60),
    1: (52, 211, 153),
}

BALL_SKINS = [
    {"id": "SOLAR", "name": "Solar Orb", "ability": "Supernova (Ledakan Area)",
     "cooldown": 480, "core": (253, 224, 71), "accent": (249, 115, 22)},
    {"id": "SHURIKEN", "name": "Cyber Shuriken", "ability": "Phantom Pierce (Tembus Balok)",
     "cooldown": 540, "core": (56, 189, 248), "accent": (224, 242, 254)},
    {"id": "FROST", "name": "Frost Crystal", "ability": "Blizzard Split (Gandakan 3 Bola)",
     "cooldown": 600, "core": (165, 243, 252), "accent": (59, 130, 246)},
    {"id": "VOID", "name": "Void Vortex", "ability": "Gravity Pull (Tarik Bonus + Skor)",
     "cooldown": 420, "core": (192, 132, 252), "accent": (88, 28, 135)},
]

PADDLE_SKINS = [
    {"id": "STEALTH", "name": "Stealth Carbon", "primary": (51, 65, 85), "accent": (56, 189, 248)},
    {"id": "PLASMA", "name": "Plasma Tech", "primary": (14, 165, 233), "accent": (224, 242, 254)},
    {"id": "ROYAL", "name": "Royal Gold", "primary": (234, 179, 8), "accent": (244, 63, 94)},
    {"id": "HAZARD", "name": "Mecha Hazard", "primary": (250, 204, 21), "accent": (24, 24, 27)},
]

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
except Exception:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker: Overdrive")
clock = pygame.time.Clock()

FONT_NAMES = "segoeui,arial,dejavusans,helvetica,freesans"
font_xs = pygame.font.SysFont(FONT_NAMES, 13, bold=True)
font_sm = pygame.font.SysFont(FONT_NAMES, 16, bold=True)
font_md = pygame.font.SysFont(FONT_NAMES, 20)
font_lg = pygame.font.SysFont(FONT_NAMES, 40, bold=True)
font_xl = pygame.font.SysFont(FONT_NAMES, 56, bold=True)

# --- HIGH SCORE PERSISTEN ---
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")


def load_high_score():
    try:
        with open(SAVE_PATH, "r") as f:
            return int(json.load(f).get("high_score", 0))
    except Exception:
        return 0


def save_high_score(value):
    try:
        with open(SAVE_PATH, "w") as f:
            json.dump({"high_score": int(value)}, f)
    except Exception:
        pass


# --- AUDIO SYNTHESIZER (sweep frekuensi + envelope) ---
MUTED = False


def make_sound(f0, f1, duration_ms, vol=0.14, wave="sine"):
    try:
        sr = 44100
        n = int(sr * duration_ms / 1000.0)
        buf = array.array("h", [0] * n)
        phase = 0.0
        for i in range(n):
            t = i / n
            freq = f0 + (f1 - f0) * t
            phase += 2.0 * math.pi * freq / sr
            if wave == "square":
                s = 1.0 if math.sin(phase) >= 0 else -1.0
                s *= 0.6
            elif wave == "noise":
                s = random.uniform(-1, 1)
            else:
                s = math.sin(phase)
            env = min(1.0, i / 120.0) * (1.0 - t) ** 1.5
            buf[i] = int(32767 * vol * env * s)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None


SND_HIT = make_sound(520, 380, 60)
SND_STEEL = make_sound(1400, 900, 50, 0.1, "square")
SND_BREAKS = [make_sound(620 + i * 70, 900 + i * 90, 90) for i in range(8)]
SND_ABILITY = make_sound(500, 1500, 220, 0.16, "square")
SND_POWERUP = make_sound(700, 1300, 150)
SND_LOSE = make_sound(400, 90, 380, 0.18, "square")
SND_BOMB = make_sound(220, 40, 260, 0.2, "noise")
SND_LAUNCH = make_sound(300, 800, 90)
SND_SHIELD = make_sound(900, 400, 120, 0.14, "square")
SND_LEVEL = make_sound(500, 1400, 400, 0.15)


def play_sfx(snd):
    if snd and not MUTED:
        snd.play()


def main():
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BG_BASE)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()

import pygame
import random
import math
import array
import json
import os

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# --- KONSTANTA ---
WIDTH, HEIGHT = 760, 600
FPS = 60
HUD_H = 48

BG_BASE = (10, 14, 24)
HUD_BG = (18, 24, 38)
TEXT_COLOR = (241, 245, 249)
MUTED_TEXT = (148, 163, 184)
STEEL = (100, 116, 139)
BOMB_COL = (239, 68, 68)

BLOCK_COLORS = {
    3: (244, 63, 94),
    2: (251, 146, 60),
    1: (52, 211, 153),
}

BALL_SKINS = [
    {"id": "SOLAR", "name": "Solar Orb", "ability": "Supernova (Ledakan Area)",
     "cooldown": 480, "core": (253, 224, 71), "accent": (249, 115, 22)},
    {"id": "SHURIKEN", "name": "Cyber Shuriken", "ability": "Phantom Pierce (Tembus Balok)",
     "cooldown": 540, "core": (56, 189, 248), "accent": (224, 242, 254)},
    {"id": "FROST", "name": "Frost Crystal", "ability": "Blizzard Split (Gandakan 3 Bola)",
     "cooldown": 600, "core": (165, 243, 252), "accent": (59, 130, 246)},
    {"id": "VOID", "name": "Void Vortex", "ability": "Gravity Pull (Tarik Bonus + Skor)",
     "cooldown": 420, "core": (192, 132, 252), "accent": (88, 28, 135)},
]

PADDLE_SKINS = [
    {"id": "STEALTH", "name": "Stealth Carbon", "primary": (51, 65, 85), "accent": (56, 189, 248)},
    {"id": "PLASMA", "name": "Plasma Tech", "primary": (14, 165, 233), "accent": (224, 242, 254)},
    {"id": "ROYAL", "name": "Royal Gold", "primary": (234, 179, 8), "accent": (244, 63, 94)},
    {"id": "HAZARD", "name": "Mecha Hazard", "primary": (250, 204, 21), "accent": (24, 24, 27)},
]

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
except Exception:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker: Overdrive")
clock = pygame.time.Clock()

FONT_NAMES = "segoeui,arial,dejavusans,helvetica,freesans"
font_xs = pygame.font.SysFont(FONT_NAMES, 13, bold=True)
font_sm = pygame.font.SysFont(FONT_NAMES, 16, bold=True)
font_md = pygame.font.SysFont(FONT_NAMES, 20)
font_lg = pygame.font.SysFont(FONT_NAMES, 40, bold=True)
font_xl = pygame.font.SysFont(FONT_NAMES, 56, bold=True)

# --- HIGH SCORE PERSISTEN ---
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")


def load_high_score():
    try:
        with open(SAVE_PATH, "r") as f:
            return int(json.load(f).get("high_score", 0))
    except Exception:
        return 0


def save_high_score(value):
    try:
        with open(SAVE_PATH, "w") as f:
            json.dump({"high_score": int(value)}, f)
    except Exception:
        pass


# --- AUDIO SYNTHESIZER (sweep frekuensi + envelope) ---
MUTED = False


def make_sound(f0, f1, duration_ms, vol=0.14, wave="sine"):
    try:
        sr = 44100
        n = int(sr * duration_ms / 1000.0)
        buf = array.array("h", [0] * n)
        phase = 0.0
        for i in range(n):
            t = i / n
            freq = f0 + (f1 - f0) * t
            phase += 2.0 * math.pi * freq / sr
            if wave == "square":
                s = 1.0 if math.sin(phase) >= 0 else -1.0
                s *= 0.6
            elif wave == "noise":
                s = random.uniform(-1, 1)
            else:
                s = math.sin(phase)
            env = min(1.0, i / 120.0) * (1.0 - t) ** 1.5
            buf[i] = int(32767 * vol * env * s)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None


SND_HIT = make_sound(520, 380, 60)
SND_STEEL = make_sound(1400, 900, 50, 0.1, "square")
SND_BREAKS = [make_sound(620 + i * 70, 900 + i * 90, 90) for i in range(8)]
SND_ABILITY = make_sound(500, 1500, 220, 0.16, "square")
SND_POWERUP = make_sound(700, 1300, 150)
SND_LOSE = make_sound(400, 90, 380, 0.18, "square")
SND_BOMB = make_sound(220, 40, 260, 0.2, "noise")
SND_LAUNCH = make_sound(300, 800, 90)
SND_SHIELD = make_sound(900, 400, 120, 0.14, "square")
SND_LEVEL = make_sound(500, 1400, 400, 0.15)


def play_sfx(snd):
    if snd and not MUTED:
        snd.play()


# --- UTILITAS GLOW ---
_glow_cache = {}


def get_glow(radius, color):
    key = (radius, color)
    if key not in _glow_cache:
        surf = pygame.Surface((radius * 2, radius * 2))
        for r in range(radius, 0, -2):
            k = (1 - r / radius) ** 2 * 0.55
            pygame.draw.circle(surf, (int(color[0] * k), int(color[1] * k), int(color[2] * k)),
                               (radius, radius), r)
        _glow_cache[key] = surf
    return _glow_cache[key]


def blit_glow(surface, pos, radius, color):
    g = get_glow(radius, color)
    surface.blit(g, (pos[0] - radius, pos[1] - radius), special_flags=pygame.BLEND_RGB_ADD)


def draw_text_center(surface, text, font, color, center):
    s = font.render(text, True, color)
    surface.blit(s, s.get_rect(center=center))


def draw_heart(surface, x, y, size, color):
    r = size // 2
    pygame.draw.circle(surface, color, (x + r, y + r), r)
    pygame.draw.circle(surface, color, (x + 3 * r, y + r), r)
    pygame.draw.polygon(surface, color, [(x, y + r + 1), (x + 4 * r, y + r + 1), (x + 2 * r, y + 4 * r)])


# --- LATAR BELAKANG DINAMIS ---
class DynamicBackground:
    def __init__(self):
        self.stars = [[random.randint(0, WIDTH), random.randint(HUD_H, HEIGHT),
                       random.uniform(0.3, 1.5), random.randint(1, 2)] for _ in range(60)]
        self.grid_offset = 0.0
        self.pulse = 0.0

    def update(self):
        self.grid_offset = (self.grid_offset + 0.6) % 40
        self.pulse += 0.03
        for s in self.stars:
            s[1] += s[2]
            if s[1] > HEIGHT:
                s[0] = random.randint(0, WIDTH)
                s[1] = HUD_H

    def draw(self, surface, level):
        surface.fill(BG_BASE)
        hue_colors = [(22, 33, 55), (32, 24, 58), (18, 42, 48), (45, 24, 38)]
        base = hue_colors[(level - 1) % len(hue_colors)]
        k = 1.0 + 0.15 * math.sin(self.pulse)
        grid_color = tuple(min(255, int(c * k)) for c in base)

        for y in range(HUD_H + int(self.grid_offset), HEIGHT, 40):
            pygame.draw.line(surface, grid_color, (0, y), (WIDTH, y), 1)
        for x in range(0, WIDTH, 40):
            pygame.draw.line(surface, grid_color, (x, HUD_H), (x, HEIGHT), 1)

        for x, y, speed, size in self.stars:
            b = int(110 + speed * 80)
            pygame.draw.circle(surface, (b, b, min(255, b + 20)), (int(x), int(y)), size)


# --- EFEK VISUAL ---
class Shockwave:
    def __init__(self, x, y, color, max_radius=130):
        self.x, self.y, self.color = x, y, color
        self.radius = 10
        self.max_radius = max_radius
        self.alpha = 255

    def update(self):
        self.radius += 8
        self.alpha = max(0, int(255 * (1 - self.radius / self.max_radius)))

    def draw(self, surface):
        if self.alpha > 0:
            d = self.max_radius * 2
            surf = pygame.Surface((d, d), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, self.alpha), (self.max_radius, self.max_radius),
                               int(self.radius), 4)
            surface.blit(surf, (self.x - self.max_radius, self.y - self.max_radius))


class Particle:
    def __init__(self, x, y, color, gravity=0.12):
        self.x, self.y, self.color = x, y, color
        ang = random.uniform(0, 2 * math.pi)
        spd = random.uniform(1.5, 5.0)
        self.vx = math.cos(ang) * spd
        self.vy = math.sin(ang) * spd
        self.gravity = gravity
        self.life = random.randint(15, 28)
        self.max_life = self.life
        self.size = random.randint(3, 6)

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(1, self.size - 0.12)

    def draw(self, surface):
        if self.life > 0:
            k = self.life / self.max_life
            col = (int(self.color[0] * (0.4 + 0.6 * k)),
                   int(self.color[1] * (0.4 + 0.6 * k)),
                   int(self.color[2] * (0.4 + 0.6 * k)))
            s = max(1, int(self.size))
            pygame.draw.rect(surface, col, (int(self.x), int(self.y), s, s))


class FloatingText:
    def __init__(self, x, y, text, color, big=False):
        self.x, self.y, self.text, self.color = x, y, text, color
        self.life = 50
        self.font = font_sm if big else font_xs

    def update(self):
        self.y -= 1.0
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            s = self.font.render(self.text, True, self.color)
            s.set_alpha(min(255, self.life * 9))
            surface.blit(s, s.get_rect(center=(int(self.x), int(self.y))))


class PowerUp:
    TYPES = {
        "EXPAND": {"color": (168, 85, 247), "sym": "W", "label": "PADDLE LEBAR", "w": 22},
        "LIFE": {"color": (236, 72, 153), "sym": "+", "label": "+1 NYAWA", "w": 8},
        "MULTI": {"color": (59, 130, 246), "sym": "M", "label": "MULTI-BALL", "w": 22},
        "CHARGE": {"color": (250, 204, 21), "sym": "C", "label": "ABILITY FULL!", "w": 18},
        "SLOW": {"color": (45, 212, 191), "sym": "S", "label": "SLOW MOTION", "w": 16},
        "SHIELD": {"color": (148, 163, 184), "sym": "U", "label": "SHIELD AKTIF", "w": 14},
    }

    def __init__(self, x, y):
        self.fx, self.fy = float(x), float(y)
        self.rect = pygame.Rect(0, 0, 26, 26)
        keys = list(self.TYPES.keys())
        self.type = random.choices(keys, weights=[self.TYPES[k]["w"] for k in keys])[0]
        self.info = self.TYPES[self.type]
        self.speed = 3.0
        self.magnetized = False
        self.rect.center = (int(self.fx), int(self.fy))

    def update(self, target_rect=None):
        if self.magnetized and target_rect:
            dx = target_rect.centerx - self.fx
            dy = target_rect.centery - self.fy
            dist = max(1, math.hypot(dx, dy))
            self.fx += dx / dist * 10
            self.fy += dy / dist * 10
        else:
            self.fy += self.speed
        self.rect.center = (int(self.fx), int(self.fy))

    def draw(self, surface):
        blit_glow(surface, self.rect.center, 26, self.info["color"])
        pygame.draw.ellipse(surface, self.info["color"], self.rect)
        pygame.draw.ellipse(surface, TEXT_COLOR, self.rect, 2)
        txt = font_xs.render(self.info["sym"], True, TEXT_COLOR)
        surface.blit(txt, txt.get_rect(center=self.rect.center))


def main():
    bg = DynamicBackground()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        bg.update()
        bg.draw(screen, level=1)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()

import pygame
import random
import math
import array
import json
import os

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# --- KONSTANTA ---
WIDTH, HEIGHT = 760, 600
FPS = 60
HUD_H = 48

BG_BASE = (10, 14, 24)
HUD_BG = (18, 24, 38)
TEXT_COLOR = (241, 245, 249)
MUTED_TEXT = (148, 163, 184)
STEEL = (100, 116, 139)
BOMB_COL = (239, 68, 68)

BLOCK_COLORS = {
    3: (244, 63, 94),
    2: (251, 146, 60),
    1: (52, 211, 153),
}

BALL_SKINS = [
    {"id": "SOLAR", "name": "Solar Orb", "ability": "Supernova (Ledakan Area)",
     "cooldown": 480, "core": (253, 224, 71), "accent": (249, 115, 22)},
    {"id": "SHURIKEN", "name": "Cyber Shuriken", "ability": "Phantom Pierce (Tembus Balok)",
     "cooldown": 540, "core": (56, 189, 248), "accent": (224, 242, 254)},
    {"id": "FROST", "name": "Frost Crystal", "ability": "Blizzard Split (Gandakan 3 Bola)",
     "cooldown": 600, "core": (165, 243, 252), "accent": (59, 130, 246)},
    {"id": "VOID", "name": "Void Vortex", "ability": "Gravity Pull (Tarik Bonus + Skor)",
     "cooldown": 420, "core": (192, 132, 252), "accent": (88, 28, 135)},
]

PADDLE_SKINS = [
    {"id": "STEALTH", "name": "Stealth Carbon", "primary": (51, 65, 85), "accent": (56, 189, 248)},
    {"id": "PLASMA", "name": "Plasma Tech", "primary": (14, 165, 233), "accent": (224, 242, 254)},
    {"id": "ROYAL", "name": "Royal Gold", "primary": (234, 179, 8), "accent": (244, 63, 94)},
    {"id": "HAZARD", "name": "Mecha Hazard", "primary": (250, 204, 21), "accent": (24, 24, 27)},
]

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
except Exception:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker: Overdrive")
clock = pygame.time.Clock()

FONT_NAMES = "segoeui,arial,dejavusans,helvetica,freesans"
font_xs = pygame.font.SysFont(FONT_NAMES, 13, bold=True)
font_sm = pygame.font.SysFont(FONT_NAMES, 16, bold=True)
font_md = pygame.font.SysFont(FONT_NAMES, 20)
font_lg = pygame.font.SysFont(FONT_NAMES, 40, bold=True)
font_xl = pygame.font.SysFont(FONT_NAMES, 56, bold=True)

# --- HIGH SCORE PERSISTEN ---
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")


def load_high_score():
    try:
        with open(SAVE_PATH, "r") as f:
            return int(json.load(f).get("high_score", 0))
    except Exception:
        return 0


def save_high_score(value):
    try:
        with open(SAVE_PATH, "w") as f:
            json.dump({"high_score": int(value)}, f)
    except Exception:
        pass


# --- AUDIO SYNTHESIZER (sweep frekuensi + envelope) ---
MUTED = False


def make_sound(f0, f1, duration_ms, vol=0.14, wave="sine"):
    try:
        sr = 44100
        n = int(sr * duration_ms / 1000.0)
        buf = array.array("h", [0] * n)
        phase = 0.0
        for i in range(n):
            t = i / n
            freq = f0 + (f1 - f0) * t
            phase += 2.0 * math.pi * freq / sr
            if wave == "square":
                s = 1.0 if math.sin(phase) >= 0 else -1.0
                s *= 0.6
            elif wave == "noise":
                s = random.uniform(-1, 1)
            else:
                s = math.sin(phase)
            env = min(1.0, i / 120.0) * (1.0 - t) ** 1.5
            buf[i] = int(32767 * vol * env * s)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None


SND_HIT = make_sound(520, 380, 60)
SND_STEEL = make_sound(1400, 900, 50, 0.1, "square")
SND_BREAKS = [make_sound(620 + i * 70, 900 + i * 90, 90) for i in range(8)]
SND_ABILITY = make_sound(500, 1500, 220, 0.16, "square")
SND_POWERUP = make_sound(700, 1300, 150)
SND_LOSE = make_sound(400, 90, 380, 0.18, "square")
SND_BOMB = make_sound(220, 40, 260, 0.2, "noise")
SND_LAUNCH = make_sound(300, 800, 90)
SND_SHIELD = make_sound(900, 400, 120, 0.14, "square")
SND_LEVEL = make_sound(500, 1400, 400, 0.15)


def play_sfx(snd):
    if snd and not MUTED:
        snd.play()


# --- UTILITAS GLOW ---
_glow_cache = {}


def get_glow(radius, color):
    key = (radius, color)
    if key not in _glow_cache:
        surf = pygame.Surface((radius * 2, radius * 2))
        for r in range(radius, 0, -2):
            k = (1 - r / radius) ** 2 * 0.55
            pygame.draw.circle(surf, (int(color[0] * k), int(color[1] * k), int(color[2] * k)),
                               (radius, radius), r)
        _glow_cache[key] = surf
    return _glow_cache[key]


def blit_glow(surface, pos, radius, color):
    g = get_glow(radius, color)
    surface.blit(g, (pos[0] - radius, pos[1] - radius), special_flags=pygame.BLEND_RGB_ADD)


def draw_text_center(surface, text, font, color, center):
    s = font.render(text, True, color)
    surface.blit(s, s.get_rect(center=center))


def draw_heart(surface, x, y, size, color):
    r = size // 2
    pygame.draw.circle(surface, color, (x + r, y + r), r)
    pygame.draw.circle(surface, color, (x + 3 * r, y + r), r)
    pygame.draw.polygon(surface, color, [(x, y + r + 1), (x + 4 * r, y + r + 1), (x + 2 * r, y + 4 * r)])


# --- LATAR BELAKANG DINAMIS ---
class DynamicBackground:
    def __init__(self):
        self.stars = [[random.randint(0, WIDTH), random.randint(HUD_H, HEIGHT),
                       random.uniform(0.3, 1.5), random.randint(1, 2)] for _ in range(60)]
        self.grid_offset = 0.0
        self.pulse = 0.0

    def update(self):
        self.grid_offset = (self.grid_offset + 0.6) % 40
        self.pulse += 0.03
        for s in self.stars:
            s[1] += s[2]
            if s[1] > HEIGHT:
                s[0] = random.randint(0, WIDTH)
                s[1] = HUD_H

    def draw(self, surface, level):
        surface.fill(BG_BASE)
        hue_colors = [(22, 33, 55), (32, 24, 58), (18, 42, 48), (45, 24, 38)]
        base = hue_colors[(level - 1) % len(hue_colors)]
        k = 1.0 + 0.15 * math.sin(self.pulse)
        grid_color = tuple(min(255, int(c * k)) for c in base)

        for y in range(HUD_H + int(self.grid_offset), HEIGHT, 40):
            pygame.draw.line(surface, grid_color, (0, y), (WIDTH, y), 1)
        for x in range(0, WIDTH, 40):
            pygame.draw.line(surface, grid_color, (x, HUD_H), (x, HEIGHT), 1)

        for x, y, speed, size in self.stars:
            b = int(110 + speed * 80)
            pygame.draw.circle(surface, (b, b, min(255, b + 20)), (int(x), int(y)), size)


# --- EFEK VISUAL ---
class Shockwave:
    def __init__(self, x, y, color, max_radius=130):
        self.x, self.y, self.color = x, y, color
        self.radius = 10
        self.max_radius = max_radius
        self.alpha = 255

    def update(self):
        self.radius += 8
        self.alpha = max(0, int(255 * (1 - self.radius / self.max_radius)))

    def draw(self, surface):
        if self.alpha > 0:
            d = self.max_radius * 2
            surf = pygame.Surface((d, d), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, self.alpha), (self.max_radius, self.max_radius),
                               int(self.radius), 4)
            surface.blit(surf, (self.x - self.max_radius, self.y - self.max_radius))


class Particle:
    def __init__(self, x, y, color, gravity=0.12):
        self.x, self.y, self.color = x, y, color
        ang = random.uniform(0, 2 * math.pi)
        spd = random.uniform(1.5, 5.0)
        self.vx = math.cos(ang) * spd
        self.vy = math.sin(ang) * spd
        self.gravity = gravity
        self.life = random.randint(15, 28)
        self.max_life = self.life
        self.size = random.randint(3, 6)

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(1, self.size - 0.12)

    def draw(self, surface):
        if self.life > 0:
            k = self.life / self.max_life
            col = (int(self.color[0] * (0.4 + 0.6 * k)),
                   int(self.color[1] * (0.4 + 0.6 * k)),
                   int(self.color[2] * (0.4 + 0.6 * k)))
            s = max(1, int(self.size))
            pygame.draw.rect(surface, col, (int(self.x), int(self.y), s, s))


class FloatingText:
    def __init__(self, x, y, text, color, big=False):
        self.x, self.y, self.text, self.color = x, y, text, color
        self.life = 50
        self.font = font_sm if big else font_xs

    def update(self):
        self.y -= 1.0
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            s = self.font.render(self.text, True, self.color)
            s.set_alpha(min(255, self.life * 9))
            surface.blit(s, s.get_rect(center=(int(self.x), int(self.y))))


class PowerUp:
    TYPES = {
        "EXPAND": {"color": (168, 85, 247), "sym": "W", "label": "PADDLE LEBAR", "w": 22},
        "LIFE": {"color": (236, 72, 153), "sym": "+", "label": "+1 NYAWA", "w": 8},
        "MULTI": {"color": (59, 130, 246), "sym": "M", "label": "MULTI-BALL", "w": 22},
        "CHARGE": {"color": (250, 204, 21), "sym": "C", "label": "ABILITY FULL!", "w": 18},
        "SLOW": {"color": (45, 212, 191), "sym": "S", "label": "SLOW MOTION", "w": 16},
        "SHIELD": {"color": (148, 163, 184), "sym": "U", "label": "SHIELD AKTIF", "w": 14},
    }

    def __init__(self, x, y):
        self.fx, self.fy = float(x), float(y)
        self.rect = pygame.Rect(0, 0, 26, 26)
        keys = list(self.TYPES.keys())
        self.type = random.choices(keys, weights=[self.TYPES[k]["w"] for k in keys])[0]
        self.info = self.TYPES[self.type]
        self.speed = 3.0
        self.magnetized = False
        self.rect.center = (int(self.fx), int(self.fy))

    def update(self, target_rect=None):
        if self.magnetized and target_rect:
            dx = target_rect.centerx - self.fx
            dy = target_rect.centery - self.fy
            dist = max(1, math.hypot(dx, dy))
            self.fx += dx / dist * 10
            self.fy += dy / dist * 10
        else:
            self.fy += self.speed
        self.rect.center = (int(self.fx), int(self.fy))

    def draw(self, surface):
        blit_glow(surface, self.rect.center, 26, self.info["color"])
        pygame.draw.ellipse(surface, self.info["color"], self.rect)
        pygame.draw.ellipse(surface, TEXT_COLOR, self.rect, 2)
        txt = font_xs.render(self.info["sym"], True, TEXT_COLOR)
        surface.blit(txt, txt.get_rect(center=self.rect.center))


# --- ENTITAS ---
class Striker:
    def __init__(self, skin_idx=0):
        self.default_width = 120
        self.height = 16
        self.speed = 9.5
        self.rect = pygame.Rect((WIDTH - self.default_width) // 2, HEIGHT - 48, self.default_width, self.height)
        self.expand_timer = 0
        self.skin = PADDLE_SKINS[skin_idx]
        self.vx = 0

    def update(self, direction, mouse_x=None):
        old = self.rect.centerx
        if mouse_x is not None:
            self.rect.centerx = mouse_x
        else:
            self.rect.x += direction * self.speed

        if self.expand_timer > 0:
            self.expand_timer -= 1
            if self.expand_timer == 0:
                c = self.rect.centerx
                self.rect.width = self.default_width
                self.rect.centerx = c

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)
        self.vx = self.rect.centerx - old

    def expand(self):
        c = self.rect.centerx
        self.rect.width = 180
        self.rect.centerx = c
        self.expand_timer = 600

    def draw(self, surface):
        sid, pri, acc = self.skin["id"], self.skin["primary"], self.skin["accent"]

        blit_glow(surface, self.rect.center, self.rect.width // 2 + 14, tuple(int(c * 0.35) for c in acc))

        pygame.draw.rect(surface, pri, self.rect, border_radius=8)

        if sid == "STEALTH":
            pygame.draw.rect(surface, acc, (self.rect.x + 4, self.rect.y + 3, 14, self.height - 6), border_radius=4)
            pygame.draw.rect(surface, acc, (self.rect.right - 18, self.rect.y + 3, 14, self.height - 6), border_radius=4)
            pygame.draw.line(surface, acc, (self.rect.x + 24, self.rect.centery), (self.rect.right - 24, self.rect.centery), 2)
        elif sid == "PLASMA":
            inner = pygame.Rect(self.rect.x + 8, self.rect.y + 4, self.rect.width - 16, self.height - 8)
            pygame.draw.rect(surface, acc, inner, border_radius=5)
        elif sid == "ROYAL":
            pygame.draw.rect(surface, (254, 240, 138), self.rect, 2, border_radius=8)
            cx, cy = self.rect.centerx, self.rect.centery
            gem = [(cx, self.rect.y + 2), (cx + 10, cy), (cx, self.rect.bottom - 2), (cx - 10, cy)]
            pygame.draw.polygon(surface, acc, gem)
        elif sid == "HAZARD":
            pygame.draw.rect(surface, acc, self.rect, 2, border_radius=8)
            for sx in range(self.rect.x + 12, self.rect.right - 14, 18):
                pygame.draw.line(surface, acc, (sx, self.rect.bottom - 3), (sx + 8, self.rect.y + 3), 4)

        # Highlight atas
        pygame.draw.line(surface, (255, 255, 255), (self.rect.x + 8, self.rect.y + 1),
                         (self.rect.right - 8, self.rect.y + 1), 1)


class Block:
    def __init__(self, x, y, width, height, hp, kind="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.kind = kind  # normal | steel | bomb
        self.hp = hp
        self.flash = 0

    @property
    def steel(self):
        return self.kind == "steel"

    def draw(self, surface):
        if self.hp <= 0:
            return
        if self.kind == "steel":
            col = STEEL
        elif self.kind == "bomb":
            col = BOMB_COL
        else:
            col = BLOCK_COLORS.get(self.hp, TEXT_COLOR)
        if self.flash > 0:
            self.flash -= 1
            col = tuple(min(255, c + 90) for c in col)

        pygame.draw.rect(surface, col, self.rect, border_radius=5)
        pygame.draw.rect(surface, (255, 255, 255), (self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, 3),
                         border_radius=2)
        # Bayangan bawah
        pygame.draw.line(surface, tuple(int(c * 0.6) for c in col),
                         (self.rect.x + 4, self.rect.bottom - 3), (self.rect.right - 4, self.rect.bottom - 3), 2)

        if self.kind == "steel":
            for rx in (self.rect.x + 8, self.rect.right - 8):
                pygame.draw.circle(surface, (51, 65, 85), (rx, self.rect.centery + 2), 2)
            pygame.draw.rect(surface, (51, 65, 85), self.rect, 1, border_radius=5)
        elif self.kind == "bomb":
            pygame.draw.circle(surface, (24, 24, 27), (self.rect.centerx, self.rect.centery + 2), 6)
            pygame.draw.circle(surface, (253, 224, 71), (self.rect.centerx + 4, self.rect.centery - 4), 2)
        elif self.hp > 1:
            pygame.draw.rect(surface, (15, 23, 42), self.rect, 1, border_radius=5)
            for i in range(self.hp - 1):
                pygame.draw.circle(surface, (15, 23, 42), (self.rect.right - 9 - i * 7, self.rect.centery + 2), 2)


class Ball:
    def __init__(self, skin_idx=0, x=None, y=None, angle=None, speed=6.0):
        self.radius = 9
        self.speed = speed
        self.skin = BALL_SKINS[skin_idx]
        self.trail = []
        self.spin_angle = 0.0
        self.pierce_timer = 0
        self.reset(x, y, angle)

    def reset(self, x=None, y=None, angle=None):
        self.x = float(x if x is not None else WIDTH // 2)
        self.y = float(y if y is not None else HEIGHT - 78)
        ang = angle if angle is not None else random.uniform(-0.5, 0.5)
        self.vx = self.speed * math.sin(ang)
        self.vy = -self.speed * math.cos(ang)
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = (int(self.x), int(self.y))
        self.trail.clear()

    def tick(self):
        """Animasi per-frame (trail, spin, timer)."""
        self.spin_angle = (self.spin_angle + 8) % 360
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 10:
            self.trail.pop(0)
        if self.pierce_timer > 0:
            self.pierce_timer -= 1

    def step(self, f):
        """Gerak sebagian frame (f = 0..1) + pantulan dinding. Return True bila jatuh."""
        self.x += self.vx * f
        self.y += self.vy * f

        if self.x - self.radius <= 0:
            self.x = float(self.radius)
            self.vx = abs(self.vx)
        elif self.x + self.radius >= WIDTH:
            self.x = float(WIDTH - self.radius)
            self.vx = -abs(self.vx)

        if self.y - self.radius <= HUD_H:
            self.y = float(HUD_H + self.radius)
            self.vy = abs(self.vy)

        # Cegah pantulan terlalu datar (bola "terjebak" horizontal)
        spd = math.hypot(self.vx, self.vy)
        if spd > 0 and abs(self.vy) < spd * 0.22:
            sign = 1 if self.vy >= 0 else -1
            self.vy = sign * spd * 0.22
            self.vx = math.copysign(math.sqrt(max(0.0, spd * spd - self.vy * self.vy)), self.vx or 1)

        self.rect.center = (int(self.x), int(self.y))
        return self.rect.top >= HEIGHT

    def bounce_paddle(self, paddle):
        offset = (self.x - paddle.rect.centerx) / (paddle.rect.width / 2)
        offset += paddle.vx * 0.012  # english dari gerakan paddle
        offset = max(-0.92, min(0.92, offset))
        ang = offset * (math.pi / 3)
        self.vx = self.speed * math.sin(ang)
        self.vy = -abs(self.speed * math.cos(ang))
        self.y = float(paddle.rect.top - self.radius)
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, surface):
        cx, cy = self.rect.center
        core, acc, sid = self.skin["core"], self.skin["accent"], self.skin["id"]

        for i, pos in enumerate(self.trail):
            k = (i + 1) / max(1, len(self.trail))
            r = int(self.radius * k * 0.7)
            if r > 1:
                col = tuple(int(c * (0.25 + 0.5 * k)) for c in acc)
                pygame.draw.circle(surface, col, pos, r)

        blit_glow(surface, (cx, cy), 30, core)

        if sid == "SOLAR":
            for k in range(8):
                rad = math.radians(self.spin_angle + k * 45)
                px = cx + math.cos(rad) * (self.radius + 4)
                py = cy + math.sin(rad) * (self.radius + 4)
                pygame.draw.line(surface, acc, (cx, cy), (px, py), 2)
            pygame.draw.circle(surface, core, (cx, cy), self.radius)
            pygame.draw.circle(surface, (255, 255, 255), (cx, cy), 4)
        elif sid == "SHURIKEN":
            pts = []
            for k in range(8):
                rad = math.radians(self.spin_angle * 1.8 + k * 45)
                dist = (self.radius + 5) if k % 2 == 0 else 4
                pts.append((cx + math.cos(rad) * dist, cy + math.sin(rad) * dist))
            pygame.draw.polygon(surface, acc if self.pierce_timer > 0 else core, pts)
            pygame.draw.circle(surface, BG_BASE, (cx, cy), 3)
        elif sid == "FROST":
            pts = []
            for k in range(6):
                rad = math.radians(self.spin_angle * 0.5 + k * 60)
                pts.append((cx + math.cos(rad) * (self.radius + 2), cy + math.sin(rad) * (self.radius + 2)))
            pygame.draw.polygon(surface, core, pts)
            pygame.draw.polygon(surface, acc, pts, 2)
        elif sid == "VOID":
            pygame.draw.circle(surface, acc, (cx, cy), self.radius + 2)
            pygame.draw.circle(surface, (15, 10, 25), (cx, cy), self.radius - 2)
            orb = math.radians(self.spin_angle * 2)
            pygame.draw.circle(surface, core,
                               (int(cx + math.cos(orb) * (self.radius + 4)), int(cy + math.sin(orb) * (self.radius + 4))), 3)


def main():
    bg = DynamicBackground()
    striker = Striker(0)
    ball = Ball(0)
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        bg.update()
        ball.tick()
        if ball.step(1.0):
            ball.reset()
        if ball.rect.colliderect(striker.rect) and ball.vy > 0:
            ball.bounce_paddle(striker)
        bg.draw(screen, 1)
        striker.draw(screen)
        ball.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()

import pygame
import random
import math
import array
import json
import os

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# --- KONSTANTA ---
WIDTH, HEIGHT = 760, 600
FPS = 60
HUD_H = 48

BG_BASE = (10, 14, 24)
HUD_BG = (18, 24, 38)
TEXT_COLOR = (241, 245, 249)
MUTED_TEXT = (148, 163, 184)
STEEL = (100, 116, 139)
BOMB_COL = (239, 68, 68)

BLOCK_COLORS = {
    3: (244, 63, 94),
    2: (251, 146, 60),
    1: (52, 211, 153),
}

BALL_SKINS = [
    {"id": "SOLAR", "name": "Solar Orb", "ability": "Supernova (Ledakan Area)",
     "cooldown": 480, "core": (253, 224, 71), "accent": (249, 115, 22)},
    {"id": "SHURIKEN", "name": "Cyber Shuriken", "ability": "Phantom Pierce (Tembus Balok)",
     "cooldown": 540, "core": (56, 189, 248), "accent": (224, 242, 254)},
    {"id": "FROST", "name": "Frost Crystal", "ability": "Blizzard Split (Gandakan 3 Bola)",
     "cooldown": 600, "core": (165, 243, 252), "accent": (59, 130, 246)},
    {"id": "VOID", "name": "Void Vortex", "ability": "Gravity Pull (Tarik Bonus + Skor)",
     "cooldown": 420, "core": (192, 132, 252), "accent": (88, 28, 135)},
]

PADDLE_SKINS = [
    {"id": "STEALTH", "name": "Stealth Carbon", "primary": (51, 65, 85), "accent": (56, 189, 248)},
    {"id": "PLASMA", "name": "Plasma Tech", "primary": (14, 165, 233), "accent": (224, 242, 254)},
    {"id": "ROYAL", "name": "Royal Gold", "primary": (234, 179, 8), "accent": (244, 63, 94)},
    {"id": "HAZARD", "name": "Mecha Hazard", "primary": (250, 204, 21), "accent": (24, 24, 27)},
]

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
except Exception:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker: Overdrive")
clock = pygame.time.Clock()

FONT_NAMES = "segoeui,arial,dejavusans,helvetica,freesans"
font_xs = pygame.font.SysFont(FONT_NAMES, 13, bold=True)
font_sm = pygame.font.SysFont(FONT_NAMES, 16, bold=True)
font_md = pygame.font.SysFont(FONT_NAMES, 20)
font_lg = pygame.font.SysFont(FONT_NAMES, 40, bold=True)
font_xl = pygame.font.SysFont(FONT_NAMES, 56, bold=True)

# --- HIGH SCORE PERSISTEN ---
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")


def load_high_score():
    try:
        with open(SAVE_PATH, "r") as f:
            return int(json.load(f).get("high_score", 0))
    except Exception:
        return 0


def save_high_score(value):
    try:
        with open(SAVE_PATH, "w") as f:
            json.dump({"high_score": int(value)}, f)
    except Exception:
        pass


# --- AUDIO SYNTHESIZER (sweep frekuensi + envelope) ---
MUTED = False


def make_sound(f0, f1, duration_ms, vol=0.14, wave="sine"):
    try:
        sr = 44100
        n = int(sr * duration_ms / 1000.0)
        buf = array.array("h", [0] * n)
        phase = 0.0
        for i in range(n):
            t = i / n
            freq = f0 + (f1 - f0) * t
            phase += 2.0 * math.pi * freq / sr
            if wave == "square":
                s = 1.0 if math.sin(phase) >= 0 else -1.0
                s *= 0.6
            elif wave == "noise":
                s = random.uniform(-1, 1)
            else:
                s = math.sin(phase)
            env = min(1.0, i / 120.0) * (1.0 - t) ** 1.5
            buf[i] = int(32767 * vol * env * s)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None


SND_HIT = make_sound(520, 380, 60)
SND_STEEL = make_sound(1400, 900, 50, 0.1, "square")
SND_BREAKS = [make_sound(620 + i * 70, 900 + i * 90, 90) for i in range(8)]
SND_ABILITY = make_sound(500, 1500, 220, 0.16, "square")
SND_POWERUP = make_sound(700, 1300, 150)
SND_LOSE = make_sound(400, 90, 380, 0.18, "square")
SND_BOMB = make_sound(220, 40, 260, 0.2, "noise")
SND_LAUNCH = make_sound(300, 800, 90)
SND_SHIELD = make_sound(900, 400, 120, 0.14, "square")
SND_LEVEL = make_sound(500, 1400, 400, 0.15)


def play_sfx(snd):
    if snd and not MUTED:
        snd.play()


# --- UTILITAS GLOW ---
_glow_cache = {}


def get_glow(radius, color):
    key = (radius, color)
    if key not in _glow_cache:
        surf = pygame.Surface((radius * 2, radius * 2))
        for r in range(radius, 0, -2):
            k = (1 - r / radius) ** 2 * 0.55
            pygame.draw.circle(surf, (int(color[0] * k), int(color[1] * k), int(color[2] * k)),
                               (radius, radius), r)
        _glow_cache[key] = surf
    return _glow_cache[key]


def blit_glow(surface, pos, radius, color):
    g = get_glow(radius, color)
    surface.blit(g, (pos[0] - radius, pos[1] - radius), special_flags=pygame.BLEND_RGB_ADD)


def draw_text_center(surface, text, font, color, center):
    s = font.render(text, True, color)
    surface.blit(s, s.get_rect(center=center))


def draw_heart(surface, x, y, size, color):
    r = size // 2
    pygame.draw.circle(surface, color, (x + r, y + r), r)
    pygame.draw.circle(surface, color, (x + 3 * r, y + r), r)
    pygame.draw.polygon(surface, color, [(x, y + r + 1), (x + 4 * r, y + r + 1), (x + 2 * r, y + 4 * r)])


# --- LATAR BELAKANG DINAMIS ---
class DynamicBackground:
    def __init__(self):
        self.stars = [[random.randint(0, WIDTH), random.randint(HUD_H, HEIGHT),
                       random.uniform(0.3, 1.5), random.randint(1, 2)] for _ in range(60)]
        self.grid_offset = 0.0
        self.pulse = 0.0

    def update(self):
        self.grid_offset = (self.grid_offset + 0.6) % 40
        self.pulse += 0.03
        for s in self.stars:
            s[1] += s[2]
            if s[1] > HEIGHT:
                s[0] = random.randint(0, WIDTH)
                s[1] = HUD_H

    def draw(self, surface, level):
        surface.fill(BG_BASE)
        hue_colors = [(22, 33, 55), (32, 24, 58), (18, 42, 48), (45, 24, 38)]
        base = hue_colors[(level - 1) % len(hue_colors)]
        k = 1.0 + 0.15 * math.sin(self.pulse)
        grid_color = tuple(min(255, int(c * k)) for c in base)

        for y in range(HUD_H + int(self.grid_offset), HEIGHT, 40):
            pygame.draw.line(surface, grid_color, (0, y), (WIDTH, y), 1)
        for x in range(0, WIDTH, 40):
            pygame.draw.line(surface, grid_color, (x, HUD_H), (x, HEIGHT), 1)

        for x, y, speed, size in self.stars:
            b = int(110 + speed * 80)
            pygame.draw.circle(surface, (b, b, min(255, b + 20)), (int(x), int(y)), size)


# --- EFEK VISUAL ---
class Shockwave:
    def __init__(self, x, y, color, max_radius=130):
        self.x, self.y, self.color = x, y, color
        self.radius = 10
        self.max_radius = max_radius
        self.alpha = 255

    def update(self):
        self.radius += 8
        self.alpha = max(0, int(255 * (1 - self.radius / self.max_radius)))

    def draw(self, surface):
        if self.alpha > 0:
            d = self.max_radius * 2
            surf = pygame.Surface((d, d), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, self.alpha), (self.max_radius, self.max_radius),
                               int(self.radius), 4)
            surface.blit(surf, (self.x - self.max_radius, self.y - self.max_radius))


class Particle:
    def __init__(self, x, y, color, gravity=0.12):
        self.x, self.y, self.color = x, y, color
        ang = random.uniform(0, 2 * math.pi)
        spd = random.uniform(1.5, 5.0)
        self.vx = math.cos(ang) * spd
        self.vy = math.sin(ang) * spd
        self.gravity = gravity
        self.life = random.randint(15, 28)
        self.max_life = self.life
        self.size = random.randint(3, 6)

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(1, self.size - 0.12)

    def draw(self, surface):
        if self.life > 0:
            k = self.life / self.max_life
            col = (int(self.color[0] * (0.4 + 0.6 * k)),
                   int(self.color[1] * (0.4 + 0.6 * k)),
                   int(self.color[2] * (0.4 + 0.6 * k)))
            s = max(1, int(self.size))
            pygame.draw.rect(surface, col, (int(self.x), int(self.y), s, s))


class FloatingText:
    def __init__(self, x, y, text, color, big=False):
        self.x, self.y, self.text, self.color = x, y, text, color
        self.life = 50
        self.font = font_sm if big else font_xs

    def update(self):
        self.y -= 1.0
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            s = self.font.render(self.text, True, self.color)
            s.set_alpha(min(255, self.life * 9))
            surface.blit(s, s.get_rect(center=(int(self.x), int(self.y))))


class PowerUp:
    TYPES = {
        "EXPAND": {"color": (168, 85, 247), "sym": "W", "label": "PADDLE LEBAR", "w": 22},
        "LIFE": {"color": (236, 72, 153), "sym": "+", "label": "+1 NYAWA", "w": 8},
        "MULTI": {"color": (59, 130, 246), "sym": "M", "label": "MULTI-BALL", "w": 22},
        "CHARGE": {"color": (250, 204, 21), "sym": "C", "label": "ABILITY FULL!", "w": 18},
        "SLOW": {"color": (45, 212, 191), "sym": "S", "label": "SLOW MOTION", "w": 16},
        "SHIELD": {"color": (148, 163, 184), "sym": "U", "label": "SHIELD AKTIF", "w": 14},
    }

    def __init__(self, x, y):
        self.fx, self.fy = float(x), float(y)
        self.rect = pygame.Rect(0, 0, 26, 26)
        keys = list(self.TYPES.keys())
        self.type = random.choices(keys, weights=[self.TYPES[k]["w"] for k in keys])[0]
        self.info = self.TYPES[self.type]
        self.speed = 3.0
        self.magnetized = False
        self.rect.center = (int(self.fx), int(self.fy))

    def update(self, target_rect=None):
        if self.magnetized and target_rect:
            dx = target_rect.centerx - self.fx
            dy = target_rect.centery - self.fy
            dist = max(1, math.hypot(dx, dy))
            self.fx += dx / dist * 10
            self.fy += dy / dist * 10
        else:
            self.fy += self.speed
        self.rect.center = (int(self.fx), int(self.fy))

    def draw(self, surface):
        blit_glow(surface, self.rect.center, 26, self.info["color"])
        pygame.draw.ellipse(surface, self.info["color"], self.rect)
        pygame.draw.ellipse(surface, TEXT_COLOR, self.rect, 2)
        txt = font_xs.render(self.info["sym"], True, TEXT_COLOR)
        surface.blit(txt, txt.get_rect(center=self.rect.center))


# --- ENTITAS ---
class Striker:
    def __init__(self, skin_idx=0):
        self.default_width = 120
        self.height = 16
        self.speed = 9.5
        self.rect = pygame.Rect((WIDTH - self.default_width) // 2, HEIGHT - 48, self.default_width, self.height)
        self.expand_timer = 0
        self.skin = PADDLE_SKINS[skin_idx]
        self.vx = 0

    def update(self, direction, mouse_x=None):
        old = self.rect.centerx
        if mouse_x is not None:
            self.rect.centerx = mouse_x
        else:
            self.rect.x += direction * self.speed

        if self.expand_timer > 0:
            self.expand_timer -= 1
            if self.expand_timer == 0:
                c = self.rect.centerx
                self.rect.width = self.default_width
                self.rect.centerx = c

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)
        self.vx = self.rect.centerx - old

    def expand(self):
        c = self.rect.centerx
        self.rect.width = 180
        self.rect.centerx = c
        self.expand_timer = 600

    def draw(self, surface):
        sid, pri, acc = self.skin["id"], self.skin["primary"], self.skin["accent"]

        blit_glow(surface, self.rect.center, self.rect.width // 2 + 14, tuple(int(c * 0.35) for c in acc))

        pygame.draw.rect(surface, pri, self.rect, border_radius=8)

        if sid == "STEALTH":
            pygame.draw.rect(surface, acc, (self.rect.x + 4, self.rect.y + 3, 14, self.height - 6), border_radius=4)
            pygame.draw.rect(surface, acc, (self.rect.right - 18, self.rect.y + 3, 14, self.height - 6), border_radius=4)
            pygame.draw.line(surface, acc, (self.rect.x + 24, self.rect.centery), (self.rect.right - 24, self.rect.centery), 2)
        elif sid == "PLASMA":
            inner = pygame.Rect(self.rect.x + 8, self.rect.y + 4, self.rect.width - 16, self.height - 8)
            pygame.draw.rect(surface, acc, inner, border_radius=5)
        elif sid == "ROYAL":
            pygame.draw.rect(surface, (254, 240, 138), self.rect, 2, border_radius=8)
            cx, cy = self.rect.centerx, self.rect.centery
            gem = [(cx, self.rect.y + 2), (cx + 10, cy), (cx, self.rect.bottom - 2), (cx - 10, cy)]
            pygame.draw.polygon(surface, acc, gem)
        elif sid == "HAZARD":
            pygame.draw.rect(surface, acc, self.rect, 2, border_radius=8)
            for sx in range(self.rect.x + 12, self.rect.right - 14, 18):
                pygame.draw.line(surface, acc, (sx, self.rect.bottom - 3), (sx + 8, self.rect.y + 3), 4)

        # Highlight atas
        pygame.draw.line(surface, (255, 255, 255), (self.rect.x + 8, self.rect.y + 1),
                         (self.rect.right - 8, self.rect.y + 1), 1)


class Block:
    def __init__(self, x, y, width, height, hp, kind="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.kind = kind  # normal | steel | bomb
        self.hp = hp
        self.flash = 0

    @property
    def steel(self):
        return self.kind == "steel"

    def draw(self, surface):
        if self.hp <= 0:
            return
        if self.kind == "steel":
            col = STEEL
        elif self.kind == "bomb":
            col = BOMB_COL
        else:
            col = BLOCK_COLORS.get(self.hp, TEXT_COLOR)
        if self.flash > 0:
            self.flash -= 1
            col = tuple(min(255, c + 90) for c in col)

        pygame.draw.rect(surface, col, self.rect, border_radius=5)
        pygame.draw.rect(surface, (255, 255, 255), (self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, 3),
                         border_radius=2)
        # Bayangan bawah
        pygame.draw.line(surface, tuple(int(c * 0.6) for c in col),
                         (self.rect.x + 4, self.rect.bottom - 3), (self.rect.right - 4, self.rect.bottom - 3), 2)

        if self.kind == "steel":
            for rx in (self.rect.x + 8, self.rect.right - 8):
                pygame.draw.circle(surface, (51, 65, 85), (rx, self.rect.centery + 2), 2)
            pygame.draw.rect(surface, (51, 65, 85), self.rect, 1, border_radius=5)
        elif self.kind == "bomb":
            pygame.draw.circle(surface, (24, 24, 27), (self.rect.centerx, self.rect.centery + 2), 6)
            pygame.draw.circle(surface, (253, 224, 71), (self.rect.centerx + 4, self.rect.centery - 4), 2)
        elif self.hp > 1:
            pygame.draw.rect(surface, (15, 23, 42), self.rect, 1, border_radius=5)
            for i in range(self.hp - 1):
                pygame.draw.circle(surface, (15, 23, 42), (self.rect.right - 9 - i * 7, self.rect.centery + 2), 2)


class Ball:
    def __init__(self, skin_idx=0, x=None, y=None, angle=None, speed=6.0):
        self.radius = 9
        self.speed = speed
        self.skin = BALL_SKINS[skin_idx]
        self.trail = []
        self.spin_angle = 0.0
        self.pierce_timer = 0
        self.reset(x, y, angle)

    def reset(self, x=None, y=None, angle=None):
        self.x = float(x if x is not None else WIDTH // 2)
        self.y = float(y if y is not None else HEIGHT - 78)
        ang = angle if angle is not None else random.uniform(-0.5, 0.5)
        self.vx = self.speed * math.sin(ang)
        self.vy = -self.speed * math.cos(ang)
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = (int(self.x), int(self.y))
        self.trail.clear()

    def tick(self):
        """Animasi per-frame (trail, spin, timer)."""
        self.spin_angle = (self.spin_angle + 8) % 360
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 10:
            self.trail.pop(0)
        if self.pierce_timer > 0:
            self.pierce_timer -= 1

    def step(self, f):
        """Gerak sebagian frame (f = 0..1) + pantulan dinding. Return True bila jatuh."""
        self.x += self.vx * f
        self.y += self.vy * f

        if self.x - self.radius <= 0:
            self.x = float(self.radius)
            self.vx = abs(self.vx)
        elif self.x + self.radius >= WIDTH:
            self.x = float(WIDTH - self.radius)
            self.vx = -abs(self.vx)

        if self.y - self.radius <= HUD_H:
            self.y = float(HUD_H + self.radius)
            self.vy = abs(self.vy)

        # Cegah pantulan terlalu datar (bola "terjebak" horizontal)
        spd = math.hypot(self.vx, self.vy)
        if spd > 0 and abs(self.vy) < spd * 0.22:
            sign = 1 if self.vy >= 0 else -1
            self.vy = sign * spd * 0.22
            self.vx = math.copysign(math.sqrt(max(0.0, spd * spd - self.vy * self.vy)), self.vx or 1)

        self.rect.center = (int(self.x), int(self.y))
        return self.rect.top >= HEIGHT

    def bounce_paddle(self, paddle):
        offset = (self.x - paddle.rect.centerx) / (paddle.rect.width / 2)
        offset += paddle.vx * 0.012  # english dari gerakan paddle
        offset = max(-0.92, min(0.92, offset))
        ang = offset * (math.pi / 3)
        self.vx = self.speed * math.sin(ang)
        self.vy = -abs(self.speed * math.cos(ang))
        self.y = float(paddle.rect.top - self.radius)
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, surface):
        cx, cy = self.rect.center
        core, acc, sid = self.skin["core"], self.skin["accent"], self.skin["id"]

        for i, pos in enumerate(self.trail):
            k = (i + 1) / max(1, len(self.trail))
            r = int(self.radius * k * 0.7)
            if r > 1:
                col = tuple(int(c * (0.25 + 0.5 * k)) for c in acc)
                pygame.draw.circle(surface, col, pos, r)

        blit_glow(surface, (cx, cy), 30, core)

        if sid == "SOLAR":
            for k in range(8):
                rad = math.radians(self.spin_angle + k * 45)
                px = cx + math.cos(rad) * (self.radius + 4)
                py = cy + math.sin(rad) * (self.radius + 4)
                pygame.draw.line(surface, acc, (cx, cy), (px, py), 2)
            pygame.draw.circle(surface, core, (cx, cy), self.radius)
            pygame.draw.circle(surface, (255, 255, 255), (cx, cy), 4)
        elif sid == "SHURIKEN":
            pts = []
            for k in range(8):
                rad = math.radians(self.spin_angle * 1.8 + k * 45)
                dist = (self.radius + 5) if k % 2 == 0 else 4
                pts.append((cx + math.cos(rad) * dist, cy + math.sin(rad) * dist))
            pygame.draw.polygon(surface, acc if self.pierce_timer > 0 else core, pts)
            pygame.draw.circle(surface, BG_BASE, (cx, cy), 3)
        elif sid == "FROST":
            pts = []
            for k in range(6):
                rad = math.radians(self.spin_angle * 0.5 + k * 60)
                pts.append((cx + math.cos(rad) * (self.radius + 2), cy + math.sin(rad) * (self.radius + 2)))
            pygame.draw.polygon(surface, core, pts)
            pygame.draw.polygon(surface, acc, pts, 2)
        elif sid == "VOID":
            pygame.draw.circle(surface, acc, (cx, cy), self.radius + 2)
            pygame.draw.circle(surface, (15, 10, 25), (cx, cy), self.radius - 2)
            orb = math.radians(self.spin_angle * 2)
            pygame.draw.circle(surface, core,
                               (int(cx + math.cos(orb) * (self.radius + 4)), int(cy + math.sin(orb) * (self.radius + 4))), 3)


# --- GENERATOR LEVEL ---
def create_level(level):
    blocks = []
    rng = random.Random(level * 7919)
    cols = 10
    rows = min(5 + (level // 2), 8)
    gap = 6
    margin_x = 28
    margin_y = 65
    bw = (WIDTH - (2 * margin_x) - (gap * (cols - 1))) // cols
    bh = 22
    pattern = (level - 1) % 4

    for r in range(rows):
        for c in range(cols):
            if pattern == 1 and (c < r or c >= cols - r):
                continue
            if pattern == 2 and abs(c - (cols - 1) / 2.0) + abs(r - (rows - 1) / 2.0) > 5.5:
                continue
            if pattern == 3 and (r + c) % 2 == 1 and r > 1:
                continue
            x = margin_x + c * (bw + gap)
            y = margin_y + r * (bh + gap)
            hp = 3 if (r == 0 and level >= 2) else (2 if r < 2 else 1)
            blocks.append(Block(x, y, bw, bh, hp))

    # Balok bom (level 2+) dan baja (level 3+)
    candidates = [b for b in blocks if b.rect.y > margin_y + bh]
    rng.shuffle(candidates)
    n_bomb = min(1 + level // 2, 6)
    for b in candidates[:n_bomb]:
        b.kind, b.hp = "bomb", 1
    if level >= 3:
        n_steel = min(level - 1, 7)
        for b in candidates[n_bomb:n_bomb + n_steel]:
            b.kind, b.hp = "steel", 999

    if not any(b.kind != "steel" for b in blocks):
        blocks.append(Block(WIDTH // 2 - 40, 100, 80, 22, 1))
    return blocks


def level_speed(level):
    return min(9.5, 6.0 + (level - 1) * 0.35)


# --- UI ---
def draw_hud(score, high_score, lives, level, combo, skin_info, cd_timer, shield, slow_timer, muted):
    pygame.draw.rect(screen, HUD_BG, (0, 0, WIDTH, HUD_H))
    pygame.draw.line(screen, (51, 65, 85), (0, HUD_H), (WIDTH, HUD_H), 2)

    screen.blit(font_sm.render(f"SKOR  {score}", True, TEXT_COLOR), (20, 14))
    screen.blit(font_sm.render(f"REKOR  {high_score}", True, (250, 204, 21)), (160, 14))
    screen.blit(font_sm.render(f"LEVEL {level}", True, (56, 189, 248)), (325, 14))
    if combo > 1:
        screen.blit(font_sm.render(f"{combo}x COMBO", True, (52, 211, 153)), (415, 14))

    for i in range(lives):
        draw_heart(screen, WIDTH - 130 + i * 24, 14, 10, (244, 63, 94))
    if muted:
        screen.blit(font_xs.render("MUTE", True, MUTED_TEXT), (WIDTH - 175, 17))

    # Status buff
    bx = 20
    if shield:
        screen.blit(font_xs.render("SHIELD", True, (148, 163, 184)), (bx, HEIGHT - 28))
        bx += 60
    if slow_timer > 0:
        screen.blit(font_xs.render(f"SLOW {slow_timer // 60 + 1}s", True, (45, 212, 191)), (bx, HEIGHT - 28))

    # Ability bar
    bar_w, bar_h = 220, 8
    bx, by = (WIDTH - bar_w) // 2, HEIGHT - 16
    pygame.draw.rect(screen, (30, 41, 59), (bx, by, bar_w, bar_h), border_radius=4)
    ratio = 1.0 - (cd_timer / skin_info["cooldown"])
    ready = cd_timer == 0
    fill_col = skin_info["core"] if ready else MUTED_TEXT
    if ready:
        blit_glow(screen, (WIDTH // 2, by + 4), 60 + int(6 * math.sin(pygame.time.get_ticks() / 150)),
                  tuple(int(c * 0.5) for c in fill_col))
    pygame.draw.rect(screen, fill_col, (bx, by, int(bar_w * ratio), bar_h), border_radius=4)
    txt = f"[F / KLIK] {skin_info['ability']}" if ready else "MENGISI ENERGI..."
    draw_text_center(screen, txt, font_xs, fill_col, (WIDTH // 2, by - 10))


def draw_minimal_menu(bg, ball_idx, paddle_idx, preview_ball, preview_paddle, high_score):
    bg.update()
    bg.draw(screen, level=1)
    b_skin, p_skin = BALL_SKINS[ball_idx], PADDLE_SKINS[paddle_idx]

    draw_text_center(screen, "BLOCK BREAKER", font_lg, TEXT_COLOR, (WIDTH // 2, 85))
    draw_text_center(screen, "O V E R D R I V E", font_xs, b_skin["core"], (WIDTH // 2, 120))

    box = pygame.Rect(WIDTH // 2 - 190, 150, 380, 145)
    pygame.draw.rect(screen, (18, 24, 38), box, border_radius=14)
    pygame.draw.rect(screen, (51, 65, 85), box, 1, border_radius=14)

    t = pygame.time.get_ticks() / 1000.0
    preview_ball.spin_angle = (preview_ball.spin_angle + 4) % 360
    preview_ball.pierce_timer = 1 if b_skin["id"] == "SHURIKEN" else 0
    preview_ball.rect.center = (WIDTH // 2 + int(math.sin(t * 1.6) * 90), 200 + int(math.cos(t * 3.2) * 8))
    preview_ball.trail = [(preview_ball.rect.centerx - i * 5 * math.cos(t * 1.6), preview_ball.rect.centery)
                          for i in range(8, 0, -1)]
    preview_ball.draw(screen)
    preview_paddle.rect.center = (WIDTH // 2, 255)
    preview_paddle.draw(screen)

    draw_text_center(screen, f"BOLA [1-4]: {b_skin['name']}", font_sm, b_skin["core"], (WIDTH // 2, 330))
    draw_text_center(screen, f"Ability: {b_skin['ability']}", font_xs, MUTED_TEXT, (WIDTH // 2, 354))
    draw_text_center(screen, f"PADDLE [Q / E]: {p_skin['name']}", font_sm, p_skin["accent"], (WIDTH // 2, 395))
    draw_text_center(screen, f"REKOR: {high_score}", font_xs, (250, 204, 21), (WIDTH // 2, 425))

    btn = pygame.Rect(WIDTH // 2 - 130, 455, 260, 44)
    pulse = int(3 * math.sin(t * 4))
    pygame.draw.rect(screen, b_skin["core"], btn.inflate(pulse * 2, pulse), border_radius=22)
    draw_text_center(screen, "TEKAN SPASI UNTUK MULAI", font_sm, BG_BASE, btn.center)

    draw_text_center(screen, "Panah / A-D / Mouse  |  Ability: F / Klik  |  Pause: P  |  Mute: N",
                     font_xs, MUTED_TEXT, (WIDTH // 2, 535))
    pygame.display.flip()


def draw_overlay_screen(snapshot, title, title_color, lines):
    if snapshot is not None:
        screen.blit(snapshot, (0, 0))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 14, 24, 200))
    screen.blit(overlay, (0, 0))
    draw_text_center(screen, title, font_lg, title_color, (WIDTH // 2, HEIGHT // 2 - 55))
    y = HEIGHT // 2
    for text, font, col in lines:
        draw_text_center(screen, text, font, col, (WIDTH // 2, y))
        y += 40
    pygame.display.flip()


def main():
    bg = DynamicBackground()
    ball_skin_idx, paddle_skin_idx = 0, 0
    preview_ball = Ball(ball_skin_idx)
    preview_paddle = Striker(paddle_skin_idx)
    high_score = load_high_score()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    ball_skin_idx = event.key - pygame.K_1
                    preview_ball = Ball(ball_skin_idx)
                elif event.key == pygame.K_q:
                    paddle_skin_idx = (paddle_skin_idx - 1) % len(PADDLE_SKINS)
                    preview_paddle = Striker(paddle_skin_idx)
                elif event.key == pygame.K_e:
                    paddle_skin_idx = (paddle_skin_idx + 1) % len(PADDLE_SKINS)
                    preview_paddle = Striker(paddle_skin_idx)

        draw_minimal_menu(bg, ball_skin_idx, paddle_skin_idx, preview_ball, preview_paddle, high_score)
    pygame.quit()


if __name__ == "__main__":
    main()