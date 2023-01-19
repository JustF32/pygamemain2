import collections
import random
import pygame
import importlib
# ВНИМАНИЕ! если ты ни хрена не поймешь смотри строку 270
cooldownMove = 400
cooldownAttack = 1201
cooldownEnemy = 0
class MainBoard:
    def __init__(self, width, height, widthScreen, heightScreen, image):
        self.width = width # ширина
        self.height = height # высота
        self.widthScreen = widthScreen
        self.heightScreen = heightScreen
        self.image = image
        self.board = [[['EMPTY', ''] for i in range(height)] for i in range(width)] # все клетки
        self.left = 10 # отклонение от края
        self.top = 10
        self.cell_size = 128 # размер клеток
        self.zero_cell = [13, 13]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        img = pygame.image.load(self.image)
        img = pygame.transform.scale(img, (896, 896))
        screen.blit(img, (0, 0))

    def set_cellNew(self, pos, type):
        self.board[pos[0]][pos[1]] = type

    def remove_cellNew(self, player_pos):
        self.board[player_pos[0]][player_pos[1]] = ['EMPTY', '']

    def check_cell(self, player_pos):
        num_x = player_pos[0]
        num_y = player_pos[1]
        if self.width > num_x >= 0 and 0 <= num_y < self.height and self.board[num_x][num_y][0] == 'EMPTY':
            return True
        else:
            return False

class Player:
    def __init__(self, curX, curY, board):
        self.curX = curX
        self.curY = curY
        img = pygame.image.load('data/player.png')
        self.img = pygame.transform.scale(img, (90, 150))
        imgShield = pygame.image.load('data/shield.png')
        self.imgShield = pygame.transform.scale(imgShield, (80, 120))
        board.set_cellNew((self.curX, self.curY), ['PLAYER', self])
        self.hp = 5
        self.curWeapon = 'SWORD'

    def gethit(self):
        if self.curWeapon != 'SHIELD':
            pygame.draw.rect(screen, 'black', ((948, 776 - (self.hp * 60)), (50, 50)))
            self.hp -= 1
            print(f'{self.hp}/5 hp')
            if self.hp <= 0:
                deathscreen()
        else:
            print('BLOCKED')
            self.curWeapon = 'SWORD'

    def bowAttack(self, x, y):
        global cooldownAttack, cdType
        cX, cY = x // 128 + mainB.zero_cell[0], y // 128 + mainB.zero_cell[1]
        if mainB.board[cX][cY][0] == 'ENEMY':
            if cooldownAttack >= 2500:
                cooldownAttack = 0
                mainB.board[cX][cY][1].gethit(10, mainB)
                cdType = 'Attack'


    def takeShield(self):
        global cooldownMove, cdType
        print(cooldownMove)
        if cooldownMove >= 400:
            print('YES')
            cooldownMove = 0
            cdType = 'Move'
            self.curWeapon = 'SHIELD'
            renderAll()

    def render(self, screen, x, y):
        screen.blit(self.img, (401, 336))
        if self.curWeapon == 'SHIELD':
            screen.blit(self.imgShield, (421, 356))


    def move(self, x, y, board):
        global cooldownMove, cdType
        if cooldownMove >= 400:
            cooldownMove = 0
        if cooldownMove == 0:
            if mainB.check_cell((self.curX + x, self.curY - y)):
                mainB.remove_cellNew((self.curX, self.curY))
                self.curX += x
                self.curY -= y
                mainB.set_cellNew((self.curX, self.curY), ['PLAYER', self])
                board.zero_cell[0] = self.curX - 3
                board.zero_cell[1] = self.curY - 3
                renderAll()
                pygame.display.flip()
                cdType = 'Move'

    def atackSword(self, board):
        global cooldownAttack, cdType
        if cooldownAttack >= 1200:
            cooldownAttack = 0
        if self.curWeapon == 'SWORD':
            if cooldownAttack == 0:
                try:
                    if board.board[self.curX][self.curY - 1][0] == 'ENEMY':
                        board.board[self.curX][self.curY - 1][1].gethit(1, board)
                        cdType = 'Attack'
                    elif board.board[self.curX][self.curY + 1][0] == 'ENEMY':
                        board.board[self.curX][self.curY + 1][1].gethit(1, board)
                        cdType = 'Attack'
                    elif board.board[self.curX - 1][self.curY][0] == 'ENEMY':
                        board.board[self.curX - 1][self.curY][1].gethit(1, board)
                        cdType = 'Attack'
                    elif board.board[self.curX + 1][self.curY][0] == 'ENEMY':
                        board.board[self.curX + 1][self.curY][1].gethit(1, board)
                        cdType = 'Attack'
                except IndexError:
                    pass

