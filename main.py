from tkinter import *
from tkinter.messagebox import *
from gameAlcore import gameAlcore


class Chess(gameAlcore):

    def __init__(self):
        super().__init__()
        # param
        self.row, self.column = 15, 15  # 落点数
        self.mesh = 40  # 网格大小
        self.ratio = 0.9  # 比例
        self.board_color = "#CDBA96"  # 背景颜色
        self.header_bg = "#CDC0B0"  # 标头颜色
        self.btn_font = ("黑体", 12, "bold")  # 字体设置
        self.step = self.mesh / 2  # 步
        self.chess_r = self.step * self.ratio  # 棋子半径
        self.point_r = self.step * 0.2  # 特殊黑点半径
        # 棋盘直接继承父类棋盘
        # self.matrix = [[0 for y in range(self.column)] for x in range(self.row)]  # 棋盘存储
        # self.game_record = self.game_record
        self.is_start = False  # 开始标志
        self.is_black = True  # 黑方标志
        self.last_p = [[0, 0], [0, 0]]  # 上一步

        # GUI
        self.root = Tk()  # 指定master
        self.root.title("Gobang")  # 标题
        self.root.resizable(width=False, height=False)  # 是否能改变窗口大小

        self.f_header = Frame(self.root, highlightthickness=0, bg=self.header_bg)  # 框架控件
        self.f_header.pack(fill=BOTH, ipadx=10)  # 包装
        # 按钮控件
        self.b_start = Button(self.f_header, text="开始", command=self.bf_start, font=self.btn_font)
        self.b_restart = Button(self.f_header, text="重来", command=self.bf_restart, state=DISABLED, font=self.btn_font)
        self.b_regret = Button(self.f_header, text="悔棋", command=self.bf_regret, state=DISABLED, font=self.btn_font)
        self.b_lose = Button(self.f_header, text="认输", command=self.bf_lose, state=DISABLED, font=self.btn_font)
        # 标签控件
        self.l_info = Label(self.f_header, text="未开始", bg=self.header_bg, font=("楷体", 18, "bold"), fg="white")
        # 按钮布局
        self.b_start.pack(side=LEFT, padx=20)
        self.b_restart.pack(side=LEFT)
        self.l_info.pack(side=LEFT, expand=YES, fill=BOTH, pady=10)
        self.b_lose.pack(side=RIGHT, padx=20)
        self.b_regret.pack(side=RIGHT)
        # 画布控件
        self.c_chess = Canvas(self.root, bg=self.board_color, width=(self.column + 1) * self.mesh,
                              height=(self.row + 1) * self.mesh, highlightthickness=0)
        self.draw_board()  # 画整个棋盘
        self.c_chess.bind("<Button-1>", self.cf_board)  # 鼠标事件 1-左键
        self.c_chess.pack()

        # self.root.mainloop()  # 消息循环

    # 画x行y列处的网格
    def draw_mesh(self, x, y):
        # 一个倍率，如果不加倍率，悔棋的时候会有一点痕迹，可以试试把这个改为1，就可以看到
        ratio = (1 - self.ratio) * 0.99 + 1
        center_x, center_y = self.mesh * (x + 1), self.mesh * (y + 1)
        # 先画背景色
        self.c_chess.create_rectangle(center_y - self.step, center_x - self.step,
                                      center_y + self.step, center_x + self.step,
                                      fill=self.board_color, outline=self.board_color)
        # 再画网格线，这里面a b c d是不同的系数，根据x,y不同位置确定。
        a, b = [0, ratio] if y == 0 else [-ratio, 0] if y == self.row - 1 else [-ratio, ratio]
        c, d = [0, ratio] if x == 0 else [-ratio, 0] if x == self.column - 1 else [-ratio, ratio]
        self.c_chess.create_line(center_y + a * self.step, center_x, center_y + b * self.step, center_x)
        self.c_chess.create_line(center_y, center_x + c * self.step, center_y, center_x + d * self.step)

        # 有一些特殊的点要画小黑点
        if ((x == 3 or x == 11) and (y == 3 or y == 11)) or (x == 7 and y == 7):
            self.c_chess.create_oval(center_y - self.point_r, center_x - self.point_r,
                                     center_y + self.point_r, center_x + self.point_r, fill="black")

    # 画x行y列处的棋子，color指定棋子颜色
    def draw_chess(self, x, y, color):
        center_x, center_y = self.mesh * (x + 1), self.mesh * (y + 1)
        # 就是画个圆
        self.c_chess.create_oval(center_y - self.chess_r, center_x - self.chess_r,
                                 center_y + self.chess_r, center_x + self.chess_r,
                                 fill=color)

    # 画整个棋盘
    def draw_board(self):
        [self.draw_mesh(x, y) for y in range(self.column) for x in range(self.row)]

    # 在正中间显示文字
    def center_show(self, text):
        width, height = int(self.c_chess['width']), int(self.c_chess['height'])
        self.c_chess.create_text(int(width / 2), int(height / 2), text=text, font=("黑体", 30, "bold"), fill="red")

    # 开始的时候设置各个组件，变量的状态，初始化matrix矩阵，初始化棋盘，初始化信息
    def bf_start(self):
        self.set_btn_state("start")
        self.is_start = True
        self.is_black = True
        self.game_record = [[0 for y in range(self.column)] for x in range(self.row)]
        self.reset_buffer()
        self.draw_board()
        self.l_info.config(text="黑方下棋")

    # 重来跟开始的效果一样
    def bf_restart(self):
        self.bf_start()

    # 用last_p来标识上一步的位置。先用网格覆盖掉棋子，操作相应的变量，matrix[x][y]要置空，只能悔一次棋
    def bf_regret(self):
        if self.last_p == [[0, 0], [0, 0]]:
            showinfo("提示", "现在不能悔棋")
            return
        x, y = self.last_p[0]
        self.draw_mesh(x, y)
        self.game_record[x][y] = 0
        x, y = self.last_p[1]
        self.draw_mesh(x, y)
        self.game_record[x][y] = 0
        self.last_p = [[0, 0], [0, 0]]
        self.reset_buffer()
        # self.trans_identify()

    # 几个状态改变，还有显示文字
    def bf_lose(self):
        self.set_btn_state("init")
        self.is_start = False
        text = self.ternary_operator("黑方认输", "白方认输")
        self.l_info.config(text=text)
        

    # Canvas的click事件
    def cf_board(self, e):
        # 找到离点击点最近的坐标
        x, y = int((e.y - self.step) / self.mesh), int((e.x - self.step) / self.mesh)
        # 找到该坐标的中心点位置
        center_x, center_y = self.mesh * (x + 1), self.mesh * (y + 1)
        # 计算点击点到中心的距离
        distance = ((center_x - e.y) ** 2 + (center_y - e.x) ** 2) ** 0.5
        # 如果距离不在规定的圆内，退出//如果这个位置已经有棋子，退出//如果游戏还没开始，退出
        if distance > self.step * 0.95 or self.game_record[x][y] != 0 or not self.is_start:
            return
        # 此时棋子的颜色，和matrix中该棋子的标识。
        color = self.ternary_operator("black", "white")
        tag = self.ternary_operator(1, 2)
        # 先画棋子，在修改matrix相应点的值，用last_p记录本次操作点
        self.draw_chess(x, y, color)
        self.game_record[x][y] = tag
        self.last_p[0] = self.last_p[1]
        self.last_p[1] = [x, y]
        # 如果赢了，则游戏结束，修改状态，中心显示某方获胜
        if self.is_win(x, y, tag):
            self.is_start = False
            self.set_btn_state("init")
            text = self.ternary_operator("黑方获胜", "白方获胜")
            self.l_info.config(text=text)
            return
        # 如果游戏继续，则交换棋手
        self.trans_identify()
        self.set_btn_state("lock")      # 锁住按钮
        self.root.update()              # 刷新


        # 以下为电脑下棋
        x, y = self.find_optimal_solution([x, y])
        color = self.ternary_operator("black", "white")
        tag = self.ternary_operator(1, 2)
        # 先画棋子，在修改matrix相应点的值，用last_p记录本次操作点
        self.draw_chess(x, y, color)
        #self.game_record[x][y] = tag
        self.last_p[0] = self.last_p[1]
        self.last_p[1] = [x, y]
        self.set_btn_state("start")     # 解锁按钮
        # 如果赢了，则游戏结束，修改状态，中心显示某方获胜
        if self.is_win(x, y, tag):
            self.is_start = False
            self.set_btn_state("init")
            text = self.ternary_operator("黑方获胜", "白方获胜")
            self.l_info.config(text=text)
            return
        # 如果游戏继续，则交换棋手
        self.trans_identify()
        



    def is_win(self, x, y, tag):
        # 获取斜方向的列表
        def direction(i, j, di, dj, row, column, matrix):
            temp = []
            while 0 <= i < row and 0 <= j < column:
                i, j = i + di, j + dj
            i, j = i - di, j - dj
            while 0 <= i < row and 0 <= j < column:
                temp.append(matrix[i][j])
                i, j = i - di, j - dj
            return temp

        four_direction = []
        # 获取水平和竖直方向的列表
        four_direction.append([self.game_record[i][y] for i in range(self.row)])
        four_direction.append([self.game_record[x][j] for j in range(self.column)])
        # 获取斜方向的列表
        four_direction.append(direction(x, y, 1, 1, self.row, self.column, self.game_record))
        four_direction.append(direction(x, y, 1, -1, self.row, self.column, self.game_record))

        # 一一查看这四个方向，有没有满足五子连珠
        for v_list in four_direction:
            count = 0
            for v in v_list:
                if v == tag:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False

    # 设置四个按钮是否可以点击
    def set_btn_state(self, state):
        state_list = []
        if state == "init":
            state_list = [NORMAL, DISABLED, DISABLED, DISABLED]
        elif state == "start":
            state_list = [DISABLED, NORMAL, NORMAL, NORMAL]
        elif state == "lock":
            state_list = [DISABLED, DISABLED, DISABLED, DISABLED]
        self.b_start.config(state=state_list[0])
        self.b_restart.config(state=state_list[1])
        self.b_regret.config(state=state_list[2])
        self.b_lose.config(state=state_list[3])

    # 因为有很多和self.black相关的三元操作，所以就提取出来
    def ternary_operator(self, true, false):
        return true if self.is_black else false

    # 交换棋手
    def trans_identify(self):
        self.is_black = not self.is_black
        text = self.ternary_operator("黑方下棋", "白方下棋")
        self.l_info.config(text=text)


if __name__ == '__main__':
    a = Chess()
    a.root.mainloop()
