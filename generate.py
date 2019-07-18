from PIL import Image
from PIL.ExifTags import TAGS
import os
import math
from fractions import Fraction
from datetime import datetime
import json

target_size = 600, 800

class Photo:
    def __init__(self, file_path):
        self.file_path = file_path
        stripped_name = os.path.basename(file_path).replace(".jpg", "")
        path = os.path.dirname(file_path)
        small_image_name = os.path.join(path, stripped_name + "_thumbnail.jpg")
        self.thumbnail_path = small_image_name

        self.image = Image.open(self.file_path)
        self.full_size = self.image.size
        print(self.full_size)

        self.shot = None
        self.ISO = None
        self.device = None
        self.date = None


        self.load()
        self.date = datetime.strptime(self.date.split(' ')[0], "%Y:%m:%d")

    def get_desc(self):
        date = self.date.strftime("%b %d %Y")
        return f"Shot with {self.device} on {date} ({self.shot} ISO {self.ISO})"

    def load(self):
        self.load_exif()
        self.create_thumbnail()

    def create_thumbnail(self):
        self.image.thumbnail(target_size)
        self.image.save(self.thumbnail_path)

    def load_exif(self):
        ret = {}
        info = self.image._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag)
            ret[decoded] = value
        
        self.ISO = ret['ISOSpeedRatings']
        self.device = ret['Model'].capitalize()
        self.shot = self.parse_shot_str(ret)
        self.date = ret["DateTimeDigitized"]

    def parse_shot_str(self, exif):
        shutter_speed = exif['ShutterSpeedValue']
        apature = exif['ApertureValue']
        focal_length = exif['FocalLength']

        real_apature = math.sqrt(2**(apature[0] / apature[1]))
        real_shutter = Fraction(2**(-shutter_speed[0]/shutter_speed[1])).limit_denominator(8000)

        return f"{str(real_shutter)} sec; f/{round(real_apature, 2)} {int(focal_length[0] / focal_length[1])} mm;"
        

def generate_small_images(resource_dir):
    images = []
    for subdir, dirs, files in os.walk(resource_dir):
        for image_file in files:
            if image_file.endswith(".jpg") and "thumbnail" not in image_file:
                images.append(os.path.join(subdir, image_file))
    
    photos = []
    for full_size in images:
        photos.append(Photo(full_size))

    return photos


def write_lists(photos):
    main_image_list = []
    for photo in photos:
        main_image_list.append({
            'src': photo.file_path,
            'w': photo.full_size[0],
            'h': photo.full_size[1],
            'title': photo.get_desc()
        })

    thumb_image_list = [photo.thumbnail_path for photo in photos]

    main_image_list_str = "photos = " + json.dumps(main_image_list)
    thumb_image_list_str = "thumbnails = " + json.dumps(thumb_image_list)

    with open("scripts/photo_list.js", 'w') as photo_list_file:
        photo_list_file.write(main_image_list_str)

    with open("scripts/thumbnail_list.js", 'w') as thubnail_list:
        thubnail_list.write(thumb_image_list_str)

if __name__ == "__main__":
    the_photos = generate_small_images("resources")

    for photo in the_photos:
        print(photo.get_desc())

    write_lists(the_photos)