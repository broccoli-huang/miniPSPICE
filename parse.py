# parse input.txt
import copy
import sys
from vpython import *
import numpy as np
import math
from ACcal import ACcalculator
from DCcal import DCcalculator

source_file = input("Input File: ")
f = open(source_file, "r", encoding = "utf-8")
input_str = f.read()
f.close()

input_lst = input_str.split('\n')

TYPE = ''
NODE = [] # list of node strings
SOURCE = []
R_LST = []
L_LST = []
C_LST = []
ORDER = []


# Parser
for line in input_lst:
    if line.startswith('#'):
        continue
    elif TYPE == '':
        if line.startswith('AC'):
            TYPE = 'AC'
            FREQ = float(line.split(' ')[1])
        elif line.startswith('DC'):
            TYPE = 'DC'
        else:
            print('ERROR! Please specify AC or DC.')
            sys.exit()
    elif line.startswith('V'):
        if TYPE == 'AC':
            splt = line.split(' ')[1:5]
            tup = (float(splt[0]),float(splt[1]),splt[2],splt[3])
            SOURCE.append(tup)
            if tup[2] not in NODE:
                NODE.append(tup[2])
            if tup[3] not in NODE:
                NODE.append(tup[3])
        if TYPE == 'DC':
            splt = line.split(' ')[1:4]
            tup = (float(splt[0]),splt[1],splt[2])
            SOURCE.append(tup)
            if tup[1] not in NODE:
                NODE.append(tup[1])
            if tup[2] not in NODE:
                NODE.append(tup[2])
    elif line.startswith('R'):
        splt = line.split(' ')[1:4]
        tup = (float(splt[0]),splt[1],splt[2])
        R_LST.append(tup)
        if tup[1] not in NODE:
            NODE.append(tup[1])
        if tup[2] not in NODE:
            NODE.append(tup[2])        
    elif line.startswith('L'):
        splt = line.split(' ')[1:4]
        tup = (float(splt[0]),splt[1],splt[2])
        L_LST.append(tup)
        if tup[1] not in NODE:
            NODE.append(tup[1])
        if tup[2] not in NODE:
            NODE.append(tup[2])
    elif line.startswith('C'):
        splt = line.split(' ')[1:4]
        tup = (float(splt[0]),splt[1],splt[2])
        C_LST.append(tup)
        if tup[1] not in NODE:
            NODE.append(tup[1])
        if tup[2] not in NODE:
            NODE.append(tup[2])
    elif line.startswith('&'):
        splt = line.split(' ')[1:]
        for i in splt:
            if i.startswith('//'):
                break
            else:
                ORDER.append(i)
    
if ORDER == []:
    ORDER = copy.deepcopy(NODE)
else:
    if sorted(ORDER) != sorted(NODE):
        #print(ORDER)
        #print(NODE)
        print('ERROR! Node order unmatched.')
        sys.exit()

num_of_nodes = len(ORDER)

'''
print('TYPE:')
print(TYPE)
print('NODE:')
print(NODE)
print('SOURCE:')
print(SOURCE)
print('R_LST')
print(R_LST)
print('L_LST')
print(L_LST)
print('C_LST')
print(C_LST)
print('ORDER')
print(ORDER)
'''


# Classes
order_dict = dict()
for i in range(num_of_nodes):
    order_dict[ORDER[i]] = i

class nodes:
    def __init__(self,name):
        self.name = name
        self.no = order_dict[name]
        self.desti = []

NODES = [] # list of nodes object
NODES_dict = dict()
for i in ORDER:
    N = nodes(i)
    NODES.append(N)
    NODES_dict[i] = N

UNIT = {
    'S':'V',
    'R':'Ω',
    'L':'H',
    'C':'F',
}

