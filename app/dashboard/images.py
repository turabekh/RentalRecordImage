from PIL import Image
from resizeimage import resizeimage



def resize_image(width, height, image_file_name):
    """ Need to 'pip install python-resize-image'
        before start. 
        Takes desired width, height, image file name
        returns new resized_image.jpg file """
    with open(image_file_name, 'r+b') as f:
        with Image.open(f) as image:
            try:
                cover = resizeimage.resize_cover(image, [width, height], validate=True)
                cover.save(image_file_name, image.format)
            except:
                print("Upload unsuccessfull. Something went wrong. Please try again")