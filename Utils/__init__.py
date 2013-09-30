import Image

def pil_image(frame,size):
    return Image.fromstring("RGB", size, frame)