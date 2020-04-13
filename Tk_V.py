# version:1.0.1808.9101
import os
import time
from tkinter import *
import cv2
import gxipy as gx
from PIL import Image, ImageTk
from PIL import *


def main():
    # print the demo information
    print("-------------------------------------------------------------")
    print("Sample to show how to acquire mono image continuously and show acquired image.")
    print("-------------------------------------------------------------")
    print("Initializing......")
    # set continuous acquisition
    cam.TriggerMode.set(gx.GxSwitchEntry.OFF)
    # set exposure
    cam.ExposureTime.set(10000)
    # set gain
    cam.Gain.set(10.0)
    cam.stream_on()

    video_size = cv2.VideoWriter_fourcc(*'XVID')
    fps = cam.AcquisitionFrameRate.get()
    size = (cam.Width.get(), cam.Height.get())
    print("the size of video is : %d X %d " % (cam.Width.get(), cam.Height.get()))

    file_path = 'D:/PyCharm Community Edition 2019.3.3/project/Daheng/' + time.strftime("%Y%m%d_%H%M%S",
                                                                                        time.localtime()) + '.avi'
    video_save = cv2.VideoWriter(file_path, video_size, fps, size)
    if video_save.isOpened():
        raw_image = cam.data_stream[0].get_image()
        numpy_image = raw_image.get_numpy_array()

        if numpy_image is None:
            print("numpy_image is none")
            # continue

        print("numpy_image:\n", numpy_image)

        numpy_image = cv2.cvtColor(numpy_image, cv2.COLOR_GRAY2BGR)  # opencv采用的是BGR图像， 讲RGB转为BGR
        cv2image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGBA)  # 转换颜色从RGB到RGBA
        current_image = Image.fromarray(cv2image)  # 将图像转换成Image对象 。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
        imgtk = ImageTk.PhotoImage(image=current_image)

        # cv2.namedWindow('video', cv2.WINDOW_NORMAL)  # 窗口大小可调节
        # cv2.imshow('video', cv2.WINDOW_NORMAL)
        # cv2.imshow('video', numpy_image)
        # video_save.write(numpy_image)  # 将捕捉到的图像numpy_image格式进行存储
        # cv2image = cv2.cvtColor(numpy_image, cv2.COLOR_GRAY2RGBA)
        # cv2.waitKey(1)
        '''
        if cv2.waitKey(1) & 0xFF == 27:
            # break
             print("do want get out")
        '''
        # img = Image.fromarray(numpy_image, 'L')  # 将图像转换成Image对象
        # img = Image.fromarray(cv2image)  # 将图像转换成Image对象
        # print("current_image...................", img)
        # imgtk = ImageTk.PhotoImage(image=img)

        panel.imgtk = imgtk
        panel.config(image=imgtk)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        root.after(10, main)

        global sum
        sum += 1
        print("sum----------------------------------", sum)
        print("sum==================================", sum)

    # cam.stream_off()
    # cam.close_device()


if __name__ == "__main__":
    
    sum = 0
    # 清空文件目录下的avi格式文件
    path = 'D:\\PyCharm Community Edition 2019.3.3\\project\\Daheng\\'
    for root1, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".avi"):  # 指定要删除的格式，这里是avi可以换成其他格式
                os.remove(os.path.join(root1, name))
                print("Delete File: " + os.path.join(root1, name))

    # 相机参数设置
    # open device
    device_manager = gx.DeviceManager()
    # device explore
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num == 0:
        gx.sys.exit(1)

    strIndex = dev_info_list[0].get("index")
    cam = device_manager.open_device_by_index(strIndex)

    root = Tk()
    root.title("生产视屏监控")
    root.geometry("800x700")

    panel = Label(root)  # initialize image panel  label用到的图像必须是经过cv2转换后生成的图像
    panel.pack(padx=100, pady=100)
    root.config(cursor="arrow")

    Button(root, text='关键帧定标').place(x=350, y=600)  # 关键帧切换函数

    print("-------------------------------------------------------------")
    print("loading......................................................")
    print("-------------------------------------------------------------")

    main()
    root.mainloop()
