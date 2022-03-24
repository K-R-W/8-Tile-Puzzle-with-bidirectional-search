import numpy as np
from .SAsrc.puzzle import puzzle, bi_dir_srch, path_directions, FINAL, db, dbf

class solver:
    def __init__(self, tile_table):
        self.tile_table=np.array(tile_table)
        # print(self.tile_table,self.tile_table[0],type(self.tile_table[0][0]))
    def solve(self):
        p = puzzle(self.tile_table, 0, [], 1)
        foundnode = bi_dir_srch(p,puzzle(FINAL,0,[],0))
        db.clear()
        dbf.clear()
        return path_directions(foundnode)