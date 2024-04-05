import os
import glob
import fitz
from docx2pdf import Converter
from pdf2docx import convert


class FileConverter:
    def __init__(self):
        pass

    def pdf2img(self, pdf_path, save_path):
        page_num = 1
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        filename = os.path.basename(pdf_path)
        filename = filename.split(".")[0]
        file_save_dir = os.path.join(save_path, filename)
        os.makedirs(file_save_dir)
        pdf = fitz.open(pdf_path)
        for page in pdf:
            rotate = int(0)
            zoom_x = 2
            zoom_y = 2
            mat = fitz.Matrix(zoom_x, zoom_y)
            pixmap = page.get_pixmap(matrix=mat, alpha=False)
            pixmap.pil_save(os.path.join(file_save_dir, f"{page_num}.png"))
            print(f"第{page_num}保存图片完成")
            page_num += 1

    def img2pdf(self, img_dir_path, save_dir_path, img_tyep="png"):
        if not os.path.exists(save_dir_path):
            os.makedirs(save_dir_path)
        for name in glob.glob(os.path.join(img_dir_path, f'*.{img_tyep}')):
            file_name = os.path.basename(name).split(".")[0]
            imgdoc = fitz.open(name)
            pdfbytes = imgdoc.convert_to_pdf()
            imgpdf = fitz.open("pdf", pdfbytes)
            imgpdf.save(os.path.join(save_dir_path, f"{file_name}.pdf"))

    def pdf2docx(self, pdf_path, docx_dir_path):
        filename = os.path.basename(pdf_path)
        filename = filename.split(".")[0]
        save_path = os.path.join(docx_dir_path, f"{filename}.docx")
        if not os.path.exists(docx_dir_path):
            os.makedirs(docx_dir_path)
        converter = Converter(pdf_path)
        converter.convert(save_path)
        converter.close()

    def docx2pdf(self, docx_path, pdf_dir_path):
        if not os.path.exists(pdf_dir_path):
            os.makedirs(pdf_dir_path)
        filename = os.path.basename(docx_path)
        filename = filename.split(".")[0]
        convert(docx_path, os.path.join(pdf_dir_path, f"{filename}.pdf"))