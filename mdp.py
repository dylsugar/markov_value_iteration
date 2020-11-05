#!/usr/bin/python
import sys
import time
import math
"""

mdp.py: defines generic mdp problem and uses value iteration to print values in gridworld
"""

class Tile:
    def __init__(self,value,action):
        self.value = value
        self.action = action

class Grid:
    
    def __init__(self,size,walls,t_states,tr_pr,reward,discount,epsilon):
        c,r = size
        self.cols = c+1
        self.rows = r+1
        self.t_states = t_states
        self.discount = discount
        self.reward = reward
        self.walls = walls
        self.trpr = tr_pr
        self.size = size
        self.epsilon = epsilon
        self.grid = [[Tile(reward," ") for i in range(1,self.cols+1)]for j in range(1,self.rows+1)]
        self.p_grid = [[Tile(reward," ") for i in range(1,self.cols+1)]for j in range(1,self.rows+1)]
    
    def getTerminal(self):
        trewards = []
        for x in self.t_states:
            trewards.append((int(x[1]),int(x[0])))

        return trewards


    def spec_grid(self,t_states,walls):
        for x in range(1,self.rows):
            for y in range(1,self.cols):
                for z in t_states:
                    if int(z[1]) == x and int(z[0]) == y:
                        self.grid[x][y].value = z[2]#.strip("+")
                        self.p_grid[x][y].value = z[2]#.strip("+")
                for a in walls:
                    if int(a[1]) == x and int(a[0]) == y:
                        self.grid[x][y].value = "Wall"
                        self.p_grid[x][y].value = "Wall"

    def update_pgrid(self):
        for x in range(1,self.rows):
            for y in range(1,self.cols):
                self.p_grid[x][y].value = self.grid[x][y].value
    
                            
    def value_iteration(self):
        converged = False
        count = 0
        while not converged:
            delta = 0
            for x in range(1,self.rows):
                for y in range(1,self.cols):
                    neighbors = []
                    if self.p_grid[x][y] != "Wall":
                        xypair = (x,y)
                        if xypair not in self.getTerminal() and self.p_grid[x][y].value != "Wall":
                            neighbors.append((x+1,y))#up
                            neighbors.append((x,y-1))#left
                            neighbors.append((x-1,y))#right
                            neighbors.append((x,y+1))#down
                            best_value = self.value_iteration_neighbors(neighbors,self.p_grid[x][y].value)
                            self.grid[x][y].value = round(float(self.grid[x][y].value) + best_value[0] - float(self.p_grid[x][y].value),2)
                            self.grid[x][y].action = best_value[1]
                            delta = max(delta,abs(float(self.grid[x][y].value) - float(self.p_grid[x][y].value)))
            if delta <= float(self.epsilon) *(1 - float(self.discount)) / float(self.discount):
                converged = True
            self.update_pgrid()
            print("Iteration: " + str(count))
            self.print_grid()
            count+=1
        print("Final Policy")
        self.policy_print()
        return self


    def value_iteration_neighbors(self,neighbors,current):
        tmp = []
        tmpa = []
        action = ['U','L','D','R']
        cneigh = neighbors.copy()
        transition = self.trpr.copy()
        for p in range(len(neighbors)):
            currsum = 0
            i = 0
            #print("+++++++++++++")
            for n in cneigh:
                
                x = n[0]
                y = n[1]
                wallpref = float(self.trpr[0])
                if 0 < x and x < self.rows and 0 < y and y < self.cols and self.p_grid[x][y].value != "Wall" and self.p_grid[x][y].value:
                    #tmp.append(self.value_iteration_onesum(x,y,action[i],current))
                    #tmpa.append((self.value_iteration_onesum(x,y,action[i],current),action[i])) 
                    #print("Action: " + str(action[i]))
                    #print("Transition: " + str(transition[i]))
                    #print("Utility at: " + str(x) + " " + str(y) + " " + str(self.p_grid[x][y].value))
                    #print("transition * utility = " + str(float(transition[i]) * float(self.p_grid[x][y].value)))
                    
                    currsum += float(transition[i]) * float(self.p_grid[x][y].value)
                    #print("Currsum : " + str(currsum))
                    #print("\n")
                else:
                    #curr = float(current)
                    #tmp.append(wallpref * curr)
                    #tmpa.append((wallpref * curr,action[i]))
                    #print("Action: " + str(action[i]))
                    #print("Hit a wall: ")
                    #print("current x y value: " + str(current))
                    currsum += float(transition[i]) * float(current)
                    #print("Currsum + " + str(currsum))
                    #print("\n")
                i+=1
            tmp.append(currsum)
            tmpa.append((currsum,action[0]))
            af = action.pop(0)
            action.append(af)
            first = cneigh.pop(0)
            cneigh.append(first)
        opt_action = " "
        tmp2 = tuple(tmp)
        for x in tmpa:
            if max(tmp2) == x[0]:
                opt_action == x[1]
                return (float(self.reward) + (float(self.discount) * max(tmp2)),x[1])

    def value_iteration_onesum(self,x,y,action,current):
        upvalue = 0
        leftvalue = 0
        rightvalue = 0
        downvalue = 0
        if action == 'U': #Up value
            up = self.trpr[0]
            left = self.trpr[1]
            right = self.trpr[2]
            down = self.trpr[3]
        elif action == 'L':
            up = self.trpr[1]
            left = self.trpr[0]
            right = self.trpr[3]
            down = self.trpr[2]
        elif action == 'R':
            up = self.trpr[2]
            left = self.trpr[3]
            right = self.trpr[0]
            down = self.trpr[1]
        elif action == 'D':
            up = self.trpr[3]
            left = self.trpr[1]
            right = self.trpr[2]
            down = self.trpr[0]
        upvalue = float(up) * float(self.p_grid[x][y].value)
        leftvalue = float(left) * float(self.p_grid[x][y].value)
        rightvalue = float(right) * float(self.p_grid[x][y].value)
        downvalue = float(down) * float(self.p_grid[x][y].value)
             
        #if  0 < x + 1 and x + 1 < self.rows and self.p_grid[x+1][y].value != "Wall" and (x+1,y) not in self.getTerminal(): #Up value
        #    upvalue = float(up) * float(self.p_grid[x+1][y].value)
        #else:
        #    if (x+1,y) in self.getTerminal():
        #        upvalue = float(up) * float(self.p_grid[x+1][y].value)
        #    else:
        #upvalue = float(up) * float(self.p_grid[x][y].value)
        
        #if  0 < y -1 and y - 1 < self.cols and self.p_grid[x][y-1].value != "Wall" and (x,y-1) not in self.getTerminal():  #Left value
        #    leftvalue = float(left) * float(self.p_grid[x][y-1].value)
        #else:
        #    if (x,y-1) in self.getTerminal():
        #        leftvalue = float(left) * float(self.p_grid[x][y-1].value)
        #    else:
        #leftvalue = float(left) * float(self.p_grid[x][y].value)
        
        #if  0 < y + 1 and y + 1 < self.cols and self.p_grid[x][y+1].value != "Wall" and (x,y+1) not in self.getTerminal(): #Right value
        #    rightvalue = float(right) * float(self.p_grid[x][y+1].value)
        #else:
        #    if (x,y+1) in self.getTerminal():
        #        rightvalue = float(right) * float(self.p_grid[x][y+1].value)
        #    else:
        #rightvalue = float(right) * float(self.p_grid[x][y].value)
        
        #if  0 < x - 1 and x - 1 < self.rows and self.p_grid[x-1][y].value != "Wall" and (x-1,y) not in self.getTerminal(): #Down value
        #    downvalue = float(down) * float(self.p_grid[x-1][y].value)
        #else:
        #    if (x-1,y) in self.getTerminal():
        #        downvalue = float(down) * float(self.p_grid[x-1][y].value)
        #    else:
        #downvalue = float(down) * float(self.p_grid[x][y].value)
        #print("Current tile: " + str(y) + " " + str(x))
        #print("neighbor utilities: " + str(round(upvalue,3)) + " " + str(round(leftvalue,3)) + " " + str(round(rightvalue,3)) + " " + str(round(downvalue,3)))
        totalvalue = upvalue+leftvalue+rightvalue+downvalue
        #if x == 3 and y == 3:
        #    print("total value")
        #    print(totalvalue)
        return totalvalue


    def print_grid(self):
        for x in reversed(range(1,self.rows)):
            print("\n    ____________________________________________________________________\n"+str(x)+"   |",end='')
            for y in range(1,self.cols):
                print("     ",end='')
                if self.grid[x][y].value == "Wall":
                    print(str(self.grid[x][y].value), end='')
                    print("     |",end='')
                else:
                    print(str(self.grid[x][y].value), end='')
                    print("    |",end='')
        print("\n    _____________________________________________________________________")
        print("     ",end='')
        for c in range(1,self.cols):
            print("       ",end='')
            print(str(c),end='')
            print("       ",end='')
        print("\n")

    def policy_print(self):
        for x in reversed(range(1,self.rows)):
            print("\n    __________________________________________________________\n"+str(x)+"   |",end='')
            for y in range(1,self.cols):
                print("     ",end='')
                if self.grid[x][y].value == "Wall":
                    print(str(self.grid[x][y].value), end='')
                    print(" |",end='')
                elif (x,y) in self.getTerminal():
                    print("T",end='')
                    print(" |",end='')
                else:
                    print(str(self.grid[x][y].action), end='')
                    print(" |",end='')
        print("\n    ____________________________________________________________")
        print("     ",end='')
        for c in range(1,self.cols):
            print("    ",end='')
            print(str(c),end='')
            print("    ",end='')
        print("\n")



