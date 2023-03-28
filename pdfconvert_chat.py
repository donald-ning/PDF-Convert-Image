import os
import zipfile
import tempfile
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor
def convert_pdf_to_jpg(pdf_file, pdf_dir, output_dir):
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        pages = convert_from_path(pdf_path)
        image_list = []
        print(f"正在处理{pdf_file}文件...")
        for i, page in enumerate(pages):
            image_path = os.path.join(temp_dir, f"{pdf_file}_{i+1}.jpg")
            page.save(image_path, 'JPEG')
            image_list.append(image_path)
        # 创建对应的zip压缩包
        zip_path = os.path.join(output_dir, f"{pdf_file}.zip")
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            for image in image_list:
                zip_file.write(image, os.path.basename(image))
            print(f"{pdf_file}文件处理完成！")
            # 删除保存的图像文件
        for image in image_list:
            os.remove(image)
# 输入包含PDF文件的目录路径和输出目录路径
pdf_dir = ''
output_dir = ''
pdf_dir = input("请输入pdf文件所在目录路径，按回车键继续...")
output_dir = input("请输入输出目录路径，按回车键继续...")

# 获取包含PDF文件的列表
pdf_files = [pdf_file for pdf_file in os.listdir(pdf_dir) if pdf_file.endswith('.pdf')]

# 创建线程池
with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(lambda pdf_file: convert_pdf_to_jpg(pdf_file, pdf_dir, output_dir), pdf_files)

