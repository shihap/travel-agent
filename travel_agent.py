#notice : you need first to install "xlrd" to run the program!!!!!!!!!!!!!!!!!!!!!!!!
#run : Print_solution(travel("Aswan","Chicago",["sat","sun","mon","tue","wed","thu","fri"]))
#made by shihap eldin

#libraries
import math
import copy
from datetime import datetime
from datetime import time
import xlrd 

#database
#constaints
FMT = '%H:%M:%S'
days = ["sat","sun","mon","tue","wed","thu","fri"]

def timevalue(x):
    x = int(x * 24 * 3600) # convert to number of seconds
    my_time = time(x//3600, (x%3600)//60, x%60) # hours, minutes, seconds
    return (my_time)

# Give the location of the file 
loc = ("database.xlsx") 

# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet1 = wb.sheet_by_index(1)
sheet2 = wb.sheet_by_index(0)

# get cities
cites = []
i1 = 1
while i1 < sheet1.nrows:
    cites.append(sheet1.row_values(i1))
    i1+=1
travels = []
i2 = 1
while i2 < sheet2.nrows:
    temp_list = []
    temp_list.append(sheet2.cell_value(i2, 0))#source
    temp_list.append(sheet2.cell_value(i2, 1))#destination
    temp_list.append(str(timevalue(sheet2.cell_value(i2, 2))))#departure
    temp_list.append(str(timevalue(sheet2.cell_value(i2, 3))))#arrival
    temp_list.append(sheet2.cell_value(i2, 4))#flight name
    temp_list.append(sheet2.cell_value(i2, 5).strip('][').split(', '))#days
    travels.append(temp_list)
    i2+=1



#the_fuctions
def travel(start,end,days):#the main fucntion , return (string)
    
    #1-chick that startnode and endnode exist
    if ( not node_exist(start) or not node_exist(end) or len(days) == 0 ):
        return "please enter valid data!!!"
    
    #2-call the recusrion function
    for d in days:
        print(test(start,end,"",d))
        
    return "--------------------------------------------------------------------------"

def test(start,end,current_time,current_day):

    start_day = current_day

    #Initialize the open list
    Open = []
    #Initialize the close list
    Closed = []
    #add the start node at this formula [[paths],f,last_node]
    temp = []
    temp.append([])
    temp.append(0)
    temp.append(start)
    temp.append(current_time)
    temp.append(current_day)
    Open.append(temp)

    #while open list in not empty
    while len(Open) > 0 :


        #print("Open=",Open)

        
        
        #a) find the node with the least f on the open list
        Open = sorted(Open, key = lambda x: x[1])
        q = Open[0]
        
        #b) pop q off the open list
        Open.pop(0)
        
        #c) push q on the closed list
        Closed.append(q)
        
        #d) if the node is the end then break (base-case successed!!!!!!)
        if q[2] == end :
            return get_paths(q[0]) +"\n\nstart day: "+start_day+"\n\n\n"
        
            
        #e) else generate q's successors and set their parents to q
        successors = get_successors(q[2],end,q[3],q[4])
        for s in successors:
            #make current node
            current_successor = copy.deepcopy(q)
            current_successor[0].append(s[:-1])
            current_successor[1] = current_successor[1] + s[6]
            current_successor[2] = s[1]
            current_successor[3] = s[3]

            #get the index
            index = days.index(current_day)
            temp1 = s[2]
            temp2 = s[3]

            if len(temp1)== 4:
                temp1= "0" + temp1

            if len(temp2)== 4:
                temp2= "0" + temp2

        
            if temp1>temp2: #increase day
                #it is the last ?!
                if index == 6:
                    index = 0
                else:
                    index = index + 1
            
            current_successor[4] = days[index]

            w = True

            #search it in open list
            for i in Open:
                if i[2] == current_successor[2] and i[1] <= current_successor[1]:
                    w = False
                    

            #search it in closed list
            for j in Closed:
                if j[2] == current_successor[2] and j[1] <= current_successor[1]:
                    w = False

            
            #add the current node at open list
            if (w):
                Open.append(current_successor)



    return "no path founded , there is no solution"#(base-case falied!!!!!!)    


def get_paths(list):
    paths = ""
    num = 1
    for l in list:
        paths+=(str(num)+"-"+str(l)+"\n")
        num+=1
    return paths    


def get_successors(start,end,current_time,current_day): #(return a list of the avilable paths)
    #1-get all the avilable paths
    list = []
    for i in travels:
        if ( i[0] == start and current_day in i[5]):
            temp = copy.deepcopy(i)
            temp.append(get_f(i,end,current_time))
            list.append(temp)

    #2-return the list
    return list

def get_f(path,end,current_time):
    g = get_g(path,current_time)
    h = get_h(path[1],end)
    return (g+h)

def get_g(path,current_time):
    #calculcate waiting time
    if(current_time == ""):
        g1 = 0
    else:
        s1 = current_time
        s2 = path[2]
        tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        g1 = tdelta.seconds
        
    #calculate fling time
    s1 = path[2]
    s2 = path[3]
    tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    g2 = tdelta.seconds
    
    #total time
    return(g1+g2)

def get_h(node1,node2):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    
    for i in cites:
        if i[0] == node1:
            x1 = i[1]
            y1 = i[2]
            
    for j in cites:
        if j[0] == node2:
            x2 = j[1]
            y2 = j[2]
    
    return (math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

def node_exist(node): #searching for the node to see if it exist or no
    for i in cites:
        if i[0] == node :
            return True
    return False

def Print_solution(str): #printing
    print(str)














