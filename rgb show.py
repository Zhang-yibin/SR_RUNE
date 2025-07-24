import cv2
import sys
# 获得opencv的版本
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__':
    # 建立跟踪器，选择跟踪器的类型
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
    # 读取视频
    video = cv2.VideoCapture("/home/yuuki/Downloads/1104.mp4")
    # 打开错误时退出
    # if not video.isOpened():
    #     print("Could not open video")
    #     sys.exit()
    # # 读取视频的第一帧
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    # 定义初始边界框
    bbox = (287, 23, 86, 320)
    # Uncomment the line below to select a different bounding box
    # 选择不同的边界框
    bbox = cv2.selectROI(frame, False)
    # Initialize tracker with first frame and bounding box
    # 使用视频的第一帧和边界框初始化跟踪器
    ok = tracker.init(frame, bbox)
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        # Start timer 记录开始时间
        timer = cv2.getTickCount()
        # Update tracker 更新检测器
        ok, bbox = tracker.update(frame)
        # Calculate Frames per second (FPS) 计算FPS
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        # Draw bounding box 绘制边界框
        if ok:
            # Tracking success 跟踪成功
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:  # 跟踪失败
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        # Display tracker type on frame
        # 显示跟踪器的类别
        cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        # Display FPS on frame 显示FPS
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        # Display result 显示跟踪结果
        cv2.imshow("Tracking", frame)
        # Exit if ESC pressed 按取消键退出
        k = cv2.waitKey(1) & 0xff
        if k == 27: break

