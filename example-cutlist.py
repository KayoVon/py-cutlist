#!/usr/bin/env python
import rectpack
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import os, os.path

# in mm
e=12
marge=2
pieces  = {
    'Bord-grand' : {'size': (360, 110),'count': 4 },
    'Bord-Petit' : {'size': (360, 100),'count': 2, },
    'Fond'       : {'count': 3, 'size': (600, 370)},
    'Glissiere'  : {'count': 4, 'size': (10, 370)},
    'Fond-Grand' : {'count': 2, 'size': (600, 120)},
    'Font-Petit' : {'count': 1, 'size': (600, 100)},
    'Front-Grand': {'count': 2, 'size': (600, 130)},
    'Front-Petit': {'count': 1, 'size': (600, 110)}
    }
bins = [(620,350),(280,340),(1350, 1220)]
#
#
#

def packwood(whatToFit,binList,kerf):
    def ex(a,b):
        a.extend(b)
        return a
    # Create rectpack compatible list, expand to a list of list
    i = map(lambda x : [ (x[1].get('size')[0]+kerf,x[1].get('size')[1]+kerf,"%s # %d\n%dx%d"%(x[0],y+1,x[1].get('size')[0],x[1].get('size')[1])) for y in range(0,x[1].get('count',1))],iter(whatToFit.items()))
    rectangles = reduce(ex,i,[])
    packer = rectpack.newPacker(rectpack.PackingMode.Offline,rectpack.PackingBin.Global)

    # Add the rectangles to packing queue
    for r in rectangles:
	       packer.add_rect(*r)
    # Add the bins where the rectangles will be placed
    for b in binList:
	       packer.add_bin(*b)
    # Start packing
    packer.pack()
    # Full rectangle list
    all_rects = packer.rect_list()

    #
    row=0
    previous = None
    for b in packer:
        row+=1
        print("Sheet ",b.width,"x", b.height, "subplot",(row,1,row))
        # Sheet %dcm x %dcm"%(b.width/10,b.height/10)
        fig1 = plot.figure()
        # several subplot  per fiegure
        #ax1 = fig1.add_subplot(plot.subplot(len(packer),1,row))
        #previous=ax1
        # on plot per fiegure
        ax1 = fig1.add_subplot(111)
        for r in b:
            ax1.add_patch(
                patches.Rectangle(
                    (r.x, r.y),   # (x,y)
                    r.width,          # width
                    r.height,          # height
                    edgecolor="red"
                )
            )
            rotation=0
            if r.height>r.width:
                rotation = 90
            ax1.annotate(r.rid,(r.x+r.width/2,r.y+r.height/2),color='w', weight='bold',
                        fontsize=6, ha='center', va='center',rotation=rotation)
            print("   Rect ",r.x,r.y,r.width,r.height,r.rid)
        ax1.set_xlim((0, b.width))
        ax1.set_ylim((0, b.height))
        ax1.set_aspect('equal')
        ax1.set_title('Sheet %dx%d '%(b.width, b.height), fontsize=8)
        #fig1.subplots_adjust(hspace=0.5)
        fig1.savefig('rect-%d.png'%(row), dpi=300, bbox_inches='tight')
    print(os.path.abspath(os.curdir))


packwood(pieces,bins,3)
