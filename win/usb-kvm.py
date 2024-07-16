# windows下查找串口：
# reg query hklm\hardware\devicemap\serialcomm

import struct
import time
import serial
import queue
from pynput import keyboard,mouse

# Kcom3 
kt= [
        0x57,
        0xab,
        0x01, # CMD
        0x00, # data1 ## index=3  control_key
        0x00, # data2 ## must be 00
        0x00, # data3 ## key 1
        0x00, # data4 ## key 2
        0x00, # data5 ## key 3
        0x00, # data6 ## key 4
        0x00, # data7 ## key 5
        0x00, # data8 ## key 6
    ]

mt= [
        0x57,
        0xab,
        0x02, # CMD
        0x00, # data1  ## index=3 mouse_key
        0x00, # data2  ## x
        0x00, # data3  ## y
        0x00, # data4  ## scroll
    ]
    
## USB HID to PS/2 Scan Code Translation Table
## HID Usage Page -- HID Usage ID
key_code_map={
    'a':0x04,
    'A':0x04,
    'b':0x05,
    'B':0x05,
    'c':0x06,
    'C':0x06,
    'd':0x07,
    'D':0x07,
    'e':0x08,
    'E':0x08,
    'f':0x09,
    'F':0x09,
    'g':0x0a,
    'G':0x0a,
    'h':0x0b,
    'H':0x0b,
    'i':0x0c,
    'I':0x0c,
    'j':0x0d,
    'J':0x0d,
    'k':0x0e,
    'K':0x0e,
    'l':0x0f,
    'L':0x0f,
    'm':0x10,
    'M':0x10,
    'n':0x11,
    'N':0x11,
    'o':0x12,
    'O':0x12,
    'p':0x13,
    'P':0x13,
    'q':0x14,
    'Q':0x14,
    'r':0x15,
    'R':0x15,
    's':0x16,
    'S':0x16,
    't':0x17,
    'T':0x17,
    'u':0x18,
    'U':0x18,
    'v':0x19,
    'V':0x19,
    'w':0x1a,
    'W':0x1a,
    'x':0x1b,
    'X':0x1b,
    'y':0x1c,
    'Y':0x1c,
    'z':0x1d,
    'Z':0x1d,
    '1':0x1e,
    '!':0x1e,
    '2':0x1f,
    '@':0x1f,
    '3':0x20,
    '#':0x20,
    '4':0x21,
    '$':0x21,
    '5':0x22,
    '%':0x22,
    '6':0x23,
    '^':0x23,
    '7':0x24,
    '&':0x24,
    '8':0x25,
    '*':0x25,
    '9':0x26,
    '(':0x26,
    '0':0x27,
    ')':0x27,
    'Key.enter':0x28,
    'Key.esc':0x29,
    'Key.backspace':0x2a,
    'Key.tab':0x2b,
    'Key.space':0x2c,
    '-':0x2d,
    '_':0x2d,
    '=':0x2e,
    '+':0x2e,
    '[':0x2f,
    '{':0x2f,
    ']':0x30,
    '}':0x30,
    '\\':0x31,
    '|':0x31,
    'Key.europe1':0x32,
    ';':0x33,
    ':':0x33,
    '\'':0x34,
    '"':0x34,
    '`':0x35,
    '~':0x35,
    ',':0x36,
    '<':0x36,
    '.':0x37,
    '>':0x37,
    '/':0x38,
    '?':0x38,
    'Key.caps_lock':0x39,
    'Key.f1':0x3a,
    'Key.f2':0x3b,
    'Key.f3':0x3c,
    'Key.f4':0x3d,
    'Key.f5':0x3e,
    'Key.f6':0x3f,
    'Key.f7':0x40,
    'Key.f8':0x41,
    'Key.f9':0x42,
    'Key.f10':0x43,
    'Key.f11':0x44,
    'Key.f12':0x45,
    'Key.print_screen':0x46,
    'Key.scroll_lock':0x47,
    'Key.break':0x48, # ctrl-pause
    'Key.pause':0x48,
    'Key.insert':0x49,
    'Key.home':0x4a,
    'Key.page_up':0x4b,
    'Key.delete':0x4c,
    'Key.end':0x4d,
    'Key.page_down':0x4e,
    'Key.right':0x4f,
    'Key.left':0x50,
    'Key.down':0x51,
    'Key.up':0x52,
}

key_mod_map = {
    'Key.ctrl':    1<<0,
    'Key.shift':1<<1,
    'Key.alt':    1<<2,
    'Key.cmd':    1<<3,
    'Key.ctrl_r':    1<<4,
    'Key.shift_r':    1<<5,
    'Key.alt_r':    1<<6,
    'Key.cmd_r':    1<<7,
    'Key.ctrl_l':    1<<0, # windows 
    'Key.alt_l':    1<<2, # windows
}

mouse_button_map = {
    mouse.Button.left: 1<<0,
    mouse.Button.right: 1<<1,
    mouse.Button.middle: 1<<2,
}

