import socket
import numpy as np
import cv2
from ultralytics import YOLO
import time
import os

# 设置UDP服务器地址和端口
UDP_IP = "0.0.0.0"  # 使用0.0.0.0来监听所有网络接口
UDP_PORT = 10000
MAX_PACKET_SIZE = 1024

# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def receive_image(sock):
    # 接收开始信号
    while True:
        data, addr = sock.recvfrom(MAX_PACKET_SIZE)
        try:
            if data.decode('utf-8') == "ok":
                break
        except UnicodeDecodeError:
            continue

    # 接收图片大小
    data, addr = sock.recvfrom(MAX_PACKET_SIZE)
    pic_length = int(data.decode('utf-8'))

    # 初始化图像数据缓冲区
    image_data = b''
    while len(image_data) < pic_length:
        data, addr = sock.recvfrom(MAX_PACKET_SIZE)
        image_data += data

    return image_data

def main():
    # 加载 YOLOv8 模型
    model = YOLO('myapp/model/yolov8n-face.pt')

    last_saved_time = time.time()

    # 创建保存截图的文件夹
    # 获取当前文件所在目录
    project_path = os.path.dirname(os.path.abspath(__file__))

    # 在项目目录下创建保存截图的文件夹
    save_path = "media/images/YOLO_Screenshots"

    # 如果文件夹不存在，则创建它
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    print(f"Screenshots will be saved in: {save_path}")

    while True:
        try:
            # 接收图像数据
            image_data = receive_image(sock)

            # 将图像数据转换为numpy数组并解码为图像
            image_array = np.frombuffer(image_data, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            if image is not None:
                # 推理
                results = model(image)

                # 处理结果并获取绘制的结果图像
                result_image = image.copy()
                has_face = False
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        if box.cls == 0:  # 只处理人脸检测结果
                            has_face = True
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            cv2.rectangle(result_image, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # 显示结果
                cv2.imshow('ESP32-CAM', result_image)

                # 每5秒保存一次屏幕截图
                current_time = time.time()
                if has_face and (current_time - last_saved_time) >= 5:
                    screenshot_name = os.path.join(save_path, f"01.jpg")
                    cv2.imwrite(screenshot_name, result_image)
                    print(f"Screenshot saved to {screenshot_name}")
                    last_saved_time = current_time
                    break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Error: {e}")

    # 关闭窗口
    cv2.destroyAllWindows()
    sock.close()
    return '/media/images/YOLO_Screenshots/01.jpg'

if __name__ == "__main__":
    main()