
import requests
import json
import datetime
import random
import torch
import cv2
import numpy as np
import math
import argparse
"""
    该类是父类，通过继承该类，可以实现输入对应的choice(相应选择)与tips(提示信息)，来随机从相应tips中选择一条信息
    继承要完成的工作：
        1. __init__()调用generateChoice()、generateTips()
        2. 实现generateChoice、generateTips()
        3. 如果出现了提示信息，可以通过修改继承类的generateReminder()的逻辑实现跳转，比如出现天气提示信息在桌宠旁边后，
        可以通过点击那个提示信息，去查看最近的天气。或者日程表中某个代办事件的deadline快到了出现提示，可以点击提示信息进行跳转
    比如： 
        choice = 雨天
        # tips有2类，分别是雨天和雪天两类提示信息
        tips = [
            # 雨天相应的提示信息共3条
            [今天有雨，记得带伞哦！", "今天有雨，记得添衣！","在下雨喵，记得带伞喵"]
            # 雪天相应的提示信息,共两条
            ["今天有雪，记得带伞哦！", "今天有雪，记得添衣！"]
        ]
        输出是从[今天有雨，记得带伞哦！", "今天有雨，记得添衣！","在下雨喵，记得带伞喵"]这3条数据中随机选择一条进行输出
"""


import torch.nn as nn


# 参数初始化
def gaussian_weights_init(m):
    classname = m.__class__.__name__
    # 字符串查找find，找不到返回-1，不等-1即字符串中含有该字符
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.04)


