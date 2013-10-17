
from minecraft import Minecraft
import block
import time

mc = Minecraft.create(address='192.168.0.17')
mc.saveCheckpoint()

types = {
    ' ': block.AIR,
    'x': block.STONE
}
pattern = """
x     x  x     x  
xx   xx   x   x
x x x x    x x
x  x  x     x
""".split('\n')


def get_type(row, col):
    c = (col + offset) % width
    if 0 <= row < len(pattern):
        if 0 <= c < len(pattern[row]):
            return types[pattern[row][c]]
    return block.AIR

width = max(len(x) for x in pattern)
height = len(pattern)

center_x, center_y, center_z = mc.player.getTilePos()

offset = 0
while True:
    print offset
    for row in range(height):
        for col in range(width):
            x = col - height // 2
            y = width // 2 - row
            z = 2
            t = get_type(row, col)
            mc.setBlock(x + center_x, y + center_y, z + center_z, t)
    time.sleep(.2)
    offset = (offset - 1) % width
