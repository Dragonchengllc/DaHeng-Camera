# DaHeng-Camera
# DaHeng Camera Application Development

import cv2
import gxipy as gx
import time

device_manager = gx.DeviceManager()
dev_num, dev_info_list = device_manager.update_device_list()
if dev_num == 0:
    sys.exit(1)

strIndex = dev_info_list[0].get("index")
cam = device_manager.open_device_by_index(strIndex)

cam.stream_on()

video_size = cv2.VideoWriter_fourcc(*'XVID')
fps = cam.AcquisitionFrameRate.get()

size = (cam.Width.get(), cam.Height.get())
print("the size of video is : %d X %d " % (cam.Width.get(), cam.Height.get()))

file_path = 'D:/PyCharm Community Edition 2019.3.3/project/Daheng'+time.strftime("%Y%m%d_%H%M%S", time.localtime())+'.avi'
video_save = cv2.VideoWriter(file_path, video_size, fps, size)

while video_save.isOpened():
    raw_image = cam.data_stream[0].get_image()  # 使用相机采集一张图片
    rgb_image = raw_image.convert("RGB")  # 从彩色原始图像获取 RGB 图像
    numpy_image = rgb_image.get_numpy_array()  # 从 RGB 图像数据创建 numpy 数组
    if rgb_image is None:
        continue
    numpy_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)  # opencv采用的是BGR图像， 讲RGB转为BGR
    cv2.namedWindow('video',cv2.WINDOW_NORMAL)
    cv2.imshow('video',cv2.WINDOW_NORMAL)
    video_save.write(numpy_image)  # 将捕捉到的图像存储

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.stream_off()
cam.close_device()