class Enemy:
    def __init__(self, hp, x, y, board, picture):
        self.dead = False
        self.hp = hp
        self.curX = x
        self.curY = y
        self.cooldown = 0
        self.board = board
        img = pygame.image.load('data/' + picture)
        self.img = pygame.transform.scale(img, (100, 150))
        board.set_cellNew((self.curX, self.curY), ['ENEMY', self])

    def render(self, screen, x, y):
        screen.blit(self.img, (x - 128, y - 128))

    def gethit(self, hp, board):
        self.hp -= hp
        if self.hp <= 0:
            print('KILLED')
            board.remove_cellNew((self.curX, self.curY))
            self.dead = True
            renderAll()
            pygame.display.flip()
        else:
            print(f'HITTED ({hp} hp)')
            
    def move(self, x, y):
        mainB.remove_cellNew((self.curX, self.curY))
        self.curX = x
        self.curY = y
        mainB.set_cellNew((self.curX, self.curY), ['ENEMY', self])
        renderAll()
        pygame.display.flip()



class EnemyWarrior(Enemy):

    def __init__(self, hp, x, y, board):
        super().__init__(hp, x, y, board, 'SkeletEnemy.png')

    def clockTime(self):
        global EnemyClock
        if self.dead == False:
            self.cooldown += EnemyClock.get_time()
            if self.cooldown >= 1000:
                self.cooldown = 0
                try:
                    x, y = self.MoveAI(mainB.board, (self.curX, self.curY), 'PLAYER', 'WALL')
                    if x == -999:
                        print('ATTACKED')
                        player.gethit()

                    else:
                        self.move(x, y)
                except TypeError:
                    pass

    def MoveAI(self, grid, start, goal, wall):
        queue = collections.deque([[start]])
        seen = {start}
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if grid[x][y][0] == goal:
                if len(path) > 2:
                    return path[1]
                else:
                    return -999, -999
            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2][0] != wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))


class EnemyBowman(Enemy):
    def __init__(self, hp, x, y, board):
        super().__init__(hp, x, y, board, 'ArcherEnemy.png')

    def clockTime(self):
        global EnemyClock
        if self.dead == False:
            self.cooldown += EnemyClock.get_time()
            if self.cooldown >= 1500:
                self.cooldown = 0
                try:
                    x, y = self.MoveAI(mainB.board, (self.curX, self.curY), 'PLAYER', 'WALL')
                    if x == -999:
                        player.gethit()
                    elif x == -111:
                        pass
                    else:
                        self.move(x, y)
                except TypeError:
                    pass

    def MoveAI(self, grid, start, goal, wall):
        queue = collections.deque([[start]])
        seen = {start}
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if grid[x][y][0] == goal:
                if 9 > len(path) > 4:
                    return path[1]
                elif len(path) >= 9:
                    return - 111, -111
                else:
                    return -999, -999
            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2][0] != wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
        

class Wall:
    def __init__(self, x, y, img):
        self.death = False
        self.curX = x
        self.curY = y
        img = 'data/' + img
        self.imgage = pygame.image.load(img)
        self.imgage = pygame.transform.scale(self.imgage, (300, 300))
        mainB.set_cellNew((self.curX, self.curY), ['WALL', self])

class Wall1:
    def __init__(self, x, y, img):
        self.death = False
        self.curX = x
        self.curY = y
        img = 'data/' + img
        self.imgage = pygame.image.load(img)
        self.imgage = pygame.transform.scale(self.imgage, (150, 150))
        mainB.set_cellNew((self.curX, self.curY), ['xd', self])


class Column(Wall):
    def __init__(self, x, y):
        super().__init__(x, y, 'Colona1.png')

    def render(self, screen, x, y):
        screen.blit(self.imgage, (x - 210, y - 260))

