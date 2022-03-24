import numpy as np
import copy
db=set()
dbf=set()
FINAL=np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

class puzzle:
    #constructor
    def __init__(self, tile_table, cost, path, type) -> None:
        self.tile_table = tile_table
        self.type=type
        coord = np.where(tile_table == 8)
        self.x, self.y = coord[0][0], coord[1][0]
        self.cost = cost
        self.path=path
        self.n = 2  # this is hardcoded edge since we have a 8 tile puzzle
        (db if type else dbf).add(tuple(self.tile_table.flatten()))
    
    #operator overload
    def __str__(self):
        return str(self.tile_table)+("\n space loc: ")+self.get_space()+("\n cost: ")+str(self.get_cost())
    
    def __eq__(self,other):
        return (self.tile_table==other.tile_table).all()


    #getter functions
    def get_path(self):
        return self.path

    def get_space(self):
        return str(self.x)+" , "+str(self.y)

    def get_table(self):
        return self.tile_table

    def get_table_tuple(self):
        return tuple(self.tile_table.flatten())
    def get_cost(self):
        return self.cost


    #setter function
    def set_coord(self):
        coord = np.where(self.tile_table == 8)
        self.x, self.y = coord[0][0], coord[1][0]
    
    def goal(self):
        return (FINAL == self.tile_table).all()

    #moving a space
    def move(self, direction):
        a, b = self.x, self.y
        if(direction == "up"):
            a = max(0, self.x-1)
        elif(direction == "down"):
            a = min(self.n, self.x+1)
        elif(direction == "left"):
            b = max(0, self.y-1)
        elif(direction == "right"):
            b = min(self.n, self.y+1)
        self.tile_table[self.x][self.y], self.tile_table[a][b] = self.tile_table[a][b], self.tile_table[self.x][self.y]
        if tuple(self.tile_table.flatten()) in (db if self.type else dbf):
            out = None
        else:
            (db if self.type else dbf).add(tuple(self.tile_table.flatten()))
            # self.set_coord()
            # self.cost+=1
            out = puzzle(copy.copy(self.tile_table), self.cost+1,self.path+[direction],self.type)
        self.tile_table[self.x][self.y], self.tile_table[a][b] = self.tile_table[a][b], self.tile_table[self.x][self.y]
        return out

#prints path of node
def pathtrace(rootstate,foundnode):
    path=foundnode.get_path()
    n=foundnode.n
    cost=foundnode.get_cost()
    
    coord = np.where(rootstate == 8)
    x, y = coord[0][0], coord[1][0]
    print(rootstate,"\n\n")
    for direction in path:
        a, b = x, y
        if(direction == "up"):
            a = max(0, x-1)
        elif(direction == "down"):
            a = min(n, x+1)
        elif(direction == "left"):
            b = max(0, y-1)
        elif(direction == "right"):
            b = min(n, y+1)
        rootstate[x][y],rootstate[a][b]=rootstate[a][b],rootstate[x][y]
        print(rootstate,"\n\n")
        coord = np.where(rootstate == 8)
        x, y = coord[0][0], coord[1][0]
    print("path found with cost: ",cost,"\n\n")
    return

def path_directions(foundnode):
    path=foundnode.get_path() if foundnode else None #should handle infinite cases here
    return path

def bfs(root):
    q = [root]
    direction = ["left", "right", "up", "down"]
    while(q):
        curr = q.pop(0)
        if(curr.goal()):
            return curr
        for dir in direction:
            nbr = curr.move(dir)
            if(nbr):
                q.append(nbr)


def dfs(root, depth):
    res = None
    if(depth == 0 or not root):
        res = None
    elif(root.goal()):
        res = root
    else:
        direction = ["left", "right", "up", "down"]
        for dir in direction:
            temp = dfs(root.move(dir), depth-1)
            if(temp):
                res = temp
                break
    return res



def iter_deep(root):
    limit = 100  # setting this incase no solution exists
    for i in range(2, limit):
        temp = dfs(root, i)
        # clear hashtable to remove all visited track set by recently completed dfs
        db.clear()
        db.add(tuple(root.tile_table.flatten()))
        if(temp):
            return temp


def path_reverser(path):
    d={'left':"right",'up':"down",'right':"left",'down':"up"}
    path.reverse() 
    return [d[direction] for direction in path]

def bi_dir_srch(root,final):
    #inplementing bfs on both root and node
    qr = [root]
    qf = [final]
    visited = [final]
    traversed={root.get_table_tuple():root}
    direction = ["left", "right", "up", "down"]

    curr_cost=0
    while(qr and qf):
        curr_root = qr.pop(0)
        curr_final = qf.pop(0)
       
        
        #refresh layer when entering nodes of new layer
        if((curr_root and curr_root.get_cost()>curr_cost) or (curr_final and curr_final.get_cost()>curr_cost)):
            #find if layers intersect
            for vis in visited:
                vtt=vis.get_table_tuple()
                if(vtt in traversed): 
                    trav = traversed[vtt]
                    return puzzle(final.get_table(),vis.get_cost()+trav.get_cost(),trav.get_path()+path_reverser(vis.get_path()),trav.type)
            curr_cost=curr_final.get_cost()
            visited=[]
        #add neighbours of current states to queue
        for dir in direction:
            nbr_root = curr_root.move(dir)
            nbr_final = curr_final.move(dir)
            if(nbr_root):
                qr.append(nbr_root)
                traversed[nbr_root.get_table_tuple()]=nbr_root
            if(nbr_final):
                qf.append(nbr_final)
                visited.append(nbr_final)
    return None

# db.clear()
# dbf.clear()
#memory profiling
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
# tracemalloc.stop()
# print(p,"\n",q)