class FaceCNN(nn.Module):
    # 初始化网络结构
    def __init__(self):
        super(FaceCNN, self).__init__()

        # layer1(conv + relu + pool)
        # input:(bitch_size, 1, 48, 48), output(bitch_size, 64, 24, 24)
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 64, 3, 1, 1),
            nn.BatchNorm2d(num_features=64),
            nn.RReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # layer2(conv + relu + pool)
        # input:(bitch_size, 64, 24, 24), output(bitch_size, 128, 12, 12)
        self.conv2 = nn.Sequential(
            nn.Conv2d(64, 128, 3, 1, 1),
            nn.BatchNorm2d(num_features=128),
            nn.RReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # layer3(conv + relu + pool)
        # input: (bitch_size, 128, 12, 12), output: (bitch_size, 256, 6, 6)
        self.conv3 = nn.Sequential(
            nn.Conv2d(128, 256, 3, 1, 1),
            nn.BatchNorm2d(num_features=256),
            nn.RReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        # 参数初始化
        self.conv1.apply(gaussian_weights_init)
        self.conv2.apply(gaussian_weights_init)
        self.conv3.apply(gaussian_weights_init)

        # 全连接层
        self.fc = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(256*6*6, 4096),
            nn.RReLU(inplace=True),

            nn.Dropout(p=0.5),
            nn.Linear(4096, 1024),
            nn.RReLU(inplace=True),

            nn.Linear(1024, 256),
            nn.RReLU(inplace=True),
            nn.Linear(256, 7)
        )

    # 向前传播
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(x.shape[0], -1)  # 数据扁平化
        y = self.fc(x)

        return y


class YOLOv8_face:
    def __init__(self, path, conf_thres=0.2, iou_thres=0.5):
        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres
        self.class_names = ['face']
        self.num_classes = len(self.class_names)
        # Initialize model
        self.net = cv2.dnn.readNet(path)
        self.input_height = 640
        self.input_width = 640
        self.reg_max = 16

        self.project = np.arange(self.reg_max)
        self.strides = (8, 16, 32)
        self.feats_hw = [(math.ceil(self.input_height / self.strides[i]), math.ceil(self.input_width / self.strides[i]))
                         for i in range(len(self.strides))]
        self.anchors = self.make_anchors(self.feats_hw)

    def make_anchors(self, feats_hw, grid_cell_offset=0.5):
        """Generate anchors from features."""
        anchor_points = {}
        for i, stride in enumerate(self.strides):
            h, w = feats_hw[i]
            x = np.arange(0, w) + grid_cell_offset  # shift x
            y = np.arange(0, h) + grid_cell_offset  # shift y
            sx, sy = np.meshgrid(x, y)
            # sy, sx = np.meshgrid(y, x)
            anchor_points[stride] = np.stack((sx, sy), axis=-1).reshape(-1, 2)
        return anchor_points

    def softmax(self, x, axis=1):
        x_exp = np.exp(x)
        # 如果是列向量，则axis=0
        x_sum = np.sum(x_exp, axis=axis, keepdims=True)
        s = x_exp / x_sum
        return s

    def resize_image(self, srcimg, keep_ratio=True):
        top, left, newh, neww = 0, 0, self.input_width, self.input_height
        if keep_ratio and srcimg.shape[0] != srcimg.shape[1]:
            hw_scale = srcimg.shape[0] / srcimg.shape[1]
            if hw_scale > 1:
                newh, neww = self.input_height, int(self.input_width / hw_scale)
                img = cv2.resize(srcimg, (neww, newh), interpolation=cv2.INTER_AREA)
                left = int((self.input_width - neww) * 0.5)
                img = cv2.copyMakeBorder(img, 0, 0, left, self.input_width - neww - left, cv2.BORDER_CONSTANT,
                                         value=(0, 0, 0))  # add border
            else:
                newh, neww = int(self.input_height * hw_scale), self.input_width
                img = cv2.resize(srcimg, (neww, newh), interpolation=cv2.INTER_AREA)
                top = int((self.input_height - newh) * 0.5)
                img = cv2.copyMakeBorder(img, top, self.input_height - newh - top, 0, 0, cv2.BORDER_CONSTANT,
                                         value=(0, 0, 0))
        else:
            img = cv2.resize(srcimg, (self.input_width, self.input_height), interpolation=cv2.INTER_AREA)
        return img, newh, neww, top, left

    def detect(self, srcimg):
        input_img, newh, neww, padh, padw = self.resize_image(cv2.cvtColor(srcimg, cv2.COLOR_BGR2RGB))
        scale_h, scale_w = srcimg.shape[0] / newh, srcimg.shape[1] / neww
        input_img = input_img.astype(np.float32) / 255.0

        blob = cv2.dnn.blobFromImage(input_img)
        self.net.setInput(blob)
        outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())
        # if isinstance(outputs, tuple):
        #     outputs = list(outputs)
        # if float(cv2.__version__[:3])>=4.7:
        #     outputs = [outputs[2], outputs[0], outputs[1]] ###opencv4.7需要这一步，opencv4.5不需要
        # Perform inference on the image
        det_bboxes, det_conf, det_classid, landmarks = self.post_process(outputs, scale_h, scale_w, padh, padw)
        return det_bboxes, det_conf, det_classid, landmarks

    def post_process(self, preds, scale_h, scale_w, padh, padw):
        bboxes, scores, landmarks = [], [], []
        for i, pred in enumerate(preds):
            stride = int(self.input_height / pred.shape[2])
            pred = pred.transpose((0, 2, 3, 1))

            box = pred[..., :self.reg_max * 4]
            cls = 1 / (1 + np.exp(-pred[..., self.reg_max * 4:-15])).reshape((-1, 1))
            kpts = pred[..., -15:].reshape((-1, 15))  ### x1,y1,score1, ..., x5,y5,score5

            # tmp = box.reshape(self.feats_hw[i][0], self.feats_hw[i][1], 4, self.reg_max)
            tmp = box.reshape(-1, 4, self.reg_max)
            bbox_pred = self.softmax(tmp, axis=-1)
            bbox_pred = np.dot(bbox_pred, self.project).reshape((-1, 4))

            bbox = self.distance2bbox(self.anchors[stride], bbox_pred,
                                      max_shape=(self.input_height, self.input_width)) * stride
            kpts[:, 0::3] = (kpts[:, 0::3] * 2.0 + (self.anchors[stride][:, 0].reshape((-1, 1)) - 0.5)) * stride
            kpts[:, 1::3] = (kpts[:, 1::3] * 2.0 + (self.anchors[stride][:, 1].reshape((-1, 1)) - 0.5)) * stride
            kpts[:, 2::3] = 1 / (1 + np.exp(-kpts[:, 2::3]))

            bbox -= np.array([[padw, padh, padw, padh]])  ###合理使用广播法则
            bbox *= np.array([[scale_w, scale_h, scale_w, scale_h]])
            kpts -= np.tile(np.array([padw, padh, 0]), 5).reshape((1, 15))
            kpts *= np.tile(np.array([scale_w, scale_h, 1]), 5).reshape((1, 15))

            bboxes.append(bbox)
            scores.append(cls)
            landmarks.append(kpts)

        bboxes = np.concatenate(bboxes, axis=0)
        scores = np.concatenate(scores, axis=0)
        landmarks = np.concatenate(landmarks, axis=0)

        bboxes_wh = bboxes.copy()
        bboxes_wh[:, 2:4] = bboxes[:, 2:4] - bboxes[:, 0:2]  ####xywh
        classIds = np.argmax(scores, axis=1)
        confidences = np.max(scores, axis=1)  ####max_class_confidence

        mask = confidences > self.conf_threshold
        bboxes_wh = bboxes_wh[mask]  ###合理使用广播法则
        confidences = confidences[mask]
        classIds = classIds[mask]
        landmarks = landmarks[mask]

        if max(mask) == False:
            indices = []
        else:
            indices = cv2.dnn.NMSBoxes(bboxes_wh.tolist(), confidences.tolist(), self.conf_threshold,
                                   self.iou_threshold).flatten()
        if len(indices) > 0:
            mlvl_bboxes = bboxes_wh[indices]
            confidences = confidences[indices]
            classIds = classIds[indices]
            landmarks = landmarks[indices]
            return mlvl_bboxes, confidences, classIds, landmarks
        else:
            print('nothing detect')
            return np.array([]), np.array([]), np.array([]), np.array([])

    def distance2bbox(self, points, distance, max_shape=None):
        x1 = points[:, 0] - distance[:, 0]
        y1 = points[:, 1] - distance[:, 1]
        x2 = points[:, 0] + distance[:, 2]
        y2 = points[:, 1] + distance[:, 3]
        if max_shape is not None:
            x1 = np.clip(x1, 0, max_shape[1])
            y1 = np.clip(y1, 0, max_shape[0])
            x2 = np.clip(x2, 0, max_shape[1])
            y2 = np.clip(y2, 0, max_shape[0])
        return np.stack([x1, y1, x2, y2], axis=-1)

    def draw_detections(self, image, boxes, scores, kpts):
        for box, score, kp in zip(boxes, scores, kpts):
            x, y, w, h = box.astype(int)
            # Draw rectangle
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), thickness=3)
            cv2.putText(image, "face:" + str(round(score, 2)), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        thickness=2)
            for i in range(5):
                cv2.circle(image, (int(kp[i * 3]), int(kp[i * 3 + 1])), 4, (0, 255, 0), thickness=-1)
                # cv2.putText(image, str(i), (int(kp[i * 3]), int(kp[i * 3 + 1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), thickness=1)
        return image
