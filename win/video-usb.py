import cv2
import time
import subprocess
import os
start_time=time.time()
zz=subprocess.Popen(['python', 'usb-kvm.py'])
print('pid',zz.pid)
print('1',time.time()-start_time)
c=cv2.VideoCapture(0,cv2.CAP_DSHOW)
print(c.isOpened())
# c=cv2.VideoCapture(0) # CAP_MSMF 打开需要17秒多。
#c.set(cv2.CAP_PROP_FPS,30) # 设置帧率，在windows上将导致更慢的速度。
#c.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
print('2',time.time()-start_time)
c.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
c.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
print('3',time.time()-start_time)

cv2.namedWindow('video',cv2.WINDOW_KEEPRATIO)
print('4',time.time()-start_time)

cv2.resizeWindow('video',1280,800)

#cv2.resizeWindow('video',1920,1080)
#cv2.setWindowProperty('video',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def no_mouse(e,x,y,f,v):
    return False

cv2.setMouseCallback('video',no_mouse)
## cv2显示图像，全屏时会对鼠标右键和滚轮产生响应。
while True:
    r,f=c.read()
    cv2.imshow("video",f)
    k=cv2.waitKey(10)
    #if k==ord('q'):
    #    break
    #print(time.time())
    xxx=cv2.getWindowProperty('video',cv2.WND_PROP_VISIBLE)
    if xxx<1:
        # cmd='taskkill /t /f /pid {}'.format(zz.pid)
        # print(cmd)
        # os.system(cmd)
        print('usb-kvm.py still running. Holding ctrl while press "c" 4 times to exit.')
        break
    if not zz.poll() is None:
        print(xxx)
        break

cv2.destroyAllWindows()

