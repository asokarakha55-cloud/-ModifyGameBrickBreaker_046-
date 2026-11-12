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