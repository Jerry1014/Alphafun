import random

from graphics import *
import numpy as np

# 行列宽度 棋子大小 行列数 白棋占位标志数
GRID_WIDTH = 40
SIZE_OF_CHESSMAN = 16
COLUMN = 15
ROW = 15
DEPTH = 1  # 搜索深度，每一"层"包括两层（极大极小）

white_situation = np.array([[0 for i in range(COLUMN)] for j in range(ROW)])
black_situation = np.array([[0 for i in range(COLUMN)] for j in range(ROW)])
all_situation = np.array([[0 for i in range(COLUMN)] for j in range(ROW)])

# 限定搜索范围，加快搜索速度
range_x_min = COLUMN // 2
range_y_min = ROW // 2
range_x_max = COLUMN // 2
range_y_max = ROW // 2


def ai():
    """使用极大极小指下棋
    :return:tuple ai选择的下棋位置
    """
    return each_it(1)[1]


def each_it(deep):
    max_point = -sys.maxsize
    pos = (0, 0)
    for j in range(range_x_min, range_x_max):
        for i in range(range_y_min, range_y_max):
            if all_situation[i][j] == 0:
                all_situation[i][j] = -1
                # ai试探下一步

                min_point = sys.maxsize
                break_sign = False
                for j in range(range_x_min, range_x_max):
                    for i in range(range_y_min, range_y_max):
                        # 模拟用户下一步
                        if all_situation[i][j] == 0:
                            all_situation[i][j] = 1
                            # 若探索深度未到，则递归
                            if deep < DEPTH:
                                tem = each_it(deep + 1)
                            else:
                                tem = get_score()
                            if tem < max_point:
                                # 减枝
                                break_sign = True
                                break
                            elif tem < min_point:
                                min_point = tem
                            all_situation[i][j] = 0

                    if break_sign:
                        break
                if not break_sign:
                    max_point = min_point
                    pos = (i, j)
                all_situation[i][j] = 0
    return max_point, pos


def get_score():
    """对当前局势进行评估，并给出分数"""
    return 1


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


def main():
    # 棋盘初始化
    global range_x_min, range_x_max, range_y_min, range_y_max
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
        # 玩家选择下棋位置
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

        # 检查游戏是否结束
        if check_win(black_situation):
            Text(Point(100, 120), "黑棋胜利").draw(win)
            print('黑棋胜利')
            win.getMouse()
            break

        # 修改搜索范围
        if player_pos[0] - 2 < range_x_min:
            range_x_min = player_pos[0] - 2 if player_pos[0] - 2 > 0 else 0
        if player_pos[0] + 2 > range_x_max:
            range_x_max = player_pos[0] + 2 if player_pos[0] + 2 > COLUMN else COLUMN + 1
        if player_pos[1] - 2 < range_y_min:
            range_y_min = player_pos[1] - 2 if player_pos[1] - 2 > 0 else 0
        if player_pos[1] + 2 > range_y_max:
            range_y_max = player_pos[1] + 2 if player_pos[1] + 2 > ROW else ROW + 1

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

        # 检查游戏是否结束
        if check_win(black_situation):
            Text(Point(100, 120), "白棋胜利").draw(win)
            print('白棋胜利')
            win.getMouse()
            break

    win.close()


if __name__ == '__main__':
    main()
