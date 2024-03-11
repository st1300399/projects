# By kelvinq (st1300399)
# Last updated at 19:00 2024/3/11
# https://minesweeper.online/

from PIL import Image, ImageGrab
import pyautogui as gui
import time as t
import win32api as win
import os

def get_position():
    print('Waiting mouse click...')
    while win.GetKeyState(0x01) >= 0:
        pass
    pos = gui.position()
    print(f'Position set {pos}')
    return pos

def range_floats(start, stop, step):
    while stop > start:
        yield start
        start += step

def scan_color(img, pos):
    color_dict = [
        (198, 198, 198),
        (0, 0, 255),
        (0, 128, 0),
        (255, 0, 0),
        (0, 0, 128),
        (128, 0, 0)
    ]
    rgb = img.getpixel(pos)
    try:
        if rgb == color_dict[0]:
            rgb2 = img.getpixel((pos[0]+width*0.45, pos[1]))
            if rgb2 == (128, 128, 128):
                return -1
        return color_dict.index(rgb)
    except ValueError as _:
        return rgb

def scan_screen(img, pos1, pos2, block):
    color_map = []
    pos_map = []
    for i in range_floats(height/2, height*block[1]-0.01, height):
        color_line = []
        pos_line = []
        for j in range_floats(width/2, width*block[0]-0.01, width):
            color = scan_color(img, (pos1[0]+j, pos1[1]+i))
            color_line.append(color)
            pos_line.append((pos1[0]+j, pos1[1]+i))
        color_map.append(color_line)
        pos_map.append(pos_line)
    return color_map, pos_map

def count_cover(bmap, pmap, i, j):
    res = []
    pos_dict = [
        [i-1]+[j-1],
        [i-1]+[j],
        [i-1]+[j+1],
        [i]+[j-1],
        [i]+[j+1],
        [i+1]+[j-1],
        [i+1]+[j],
        [i+1]+[j+1]
    ]
    if i == 0:
        [pos_dict.pop(0) for a in range(3)]
    elif i == len(pmap)-1:
        [pos_dict.pop(-1) for a in range(3)]
    if j == 0:
        [pos_dict.remove(a) for a in [[i-1]+[j-1], [i]+[j-1], [i+1]+[j-1]] if a in pos_dict]
    elif j == len(pmap[0])-1:
        [pos_dict.remove(a) for a in [[i-1]+[j+1], [i]+[j+1], [i+1]+[j+1]] if a in pos_dict]
    for s in pos_dict:
        if bmap[s[0]][s[1]] == -1:
            res.append(s)
    return res

def scan_flag(bmap, pmap):
    f = []
    for i in range(len(bmap)):
        for j in range(len(bmap[i])):
            res = count_cover(bmap, pmap, i, j)
            if len(res) != 0 and len(res) == bmap[i][j]:
                [f.append(r) for r in res]
    return f

def count_flag(bmap, pmap, i, j, flags):
    res = []
    pos_dict = [
        [i-1]+[j-1],
        [i-1]+[j],
        [i-1]+[j+1],
        [i]+[j-1],
        [i]+[j+1],
        [i+1]+[j-1],
        [i+1]+[j],
        [i+1]+[j+1]
    ]
    if i == 0:
        [pos_dict.pop(0) for a in range(3)]
    elif i == len(pmap)-1:
        [pos_dict.pop(-1) for a in range(3)]
    if j == 0:
        [pos_dict.remove(a) for a in [[i-1]+[j-1], [i]+[j-1], [i+1]+[j-1]] if a in pos_dict]
    elif j == len(pmap[0])-1:
        [pos_dict.remove(a) for a in [[i-1]+[j+1], [i]+[j+1], [i+1]+[j+1]] if a in pos_dict]
    for s in pos_dict:
        if [s[0]]+[s[1]] in flags:
            res.append(s)
    return res

def scan_block(bmap, pmap, flags):
    b = []
    for i in range(len(bmap)):
        for j in range(len(bmap[i])):
            if bmap[i][j] == 0:
                continue
            res = count_flag(bmap, pmap, i, j, flags)
            res2 = count_cover(bmap, pmap, i, j)
            if len(res) != 0 and len(res) == bmap[i][j] and len(res2) > bmap[i][j]:
                p = [k for k in res2 if k not in res]
                [b.append(pi) for pi in p if pi not in b]
    return b

def click_block(pmap, b):
    for i in b:
        x, y = pmap[i[0]][i[1]]
        gui.click(x, y)
        t.sleep(0.05)

width, height = 0, 0
flags = []
BLOCK = (int(input('Block-x:')), int(input('Block-y:')))
POS1 = get_position()
t.sleep(0.5)
POS2 = get_position()
width = (POS2[0] - POS1[0]) / BLOCK[0]
height = (POS2[1] - POS1[1]) / BLOCK[1]
while not win.GetAsyncKeyState(ord('C')):
    screen = ImageGrab.grab()
    os.system('cls')
    bmap, pmap = scan_screen(screen, POS1, POS2, BLOCK)
    [print(i) for i in bmap]
    t.sleep(0.1)
    f = scan_flag(bmap, pmap)
    [flags.append(fi) for fi in f if fi not in flags]
    b = scan_block(bmap, pmap, flags)
    print(b)
    click_block(pmap, b)
    t.sleep(0.1)
