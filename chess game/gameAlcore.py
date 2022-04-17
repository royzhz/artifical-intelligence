from Evaluate import *
import sys
import copy

ai_robot=2
ai_player=1
no_chess=0

class gameAlcore:
    def __init__(self):
        self.chessboard_size = 15    #设定棋盘大小
        self.search_depth=2          #设定搜索深度
        self.check_width=2         #设定搜索范围
        self.game_record=[[0 for i in range(self.chessboard_size)] for i in range(self.chessboard_size)]   #建立棋盘,1为我方，2为敌方，0为空
        self.possible_location=[]   #更加已知棋子位置记录所有可能位置
        self.Evalclass = Evaluate(a)    #建立评估类
        self.node_num=1
        self.dp_value=0

    def max_min_tree(self):#进行极大极小树搜索,返回最优解
        return self.deep_seach([],[],0,sys.maxsize,self.search_depth)


    def deep_seach(self,confirmed_loction,temp_possible_location,dp_value,past_value,depth):#递归搜索函数，配合ab枝剪,confirmed_loction为搜索中临时确定的落子位置，possible_location为增加的可能落子位置
        #comfirmed_loction为三元组,dp_value为上层落子的评分
        def simple_return():#需要多次使用，定义一个函数来执行还原
            self.game_record[i[0]][i[1]] = no_chess  # 还原
            confirmed_loction.pop()
            temp_possible_location.pop()


        term=depth%2+1#depth%2==0时，为我方落子，记录1，反之记录2,同时记录1 时，为极大值
        result=0
        if term ==1:
            value=-sys.maxsize - 1#求最大值
        else:
            value=sys.maxsize#最小值

        search_range = []
        for i in temp_possible_location:
            search_range.extend(i)#获得本轮所有子树，为已经下下来的棋子和分支棋子周围所有可能位置

        for i in self.possible_location+search_range:#对可能的位置
            self.node_num += 1#计算节点数
            if(i not in confirmed_loction and i != [] and self.game_record[i[0]][i[1]]==no_chess):#检查这一节点有没有没有棋子已经在了
                temp_possible_location.append(self.insert_possible_location(i,confirmed_loction,temp_possible_location))#记录新节点的新加入的可能值
                confirmed_loction.append(i)#记录临时落子位置
                if term==1:
                    self.game_record[i[0]][i[1]]=ai_robot#落子记录
                else:
                    self.game_record[i[0]][i[1]]=ai_player
                new_chess=[i[0],i[1]]
                value_of_total_point=dp_value+self.Evalclass.eval(self.game_record,new_chess)#计算分支树到目前的所有得分

                #print(term)
                #for te in a.game_record:
                #    print(te)
                #print("next")

                #ab枝剪算法开始
                if(term==1):#极大层
                    if depth==1:#结束递归
                        value=max(value, value_of_total_point)#利用评价函数计算评价值
                    else:
                        t=self.deep_seach(confirmed_loction, temp_possible_location,value_of_total_point, value, depth - 1)#计算节点值
                        #print(t)
                        if(t>=value):
                            value=t
                            if(depth==self.search_depth):#最外层递归
                                result=i#记录下这个值，作为结果

                    if(value>past_value):#枝剪
                        simple_return()
                        return value
                else:#极小层
                    if(depth==1):
                        value=min(value, value_of_total_point)
                    else:
                        value=min(value,self.deep_seach(confirmed_loction, temp_possible_location,value_of_total_point, value, depth - 1))

                    if(value<past_value):#枝剪
                        simple_return()
                        return value
                #接下来还原之前的操作
                simple_return()
            else:
                continue
        if(depth==self.search_depth):
            return result
        else:
            return value

    def insert_possible_location(self,location,confirmed_loction,temp_possible_location):
        result=[]
        for i in range(location[0]-self.check_width,location[0]+self.check_width+1):
            for j in range(location[1] - self.check_width, location[1] + self.check_width+1):#在落子周围搜索
                if(i<0 or i>self.chessboard_size-1 or j<0 or j>self.chessboard_size -1 or [i,j] in self.possible_location):#检查范围
                    continue
                if(self.game_record[i][j]==no_chess):#检查已经确定的棋盘
                    ready_to_add=True
                    for t in range(len(confirmed_loction)):#检查未确定的棋子和位置
                        if (confirmed_loction[t][0]==i and confirmed_loction[t][1]==j) or ([i,j] in temp_possible_location[t]):
                            ready_to_add=False
                    if(ready_to_add and [i,j]!=location):
                        result.append([i,j])
        return result


    def find_optimal_solution(self,new_chess_location):#new_chess_location为更新点（列表储存用户下的点，格式为[x,y]，x为横轴)，返回AI下的点，格式为[x,y]
        self.game_record[new_chess_location[0]][new_chess_location[1]]=ai_player
        if(new_chess_location in self.possible_location):
            self.possible_location.remove(new_chess_location)#删除已经下的值

        self.possible_location.extend(self.insert_possible_location(new_chess_location,[],[]))

        result=self.max_min_tree()
        #print(result)
        self.game_record[result[0]][result[1]]=ai_robot
        self.possible_location.extend(self.insert_possible_location(result, [], []))
        self.possible_location.remove(result)  # 删除已经落下的子
        #print(self.node_num)
        return result

    def reset_buffer(self):
        self.possible_location=[]#清空缓冲区
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if(self.game_record[i][j]!=no_chess):#检查棋局
                    self.possible_location.extend(self.insert_possible_location([i,j], [], []))

        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if(self.game_record[i][j]!=no_chess and [i,j] in self.possible_location):#检查棋局
                    self.possible_location.remove([i,j])


'''if __name__ == '__main__':
    print(1)
    a = gameAlcore()
    print(a.find_optimal_solution([7,7]))
    print(a.find_optimal_solution([6,8]))
    print(a.find_optimal_solution([7,9]))
    print(a.find_optimal_solution([8,10]))
    for i in a.game_record:
        print(i)
    #a.game_record[7][7]=ai_robot
    #a.game_record[7][6]=ai_robot
    #a.game_record[7][5]=ai_robot

    for i in a.game_record:
        print(i)
    while(1):
        slist = input("输入：").split()
        slist = [int(slist[i]) for i in range(len(slist))]

        j=a.find_optimal_solution(slist)
        for i in a.game_record:
            print(i)

        print(a.node_num)'''