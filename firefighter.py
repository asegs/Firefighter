import random
import math
map_height = 15
map_width = 50
grid = [[" " for i in range(map_width)] for j in range(map_height)]
visible = [["?" for i in range(map_width)] for j in range(map_height)]
smoke = {}
fire = {}
objects = {}
player_row = -1
player_col = -1
player_pos = " "
def print_grid():
    global grid
    for i in range(0,map_height):
        string=""
        for j in range(0,map_width):
            string+=grid[i][j]
        print(string)


def print_visible():
    global visible
    for i in range(0,map_height):
        string=""
        for j in range(0,map_width):
            string+=visible[i][j]
        print(string)



def give_borders():
    global grid
    global visible
    for i in range(0,map_width):
        grid[0][i]="#"
        grid[map_height-1][i] = "#"
        visible[0][i]="#"
        visible[map_height-1][i] = "#"
    for i in range(1,map_height-1):
        grid[i][0] = "#"
        grid[i][map_width-1] = "#"
        visible[i][0] = "#"
        visible[i][map_width-1] = "#"
        

def get_absolute_pos(row,col):
    return row*map_width+col


def get_coords_from_abs(absolute):
    row = int(absolute/map_width)
    col = absolute-row*map_width
    return [row,col]

def pick_random_coords():
    total = map_height*map_width
    num = random.randint(0,total-1)
    return get_coords_from_abs(num)


def is_object(obj,row,col):
    try:
        if grid[row][col]==obj:
            return True
        else:
            return False
    except:
        return False

    
def if_borders(borders,row,col,diag=False):
    has_border = False
    if diag:
        has_border = is_object(borders,row-1,col-1) or is_object(borders,row+1,col-1) or is_object(borders,row-1,col+1) or is_object(borders,row+1,col+1)
    return has_border or is_object(borders,row-1,col) or is_object(borders,row,col-1) or is_object(borders,row,col+1) or is_object(borders,row+1,col)



def draw_rooms(count=10,width_max=12,height_max=12,growth_percent=0.9,door_max=2):
    global grid
    for i in range(0,count):
        doors = 0
        coords = pick_random_coords()
        if grid[coords[0]][coords[1]]=="#":
            i-=1
            continue
        else:
            grid[coords[0]][coords[1]]="#"
            xmax = 0
            for i in range(1,width_max+1):
                try:
                    if random.random()<growth_percent:
                        if doors>door_max or random.random()>0.1:
                            grid[coords[0]][coords[1]+i]="#"
                        xmax = i
                    else:
                        break
                except:
                    pass
            ymax = 0
            for i in range(1,height_max+1):
                try:
                    if random.random()<growth_percent:
                        grid[coords[0]+i][coords[1]]="#"
                        ymax = i
                    else:
                        break
                except:
                    pass
            for i in range(1,width_max+1):
                try:
                    grid[coords[0]+ymax][coords[1]+i]="#"
                except:
                    pass
            for i in range(1,height_max+1):
                try:
                    grid[coords[0]+i][coords[1]+xmax]="#"
                except:
                    pass


def make_border_arr(absolute,diag=True):
    coords = get_coords_from_abs(absolute)
    border = []
    full_borders = []
    b = [-1,0,0,-1,0,1,1,0]
    fb = [-1,-1,-1,1,1,-1,1,1]
    for i in range(0,8,2):
        try:
            if coords[0]+b[i]<0 or coords[0]+b[i]>=map_height or coords[1]+b[i+1]<0 or coords[1]+b[i+1]>=map_width:
                1/0
            grid[coords[0]+b[i]][coords[1]+b[i+1]]
            border.append([coords[0]+b[i],coords[1]+b[i+1]])
            full_borders.append([coords[0]+b[i],coords[1]+b[i+1]])
        except:
            pass
    for i in range(0,8,2):
        try:
            if coords[0]+fb[i]<0 or coords[0]+fb[i]>=map_height or coords[1]+fb[i+1]<0 or coords[1]+fb[i+1]>=map_width:
                1/0
            grid[coords[0]+fb[i]][coords[1]+fb[i+1]]
            full_borders.append([coords[0]+fb[i],coords[1]+fb[i+1]])
        except:
            pass
    if diag:
        return full_borders
    else:
        return borders
    


def spread_fire(fire_chance=0.2,smoke_chance=0.3):
    global fire
    to_add_fire = []
    to_add_smoke = []
    for absolute in fire:
        borders = make_border_arr(absolute)
        coords = get_coords_from_abs(absolute)
        for pair in borders:
            if random.random()<smoke_chance and grid[pair[0]][pair[1]]!="X" and grid[pair[0]][pair[1]]!="#":
                grid[pair[0]][pair[1]] = "O"
                smoke[get_absolute_pos(pair[0],pair[1])] ="O"
            if random.random()<fire_chance:
                grid[pair[0]][pair[1]] = "X"
                to_add_fire.append(get_absolute_pos(pair[0],pair[1]))
    for absolute in smoke:
        borders = make_border_arr(absolute)
        coords = get_coords_from_abs(absolute)
        for pair in borders:
            if random.random()<smoke_chance and grid[pair[0]][pair[1]]!="X" and grid[pair[0]][pair[1]]!="#":
                grid[pair[0]][pair[1]] = "O"
                to_add_smoke.append(get_absolute_pos(pair[0],pair[1]))
    for absolute in to_add_fire:
        fire[absolute]="X"
    for absolute in to_add_smoke:
        smoke[absolute]="O"
            
        

