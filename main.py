import pygame as pg

from gen_field import *

from pygame.colordict import THECOLORS as COLORS

W_HEIGHT, W_WIDTH = 600, 800
FPS = 10
N, M = 30, 40
C_HEIGHT, C_WIDTH = W_HEIGHT / N, W_WIDTH / M

MURDER_C, ALIVE_C = COLORS["black"], COLORS['white']

class Cell(pg.sprite.Sprite):

    def __init__(self, position, state, i, j):
        super().__init__()
        self.i = i
        self.j = j
        self.state = state
        self.image = pg.Surface((C_WIDTH-0.1, C_HEIGHT-0.1))
        self.rect  = self.image.get_rect()
        self.rect.topleft = position

    def update(self, field_):
        self.state = field_[self.i][self.j]
        color = MURDER_C
        if self.state == 1:
            color = ALIVE_C

        self.image.fill(color)


pg.init()

main_screen = pg.display.set_mode((W_WIDTH, W_HEIGHT))
main_clock = pg.time.Clock()
field_ = create_field(N, M)

field = pg.sprite.Group()

for i in range(N):
    for j in range(M):
        field.add(
            Cell(
                position=(C_WIDTH * j, C_HEIGHT * i), 
                state=field_[i+1][j+1],
                i=i+1,
                j=j+1
            )
        )

time = 0
is_running = True
flag = False
simulation = False
while is_running:
    timedelta = main_clock.tick(FPS)
    time += timedelta

    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
        # else:
            # print(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            flag = True
        if event.type == pg.MOUSEMOTION:
            if flag:
                x, y = event.pos
                i, j = int(y / C_WIDTH), int(x / C_HEIGHT)
                field_[i][j] = 1
        if event.type == pg.MOUSEBUTTONUP:
            flag = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                simulation = True
    if simulation:
        field_ = new_field_of_life(field_, N, M)

    field.update(field_)

    main_screen.fill(COLORS['black'])
    field.draw(main_screen)

    pg.display.flip()

pg.quit()
