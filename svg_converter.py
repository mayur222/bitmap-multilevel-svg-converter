import os
import sys
import imghdr
import cv2
import xmltodict

N = len(sys.argv)
FILE = ''
if N > 1:
    FILE = sys.argv[1]
    if os.path.exists(FILE):
        if not imghdr.what(FILE):
            print(FILE, 'is not image file')
            sys.exit()
    else:
        print(FILE, 'doesn\'t exists')
        sys.exit()
else:
    print('No Arguments!')
    sys.exit()

OUT_FILE = '.'.join(FILE.split('.')[:-1])+'.svg'

TMP_DIR='./.tmp'
if not os.path.isdir(TMP_DIR):
	os.mkdir(TMP_DIR)
img = cv2.imread(FILE)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
newImg = gray.copy()
LAYERS = 8
WIDTH = int(256 / LAYERS)

newImg = gray /WIDTH
newImg = newImg.astype('int')
newImg = newImg * WIDTH

for k in range(LAYERS):
    gray_tmp = newImg.copy()
    mask = gray_tmp == int(k * WIDTH)
    gray_tmp[mask] = 0
    gray_tmp[~mask] = 255
    cv2.imwrite(TMP_DIR+'/gray' + str(k) + '.bmp', gray_tmp)

for k in range(LAYERS):
    os.system('cd '+TMP_DIR+' && potrace -s gray' + str(k) + '.bmp && cd ..')

MAIN = None
gs = list()
for i in range(LAYERS):
    with open(TMP_DIR+'/gray' + str(i) + '.svg') as fd:
        doc = xmltodict.parse(fd.read())
    if MAIN is None:
        MAIN = doc
    g = doc['svg']['g']
    if i != 0:
        VAL = '#' + str(hex(WIDTH * i).lstrip("0x").rstrip("L")) * 3
    else:
        VAL = '#000000'
    # print(hex(32*i).lstrip("0x"))
    g['@fill'] = VAL
    gs.append(g)
MAIN['svg']['g'] = gs

with open(OUT_FILE, 'w') as fd:
    fd.write(xmltodict.unparse(MAIN))

if os.path.isdir(TMP_DIR):
	os.system('rm '+TMP_DIR+' -r')
