import cv2
import numpy as np
def process_image(image, red_hsv_lower, red_hsv_upper, green_hsv_lower, green_hsv_upper):
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 边缘检测
    edges = cv2.Canny(binary, 100, 200)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 筛选轮廓
    filtered_contours = [contour for contour in contours if 10000 > cv2.contourArea(contour) > 500]

    # 找到最大的两个边缘
    largest_two_contours = sorted(filtered_contours, key=cv2.contourArea, reverse=True)[:2]

    # 创建mask1
    mask1 = np.zeros_like(gray)
    cv2.drawContours(mask1, largest_two_contours, -1, 255, thickness=cv2.FILLED)

    # 将图片转换为HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 红色mask
    mask_red = cv2.inRange(hsv, np.array(red_hsv_lower), np.array(red_hsv_upper))

    # 绿色mask
    mask_green = cv2.inRange(hsv, np.array(green_hsv_lower), np.array(green_hsv_upper))

    # 取交集
    mask1_red = cv2.bitwise_and(mask1, mask_red)
    mask1_green = cv2.bitwise_and(mask1, mask_green)

    # 找到交集对应的轮廓
    contours_red, _ = cv2.findContours(mask1_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask1_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 绘制轮廓并拟合矩形
    rectangles = []
    for contours in [contours_red, contours_green]:
        for contour in contours:
            rect = cv2.boundingRect(contour)
            x, y, w, h = rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rectangles.append(rect)

    return rectangles, image
if __name__ == '__main__':

    cap = cv2.VideoCapture(2)
    while True:
        ret, image = cap.read()
        # image_gray = bit_color_merge(image, np.array([0, 0, 186]), np.array([255, 255, 255]))'
        rectangles, image = process_image(image)
        cv2.imshow(f"img", image)
        cv2.waitKey(1)