def create_fire(count=1,cycles=10,fire_chance=0.03,smoke_chance=0.4):
    global grid
    for i in range(0,count):
        coords = pick_random_coords()
        if grid[coords[0]][coords[1]]=="X" or grid[coords[0]][coords[1]]=="x":
            i-=1
            continue
        grid[coords[0]][coords[1]]="X"
        fire[get_absolute_pos(coords[0],coords[1])]="X"
        for i in range(0,cycles):
            spread_fire(fire_chance,smoke_chance)


def get_distance(absolute1,absolute2):
    coords1 = get_coords_from_abs(absolute1)
    coords2 = get_coords_from_abs(absolute2)
    x_dist = abs(coords1[1]-coords2[1])
    y_dist = abs(coords1[0]-coords2[0])
    return math.sqrt(x_dist**2+y_dist**2)


def get_coords_away_from_fire(dist=5):
    while True:
        coords = pick_random_coords()
        full = get_absolute_pos(coords[0],coords[1])
        safe = True
        for absolute in fire:
            if get_distance(full,absolute)<dist or not(grid[coords[0]][coords[1]]==" " or grid[coords[0]][coords[1]]=="O"):
                safe = False
        if safe:
            return coords


def populate(people=1,children=1,babies=1,animals=1,gas_tanks=3):
    global grid
    global player_row
    global player_col
    global player_pos
    for i in range(0,people):
        coords = get_coords_away_from_fire()
        if grid[coords[0]][coords[1]]!="O":
            grid[coords[0]][coords[1]] = "A"
        objects[get_absolute_pos(coords[0],coords[1])]="A"
    for i in range(0,children):
        coords = get_coords_away_from_fire()
        if grid[coords[0]][coords[1]]!="O":
            grid[coords[0]][coords[1]] = "C"
        objects[get_absolute_pos(coords[0],coords[1])]="C"
    for i in range(0,babies):
        coords = get_coords_away_from_fire()
        if grid[coords[0]][coords[1]]!="O":
            grid[coords[0]][coords[1]] = "B"
        objects[get_absolute_pos(coords[0],coords[1])]="B"
    for i in range(0,animals):
        coords = get_coords_away_from_fire()
        if grid[coords[0]][coords[1]]!="O":
            grid[coords[0]][coords[1]] = "P"
        objects[get_absolute_pos(coords[0],coords[1])]="P"
    for i in range(0,gas_tanks):
        coords = get_coords_away_from_fire()
        if grid[coords[0]][coords[1]]!="O":
            grid[coords[0]][coords[1]] = "G"
        objects[get_absolute_pos(coords[0],coords[1])]="G"
    coords = get_coords_away_from_fire()
    player_pos = grid[coords[0]][coords[1]]
    grid[coords[0]][coords[1]]="@"
    player_row = coords[0]
    player_col = coords[1]


def select_new(direction):
        global grid
        global player_row
        global player_col
        new_row = player_row
        new_col = player_col
        if direction == "a":
            new_row = player_row
            new_col = player_col-1
        if direction == "w":
            new_row = player_row-1
            new_col = player_col
        if direction == "s":
            new_row = player_row+1
            new_col = player_col
        if direction =="d":
            new_row = player_row
            new_col = player_col+1
        return [new_row,new_col]


def move_player(direction,distance=1):
    global player_row
    global player_col
    global grid
    global player_pos
    coords = select_new(direction)
    new_row = coords[0]
    new_col = coords[1]
    try:
        original_tile = player_pos
        new_pos = grid[new_row][new_col]
        if new_col<0 or new_row<0 or new_row>map_height or new_col>map_width:
            return grid
        if grid[new_row][new_col]=="#":
            return grid
        grid[player_row][player_col] = player_pos
        player_pos = grid[new_row][new_col]
        grid[new_row][new_col] = "@"
        player_row = new_row
        player_col = new_col
        return grid
    except:
        return grid