class Tree(Wall):
    def __init__(self, x, y):
        super().__init__(x, y, 'Tree.png')

    def render(self, screen, x, y):
        screen.blit(self.imgage, (x - 190, y - 260))

class Tree1(Wall):
    def __init__(self, x, y):
        super().__init__(x, y, 'Tree2.png')

    def render(self, screen, x, y):
        screen.blit(self.imgage, (x - 210, y - 260))

class Fountain(Wall1):
    def __init__(self, x, y):
        super().__init__(x, y, 'fountain.png')

    def render(self, screen, x, y):
        screen.blit(self.imgage, (x - 130, y - 140))

class Chest_main:
    #если хочешь допишешь типо, сундука текстурка есть - сейчас это просто стена
    def __init__(self, x, y, img):
        self.death = False
        self.curX = x
        self.curY = y
        img = 'data/' + img
        self.imgage = pygame.image.load(img)
        self.imgage = pygame.transform.scale(self.imgage, (300, 300))
        mainB.set_cellNew((self.curX, self.curY), ['WALL', self])


class Chest_obj(Chest_main):
    def __init__(self, x, y):
        super().__init__(x, y, "Chest.png")

    def render(self, screen, x, y):
        screen.blit(self.imgage, (x -850, y - 850))



def deathscreen():
    player.hp = 5
    running = False
    import end_level
    importlib.reload(end_level)



def renderAll():
    mainB.render(screen)
    sX, sY = mainB.zero_cell
    posX, posY = 120, 64
    for i in range(sX, sX + mainB.widthScreen):
        for j in range(sY, sY + mainB.heightScreen):
            if mainB.board[i][j][1] != '':
                mainB.board[i][j][1].render(screen, posX, posY)
            posY += 128
        posX += 128
        posY = 64
    pygame.draw.rect(screen, 'black', ((895, 10), (40, 900)))
    if player.curWeapon != 'BOW':
        screen.blit(ArroWPic, (890, 150))
    else:
        screen.blit(ArroWPic, (890, 300))



#if __name__ == '__main__':
pygame.init()
cdType = 'None'
col2 = 0
clock = pygame.time.Clock()
EnemyClock = pygame.time.Clock()
cellSize = 64
size = width, height = 1024, 896
screen = pygame.display.set_mode(size)

# основные объекты
# короче - что бы создавать объекты для врага пишешь здоровье + координаты по таблице, для коллоны просто корды
mainB = MainBoard(128, 128, 7, 7, 'finalflor.jpg')
mainB.set_view(100, 100, 128)
player = Player(16, 16, mainB)
enemy1 = EnemyWarrior(2, 14, 14, mainB)
enemy2 = EnemyBowman(1, 14, 24, mainB)
colon1 = Column(5, 5)
tree = Tree(13, 13)
colon3 = Column(9, 9)

border = Tree(26, 23)
border1 = Tree(26, 24)
border2 = Tree(26, 25)
border3 = Tree(27, 24)
border4 = Tree(27, 25)
border5 = Tree(26, 26)
border6 = Tree(27, 26)
border7 = Tree(28, 26)
border8 = Tree(27, 27)
border9 = Tree(28, 27)
border10 = Tree(28, 28)
border11 = Tree(28, 29)
border12 = Tree(28, 25)
border13 = Tree(25, 25)

america_great_again = Column(13, 22)
america_great_again1 = Column(13, 25)
for y in range(23, 26):
    pon = Column(13, y)
for x in range(14, 16):
    pon = Column(x, 25)



fountain = Fountain(21,17)
eger = Tree1(23, 15)
eger1 = Tree1(23, 18)
eger2 = Tree1(18, 18)
eger3 = Tree1(18, 15)
enemy1 = EnemyWarrior(5, 19, 15, mainB)
enemy2 = EnemyWarrior(5, 19, 18, mainB)
enemy3 = EnemyBowman(1, 24, 18, mainB)
enemy4 = EnemyBowman(1, 24, 15, mainB)
enemy5 = EnemyWarrior(5, 15, 23, mainB)

# это типо границы поля можешь поставить любые хз)
# если враг стоит на месте значит он к тебе не может попасть)

