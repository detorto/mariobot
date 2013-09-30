import Image

def pil_image(frame,size):
    return Image.fromstring("RGB", size, frame)

def crop_rect(xy,wh):
    return xy+(xy[0]+wh[0],xy[1]+wh[1])