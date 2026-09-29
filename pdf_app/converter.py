from PIL import Image
import os


def image_to_pdf(input_file):
    img = Image.open(input_file)

    if img.mode == "RGBA":
        img = img.convert("RGB")

    output_file = os.path.splitext(input_file)[0] + ".pdf"

    img.save(output_file)

    return output_file


def image_to_png(input_file):
    img = Image.open(input_file)

    output_file = os.path.splitext(input_file)[0] + ".png"

    img.save(output_file)

    return output_file


def image_to_jpg(input_file):
    img = Image.open(input_file)

    if img.mode == "RGBA":
        img = img.convert("RGB")

    output_file = os.path.splitext(input_file)[0] + ".jpg"

    img.save(output_file)

    return output_file