def main(argv):
    file = open(str(argv),"r")
    print(str(argv))

    size = ()
    walls = []
    t_states = []
    reward = 0
    tprobs = []
    discount = 0
    epsilon = 0.00
    for line in file:
        if line.find("size :") != -1:
            idx = line.find("size :")
            size = tuple(int(i) for i in line.split() if i.isdigit())
            print("Size :" + str(size))
        elif line.find("walls :") != -1:
            count = 0
            tmp = []
            for i in line.split():
                if i.isdigit() and count != 1:
                    tmp.append(i)
                    count = count + 1
                elif i.isdigit() and count == 1:
                    tmp.append(i)
                    tmptuple = tuple(tmp)
                    walls.append(tmptuple)
                    count = 0
                    tmp = []
            print("walls: " + str(walls))
        elif line.find("terminal_states :") != -1:
            count = 0
            tmp = []
            for i in line.split():
                if i.isdigit() and count != 2:
                    tmp.append(i)
                    count = count + 1
                elif (i.find("+") != -1 or i.find("-") != -1) and count == 2:
                    i = i.split(",")
                    i = i[0]
                    tmp.append(i)
                    tmptuple = tuple(tmp)
                    t_states.append(tmptuple)
                    count = 0
                    tmp = []
            print("Transitional States: " + str(t_states))
        elif line.find("reward :") != -1:
            idx = line.find("reward :")+8
            reward = line[idx::].strip()
            print("Reward: " + str(reward))
        elif line.find("transition_probabilities :") != -1:
            tprobs = list(i.strip() for i in line[27::].split(" "))
            tmp = tprobs[2]
            tprobs[2] = tprobs[3]
            tprobs[3] = tmp
            print("Transitional Probabilties: " + str(tprobs))
        elif line.find("discount_rate :") != -1:
            discount = line[15::].strip()
            print(discount)
        elif line.find("epsilon :") != -1:
            epsilon = line[9::].strip()
            print("Epsilon: " + str(epsilon))
    
    grid = Grid(size,walls,t_states,tprobs,reward,discount,epsilon)
    grid.spec_grid(grid.t_states,grid.walls)
    grid.value_iteration()
       

if __name__=="__main__":
        main(sys.argv[1])
