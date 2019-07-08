from AlphaFun import battle_fun, battle_fun_init
from gobang_AI import battle_gobang, battle_gobang_init
from graphics import *

GRID_WIDTH = 40
SIZE_OF_CHESSMAN = 16
COLUMN = 15
ROW = 15

# 暂未加入输赢判断
# 棋盘初始化
win = GraphWin("Battle with AlphaFun", GRID_WIDTH * (COLUMN - 1), GRID_WIDTH * (ROW - 1))
win.setBackground("yellow")

i1 = 0
while i1 < GRID_WIDTH * (COLUMN - 1):
    Line(Point(i1, 0), Point(i1, GRID_WIDTH * COLUMN)).draw(win)
    i1 = i1 + GRID_WIDTH
i2 = 0
while i2 < GRID_WIDTH * (ROW - 1):
    Line(Point(0, i2), Point(GRID_WIDTH * ROW, i2)).draw(win)
    i2 = i2 + GRID_WIDTH

battle_gobang_init()
pos1 = battle_fun_init()
piece = Circle(Point(GRID_WIDTH * pos1[1], GRID_WIDTH * pos1[0]), SIZE_OF_CHESSMAN)
piece.setFill('black')
piece.draw(win)

while True:
    pos2 = battle_gobang((pos1[1], pos1[0]))
    piece = Circle(Point(GRID_WIDTH * pos2[0], GRID_WIDTH * pos2[1]), SIZE_OF_CHESSMAN)
    piece.setFill('white')
    piece.draw(win)

    pos1 = battle_fun((pos2[1],pos2[0]))
    if type(pos1) == bool:
        if pos1:
            Text(Point(100, 120), "黑棋胜利").draw(win)
            print('黑棋胜利')
        else:
            Text(Point(100, 120), "白棋胜利").draw(win)
            print('白棋胜利')
        win.getMouse()
        break

    piece = Circle(Point(GRID_WIDTH * pos1[1], GRID_WIDTH * pos1[0]), SIZE_OF_CHESSMAN)
    piece.setFill('black')
    piece.draw(win)
