#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageOps

width=1200
height=1200

# for rotate in [0, 45, 40]:
#     for r in [5,10]:
#         for space in [2,5,10]:
#             im = Image.new('RGBA', (width*2, height*2), (255,0,0,0))
#             draw = ImageDraw.Draw(im)

#             for x in range(0, width*2, r+space):
#                 for y in range(0, height*2,r+space ):
#                     draw.ellipse( [x,y,x+r,y+r], fill=(0,0,0,255), width=0 )

#             im = im.rotate(rotate)
#             im = im.crop( (width/2, height/2, width+width/2,height+height/2) )

#             im.save("output/halftone_{}_{}_rotate_{}_radius_{}_space_{}.png".format(width,height,rotate,r, space) , quality=100)


for space in [ 15]:
    for rotate in [0, 45, 60]:
        for r in [3,5,10,14]:
            im = Image.new('RGBA', (width*2, height*2), (255,0,0,0))
            draw = ImageDraw.Draw(im)

            for x in range(0, width*2, space):
                for y in range(0, height*2,space ):
                    draw.ellipse( [x-r/2,y-r/2,x+r/2,y+r/2], fill=(0,0,0,255), width=0 )

            im = im.rotate(rotate)
            im = im.crop( (width/2, height/2, width+width/2,height+height/2) )

            im.save("output/halftone_{}_{}_rotate_{}_radius_{}_space_{}.png".format(width,height,rotate,r, space) , quality=100)