for i in range(3):
    for x in range(10 - i, 26 + i):
        tree = Tree(10 + i, x)
    for x in range(10 - i, 26 + i):
        tree = Tree(x, 10 + i)
    for x in range(10 - i, 27 + i):
        tree = Tree(26 + i, x)
    for x in range(10 - i, 26 + i):
        tree = Tree(x, 26 + i)

# прочее
SwordPic = pygame.transform.scale(pygame.image.load('data/sword.png'), (100, 150))
screen.blit(SwordPic, (920, 100))
SwordPic = pygame.transform.scale(pygame.image.load('data/bow.png'), (100, 150))
screen.blit(SwordPic, (920, 250))
ArroWPic = pygame.transform.scale(pygame.image.load('data/ArroW.png'), (50, 50))
screen.blit(ArroWPic, (890, 150))
myfont1 = pygame.font.SysFont("monospace", 15)
myfont2 = pygame.font.SysFont("monospace", 20)
for x in range(player.hp + 1):
    heart = pygame.transform.scale(pygame.image.load('data/hp.png'), (50, 50))
    screen.blit(heart, (948, 776 - x * 60))
renderAll()
player.move(0, 0, mainB)

'''for x in mainB.board:
    for j in x:
        print(j[0], end=' ')
    print()'''
isPressed = False

running = True
while running: # ивееентики))
    clock.tick(10)
    EnemyClock.tick(random.randint(8, 12))
    '''
    enemy1.clockTime()
    enemy2.clockTime()
    enemy3.clockTime()
    enemy4.clockTime()
    enemy5.clockTime()'''
    if cdType != 'None':
        cooldownMove += clock.get_time()
        cooldownAttack += clock.get_time()
    if cooldownMove >= 400 and player.curWeapon == 'SHIELD':
        player.curWeapon = 'SWORD'
        renderAll()
    pygame.draw.rect(screen, 'black', ((895, 779), (1023, 892)))
    pygame.draw.rect(screen, 'black', ((906, 28), (1014, 96)))
    if cdType == 'Move':
        col2 = round(0.4 - round(cooldownMove / 1000, 2), 2)
    else:
        if player.curWeapon == 'SWORD':
            col2 = round(1.2 - round(cooldownAttack / 1000, 2), 2)
        else:
            col2 = round(2.5 - round(cooldownAttack / 1000, 2), 2)
    if col2 < 0:
        col2 = 0
    label = myfont1.render(f"Перезарядка:", True, (255, 255, 0))
    label2 = myfont2.render(str(col2), True, (255, 255, 0))
    label3 = myfont1.render(f"Оружие:", True, (255, 255, 0))
    screen.blit(label, (900, 820))
    screen.blit(label2, (940, 850))
    screen.blit(label3, (930, 60))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.curWeapon == 'BOW':
                x, y = event.pos
                player.bowAttack(x, y)
        keyState = pygame.key.get_pressed()
        if not isPressed:
            if keyState[pygame.K_UP]:
                player.move(0, 1, mainB)
                isPressed = True
                break
            elif keyState[pygame.K_DOWN]:
                player.move(0, -1, mainB)
                isPressed = True
                break
            elif keyState[pygame.K_RIGHT]:
                player.move(1, 0, mainB)
                isPressed = True
                break
            elif keyState[pygame.K_LEFT]:
                player.move(-1, 0, mainB)
                isPressed = True
                break
            if keyState[pygame.K_SPACE]:
                isPressed = True
                player.atackSword(mainB)

            if keyState[pygame.K_LSHIFT]:
                player.takeShield()

            if keyState[pygame.K_q]:
                pygame.draw.rect(screen, 'black', ((895, 100), (40, 300)))
                screen.blit(ArroWPic, (890, 150))
                player.curWeapon = 'SWORD'

            if keyState[pygame.K_w]:
                player.curWeapon = 'BOW'
                pygame.draw.rect(screen, 'black', ((895, 100), (40, 300)))
                screen.blit(ArroWPic, (890, 300))
                print('YES')

            if keyState[pygame.K_LSHIFT]:
                player.curWeapon = 'SHIELD'

        if event.type == pygame.KEYUP:
            isPressed = False
        pygame.event.pump()