def my_inference()->str:
    # model = torch.load("D:\\programmingsoftWare\\all_codes\\pycharm code\\zhuochong2333\\RumiaPet_main\\work_place\\SmartDeskPet\\model_net.pkl")


    model = FaceCNN()
    # 保存模型权重
    model_path = "D:\huxiaoan-python\Deskpet\zhuochong2333\RumiaPet_main\work_place\SmartDeskPet\model_weights.pth"
    # model.load_state_dict(torch.load("SmartDeskPet/model_weights.pth"))
    model.load_state_dict(torch.load(model_path))


    map_dict = {0: "生气",
                1: "厌恶",
                2: "恐慌",
                3: "高兴",
                4: "难过",
                5: "惊讶",
                6: "中立"}
    # 打开摄像头
    cap = cv2.VideoCapture(0)  # 参数 0 表示默认摄像头，如果有多个摄像头，你可以尝试不同的索引号
    if not cap.isOpened():
        print("无法打开摄像头！")
        return '中立'
        exit()
    # 捕获一帧画面
    ret, frame = cap.read()
    # 关闭摄像头
    cap.release()
    if ret is False:
        return "未读取到图片"

    # 使用yolo获取人脸
    parser = argparse.ArgumentParser()
    # parser.add_argument('--imgpath', type=str, default='images/OIP.jpg', help="image path")
    parser.add_argument('--modelpath', type=str, default='D:\huxiaoan-python\Deskpet\zhuochong2333\RumiaPet_main\work_place\SmartDeskPet\weights\yolov8n-face.onnx',
                        help="onnx filepath")
    parser.add_argument('--confThreshold', default=0.45, type=float, help='class confidence')
    parser.add_argument('--nmsThreshold', default=0.5, type=float, help='nms iou thresh')
    args = parser.parse_args()

    # Initialize YOLOv8_face object detector
    YOLOv8_face_detector = YOLOv8_face(args.modelpath, conf_thres=args.confThreshold, iou_thres=args.nmsThreshold)
    srcimg = frame

    # Detect Objects
    boxes, scores, classids, kpts = YOLOv8_face_detector.detect(srcimg)

    # boxes是获取的多个人脸[[x1,y1,w1,h1], [x2,y2,w2,h2], ... ,[xn, yn, wn, hn]
    # 对于桌宠只需要一个人脸就好了
    if len(boxes) == 0:
        return "没有检查到人脸"

    x, y, w, h = boxes[0].astype(int)
    face = srcimg[y:y + h, x:x + w]
    # 将捕获的图像转换为灰度图
    frame_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    # 将灰度图调整为指定大小（例如 48x48）
    resized_frame = cv2.resize(frame_gray, (48, 48))

    # 将图像数据归一化并reshape
    face_normalized = resized_frame.reshape(1, 48, 48) / 255.0

    face_tensor = torch.from_numpy(face_normalized)
    face_tensor = face_tensor.type('torch.FloatTensor')
    face_tensor = face_tensor.unsqueeze(0)
    infer = model(face_tensor).argmax(dim=-1)

    return map_dict[infer.item()]


