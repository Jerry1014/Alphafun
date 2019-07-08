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
    return random.randint(0, ROW - 1), random.randint(0, COLUMN - 1)
    # return each_it(1)[1]


def each_it(deep):
    """使用极大极小指下棋
    :param deep:当前迭代深度
    :return:tuple 最大值 对应的下棋位置
    """
    max_point = -sys.maxsize
    pos = (0, 0)
    for j in range(range_x_min, range_x_max):
        for i in range(range_y_min, range_y_max):
            if all_situation[i][j] == 0:
                all_situation[i][j] = -1
                white_situation[i][j] = 1
                # ai试探下一步

                min_point = sys.maxsize
                break_sign = False
                for j in range(range_x_min, range_x_max):
                    for i in range(range_y_min, range_y_max):
                        # 模拟用户下一步
                        if all_situation[i][j] == 0:
                            all_situation[i][j] = 1
                            black_situation[i][j] = 1
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
                            black_situation[i][j] = 0

                    if break_sign:
                        break
                if not break_sign:
                    max_point = min_point
                    pos = (i, j)
                all_situation[i][j] = 0
                white_situation[i][j] = 0
    return max_point, pos


def get_score():
    """对当前局势进行评估，并给出分数"""


# num代表连起来的个数，（活，死）
score = {2: (10, 5), 3: (20, 10), 4: (90, 50), 5: (100, 100)}


def count_score(num, check_situation):
    if check_situation is black_situation:
        color = 1
    count = 0
    condition1 = np.array([True for i in range(num)])
    condition2 = condition1.T
    condition3 = np.array([[True if j != i else False for j in range(num)] for i in range(num)])
    condition4 = np.rot90(condition3, 1)

    for i in range(ROW - num + 1):
        for j in range(COLUMN - num + 1):
            # 左右
            if np.logical_and(check_situation[i, j:j + num], condition1).all():
                # 当左右存在相同棋子时，跳过，避免重复计算
                avoid_recalculate_left = all_situation[i][j - 1] != color if j > 0 else True
                avoid_recalculate_right = all_situation[i][j + num] != color if j + num < COLUMN else True
                if avoid_recalculate_left and avoid_recalculate_right:
                    # 判断左右边界，是活棋还是死棋
                    boundary = (all_situation[i][j - 1] == 1 if j > 0 else True,
                                all_situation[i][j + num] == 1 if j + num < COLUMN else True)
                    if sum(boundary) == 0:
                        count += score[num][0]
                    elif sum(boundary) == 1:
                        count += score[num][1]
                    elif num == 5:
                        count += 100
                        break

            # 上下
            if np.logical_and(check_situation[i:i + num, j], condition2).all():
                avoid_recalculate_top = all_situation[i - 1][j] != color if i > 0 else True
                avoid_recalculate_bottom = all_situation[i + num][j] != color if i + num < ROW else True
                if avoid_recalculate_top and avoid_recalculate_bottom:
                    boundary = (all_situation[i - 1][j] == 1 if i > 0 else True,
                                all_situation[i + num][j] == 1 if i + num < ROW else True)
                    if sum(boundary) == 0:
                        count += score[num][0]
                    elif sum(boundary) == 1:
                        count += score[num][1]
                    elif num == 5:
                        count += 100
                        break

            tem = check_situation[i:i + num, j:j + num]
            # \
            if np.logical_or(tem, condition3).all():
                avoid_recalculate_left_upper = all_situation[i - 1][j - 1] != color if i > 0 and j > 0 else True
                avoid_recalculate_right_lower = all_situation[i + num][
                                                    j + num] != color if i + num < ROW and j + num < COLUMN else True
                if avoid_recalculate_left_upper and avoid_recalculate_right_lower:
                    boundary = (all_situation[i - 1][j - 1] == 1 if i > 0 and j > 0 else True,
                                all_situation[i + num][
                                    j + num] == 1 if i + num < ROW and j + num < COLUMN else True)
                    if sum(boundary) == 0:
                        count += score[num][0]
                    elif sum(boundary) == 1:
                        count += score[num][1]
            # /
            if np.logical_or(tem, condition4).all():
                avoid_recalculate_right_upper = all_situation[i - 1][
                                                    j + num] != color if j + num < COLUMN and i > 0 else True
                avoid_recalculate_left_lower = all_situation[i + num][
                                                   j - 1] != color if j > 0 and i + num < ROW else True
                if avoid_recalculate_right_upper and avoid_recalculate_left_lower:
                    boundary = (all_situation[i - 1][j + num] == 1 if j + num < COLUMN and i > 0 else True,
                                all_situation[i + num][j - 1] == 1 if j > 0 and i + num < ROW else True)
                    if sum(boundary) == 0:
                        count += score[num][0]
                    elif sum(boundary) == 1:
                        count += score[num][1]
                    elif num == 5:
                        count += 100
                        break

    for i in range(ROW - num + 1, ROW):
        for j in range(COLUMN - num + 1):
            if np.logical_and(check_situation[i, j:j + num], condition1).all():
                avoid_recalculate_left = all_situation[i][j - 1] != color if j > 0 else True
                avoid_recalculate_right = all_situation[i][j + num] != color if j + num < COLUMN else True
                if avoid_recalculate_left and avoid_recalculate_right:
                    boundary = (all_situation[i][j - 1] == 1 if j > 0 else True,
                                all_situation[i][j + num] == 1 if j + num < COLUMN else True)
                    if sum(boundary) == 0:
                        count += score[num][0]
                    elif sum(boundary) == 1:
                        count += score[num][1]
                    elif num == 5:
                        count += 100
                        break

    for i in range(ROW - num + 1):
        for j in range(COLUMN - num + 1, COLUMN):
            if np.logical_and(check_situation[i:i + num, j], condition2).all():
                avoid_recalculate_top = all_situation[i - 1][j] != color if i > 0 else True
                avoid_recalculate_bottom = all_situation[i + num][j] != color if i + num < ROW else True
                if avoid_recalculate_top and avoid_recalculate_bottom:
                    boundary = (all_situation[i - 1][j] == 1 if i > 0 else True,
                                all_situation[i + num][j] == 1 if i + num < ROW else True)
                    if sum(boundary) == 0:
                        count += score[num][0]
                    elif sum(boundary) == 1:
                        count += score[num][1]
                    elif num == 5:
                        count += 100
                        break

    return count


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
            player_pos = (round((player_mouse_pos.getY()) / GRID_WIDTH), round((player_mouse_pos.getX()) / GRID_WIDTH))
        all_situation[player_pos[0]][player_pos[1]] = 1
        black_situation[player_pos[0]][player_pos[1]] = 1
        piece = Circle(Point(GRID_WIDTH * player_pos[1], GRID_WIDTH * player_pos[0]), SIZE_OF_CHESSMAN)
        piece.setFill('black')
        piece.draw(win)

        # 检查游戏是否结束
        print(count_score(2, black_situation) + count_score(3, black_situation) + count_score(4, black_situation))
        if count_score(5, black_situation) >= 100:
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
        piece = Circle(Point(GRID_WIDTH * ai_pos[1], GRID_WIDTH * ai_pos[0]), SIZE_OF_CHESSMAN)
        piece.setFill('white')
        piece.draw(win)

        # 检查游戏是否结束
        if count_score(5, white_situation) >= 100:
            Text(Point(100, 120), "白棋胜利").draw(win)
            print('白棋胜利')
            win.getMouse()
            break

    win.close()


if __name__ == '__main__':
    main()