class component:
    def __init__(self,typ,tup,no,type_no):
        #no,typ,type_no,tup,val,(phase),display,start,end,width 
        self.no = no  #component number
        self.typ = typ  #type:S,R,L,C
        self.type_no = type_no  #component number of the type
        self.tup = tup # the tuple
        if typ == 'S' and TYPE == 'AC':
            self.val = tup[0]  #value
            self.phase = tup[1]  #phase
            val_int = int(tup[0]) if int(tup[0]) == tup[0] else tup[0]
            deg_int = int(tup[1]) if int(tup[1]) == tup[1] else tup[1]
            self.display = typ + str(type_no) + " " + str(val_int) + UNIT[typ] + " " + str(deg_int) + "°" + '\n' # words to display
            if NODES_dict[tup[2]].no<NODES_dict[tup[3]].no:
                self.start = NODES_dict[tup[2]]  #starting node
                self.end = NODES_dict[tup[3]]  #ending node
                self.width = NODES_dict[tup[3]].no-NODES_dict[tup[2]].no #width
            else:
                self.start = NODES_dict[tup[3]]
                self.end = NODES_dict[tup[2]]
                self.width = NODES_dict[tup[2]].no-NODES_dict[tup[3]].no     
        else:
            self.val = tup[0]  #value
            val_int = int(tup[0]) if int(tup[0]) == tup[0] else tup[0]
            self.display = typ + str(type_no) + " " + str(val_int) + UNIT[typ] + '\n' # words to display
            if NODES_dict[tup[1]].no<NODES_dict[tup[2]].no:
                self.start = NODES_dict[tup[1]]  #starting node
                self.end = NODES_dict[tup[2]]  #ending node
                self.width = NODES_dict[tup[2]].no-NODES_dict[tup[1]].no #width
            else:
                self.start = NODES_dict[tup[2]]
                self.end = NODES_dict[tup[1]]
                self.width = NODES_dict[tup[1]].no-NODES_dict[tup[2]].no

component_no = 0
S_no = 0
for tup in SOURCE:
    component_no += 1
    S_no += 1
    C = component('S',tup,component_no,S_no)
    C.start.desti.append(C)
R_no = 0
for tup in R_LST:
    component_no += 1
    R_no += 1
    C = component('R',tup,component_no,R_no)
    C.start.desti.append(C)
L_no = 0
for tup in L_LST:
    component_no += 1
    L_no += 1
    C = component('L',tup,component_no,L_no)
    C.start.desti.append(C)
C_no = 0
for tup in C_LST:
    component_no += 1
    C_no += 1
    C = component('C',tup,component_no,C_no)
    C.start.desti.append(C)

for N in NODES:
    N.desti.sort(key=lambda x: x.width)


#placement
remain_no = component_no

pos_x = 0
pos_y = 1
def next_pos():
    global pos_x
    global pos_y
    pos_x += 1
    if pos_x == num_of_nodes:
        pos_x = 0
        pos_y += 1

all_components = [] # list of component object

while remain_no>0:
    at_node = NODES[pos_x]
    if len(at_node.desti) == 0:
        next_pos()
        continue
    else:
        obj = at_node.desti[0]
        obj.start_pos = (pos_x,pos_y)
        obj.end_pos = (pos_x+obj.width,pos_y)
        for i in range(obj.width):
            next_pos()
        all_components.append(obj)
        at_node.desti.pop(0)
        remain_no -= 1



# AC Calculator
if TYPE == 'AC':
    vol_node2, vol_R, vol_L, vol_C = ACcalculator(NODE,SOURCE[0],R_LST,L_LST,C_LST,FREQ)
    for i in range(len(NODE)):
        node_str = NODE[i]
        node = NODES_dict[node_str]
        node.V = vol_node2[i][0]
        node.ph = vol_node2[i][1]
        node.V_str = str(round(node.V,2)) + '<' + str(round(node.ph,2)) + '°'
    for obj in all_components:
        if obj.typ == 'S':
            obj.V = obj.val
            obj.ph = obj.phase
            if order_dict[obj.start.name] < order_dict[obj.end.name]:
                obj.display += '+ ' + str(round(obj.V,2)) + '<' + str(round(obj.ph,2)) + '°' + ' -'
            else:
                obj.display += '- ' + str(round(obj.V,2)) + '<' + str(round(obj.ph,2)) + '°' + ' +'
        if obj.typ == 'R':
            obj.V = vol_R[obj.type_no-1][0]
            obj.ph = vol_R[obj.type_no-1][1]
            if obj.start.name == obj.tup[1]:
                obj.display += '+ ' + str(round(obj.V,2)) + '<' + str(round(obj.ph,2)) + '°' + ' -'
            else:
                obj.display += '- ' + str(round(obj.V,2)) + '<' + str(round(obj.ph,2)) + '°' + ' +'
        if obj.typ == 'L':
            obj.V = vol_L[obj.type_no-1][0]
            obj.ph = vol_L[obj.type_no-1][1]
            if obj.start.name == obj.tup[1]:
                obj.display += '+ ' + str(round(obj.V,2)) + '<' + str(round(obj.ph,2)) + '°' + ' -'
            else:
                obj.display += '- ' + str(round(obj.V,2)) + '<' + str(round(obj.ph,2)) + '°' + ' +'
        if obj.typ == 'C':
            obj.V = vol_C[obj.type_no-1][0]
            obj.ph = vol_C[obj.type_no-1][1]
            if obj.start.name == obj.tup[1]:
                obj.display += '+ ' + str(round(obj.V,2)) + '<' + str(round(obj.ph,2)) + '°' + ' -'
            else:
                obj.display += '- ' + str(round(obj.V,2)) + '<' + str(round(obj.ph,2)) + '°' + ' +'

        
