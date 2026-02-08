import random
import math


class Hero:
    def __init__(self, actor, frames, hp, speed):
        self.actor = actor
        self.frames = frames
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.anim_t = 0.0
        self.frame_i = 0

    def reset(self, pos):
        self.actor.pos = pos
        self.actor.image = self.frames[0]
        self.hp = self.max_hp
        self.anim_t = 0.0
        self.frame_i = 0

    def update(self, dt, keyboard, w, h):
        dx = (keyboard.right or keyboard.d) - (keyboard.left or keyboard.a)
        dy = (keyboard.down or keyboard.s) - (keyboard.up or keyboard.w)
        moving = dx != 0 or dy != 0

        if dx and dy:
            dx *= 0.70710678
            dy *= 0.70710678

        self.actor.x += dx * self.speed * dt
        self.actor.y += dy * self.speed * dt

        hw, hh = self.actor.width / 2, self.actor.height / 2
        self.actor.x = max(hw, min(w - hw, self.actor.x))
        self.actor.y = max(hh, min(h - hh, self.actor.y))

        self.anim_t += dt * (1.0 if moving else 0.45)
        if self.anim_t >= 0.12:
            self.anim_t = 0.0
            self.frame_i = (self.frame_i + 1) % len(self.frames)
            self.actor.image = self.frames[self.frame_i]


class Enemy:
    def __init__(self, actor, frames):
        self.actor = actor
        self.frames = frames
        self.speed = random.uniform(60, 95)
        self.hit_cd = 0.0
        self.anim_t = 0.0
        self.frame_i = random.randint(0, len(frames) - 1)

    def update(self, dt, hero_actor):
        dx = hero_actor.x - self.actor.x
        dy = hero_actor.y - self.actor.y
        d = math.hypot(dx, dy)

        if d > 0.0001:
            self.actor.x += (dx / d) * self.speed * dt
            self.actor.y += (dy / d) * self.speed * dt

        self.anim_t += dt
        if self.anim_t >= 0.16:
            self.anim_t = 0.0
            self.frame_i = (self.frame_i + 1) % len(self.frames)
            self.actor.image = self.frames[self.frame_i]

        if self.hit_cd > 0:
            self.hit_cd -= dt
