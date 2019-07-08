from graphics import *
import numpy as np

# 行列宽度 棋子大小 行列数 白棋占位标志数
GRID_WIDTH = 40
SIZE_OF_CHESSMAN = 16
COLUMN = 15
ROW = 15
SIGN_OF_WHITE = 100

situation = np.array([[0 for i in range(COLUMN)] for j in range(ROW)])


def ai():
    """使用极大极小指下棋
    :return:tuple ai选择的下棋位置
    """
    return 0, 0


# 棋盘初始化
win = GraphWin("Battle with AlphaFun", GRID_WIDTH * COLUMN, GRID_WIDTH * ROW)
win.setBackground("yellow")

i1 = 0
while i1 <= GRID_WIDTH * COLUMN:
    Line(Point(i1, 0), Point(i1, GRID_WIDTH * COLUMN)).draw(win)
    i1 = i1 + GRID_WIDTH
i2 = 0
while i2 <= GRID_WIDTH * ROW:
    Line(Point(0, i2), Point(GRID_WIDTH * ROW, i2)).draw(win)
    i2 = i2 + GRID_WIDTH

while True:
    # todo 默认为使用者先手，未来改为可选择
    # todo 未对下棋胜负进行分析
    # 玩家下棋
    player_mouse_pos = win.getMouse()
    player_pos = (round((player_mouse_pos.getX()) / GRID_WIDTH), round((player_mouse_pos.getY()) / GRID_WIDTH))
    while situation[player_pos[0]][player_pos[1]] != 0:
        player_mouse_pos = win.getMouse()
        player_pos = (round((player_mouse_pos.getX()) / GRID_WIDTH), round((player_mouse_pos.getY()) / GRID_WIDTH))
    situation[player_pos[0]][player_pos[1]] = 1
    piece = Circle(Point(GRID_WIDTH * player_pos[0], GRID_WIDTH * player_pos[1]), SIZE_OF_CHESSMAN)
    piece.setFill('black')
    piece.draw(win)

    # AI下棋
    ai_pos = ai()
    if situation[ai_pos[0]][ai_pos[1]] != 0:
        Text(Point(100, 120), "AI投降").draw(win)
        print('AI投降')
        win.getMouse()
        break
    situation[ai_pos[0]][ai_pos[1]] = SIGN_OF_WHITE
    piece = Circle(Point(GRID_WIDTH * ai_pos[0], GRID_WIDTH * ai_pos[1]), SIZE_OF_CHESSMAN)
    piece.setFill('white')
    piece.draw(win)

    print(situation)

win.close()