# DC calculator
if TYPE == 'DC':
    NODE_V = DCcalculator(NODE,SOURCE,R_LST,L_LST,C_LST)
    for i in range(len(NODE)):
        node_str = NODE[i]
        node = NODES_dict[node_str]
        node.V = NODE_V[i]
        v_int = int(node.V) if int(node.V) == node.V else round(node.V,2)
        node.V_str = str(v_int) + 'V'
    for obj in all_components:
        if obj.typ == 'R':
            obj.V = abs(obj.start.V - obj.end.V)
        if obj.typ == 'L':
            obj.V = 0
        if obj.typ == 'C':
            obj.V = abs(obj.start.V - obj.end.V)
        if obj.typ == 'S':
            obj.V = abs(obj.val)
        v_int = int(obj.V) if int(obj.V) == obj.V else round(obj.V,2)
        if obj.start.V >= obj.end.V:
            obj.display += '+ ' + str(v_int) + 'V' + ' -'
        else:
            obj.display += '- ' + str(v_int) + 'V' + ' +'

    

# display

x_u = 20 # x unit
y_u = 10 # y unit
b_l = 12 #box length
b_h = 6 # box height
b_w = 0.5 # box width
h_off = 5 # horizontal offset
cy_r = 1.5 # cylinder radius
cy_w = 0.5 # cylinder width
rad_wire = 0.2 # wire radius
n_t_h = 2 # node text height
n_t_off = vec(0,-6,0) # node text offset
o_t_h = 1.3 # component text height
o_t_off = vec(0,0,b_w*0.5) # component text offset

s_w = x_u*(num_of_nodes+1) # scene width
s_h = y_u*(pos_y+2) # scene height
move = vec(x_u*1,y_u*1,0)

scene = canvas(width=800, height=800, center=vec(s_w/2,s_h/2,0), background=vec(0.74,0.98,0.79))

for node in NODES:
    node.pos = vec(x_u*node.no,0,0)+move
    node.cyl = cylinder(pos = node.pos + vec(0,0,-cy_w*0.5), axis = vec(0,0,cy_w), radius = cy_r)
    node.text = text(text = node.name + '\n' + node.V_str, pos = node.pos + n_t_off, color = color.black, align = 'center', height = n_t_h)

for obj in all_components:
    obj.pos = move+vec(x_u*((obj.start_pos[0]+obj.end_pos[0])/2) , y_u*obj.start_pos[1] , 0)
    obj.box = box(pos=obj.pos,length=b_l,height=b_h,width=b_w)
    obj.trans_l = vec(x_u*obj.start_pos[0]+h_off,y_u*obj.start_pos[1] , 0)+move
    obj.trans_r = vec(x_u*obj.end_pos[0]-h_off,y_u*obj.end_pos[1] , 0)+move
    obj.wire_l = cylinder(pos=obj.start.pos, axis=obj.trans_l-obj.start.pos, radius=rad_wire)
    obj.wire_r = cylinder(pos=obj.end.pos, axis=obj.trans_r-obj.end.pos, radius=rad_wire)
    obj.wire_m = cylinder(pos=obj.trans_l, axis=obj.trans_r-obj.trans_l, radius=rad_wire)
    obj.text = text(text = obj.display, pos = obj.pos + o_t_off, color = color.black, align = 'center', height = o_t_h)
