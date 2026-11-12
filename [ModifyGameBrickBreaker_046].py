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