import numpy as np
import sys

WIN = 1  # 1000000    白赢
LOSE = 2  # -10000000  黑赢
wflex4 = 3  # 50000      白活4
bflex4 = 4  # -100000    黑活4
wrush4 = 5  # 400        白冲4
brush4 = 6  # -100000    黑冲4
wflex3 = 7  # 400        白活3
bflex3 = 8  # -8000      黑活3
wblock3 = 9  # 20         白眠3
bblock3 = 10  # -50        黑眠3
wflex2 = 11  # 20         白活2
bflex2 = 12  # -50        黑活2
wblock2 = 13  # 1          白眠2
bblock2 = 14  # -3         黑眠2
wflex1 = 15  # 1          白活1
bflex1 = 16  # -5          黑活1
wdead4 = 17  # -2         白死4
bdead4 = 18  # 5          黑死4
wdead3 = 19  # -2         白死3
bdead3 = 20  # 5          黑死3
wdead2 = 21  # -2         白死2
bdead2 = 22  # 5          黑死2

blank = 0
black = 1
people = 1
robot = 2
white = 2
border = 3

# 创建4x3x3x3x3x4的数组存类型,相当于一个表用来查的
a = np.zeros(4 * 3 * 3 * 3 * 3 * 4).reshape(4, 3, 3, 3, 3, 4)

