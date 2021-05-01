import cv2
import numpy as np
import os
import xmltodict
import sys
import imghdr

n = len(sys.argv)
files = ''
if n > 1:
    files = sys.argv[1]
    if os.path.exists(files):
        if not imghdr.what(files):
            print(files, 'is not image file')
            quit()
    else:
        print(files, 'doesn\'t exists')
        quit()
else:
    print('No Arguments!')
    quit()

dir_t='./.tmp'
if not os.path.isdir(dir_t):
	os.mkdir(dir_t)
img = cv2.imread(files)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
newImg = gray.copy()
layers = 8
width = int(256 / layers)

newImg = gray /width
newImg = newImg.astype('int')
newImg = newImg * width

for k in range(layers):
    gray_tmp = newImg.copy()
    mask = gray_tmp == int(k * width)
    gray_tmp[mask] = 0
    gray_tmp[~mask] = 255
    cv2.imwrite(dir_t+'/gray' + str(k) + '.bmp', gray_tmp)

for k in range(layers):
    os.system('cd '+dir_t+' && potrace -s gray' + str(k) + '.bmp && cd ..')

main = None
gs = list()
for i in range(layers):
    with open(dir_t+'/gray' + str(i) + '.svg') as fd:
        doc = xmltodict.parse(fd.read())
    if main is None:
        main = doc
    g = doc['svg']['g']
    if i != 0:
        val = '#' + str(hex(width * i).lstrip("0x").rstrip("L")) * 3
    else:
        val = '#000000'
    # print(hex(32*i).lstrip("0x"))
    g['@fill'] = val
    gs.append(g)
main['svg']['g'] = gs

with open('final.svg', 'w') as fd:
    fd.write(xmltodict.unparse(main))

if os.path.isdir(dir_t):
	os.system('rm '+dir_t+' -r')