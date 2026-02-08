import pgzrun
import random
from pygame import Rect

from config import *
from entities import Hero, Enemy

state = MENU
sound_on = True
score = 0
survive_time = 0.0
spawn_timer = 0.0
cross_timer = 6.0

hero = Hero(Actor(HERO_FRAMES[0], (WIDTH // 2, HEIGHT // 2)), HERO_FRAMES, PLAYER_HP, PLAYER_SPEED)
enemies = []
holy_cross = None

btn_start = Rect((WIDTH // 2 - 140, 200), (280, 56))
btn_sound = Rect((WIDTH // 2 - 140, 280), (280, 56))
btn_exit = Rect((WIDTH // 2 - 140, 360), (280, 56))


def play_sound(name):
    if not sound_on:
        return
    try:
        getattr(sounds, name).play()
    except Exception:
        pass


def reset_game():
    global score, survive_time, spawn_timer, cross_timer, enemies, holy_cross
    score, survive_time, spawn_timer, cross_timer = 0, 0.0, 0.0, 6.0
    enemies, holy_cross = [], None
    hero.reset((WIDTH // 2, HEIGHT // 2))


def draw_floor():
    tw, th = images.floor.get_width(), images.floor.get_height()
    y = 0
    while y < HEIGHT:
        x = 0
        while x < WIDTH:
            screen.blit("floor", (x, y))
            x += tw
        y += th


def spawn_enemy():
    s, m = random.randint(0, 3), 20
    if s == 0:
        pos = (random.randint(0, WIDTH), -m)
    elif s == 1:
        pos = (WIDTH + m, random.randint(0, HEIGHT))
    elif s == 2:
        pos = (random.randint(0, WIDTH), HEIGHT + m)
    else:
        pos = (-m, random.randint(0, HEIGHT))
    enemies.append(Enemy(Actor(ENEMY_FRAMES[0], pos), ENEMY_FRAMES))


def spawn_cross():
    global holy_cross
    holy_cross = Actor("holycross", (random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40)))


def update(dt):
    global state, survive_time, spawn_timer, cross_timer, holy_cross, enemies, score
    if state != PLAYING:
        return

    survive_time += dt
    hero.update(dt, keyboard, WIDTH, HEIGHT)

    spawn_timer += dt
    if spawn_timer >= SPAWN_INTERVAL:
        spawn_timer = 0.0
        spawn_enemy()

    cross_timer -= dt
    if cross_timer <= 0 and holy_cross is None:
        spawn_cross()
        cross_timer = random.uniform(7.0, 11.0)

    for e in enemies:
        e.update(dt, hero.actor)
        if e.actor.colliderect(hero.actor) and e.hit_cd <= 0:
            hero.hp -= 10
            e.hit_cd = 0.7
            play_sound("hit")

    if holy_cross and hero.actor.colliderect(holy_cross):
        score += len(enemies)
        enemies = []
        hero.hp = min(PLAYER_HP, hero.hp + 30)
        holy_cross = None
        play_sound("click")

    if hero.hp <= 0:
        state = GAME_OVER
        music.stop()
        play_sound("gameover")
    elif survive_time >= WIN_TIME:
        state = WIN
        music.stop()


def draw_menu():
    screen.fill(BG_COLOR)
    screen.draw.text("GLADIADOR ARENA", center=(WIDTH // 2, 110), fontsize=64, color="white")
    screen.draw.filled_rect(btn_start, (60, 90, 140))
    screen.draw.filled_rect(btn_sound, (60, 90, 140))
    screen.draw.filled_rect(btn_exit, (130, 65, 65))
    screen.draw.text("Começar", center=btn_start.center, fontsize=32, color="white")
    screen.draw.text(f"Som: {'ON' if sound_on else 'OFF'}", center=btn_sound.center, fontsize=32, color="white")
    screen.draw.text("Saída", center=btn_exit.center, fontsize=32, color="white")


def draw_play():
    draw_floor()
    for e in enemies:
        e.actor.draw()
    if holy_cross:
        holy_cross.draw()
    hero.actor.draw()

    screen.draw.text(f"HP: {hero.hp}", (16, 14), fontsize=34, color="white")
    screen.draw.text(f"Abates: {score}", (16, 48), fontsize=30, color="white")
    screen.draw.text(f"Sobreviva: {max(0, int(WIN_TIME - survive_time))}s", (16, 78), fontsize=30, color="white")


def draw_end(win):
    draw_play()
    screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (0, 0, 0))
    screen.draw.text("VOCÊ VENCEU!" if win else "GAME OVER",
                     center=(WIDTH // 2, HEIGHT // 2 - 30),
                     fontsize=70,
                     color=(120, 230, 140) if win else (230, 100, 100))
    screen.draw.text("ENTER: menu", center=(WIDTH // 2, HEIGHT // 2 + 36), fontsize=34, color="white")


def draw():
    if state == MENU:
        draw_menu()
    elif state == PLAYING:
        draw_play()
    elif state == WIN:
        draw_end(True)
    else:
        draw_end(False)


def on_mouse_down(pos):
    global state, sound_on
    if state != MENU:
        return

    if btn_start.collidepoint(pos):
        play_sound("click")
        reset_game()
        state = PLAYING
        if sound_on:
            music.play("music")
            music.set_volume(0.35)

    elif btn_sound.collidepoint(pos):
        sound_on = not sound_on
        play_sound("click")
        if not sound_on:
            music.stop()

    elif btn_exit.collidepoint(pos):
        raise SystemExit


def on_key_down(key):
    global state
    if state in (WIN, GAME_OVER) and key == keys.RETURN:
        state = MENU
    elif state == PLAYING and key == keys.ESCAPE:
        state = MENU
        music.stop()


pgzrun.go()
