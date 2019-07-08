import random

from graphics import *
import numpy as np

# 行列宽度 棋子大小 行列数 白棋占位标志数
GRID_WIDTH = 40
SIZE_OF_CHESSMAN = 16
COLUMN = 15
ROW = 15

# 棋型的评估分数
shape_score = {
    ()
}

white_situation = np.array([[0 for i in range(COLUMN)] for j in range(ROW)])
black_situation = np.array([[0 for i in range(COLUMN)] for j in range(ROW)])
all_situation = np.array([[0 for i in range(COLUMN)] for j in range(ROW)])


def ai():
    """使用极大极小指下棋
    :return:tuple ai选择的下棋位置
    """
    return random.randint(0, ROW-1), random.randint(0, COLUMN-1)


def chessboard_evaluation():
    """对当前局势进行评估，并给出分数"""
    pass


def check_win(check_situation):
    """检查棋局是否已经结束"""
    win_condition_1 = np.array([True, True, True, True, True])
    win_condition_2 = win_condition_1.T
    win_condition_3 = np.array(
        [[False, True, True, True, True], [True, False, True, True, True], [True, True, False, True, True],
         [True, True, True, False, True], [True, True, True, True, False]])
    win_condition_4 = np.array(
        [[True, True, True, True, False], [True, True, True, False, True], [True, True, False, True, True],
         [True, False, True, True, True], [False, True, True, True, True]])

    for i in range(ROW - 5):
        for j in range(COLUMN - 5):
            if np.logical_and(check_situation[i, j:j + 5], win_condition_1).all():
                return True
            if np.logical_and(check_situation[i:i + 5, j], win_condition_2).all():
                return True
            tem = check_situation[i:i + 5, j:j + 5]
            if np.logical_or(tem, win_condition_3).all():
                return True
            if np.logical_or(tem, win_condition_4).all():
                return True

    for i in range(ROW - 5, ROW):
        for j in range(COLUMN - 5):
            if np.logical_and(check_situation[i, j:j + 5], win_condition_1).all():
                return True

    for i in range(ROW - 5):
        for j in range(COLUMN - 5, COLUMN):
            if np.logical_and(check_situation[i:i + 5, j], win_condition_2).all():
                return True
    return False


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

while True:
    # todo 默认为使用者先手，未来改为可选择
    # todo 未对下棋胜负进行分析
    # 玩家下棋
    player_mouse_pos = win.getMouse()
    player_pos = (round((player_mouse_pos.getY()) / GRID_WIDTH), round((player_mouse_pos.getX()) / GRID_WIDTH))
    while all_situation[player_pos[0]][player_pos[1]] != 0:
        player_mouse_pos = win.getMouse()
        player_pos = (round((player_mouse_pos.getY()) / GRID_WIDTH, round((player_mouse_pos.getX()) / GRID_WIDTH)))
    all_situation[player_pos[0]][player_pos[1]] = 1
    black_situation[player_pos[0]][player_pos[1]] = 1
    piece = Circle(Point(GRID_WIDTH * player_pos[1], GRID_WIDTH * player_pos[0]), SIZE_OF_CHESSMAN)
    piece.setFill('black')
    piece.draw(win)

    if check_win(black_situation):
        Text(Point(100, 120), "黑棋胜利").draw(win)
        print('黑棋胜利')
        win.getMouse()
        break

    # AI下棋
    ai_pos = ai()
    if all_situation[ai_pos[0]][ai_pos[1]] != 0:
        Text(Point(100, 120), "AI投降").draw(win)
        print('AI投降')
        win.getMouse()
        break
    all_situation[ai_pos[0]][ai_pos[1]] = -1
    white_situation[ai_pos[0]][ai_pos[1]] = 1
    piece = Circle(Point(GRID_WIDTH * ai_pos[0], GRID_WIDTH * ai_pos[1]), SIZE_OF_CHESSMAN)
    piece.setFill('white')
    piece.draw(win)

    if check_win(black_situation):
        Text(Point(100, 120), "白棋胜利").draw(win)
        print('白棋胜利')
        win.getMouse()
        break

win.close()
