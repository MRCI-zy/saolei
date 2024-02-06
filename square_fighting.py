if __name__ == "__main__":
    print("测试中")

import pygame
import math
import time
import random

PI = math.pi


class My_square:
    hp = 100
    color = (0, 0, 0)
    orientation_len = None
    orientation_color = (0, 0, 0)
    rect = None
    side = None
    speed = 0
    acc = None
    friction = None
    angle = 0
    speed_direction = 0
    acc_direction = 0
    steering_sensitivity = None
    angle_velocity = None
    life = True
    life_over = 0
    move_list = [False, False, False, False]

    def __init__(self, rect, side, acc, friction, angle_velocity, steering_sensitivity):
        self.rect = rect
        self.side = side
        self.acc = acc
        self.friction = friction
        self.angle_velocity = angle_velocity
        self.orientation_len = side * 1
        self.steering_sensitivity = steering_sensitivity

    def move_set(self, key, key_type):
        if key == 'w' and key_type == "DOWN":
            self.move_list[0] = True
        if key == 's' and key_type == "DOWN":
            self.move_list[1] = True
        if key == 'a' and key_type == "DOWN":
            self.move_list[2] = True
        if key == 'd' and key_type == "DOWN":
            self.move_list[3] = True
        if key == 'w' and key_type == "UP":
            self.move_list[0] = False
        if key == 's' and key_type == "UP":
            self.move_list[1] = False
        if key == 'a' and key_type == "UP":
            self.move_list[2] = False
        if key == 'd' and key_type == "UP":
            self.move_list[3] = False

    def move(self):
        if self.move_list[0]:
            self.amend_speed()
        if self.move_list[1]:
            self.speed -= self.speed * self.friction * 3
        if self.move_list[2]:
            self.acc_direction -= self.steering_sensitivity
        if self.move_list[3]:
            self.acc_direction += self.steering_sensitivity
        self.speed -= self.speed * self.friction

    def orientation_patch(self):
        if self.angle >= PI:
            self.angle -= PI * 2
        if self.speed_direction >= PI:
            self.speed_direction -= PI * 2
        if self.acc_direction >= PI:
            self.acc_direction -= PI * 2

    def spin(self):
        self.angle += self.angle_velocity

    def advance(self):
        lx, ly = self.rect
        self.rect = lx + self.speed * math.cos(self.speed_direction), ly + self.speed * math.sin(self.speed_direction)

    def amend_speed(self):
        x1, y1 = self.speed * math.cos(self.speed_direction), self.speed * math.sin(self.speed_direction)
        x2, y2 = self.acc * math.cos(self.acc_direction), self.acc * math.sin(self.acc_direction)
        self.speed = math.sqrt(math.pow(y1 + y2, 2) + math.pow(x1 + x2, 2))
        if x1 + x2 == 0:
            self.speed_direction = PI / 2
        else:
            rphi = math.atan((y1 + y2) / (x1 + x2))
            self.speed_direction = rphi
        if x1 + x2 < 0:
            self.speed_direction += PI

    def draw(self):
        # 开始绘制本体
        s = math.sin(self.angle)
        c = math.cos(self.angle)
        sx, sy = self.side, self.side
        clx, cly = self.rect
        point = [(- sx / 2, - sy / 2), (- sx / 2, + sy / 2), (+ sx / 2, + sy / 2),
                 (+ sx / 2, - sy / 2)]
        for i in range(4):
            x, y = point[i]
            x, y = x * c - y * s, x * s + y * c
            point[i] = (clx + x, cly + y)
        pygame.draw.lines(window, self.color, True, point)
        if self.life:
            # 开始绘制朝向
            lx, ly = self.rect
            pygame.draw.line(window, self.color, self.rect, (lx + self.orientation_len * math.cos(self.acc_direction),
                                                             ly + self.orientation_len * math.sin(self.acc_direction)))
            # draw hp
            rx, ry = self.rect
            pygame.draw.arc(window, (200, 2 * self.hp, 2 * self.hp),
                            (rx - self.side, ry - self.side, 2 * self.side, 2 * self.side), PI/2,
                            PI * (self.hp+25) / 50)

    def shoot(self):
        if self.life:
            lx, ly = self.rect
            color = (0, 0, 0)
            rect = (lx + self.orientation_len * math.cos(self.acc_direction),
                    ly + self.orientation_len * math.sin(self.acc_direction))
            side = 3
            speed = self.speed * math.cos(self.speed_direction - self.acc_direction) + 10
            angle = self.acc_direction
            my_button_list.append(Button(color, rect, side, speed, angle))

    def crash(self):
        w, h = window.get_size()
        rx, ry = self.rect
        s = math.sin(self.angle)
        c = math.cos(self.angle)
        sx, sy = self.side, self.side
        clx, cly = self.rect
        point = [(- sx / 2, - sy / 2), (- sx / 2, + sy / 2), (+ sx / 2, + sy / 2),
                 (+ sx / 2, - sy / 2)]
        for i in range(4):
            x, y = point[i]
            x, y = x * c - y * s, x * s + y * c
            point[i] = (clx + x, cly + y)
            if clx + x >= w or clx + x <= 0 or cly + y <= 0 or cly + y >= h:
                if clx + x >= w or clx + x <= 0:
                    if clx + x >= w:
                        self.rect = (w - x, ry)
                    elif clx + x <= 0:
                        self.rect = (-x, ry)
                    self.speed_direction = PI - self.speed_direction
                if cly + y <= 0 or cly + y >= h:
                    if cly + y <= 0:
                        self.rect = (rx, -y)
                    elif cly + y >= h:
                        self.rect = (rx, h - y)
                    self.speed_direction *= -1
                self.speed *= 0.7

    def run(self):
        if self.hp > 0:
            self.orientation_patch()
            self.advance()
            self.move()
            self.crash()
        if self.hp <= 0:
            self.life = False
            self.life_over += 1
            self.angle += self.life_over * PI/720
            if self.life_over <= 40:
                self.side += 2 - self.life_over/20
            else:
                self.side -= 4 - self.life_over/20
        if self.life_over <= 60:
            self.draw()
            self.spin()


