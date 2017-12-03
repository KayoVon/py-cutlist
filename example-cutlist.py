#!/usr/bin/env python
from rectpack import newPacker
import matplotlib.pyplot as plot
import matplotlib.patches as patches

# mm
kerf = 3
# in cm

pieces = [(60,37,3,"fond"),(60,13,2,"Front-1"),
          (60,11,1,"Front-2"),(60,12,2,"Back-1"),
          (60,10,1,"Back-2"),(36,11,4,"side-1"),(36,10,2,"side-2"),(1,37,4,"Glissiere")]
def ex(a,b):
    a.extend(b)
    return a
i = map(lambda x : [ (x[0]*10+kerf,x[1]*10+kerf,x[3]) for y in range(0,x[2])],pieces)
rectangles = reduce(ex,i,[])

bins = [(620,350),(280,340),(1350, 1220)]
bins = [(620,350),(280,340)]

#bins = [(1350, 1220), (620,340),(280,350)]

packer = newPacker()

# Add the rectangles to packing queue
for r in rectangles:
	packer.add_rect(*r)

# Add the bins where the rectangles will be placed
for b in bins:
	packer.add_bin(*b)

# Start packing
packer.pack()


# Full rectangle list
all_rects = packer.rect_list()
fig1 = plot.figure()

import os, os.path
#
for b in packer:
    print("Bin",b.width,"x", b.height)
    # Sheet %dcm x %dcm"%(b.width/10,b.height/10)
    ax1 = fig1.add_subplot("111", aspect='equal')
    for r in b:
        ax1.add_patch(
            patches.Rectangle(
                (r.x, r.y),   # (x,y)
                r.width,          # width
                r.height,          # height
                edgecolor="red"
            )
        )
        ax1.annotate(r.rid,(r.x+r.width/2,r.y+r.height/2),color='w', weight='bold',
                    fontsize=6, ha='center', va='center')
        print("   Rect ",r.x,r.y,r.width,r.height,r.rid)
    ax1.set_xlim((0, b.width))
    ax1.set_ylim((0, b.height))
    ax1.set_aspect('equal')
fig1.savefig('rect1.png', dpi=90, bbox_inches='tight')
print(os.path.abspath(os.curdir))

# b - Bin index
# x - Rectangle bottom-left corner x coordinate
# y - Rectangle bottom-left corner y coordinate
# w - Rectangle width
# h - Rectangle height
# rid - User asigned rectangle id or None