class RandomReminder():
    def __init__(self, *args, **kwargs):
        self.choice = -1
        self.tips = []
    def generateChoice(self, *args, **kwargs)->None:
        pass

    # 根据不同场景选择不同的输入
    def generateTips(self, *args, **kwargs)->None:
        pass

    def generateRemind(self, *args, **kwargs)->str:
        # choice大于tips的个数或者choice没有生成则返回None
        if self.choice == -1 or self.choice > len(self.tips):
            return
        #return random.choice(self.tips[self.choice])
        # return "ヾ(･∀･`)有什么开心的事吗！", "ヾ(･∀･`)很开心喵！"
        return '主人，最近有什么难过的事情吗？Rumia可以一直陪着您૮(˶ᵔ ᵕ ᵔ˶)ა'

### 天气情况提示信息
class WeatherReminder(RandomReminder):
    def __init__(self, city, **kwargs):
        super().__init__(**kwargs)
        self.city = city
        self.KEY = '20c4f5de754b4b2a9b475d12ccf88bd9'
        # 生成choice与Tips
        self.generateChoice()
        self.generateTips()
    def get_city_id(self) -> str:
        url_v2 = f'https://geoapi.qweather.com/v2/city/lookup?location={self.city}&key={self.KEY}'  # 城市地理信息
        city_id = requests.get(url_v2).json()['location'][0]['id']
        return city_id

    def generateChoice(self) -> None:
        # 内容返回一个int类型的值
        city_id = self.get_city_id()
        url = f'https://devapi.qweather.com/v7/weather/now?location={city_id}&key={self.KEY}'  # 每日的数据（包含体感温度和相对湿度）
        response = requests.get(url)
        data = response.json()['now']["text"]  # 获取当日情况

        # 生成choice
        if "雨" in data:
            self.choice = 0
        elif "雪" in data:
            self.choice = 1
        else:
            self.choice = 2
    def generateTips(self) -> None:
        # 命名格式  choice + 数字命名，数字最好与Choice的值对应
        # 内容格式  ["str1", "str2", ... , "strn"]
        choice0 = ["今天有雨，记得带伞哦！", "今天有雨，记得添衣！","在下雨喵，记得带伞喵"]
        choice1 = ["今天有雪，记得带伞哦！", "今天有雪，记得添衣！", "在下雪喵，记得带伞喵"]
        choice2 = ["今天天气不错，出门记得享受阳光！"]

        for i in range(3):
            tip = locals()[f"choice{i}"]  # 获取局部变量
            self.tips.append(tip)  # 添加到其中



class ExpressionReminder(RandomReminder):
    def __init__(self):
        super().__init__()
        self.generateChoice()
        self.generateTips()
    def generateChoice(self, *args, **kwargs) ->None:
        # 生成的结果有这些，但是正确率不高，高兴、难过和中立比较好检测到，所以只选择其中2种情绪
        """
        0: "生气",
        1: "厌恶",
        2: "恐慌",
        3: "高兴",
        4: "难过",
        5: "惊讶",
        6: "中立"
        """
        infer = my_inference()
        if infer == "高兴":
            self.choice = 0
        else:
            self.choice = 1
    def generateTips(self, *args, **kwargs) ->None:
        choice0 = ["ヾ(･∀･`)有什么开心的事吗！", "ヾ(･∀･`)很开心喵！"]
        choice1 = ["你可以向我倾诉，我会一直陪伴在你身边d(`･∀･)b", ]

        for i in range(2):
            tip = locals()[f"choice{i}"]  # 获取局部变量
            self.tips.append(tip)  # 添加到其中

def main()->None:
    e = ExpressionReminder()
    print(e.generateRemind())

    w = WeatherReminder("武汉")
    print(w.generateRemind())



def Sentiment_pet():
    e = ExpressionReminder()
    expression = e.generateRemind()
    return expression

def Weather_pet():
    w = WeatherReminder("武汉")
    weather = w.generateRemind()
    return weather

if __name__ == "__main__":
    main()