class Shard:
    angle = None
    rect = None
    side = None
    angle_velocity = None
    color = None



class Button:
    life_over = 0
    color = None
    rect = None
    side = None
    speed = None
    angle = None
    life = True
    move = True
    r = 0

    def __init__(self, color, rect, side, speed, angle):
        self.color = color
        self.rect = rect
        self.side = side
        self.speed = speed
        self.angle = angle

    @staticmethod
    def advance(button_list):
        for button in button_list:
            if button.life and button.move:
                lx, ly = button.rect
                button.rect = lx + button.speed * math.cos(button.angle), ly + button.speed * math.sin(button.angle)

    @staticmethod
    def crash(button_list, player: My_square):
        # 告诉文件，中心位置，偏转角，鼠标位置
        for button in button_list:
            px, py = button.rect
            cx, cy = player.rect
            x, y = px - cx, py - cy
            # 通过矩阵变换判断x,y是否在矩形范围内
            rx, ry = x * math.cos(player.angle) + y * math.sin(player.angle), - x * math.sin(
                player.angle) + y * math.cos(player.angle)
            if -player.side / 2 < rx < player.side / 2 and -player.side / 2 < ry < player.side / 2:
                button.life = False
                if button.life_over == 0:
                    player.hp -= 10

    @staticmethod
    def draw(button_list):
        for button in button_list:
            pygame.draw.circle(window, button.color, button.rect, button.side, button.r)

    @staticmethod
    def auto_clear(button_list: list):
        for button in button_list:
            x, y = button.rect
            w, h = window.get_size()
            if x < 0 or x > w or y < 0 or y > h:
                button.life = False
            if not button.life:
                button.r = 2
                button.side = button.life_over
                button.life_over += 2
            if button.life_over >= 20:
                button_list.remove(button)


class Emery_button(Button):
    def __init__(self, button_list: list):
        w, h = window.get_size()
        x = random.randint(1, w)
        y = random.randint(1, h)

        side = 33

        speed = 10

        angle = 0

        color = (255, 255, 255)

        rect = x, y

        self.r = 3
        self.life_over = -30
        self.move = False
        super().__init__(color, rect, side, speed, angle)
        button_list.append(self)

    @staticmethod
    def advance(button_list):
        for self in button_list:
            if self.life_over == 0:
                self.move = True
                Button.advance(button_list)
                self.move = False
            elif self.life_over == -1:
                x, y = self.rect
                mx, my = me.rect
                self.angle = math.atan((y - my) / (x - mx))
                if x - mx > 0:
                    self.angle += PI
                self.r = 0
                self.life_over += 1
                self.side -= 1
            else:
                self.life_over += 1
                self.side -= 1
                r, b, g = self.color
                self.color = (r, b - 7, g - 7)

    @staticmethod
    def summon(button_list, l_num, l_dt, c):
        if l_num % (l_dt / c) == 0:
            Emery_button(button_list)
        Emery_button.advance(emery_button_list)
        if me.life:
            Emery_button.crash(emery_button_list, me)
        Button.auto_clear(emery_button_list)
        Button.draw(emery_button_list)


pygame.init()

Win_W = 1200
Win_H = 800
window = pygame.display.set_mode((Win_W, Win_H))
#
me = My_square((50, 50), 30, 1, 0.06, PI / 60, PI / 20)
my_button_list = []
emery_button_list = []
#
RUNNING = True
dt = 60
num = 0
while RUNNING:
    num += 1
    if num == 60:
        num = 0
    time.sleep(1 / dt)
    window.fill((255, 255, 255))
    me.run()
    Emery_button.summon(emery_button_list, num, dt, 10)
    Button.draw(my_button_list)
    Button.advance(my_button_list)
    Button.auto_clear(my_button_list)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            print(event.key)
            try:
                KEY = chr(event.key)
            except ValueError:
                KEY = 0
            if event.key == 27:
                RUNNING = False
            elif event.key == 32:
                me.shoot()
            else:
                me.move_set(KEY, "DOWN")

        elif event.type == pygame.KEYUP:
            try:
                KEY = chr(event.key)
            except ValueError:
                KEY = 0
            me.move_set(KEY, "UP")