def reveal_map():
    global visible
    global grid
    ##check right
    counter = 0
    while grid[player_row][player_col+counter]!="#" and grid[player_row][player_col+counter]!="O":
        visible[player_row][player_col+counter] = grid[player_row][player_col+counter]
        counter+=1
        sub_counter = 0
        while grid[player_row+sub_counter][player_col+counter]!="#" and grid[player_row+sub_counter][player_col+counter]!="O":
            visible[player_row+sub_counter][player_col+counter] = grid[player_row+sub_counter][player_col+counter]
            sub_counter+=1
        visible[player_row+sub_counter][player_col+counter] = grid[player_row+sub_counter][player_col+counter]
        sub_counter = 0
        while grid[player_row+sub_counter][player_col+counter]!="#" and grid[player_row+sub_counter][player_col+counter]!="O":
            visible[player_row+sub_counter][player_col+counter] = grid[player_row+sub_counter][player_col+counter]
            sub_counter-=1
        visible[player_row+sub_counter][player_col+counter] = grid[player_row+sub_counter][player_col+counter]
        
    visible[player_row][player_col+counter] = grid[player_row][player_col+counter]
    ##check left
    counter = 0
    while grid[player_row][player_col+counter]!="#" and grid[player_row][player_col+counter]!="O":
        visible[player_row][player_col+counter] = grid[player_row][player_col+counter]
        counter-=1
        sub_counter = 0
        while grid[player_row+sub_counter][player_col+counter]!="#" and grid[player_row+sub_counter][player_col+counter]!="O":
            visible[player_row+sub_counter][player_col+counter] = grid[player_row+sub_counter][player_col+counter]
            sub_counter+=1
        visible[player_row+sub_counter][player_col+counter] = grid[player_row+sub_counter][player_col+counter]
        sub_counter = 0
        while grid[player_row+sub_counter][player_col+counter]!="#" and grid[player_row+sub_counter][player_col+counter]!="O":
            visible[player_row+sub_counter][player_col+counter] = grid[player_row+sub_counter][player_col+counter]
            sub_counter-=1
        visible[player_row+sub_counter][player_col+counter] = grid[player_row+sub_counter][player_col+counter]
        
    visible[player_row][player_col+counter] = grid[player_row][player_col+counter]

    ##check down
    counter = 0
    while grid[player_row+counter][player_col]!="#" and grid[player_row+counter][player_col]!="O":
        visible[player_row+counter][player_col] = grid[player_row+counter][player_col]
        counter+=1
        sub_counter = 0
        while grid[player_row+counter][player_col+sub_counter]!="#" and grid[player_row+counter][player_col+sub_counter]!="O":
            visible[player_row+counter][player_col+sub_counter] = grid[player_row+counter][player_col+sub_counter]
            sub_counter+=1
        visible[player_row+counter][player_col+sub_counter] = grid[player_row+counter][player_col+sub_counter]
        sub_counter = 0
        while grid[player_row+counter][player_col+sub_counter]!="#" and grid[player_row+counter][player_col+sub_counter]!="O":
            visible[player_row+counter][player_col+sub_counter] = grid[player_row+counter][player_col+sub_counter]
            sub_counter-=1
        visible[player_row+counter][player_col+sub_counter] = grid[player_row+counter][player_col+sub_counter]
        
    visible[player_row+counter][player_col] = grid[player_row+counter][player_col]

    ##check down
    counter = 0
    while grid[player_row+counter][player_col]!="#" and grid[player_row+counter][player_col]!="O":
        visible[player_row+counter][player_col] = grid[player_row+counter][player_col]
        counter-=1
        sub_counter = 0
        while grid[player_row+counter][player_col+sub_counter]!="#" and grid[player_row+counter][player_col+sub_counter]!="O":
            visible[player_row+counter][player_col+sub_counter] = grid[player_row+counter][player_col+sub_counter]
            sub_counter+=1
        visible[player_row+counter][player_col+sub_counter] = grid[player_row+counter][player_col+sub_counter]
        sub_counter = 0
        while grid[player_row+counter][player_col+sub_counter]!="#" and grid[player_row+counter][player_col+sub_counter]!="O":
            visible[player_row+counter][player_col+sub_counter] = grid[player_row+counter][player_col+sub_counter]
            sub_counter-=1
        visible[player_row+counter][player_col+sub_counter] = grid[player_row+counter][player_col+sub_counter]
        
    visible[player_row+counter][player_col] = grid[player_row+counter][player_col]


def smoke_vision(r=1):
    global player_row
    global player_col
    global visible
    for i in range(0,map_height):
        for j in range(0,map_width):
            dist = get_distance(get_absolute_pos(player_row,player_col),get_absolute_pos(i,j))
            if dist<=r:
                if get_absolute_pos(i,j) in objects:
                    visible[i][j] = objects[get_absolute_pos(i,j)]
                elif grid[i][j]=="O":
                    visible[i][j] = " "
                elif dist==0:
                    visible[i][j]="@"
            


def update_visible(smoke_vision=2):
    global visible
    global grid
    for row in range(0,map_height):
        for col in range(0,map_width):
            if visible[row][col]!="?" and visible[row][col]!="#":
                visible[row][col] = grid[row][col]

    

    
give_borders()
draw_rooms()
create_fire()
spread_fire()
populate()
reveal_map()
while True:
    direction = input("Direction?:")
    grid = move_player(direction)
    for i in range(0,30):
        print("")
    print(player_row)
    print(player_col)
    spread_fire(0.01,0.1)
    reveal_map()
    update_visible()
    smoke_vision()
    print_grid()
    print_visible()


"""
CLEAN UP REVEAL MAP
"""
