import os
from PIL import Image, ImageDraw, ImageFont

NUMBER_OF_CHARS = 100000
CHARS_PER_LINE = 220

if __name__ == "__main__":
    text_rows = []
    
    with open("test.bin", "rb") as file:
        data = file.read()[:NUMBER_OF_CHARS]
    
    for row in range(1, NUMBER_OF_CHARS//CHARS_PER_LINE):
        row_string = ""
        for index in range(1, CHARS_PER_LINE):
            row_string += str(hex(data[row*index])[2:]).upper()
            
        text_rows.append(row_string)
        
    im = Image.new(mode="RGB", size=(1000,1000), color="#606B73")
    draw = ImageDraw.Draw(im)
    
    for index, string in enumerate(text_rows):      
        draw.text(xy=(0,index * 10), text=string, fill="#7A7A7A")

    draw.text(xy=(10,120), text="Example", fill="#000000")
    # write to stdout
    # im.save(sys.stdout, "PNG")
    im.save("test.png")