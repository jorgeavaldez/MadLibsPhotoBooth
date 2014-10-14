from PIL import Image
from PIL import ImageDraw
import os
import time

# program creates final image when raw images are all available

def imgout(pictureIn, pictureOut):

	#opens all input imgs
    originPic = Image.open(pictureIn)
    originPic = originPic.rotate(270)

    #Crops the images
    head = originPic.crop((0, 0, 225, 287 - 129))
    word = originPic.crop((0, 287 - 129, 225, 287))

    #opens the template
    fp = r"D:\Github\Fall2014IDE\Fall2014IDE\Fall2014IDE\PictureManipulation\Resources\tedx2014template.png"
    bg = Image.open(fp)

    #all headshot imgs opened to 225x287 px, word imgs open to 263x129 px:
    head.thumbnail((225,287))
    word.thumbnail((263,129))
    bg.thumbnail((1400,900))

    #Draws the Background
    draw = ImageDraw.Draw(bg)
    draw.line((0, 320, 1400, 320), 0)

    #paste the image at locations: #change locations as needed
    
    #Person 1
    bg.paste(head, (143, 500))

    #Person 2
    bg.paste(head, (439, 500))

    #Person 3
    bg.paste(head, (733, 500))

    #Person 4
    bg.paste(head, (1030, 500))

    #Left two word board images
    bg.paste(word, (360, 41))
    bg.paste(word, (652, 41))

    #Right two word board images
    bg.paste(word, (510, 195))
    bg.paste(word, (902, 195))

    bg.save(pictureOut)


#checks for new file in directory to draw
if __name__ == "__main__":
    imgout(r"D:\Github\Fall2014IDE\Fall2014IDE\Fall2014IDE\PictureManipulation\Input Images\IMG0.jpg", r"D:\Github\Fall2014IDE\Fall2014IDE\Fall2014IDE\PictureManipulation\Output Images\TEST1.png")