def add_key_mod(k):
    global key_mod
    if k in key_mod_map.keys():
        v=key_mod_map[k]
        key_mod |=v

def del_key_mod(k):
    global key_mod
    if k in key_mod_map.keys():
        v=key_mod_map[k]
        key_mod &=~v

def add_keys(k):
    if k in key_code_map.keys():
        k=key_code_map[k]
        if key_pressing.count(k)==0:
            key_pressing.append(k)

def del_keys(k):
    if k in key_code_map.keys():
        k=key_code_map[k]
        while key_pressing.count(k)>0:
            key_pressing.remove(k)

def get_key_val(k):
    k=str(k) # 可能是pynput特有的问题，对于普通字符按键，返回值转字符串后带单引号。
    print(k)
    if len(k)==3 and k[0]=='\'' :
        return k[1]
    if len(k)==3 and k[0]=='\"' :
        return k[1]
    if len(k)==4 and k[1]=='\\' :
        return k[1]
    else:
        return k

def check_exit():
    global ctrl_c_times,running
    if (key_mod==1 or key_mod==16) and 6 in key_pressing: # key_mod==1 -> ctrl  6-->'c'
        ctrl_c_times+=1
        if ctrl_c_times==4:
            running=False
    else:
        ctrl_c_times=0
    # windows下ctrl-alt-del不能被捕获。这里用ctrl-alt-ins代替。
    if (key_mod==0x5 or key_mod==0x50 or key_mod==0x14 or key_mod==0x41) and 0x49 in key_pressing:
        key_pressing.remove(0x49)
        key_pressing.append(0x4c)
    #return True

def put_in_kq():
    kq.put_nowait((key_mod,key_pressing))

def on_press(key):
    k=get_key_val(key)
    add_key_mod(k)
    add_keys(k)
    put_in_kq()
    check_exit()
    return running

def on_release(key):
    k=get_key_val(key)
    del_key_mod(k)
    del_keys(k)
    put_in_kq()

def put_in_mq(x,y,s=0):
    mq.put_nowait((mouse_button,x,y,s))

def on_move(x, y): # 移动快，可低于10毫秒
    #print('Pointer moved to {0}'.format((x, y)))
    if x==mouse_pos[0] and y==mouse_pos[1]:
        return
    put_in_mq(x,y)
    mouse_pos[0]=x
    mouse_pos[1]=y
    return running

def on_click(x, y, button, pressed): # 点击较慢
    #print(button,'{0} at {1}'.format('Pressed ' if pressed else 'Released',(x, y)))
    v=mouse_button_map[button]
    global mouse_button
    if pressed:
        mouse_button |= v
    else:
        mouse_button &= ~v
    put_in_mq(x,y)

def on_scroll(x, y, dx, dy):  # dx always be 0, dy is in (-1,1) # 滚动可低于10毫秒
    #print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up  ',(x, y)))
    put_in_mq(x,y,dy)

def send_keys(km,ks): # km -- key_mod  ks-- key_pressing
    rr=kt+[]
    rr[3]=km & 0xff
    p=0
    while p<min(6,len(ks)): # only 6 keys can be send.
        rr[p+5]=ks[p]
        p+=1
    ss.write(struct.pack('11B',*rr))

def to_one_byte(v):
    if v>=0:
        if v>127:
            v=127
    else:
        if v<-127:
            v=-127
    return v

def send_mouse(bt,x,y,s):
    rr=mt+[]
    rr[3]=bt
    rr[4]=to_one_byte(x-send_mouse_pos[0])
    rr[5]=to_one_byte(y-send_mouse_pos[1])
    rr[6]=s
    send_mouse_pos[0]=x
    send_mouse_pos[1]=y
    #print(rr)
    ss.write(struct.pack('4B3b',*rr))

mouse_listener=mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)
    
mouse_listener.start()

key_listener=keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        suppress=True)

key_listener.start()

last_t=time.time()

mq=queue.Queue()
kq=queue.Queue()

key_pressing=[]
key_mod=0
mouse_button=0
send_mouse_pos=[0,0]
mouse_pos=[0,0]
ctrl_c_times=0
ss = serial.Serial('COM5', 57600)
running=True

while running:
    # 先遍历键盘队列，再遍历鼠标队列。
    # 键盘最快也需要20毫秒左右，持续按键重复输入是30毫秒，而鼠标移动经常在10毫秒以下。
    # 鼠标移动事件和滚轮事件可以丢弃，滚轮改变方向和点击时间差不多。
    # 退出：按住ctrl键后，连续按四次c。
    # 快速移动鼠标时，被控端鼠标会在移动方向上超过主控端鼠标。
    if True:
        if not kq.empty():
            v=kq.get_nowait()
            send_keys(v[0],v[1])
        else:
            if not mq.empty():
                v=mq.get_nowait()
                send_mouse(v[0],v[1],v[2],v[3])
        time.sleep(0.006)
    try:
        pass
    except :
        break
mouse_listener.stop()
print('\x0ddone') # 吃掉ctrl-c产生的^C字符。
exit(0)
