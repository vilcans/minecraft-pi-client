
from minecraft import Minecraft
import block

mc = Minecraft.create(address='192.168.0.17')
mc.postToChat("Hello, Minecraft!")

radius = 100

def is_inside(x, y, z):
    return x * x + z * z + y * y <= radius

center_x, center_y, center_z = mc.player.getTilePos()
for y in range(-radius, radius + 1):
    for x in range(-radius, radius + 1):
        for z in range(-radius, radius + 1):
            if is_inside(x, y, z):
                if any(
                    not is_inside(x + dx, y + dy, z + dz)
                    for (dx, dy, dz) in (
                        ( 1,  0,  0), (-1,  0,  0),
                        ( 0,  1,  0), ( 0, -1,  0),
                        ( 0,  0,  1), ( 0,  0, -1)
                    )
                ):
                    print 'Setting', x, y, z
                    mc.setBlock(x + center_x, y + center_y, z + center_z, block.COBBLESTONE)
                else:
                    mc.setBlock(x + center_x, y + center_y, z + center_z, block.AIR)
