import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import face_recognition
import pymysql
import pickle
import torch
from PIL import Image
import cv2
import numpy as np

# 加载YOLOv5模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path='myapp/model/best.pt')

# 数据库连接信息
DB_CONFIG = {
    'host': '47.94.220.5',
    'user': 'root',
    'password': '20040826MMmm',
    'db': 'User',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 模型路径初始化
FACE_PROTO = "myapp/model/opencv_face_detector.pbtxt"
FACE_MODEL = "myapp/model/opencv_face_detector_uint8.pb"
AGE_PROTO = "myapp/model/age_deploy.prototxt"
AGE_MODEL = "myapp/model/age_net.caffemodel"
GENDER_PROTO = "myapp/model/gender_deploy.prototxt"
GENDER_MODEL = "myapp/model/gender_net.caffemodel"

# 其他初始化变量
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Male', 'Female']
MEAN_VALUES = (78.4263377603, 87.76891437444, 114.895847746)

# 加载网络模型
faceNet = cv2.dnn.readNet(FACE_MODEL, FACE_PROTO)
ageNet = cv2.dnn.readNet(AGE_MODEL, AGE_PROTO)
genderNet = cv2.dnn.readNet(GENDER_MODEL, GENDER_PROTO)


def load_known_faces_from_db():
    """从数据库加载已知人脸特征向量和名字"""
    known_face_encodings = []
    known_face_names = []

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_name, encoding FROM faces")
            rows = cursor.fetchall()
            for row in rows:
                name = row['user_name']
                encoding = pickle.loads(row['encoding'])
                known_face_names.append(name)
                known_face_encodings.append(encoding)
    finally:
        conn.close()

    return known_face_encodings, known_face_names


def process_image(img_path):
    """处理输入图像并返回处理后的图像路径"""
    # 读取并处理图像
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

    # 加载已知人脸
    known_face_encodings, known_face_names = load_known_faces_from_db()

    # 人脸检测
    results = model(img_pil)

    # 获取边界框
    bboxes = results.xyxy[0].cpu().numpy()  # 将张量移动到CPU并转换为NumPy数组
    for bbox in bboxes:
        x1, y1, x2, y2, conf, cls = bbox
        face = img_rgb[int(y1):int(y2), int(x1):int(x2)]

        # 调整人脸尺寸为160x160
        face_pil = Image.fromarray(face).resize((160, 160))

        # 使用face_recognition库生成人脸编码
        face_encoding = face_recognition.face_encodings(np.array(face_pil))

        # 性别与年龄预测
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MEAN_VALUES, swapRB=False)

        # 性别预测
        genderNet.setInput(blob)
        genderOuts = genderNet.forward()
        gender = GENDER_LIST[genderOuts[0].argmax()]

        # 年龄预测
        ageNet.setInput(blob)
        ageOuts = ageNet.forward()
        age = AGE_LIST[ageOuts[0].argmax()]

        # 绘制矩形框
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color=(0, 0, 255), thickness=2)

        name = "Unknown"
        if face_encoding:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding[0])
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding[0])
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        # 显示识别结果
        cv2.putText(img, f"{name}, {gender}, {age}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                    2)

    # 调整图像大小
    scale_percent = 50  # 将图像缩小为原始大小的50%
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # 使用cv2.resize()调整图像大小
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # 保存处理后的图像
    output_path = 'media/images/commodity/result.jpg'
    cv2.imwrite(output_path, resized_img)

    return output_path, name, gender, age
