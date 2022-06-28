import os
from PIL import Image

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = BASE_DIR + '/data/photos.db'
FILES_DIR = BASE_DIR + '/files'

# 画像ファイルの保存パス
def get_path(file_id, ptype=''):
    return FILES_DIR + '/' + str(file_id) + ptype + '.jpg'

# サムネイルを作成
def make_thumbnail(file_id, size):
    src = get_path(file_id)
    des = get_path(file_id, '-thumb')
    # すでにサムネイルがあれば作成しない
    if os.path.exists(des): return des
    # 正方形に切り取る
    img = Image.open(src)
    msize = img.width if img.width < img.height else img.height
    img_crop = image_crop_center(img, msize)
    # 指定サイズにリサイズ
    img_resize = img_crop.resize((size, size))
    img_resize.save(des, quality=95)
    return des

# 画像の中心を正方形に切り取る
def image_crop_center(img, size):
    cx = int(img.width/2)
    cy = int(img.height/2)
    img_crop = img.crop((
        cx - size / 2, cy - size / 2,
        cx + size / 2, cy + size / 2
    ))
    return img_crop