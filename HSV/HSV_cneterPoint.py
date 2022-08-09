# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 1. Read the image
image = cv2.imread("recs_Color.png")
print(image.shape)
# Input: 3 channel image
height, width, channel = image.shape
image = cv2.resize(image, (int(1 * width), int(1 * height)), interpolation=cv2.INTER_CUBIC)
# cv2.imshow("original", image)

# 2. extract the target color from the image (in this case, yellow)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
low_hsv = np.array([28, 222, 160])
high_hsv = np.array([178, 255, 255])
mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
# cv2.imshow("find_yellow",mask)


# 3. erode
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 设置kernel卷积核为 3 * 3 正方形，8位uchar型，全1结构元素
mask = cv2.erode(mask, kernel, 3)
#cv2.imshow("morphology", mask)

# 4. count contours
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print("find", len(contours), "contours")


# 绘制轮廓函数
# 自定义绘制轮廓的函数（为简化操作）
# 输入1：winName：窗口名
# 输入2：image：原图
# 输入3：contours：轮廓
# 输入4：draw_on_blank：绘制方式，True在白底上绘制，False:在原图image上绘制
def drawMyContours(WinName, Image, Contours, draw_on_blank):
    # cv2.drawContours(image, contours, index, color, line_width)
    # 输入参数：
    # image:与原始图像大小相同的画布图像（也可以为原始图像）
    # contours：轮廓（python列表）
    # index：轮廓的索引（当设置为-1时，绘制所有轮廓）
    # color：线条颜色，
    # line_width：线条粗细
    # 返回绘制了轮廓的图像image
    if draw_on_blank:  # 在白底上绘制轮廓
        temp = np.ones(Image.shape, dtype=np.uint8) * 255
        cv2.drawContours(temp, Contours, -1, (0, 1, 0), 2)
    else:
        temp = Image.copy()
        cv2.drawContours(temp, Contours, -1, (0, 1, 255), 2)
    #cv2.imshow(WinName, temp)


# 5.绘制原始轮廓
drawMyContours("find contours", image, contours, True)


#  自定义函数：用于删除列表指定序号的轮廓
#  输入 1：contours：原始轮廓
#  输入 2：delete_list：待删除轮廓序号列表
#  返回值：contours：筛选后轮廓
def delet_contours(contours, delete_list):
    delta = 0
    contours = list(contours)
    for i in range(len(delete_list)):
        # print("i= ", i)
        del contours[delete_list[i] - delta]
        delta = delta + 1
    tuple(contours)
    return contours


# 6.筛选轮廓,计算每个轮廓长度
lengths = list()
for i in range(len(contours)):
    length = cv2.arcLength(contours[i], True)
    lengths.append(length)
    print("轮廓%d 的周长: %d" % (i, length))

# 使用轮廓长度滤波
min_size = 30
max_size = 80
delete_list = []
for i in range(len(contours)):
    if (cv2.arcLength(contours[i], True) < min_size) or (cv2.arcLength(contours[i], True) > max_size):
        delete_list.append(i)

# 根据列表序号删除不符合要求的轮廓
# 筛选后的轮廓
contours = delet_contours(contours, delete_list)
# 打印筛选后的轮廓
print("find", len(contours), "contours left after length filter")
drawMyContours("contours after length filtering", image, contours, False)

# 8.标记左上角坐标点(轮廓和点在同一张图中显示)
for i in range(len(contours)):
    rect = cv2.minAreaRect(contours[i])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    draw_rect = cv2.drawContours(image.copy(), [box], -1, (0, 0, 255), 2)

    # 获取顶点坐标
    left_point_x = np.min(box[:, 0])
    right_point_x = np.max(box[:, 0])
    top_point_y = np.min(box[:, 1])
    bottom_point_y = np.max(box[:, 1])

    left_point_y = box[:, 1][np.where(box[:, 0] == left_point_x)][0]
    right_point_y = box[:, 1][np.where(box[:, 0] == right_point_x)][0]
    top_point_x = box[:, 0][np.where(box[:, 1] == top_point_y)][0]
    bottom_point_x = box[:, 0][np.where(box[:, 1] == bottom_point_y)][0]

    # 中央坐标值
    center_point_x = (left_point_x + right_point_x) / 2
    center_point_y = (top_point_y + bottom_point_y) / 2
    center_point = np.int0([center_point_x, center_point_y])
    # 画绿点
    circle = cv2.circle(draw_rect.copy(), center_point, 2, (0, 255, 0), 2)
    text = "(" + str(center_point[0]) + ", " + str(center_point[1]) + ")"
    all = cv2.putText(circle.copy(), text, (center_point[0] + 10, center_point[1] + 10),
                      cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1, 8, 0)
    image = all
cv2.imshow("all_res", all)


cv2.waitKey()
cv2.destroyAllWindows()
