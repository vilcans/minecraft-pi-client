import time
import numpy as np
from math import ceil
from minecraft import Minecraft
import block

mc = Minecraft.create(address='192.168.0.17')
#mc.restoreCheckpoint()

size = 8


def get_rotation_matrix(theta):
    R = np.zeros((3, 3))
    cx,cy,cz = np.cos(theta)
    sx,sy,sz = np.sin(theta)
    R.flat = (cx*cz - sx*cy*sz, cx*sz + sx*cy*cz, sx*sy,
        -sx*cz - cx*cy*sz, -sx*sz + cx*cy*cz,
        cx*sy, sy*sz, -sy*cz, cy)
    return R 

points = np.array([
    [ 1,  1,  1],  # 0
    [ 1,  1, -1],  # 1
    [ 1, -1,  1],  # 2
    [ 1, -1, -1],  # 3
    [-1,  1,  1],  # 4
    [-1,  1, -1],  # 5
    [-1, -1,  1],  # 6
    [-1, -1, -1],  # 7
])
lines = (
    (0, 1),
    (0, 2),
    (1, 3),
    (2, 3),
    (4, 0),
    (4, 5),
    (4, 6),
    (5, 1),
    (5, 7),
    (6, 7),
    (6, 2),
    (7, 3),
)

points *= size
center = np.array(tuple(mc.player.getTilePos()))
print 'center', center
rotation = np.array((0, 0, 0), dtype=float)
rotation_delta = np.array((.2, .1, .0), dtype=float) * .01

previous_set = set()
while True:
    matrix = get_rotation_matrix(rotation)
    transformed_points = [
        np.round(np.dot(point, matrix) + center)
        for point in points
    ]
    #print transformed_points
    current_set = set()
    for from_p, to_p in lines:
        start_point = transformed_points[from_p]
        end_point = transformed_points[to_p]
        delta = end_point - start_point
        length = int(ceil(max(abs(x) for x in delta)))
        #print from_p, to_p, 'delta', delta, 'length', length
        for i in range(length + 1):
            t = float(i) / length
            p = start_point * (1 - t) + end_point * t
            p = tuple(int(x) for x in p)
            current_set.add(p)

    blocks_to_add = current_set - previous_set
    blocks_to_remove = previous_set - current_set

    print 'adding', len(blocks_to_add), 'removing', len(blocks_to_remove)
    for p in blocks_to_add:
        mc.setBlock(p[0], p[1], p[2], block.WOOD_PLANKS)
    for p in blocks_to_remove:
        mc.setBlock(p[0], p[1], p[2], block.AIR)

    time.sleep(.010)
    previous_set = current_set
    rotation += rotation_delta
