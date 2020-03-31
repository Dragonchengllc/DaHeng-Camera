# _*_ coding: utf-8 _*_
import cv2
import sys
import gxipy as gx
from PIL import Image
from threading import Timer
import datetime


def Frame_acquire():
    # 参数设定
    Width_set = 640  # 设置分辨率宽
    Height_set = 480  # 设置分辨率高
    framerate_set = 80  # 设置帧率

    # 枚举设备
    device_manager = gx.DeviceManager()    # 函数返回值为设备数量
    # 枚举设备。dev_info_list 是设备信息列表，列表klp数为枚举到的设备个数，列表元素是字典，其中包含设备索引（index）、ip 信息（ip）等设备信息
    dev_num, dev_info_list = device_manager.update_device_list()
    # update_device_list使用子网枚举，只能枚举到局域网内的同一网段的千兆网相机
    print("检测到的设备数：", dev_num)

    if dev_num == 0:
        sys.exit(1)
    # 打开设备

    # 方法一
    # 获取设备基本信息列表
    # strSN = dev_info_list[0].get("sn")
    # 通过序列号打开设备
    # cam = device_manager.open_device_by_sn(strSN)

    # 方法二
    # 通过用户 ID 打开设备
    # strUserID = dev_info_list[0].get("user_id")
    # cam = device_manager.open_device_by_user_id(strUserID)

    # 方法三
    # 通过索引打开设备
    strIndex = dev_info_list[0].get("index")
    cam = device_manager.open_device_by_index(strIndex)
    # 下面为只针对千兆网相机使用的打开方式

    # 方法四
    # 通过 IP 地址打开设备
    # strIP = dev_info_list[3].get("ip")
    # cam = device_manager.open_device_by_ip(strIP)

    # 方法五
    # 通过 MAC 地址打开设备
    # strMAC = dev_info_list[0].get("mac")
    # cam = device_manager.open_device_by_mac(strMAC)

    # set exposure
    # cam.ExposureTime.set(10000)

    # 参数设定
    cam.Width.set(Width_set)
    cam.Height.set(Height_set)

    # 设置连续采集
    # cam.TriggerMode.set(gx.GxSwitchEntry.OFF) # 设置触发模式
    cam.AcquisitionFrameRateMode.set(gx.GxSwitchEntry.ON)

    # 设置帧率
    cam.AcquisitionFrameRate.set(framerate_set)

    framerate_get = cam.CurrentAcquisitionFrameRate.get()  # 获取当前采集的帧率
    print("当前采集的帧率为:%d fps" % framerate_get)

    # 开始采集
    print("")
    print("**********************************************************")
    print("开始数据采集......")
    print("")
    cam.stream_on()

    # ...........................................................................获取流通道个数
    # 如果 int_channel_num == 1，设备只有一个流通道，列表 data_stream 元素个数为 1
    # 如果 int_channel_num > 1，设备有多个流通道，列表 data_stream 元素个数大于 1
    # 目前千兆网相机、USB3.0、USB2.0 相机均不支持多流通道。
    # int_channel_num = cam.get_stream_channel_num()
    # 获取数据

    # num 为采集图片次数
    num = 6
    t = 0
    print("采集图片次数：", num)
    for i in range(num):
        # 从第 0 个流通道获取一副图像  MER-500-GM只有一个灰色gray通道
        raw_image = cam.data_stream[0].get_image()

        if raw_image is None:
            print("获取彩色原始图像失败.")
            continue

        # 从彩色原始图像获取 RGB 图像
        rgb_image = raw_image.convert("RGB")
        if rgb_image is None:
            continue

        # 从 RGB 图像数据创建 numpy 数组
        numpy_image = rgb_image.get_numpy_array()

        if numpy_image is None:
            continue

        img = Image.fromarray(numpy_image, 'RGB')
        # img.show()

        mtime = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        # 保存图片到本地
        # img.save(r"D:\PyCharm Community Edition 2019.3.3\project\Python SDK\\" + str(i) + str("-") + mtime + ".jpg")

        img.save("test_image.jpg")
        t += 1
        print("circel次数：", t)

        # 打印采集的图像的高度、宽度、帧ID、用户设置的帧率、当前采集到的帧率
        print("Frame ID: %d   Height: %d   Width: %d   framerate_set:%dfps   framerate_get:%dfps"
              % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width(), framerate_set,
                 framerate_get))
    # Function recursive
    # Timer(1, Frame_acquire).start()

    cam.stream_off()
    cam.close_device()


if __name__ == '__main__':
    # acquire image frame
    while 1:
        Frame_acquire()

    '''
    while ():
        cap = cv2.imread("D://PyCharm Community Edition 2019.3.3//project//Daheng//test_image.jpg")
        cv2.namedWindow("frame")
        cv2.imshow('frame', cap)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.destroyAllWindows()
    '''