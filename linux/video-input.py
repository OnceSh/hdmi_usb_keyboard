import cv2
import time
import subprocess

zz=subprocess.Popen('python3 /home/user/usb-kvm.py',shell=True)

c=cv2.VideoCapture(0)
c.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
c.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
c.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

#c.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
#c.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)

cv2.namedWindow('video',cv2.WINDOW_KEEPRATIO)

cv2.resizeWindow('video',1920,1080)
#cv2.resizeWindow('video',1440,900)
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
    if xxx<1 or not zz.poll() is None:
        print(xxx)
        break

cv2.destroyAllWindows()

