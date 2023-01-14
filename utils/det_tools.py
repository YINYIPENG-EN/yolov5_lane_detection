import cv2
import numpy as np


def canny_edg_(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 转为灰度图像
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0) # 高斯滤波
    low_thres = 160
    high_thres = 240
    edg_img = cv2.Canny(blur_gray, low_thres, high_thres)
    return edg_img


def color_select(img, red_thres=120, green_thres=160, blue_thres=120):
    # h, w = img.shape[:2]
    color_select = np.copy(img)
    bgr_thre = [blue_thres, green_thres, red_thres]
    thresholds = (img[:, :, 0] < bgr_thre[0]) | (img[:, :, 1] < bgr_thre[1]) | (img[:, :, 2] < bgr_thre[2])
    color_select[thresholds] = [0, 0, 0]  # 小于阈值的像素设置为0
    return color_select


def get_mask(edg_img, mask_scale=0.6):
    # ----------------检测区域的选择---------------------
    mask = np.zeros_like(edg_img)  # 全黑的图像
    ignore_mask_color = 255
    # get image size
    imgshape = edg_img.shape
    # 设置mask shape [1,4,2] 一般车道位置大概占据画面的1/3的位置
    ret = np.array([[(1, imgshape[0]), (1, int(imgshape[0] * mask_scale)), (imgshape[1] - 1, int(imgshape[0] * mask_scale)),
                     (imgshape[1] - 1, imgshape[0] - 1)]], dtype=np.int32)
    # 多边形填充，mask是需要填充的图像，ret是多边形顶点, 将需要保留的区域填充为白色矩形
    cv2.fillPoly(mask, ret, ignore_mask_color)  # mask下面部分变成白色
    # 图像与运算，保留掩膜图像
    mask_img = cv2.bitwise_and(edg_img, mask)
    # ------------------------------------------------
    return mask_img


def Hough_transform(edg_img, img, mask_scale=0.6):
    # img是原始图像

    mask_img = get_mask(edg_img, mask_scale)  # 掩膜图像
    # -----------------霍夫曼变换-----------------------
    # 定义Hough 变换的参数
    rho = 1
    theta = np.pi/180
    threshold = 2
    min_line_length = 4  # 组成一条线的最小像素
    max_line_length = 5  # 可连接线段之间的最大像素距离

    lines = cv2.HoughLinesP(mask_img, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_length)

    left_line = []
    right_line = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:
                pass
            else:
                # 求直线方程斜率判断左右车道
                m = (y2 - y1) / (x2 - x1)
                c = y1 - m * x1
                if m < 0:  # 左车道
                    left_line.append((m, c))
                elif m >= 0:  # 右车道
                    right_line.append((m, c))
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 5)
    return img




# img = cv2.imread('../img/demo.png')
# imgshape = img.shape  # h,w
# print(imgshape)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # 多边形绘制的顺序是顺时针坐标
# rec = np.array([ [(0, imgshape[0]), (0, imgshape[0]//2), (imgshape[1], imgshape[0] // 2), (imgshape[1], imgshape[0])] ])
# cv2.fillPoly(img, rec, 255)
# cv2.imshow('img', img)
# cv2.waitKey(0)