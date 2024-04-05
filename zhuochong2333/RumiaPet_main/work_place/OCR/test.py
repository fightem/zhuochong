from paddleocr import PaddleOCR, draw_ocr
from PIL import Image


class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")

    def process_image(self, img_path):
        result = self.ocr.ocr(img_path, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                print(line)

        result = result[0]
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='doc/fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')


# 使用示例
processor = OCRProcessor()
img_path = 'img_1.png'
processor.process_image(img_path)