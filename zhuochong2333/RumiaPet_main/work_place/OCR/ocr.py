from paddleocr import PaddleOCR, draw_ocr
from PIL import Image


class OCRProcessor():
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        self.txts=[]

    def process_image(self, img_path):
        result = self.ocr.ocr(img_path, cls=True)
        if result is None:
            return "未发现文字"
        result = result[0]
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        self.txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, self.txts, scores, font_path='doc/fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        #im_show.save('C:/Users/29549/Pictures/222.jpeg') #图片保存路径
        return "\n".join(self.txts)



#使用示例
# processor = OCRProcessor()
# img_path = 'C:/Users/29549/Pictures/ocr.jpeg'
# print(processor.process_image(img_path))