class Evaluate:  # 评估类
    def __init__(self, a):  # 初始化a,之后a就不变了
        # 白赢
        a[2][2][2][2][2][2] = WIN
        a[2][2][2][2][2][0] = WIN
        a[0][2][2][2][2][2] = WIN
        a[2][2][2][2][2][1] = WIN
        a[1][2][2][2][2][2] = WIN
        a[3][2][2][2][2][2] = WIN
        a[2][2][2][2][2][3] = WIN
        # 白输
        a[1][1][1][1][1][1] = LOSE
        a[1][1][1][1][1][0] = LOSE
        a[0][1][1][1][1][1] = LOSE
        a[1][1][1][1][1][2] = LOSE
        a[2][1][1][1][1][1] = LOSE
        a[3][1][1][1][1][1] = LOSE
        a[1][1][1][1][1][3] = LOSE
        # 白活4
        a[0][2][2][2][2][0] = wflex4
        # 黑活4
        a[0][1][1][1][1][0] = bflex4
        # 白死4
        a[1][2][2][2][2][1] = wdead4
        a[3][2][2][2][2][1] = wdead4
        a[1][2][2][2][2][3] = wdead4
        # 黑死4
        a[2][1][1][1][1][2] = bdead4
        a[3][1][1][1][1][2] = bdead4
        a[2][1][1][1][1][3] = bdead4
        # 白死3
        a[1][1][2][2][2][1] = wdead3
        a[1][2][2][2][1][1] = wdead3
        a[1][1][2][2][2][3] = wdead3
        a[3][2][2][2][1][1] = wdead3
        a[3][1][2][2][2][1] = wdead3
        a[1][2][2][2][1][3] = wdead3
        # 黑死3
        a[2][2][1][1][1][2] = bdead3
        a[2][1][1][1][2][2] = bdead3
        a[2][2][1][1][1][3] = bdead3
        a[3][1][1][1][2][2] = bdead3
        a[3][2][1][1][1][2] = bdead3
        a[2][1][1][1][2][3] = bdead3
        # 白死2
        a[1][2][2][1][1][1] = wdead2
        a[3][2][2][1][1][1] = wdead2
        a[1][2][2][1][1][3] = wdead2
        a[1][1][2][2][1][1] = wdead2
        a[3][1][2][2][1][1] = wdead2
        a[1][1][2][2][1][3] = wdead2
        a[1][1][1][2][2][1] = wdead2
        a[3][1][1][2][2][1] = wdead2
        a[1][1][1][2][2][3] = wdead2
        # 黑死2
        a[2][1][1][2][2][2] = bdead2
        a[3][1][1][2][2][2] = bdead2
        a[2][1][1][2][2][3] = bdead2
        a[2][2][1][1][2][2] = bdead2
        a[3][2][1][1][2][2] = bdead2
        a[2][2][1][1][2][3] = bdead2
        a[2][2][2][1][1][2] = bdead2
        a[3][2][2][1][1][2] = bdead2
        a[2][2][2][1][1][3] = bdead2

        for p1 in range(4):
            for p2 in range(3):
                for p3 in range(3):
                    for p4 in range(3):
                        for p5 in range(3):
                            for p6 in range(4):
                                # lx:左5中黑个数,ly:左5中白个数,rx:右5中黑个数,ry:右5中白个数
                                lx = ly = rx = ry = 0
                                if p1 == 1:
                                    lx += 1
                                elif p1 == 2:
                                    ly += 1
                                if p2 == 1:
                                    lx += 1
                                    rx += 1
                                elif p2 == 2:
                                    ly += 1
                                    ry += 1
                                if p3 == 1:
                                    lx += 1
                                    rx += 1
                                elif p3 == 2:
                                    ly += 1
                                    ry += 1
                                if p4 == 1:
                                    lx += 1
                                    rx += 1
                                elif p4 == 2:
                                    ly += 1
                                    ry += 1
                                if p5 == 1:
                                    lx += 1
                                    rx += 1
                                elif p5 == 2:
                                    ly += 1
                                    ry += 1
                                if p6 == 1:
                                    rx += 1
                                elif p6 == 2:
                                    ry += 1
                                # 考虑边界情况
                                if p1 == 3 or p6 == 3:  # 有边界
                                    if p1 == 3 and p6 != 3:  # 左边界
                                        # 白冲4
                                        if rx == 0 and ry == 4:  # 若右边有空位是活4也没关系，因为活4权重远大于冲4，再加上冲4权重变化可以不计
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = wrush4
                                        # 黑冲4
                                        if rx == 4 and ry == 0:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = brush4
                                        # 白眠3
                                        if rx == 0 and ry == 3:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = wblock3
                                        # 黑眠3
                                        if rx == 3 and ry == 0:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = bblock3
                                        # 白眠2
                                        if rx == 0 and ry == 2:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = wblock2
                                        # 黑眠2
                                        if rx == 2 and ry == 0:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = bblock2
                                    elif p6 == 3 and p1 != 3:  # 右边界
                                        # 白冲4
                                        if lx == 0 and ly == 4:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = wrush4
                                        # 黑冲4
                                        if lx == 4 and ly == 0:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = brush4
                                        # 白眠3
                                        if lx == 0 and ly == 3:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = wblock3
                                        # 黑眠3
                                        if lx == 3 and ly == 0:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = bblock3
                                        # 白眠2
                                        if lx == 0 and ly == 2:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = wblock2
                                        # 黑眠2
                                        if lx == 2 and ly == 0:
                                            if a[p1][p2][p3][p4][p5][p6] == 0:
                                                a[p1][p2][p3][p4][p5][p6] = bblock2
                                else:  # 无边界
                                    # 白冲4
                                    if (lx == 0 and ly == 4) or (rx == 0 and ry == 4):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = wrush4
                                    # 黑冲4
                                    if (lx == 4 and ly == 0) or (rx == 4 and ry == 0):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = brush4
                                    # 白活3
                                    if (ly == 3 and ry == 3) and (lx == 0 and rx == 0):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = wflex3
                                    # 白眠3
                                    if (lx == 0 and ly == 3) or (rx == 0 and ry == 3):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = wblock3
                                    # 黑活3
                                    if (ly == 0 and ry == 0) and (lx == 3 and rx == 3):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = bflex3
                                    # 黑眠3
                                    if (lx == 3 and ly == 0) or (rx == 3 and ry == 0):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = bblock3
                                    # 白活2
                                    if (ly == 2 and ry == 2) and (lx == 0 and rx == 0):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = wflex2
                                    # 白眠2
                                    if (lx == 0 and ly == 2) or (rx == 0 and ry == 2):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = wblock2
                                    # 白活2
                                    if (ly == 0 and ry == 0) and (lx == 2 and rx == 2):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = bflex2
                                    # 黑眠2
                                    if (lx == 2 and ly == 0) or (rx == 2 and ry == 0):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = bblock2
                                    # 白活1
                                    if (ly == 1 and ry == 1) and (lx == 0 and rx == 0):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = wflex1
                                    # 黑活1
                                    if (ly == 0 and ry == 0) and (lx == 1 and rx == 1):
                                        if a[p1][p2][p3][p4][p5][p6] == 0:
                                            a[p1][p2][p3][p4][p5][p6] = bflex1

    def eval(self, table, pos):
        score = 0
        pos[0] = pos[0] + 1
        pos[1] = pos[1] + 1
        if 5 <= pos[1] <= 11:  # 棋子在靠中间的位置
            ran1 = 6
        elif pos[1] < 5 or pos[1] > 11:  # 靠左右边缘的位置
            ran1 = 9 - abs(pos[1] - 8)

        if 5 <= pos[0] <= 11:  # 棋子在靠中间的位置
            ran0 = 6
        elif pos[0] < 5 or pos[0] > 11:  # 靠上下边缘的位置
            ran0 = 9 - abs(pos[0] - 8)
        pmin = min(pos[0], pos[1])
        ppmin = min(pos[0], 16-pos[1])
        pmax = max(pos[0], pos[1])
        psum = pos[0] + pos[1]
        ppsum = pos[0]+16-pos[1]
        dis = abs(16 - psum)
        ddis = abs(16 - ppsum)
        ran2 = 12 - ddis > 0 and 12 - ddis or 0
        ran3 = 12 - dis > 0 and 12 - dis or 0
        #weight = [0, 1000000, -10000000, 50000, -100000, 400, -8000, 400, -8000, 20, -50, 20, -50, 1, -3, 1, -3, 4, 4, 3, 3, 2, 2]  # 23个权重
        weight = [0, 1000000, -10000000, 50000, -100000, 400, -8000, 400, -8000, 20, -50, 20, -50,  1, -3, 1, -5, -2, 5, -2, 5, -2, 5]  # 23个权重
        num_dir = np.zeros(4 * 23).reshape(4, 23)  # 四个维度分别是横、竖、左上至右下、右上至左下，存四个维度棋型个数
        num = np.zeros(23)  # 存放17种棋型各自的数量
        virtual_table = np.zeros(17 * 17).reshape(17, 17)
        # 设置边缘
        virtual_table[0, :] = 3
        virtual_table[16, :] = 3
        virtual_table[:, 0] = 3
        virtual_table[:, 16] = 3
        # 复制横纵
        for i in range(1, 16):
            virtual_table[i][pos[1]] = table[i - 1][pos[1] - 1]
            virtual_table[pos[0]][i] = table[pos[0] - 1][i - 1]
        # 复制斜方向
        for i in range(-(pmin-1), 16-pmax):
            virtual_table[pos[0]+i][pos[1]+i] = table[pos[0]+i - 1][pos[1]+i - 1]
        if psum <= 16:#左上
            for i in range(psum-1):
                virtual_table[1+i][psum-1-i] = table[i][psum-2-i]
        else:#右下
            for i in range(31-psum):
                virtual_table[psum+i-15][15-i] = table[psum+i-16][14-i]


        start1 = pos[1] - 5 > 0 and pos[1]-5 or 0
        start0 = pos[0] - 5 > 0 and pos[0]-5 or 0

        len0 = pmin - 5 > 0 and 5 or pmin
        len1 = ppmin-5>0 and 5 or ppmin
        # 判断横向棋型
        for j in range(ran1):
            type = a[int(virtual_table[pos[0]][j+start1]), int(virtual_table[pos[0]][j +start1+1]), int(virtual_table[pos[0]][j + start1+2]), int(virtual_table[pos[0]][j + start1 +3]), int(virtual_table[pos[0]][j +start1+4]), int(virtual_table[pos[0]][j +start1+5])]
            num_dir[0][int(type)] += 1
        # 判断竖向棋型
        for i in range(ran0):
            type = a[int(virtual_table[i + start0][pos[1]]), int(virtual_table[i + start0 + 1][pos[1]]), int(virtual_table[i + start0 + 2][pos[1]]), int(virtual_table[i + start0 + 3][pos[1]]), int(virtual_table[i +start0+ 4][pos[1]]), int(virtual_table[i +start0+ 5][pos[1]])]
            num_dir[1][int(type)] += 1
        # 判断左上至右下棋型
        for i in range(min(ran0, ran1, ran2)):
            type = a[int(virtual_table[pos[0]-len0+i][pos[1]-len0+i]), int(virtual_table[pos[0]-len0 + 1+i][pos[1]-len0 + 1+i]), int(virtual_table[pos[0]-len0 + 2+i][pos[1]-len0 + 2+i]), int(virtual_table[pos[0]-len0 + 3+i][pos[1]-len0 + 3+i]), int(virtual_table[pos[0]-len0 + 4+i][pos[1]-len0 + 4+i]), int(virtual_table[pos[0]-len0 + 5+i][pos[1]-len0 + 5+i])]
            num_dir[2][int(type)] += 1
        # 判断右上至左下棋型
        for i in range(min(ran0, ran1, ran3)):
            type = a[int(virtual_table[pos[0]-len1+i][pos[1]+len1-i]), int(virtual_table[pos[0]-len1 + 1+i][pos[1]+len1-i - 1]), int(virtual_table[pos[0]-len1 + 2+i][pos[1]+len1-i - 2]), int(virtual_table[pos[0]-len1 + 3+i][pos[1]+len1-i - 3]), int(virtual_table[pos[0]-len1 + 4+i][pos[1]+len1-i - 4]), int(virtual_table[pos[0]-len1 + 5+i][pos[1]+len1-i - 5])]
            num_dir[3][int(type)] += 1

        for i in range(1, 23):
            num[i] = num_dir[0][i] + num_dir[1][i] + num_dir[2][i] + num_dir[3][i]
            score += num[i] * weight[i]
        if num[WIN] > 0:
            score = sys.maxsize / 2  # 白赢
        elif num[LOSE] > 0:
            score = -sys.maxsize / 2  # 黑赢
        return score


if __name__ == '__main__':
    b = Evaluate(a)
    table = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             ]

    for i in range(10000):
        b.eval(table,[7,11])

