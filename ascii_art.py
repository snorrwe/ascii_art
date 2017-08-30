from PIL import Image
import numpy as np
import argparse

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`. "
gscale2 = "@%#*+=-:. "

def get_average_luminance(image):
    im = np.array(image)
    w,h = im.shape
    return np.average(im.reshape(w*h))

def convert_image_to_ascii(fileName, columns, scale, moreLevels):
    global gscale1
    global gscale2

    image = Image.open(fileName).convert("L")
    #image = Image.Open(argv[1]).convert("L")
    width, height = image.size[0], image.size[1]
    tileWidth = width / columns
    tileHeight = tileWidth / scale
    rows = int(height/tileHeight)

    if columns > width or rows > height:
        return ["Image is too small for specified columns!"]

    result = []
    for j in range(rows):
        y1 = int(j*tileHeight)
        y2 = int((j+1)*tileHeight) if j != rows-1 else height
        result.append("")
        for i in range(columns):
            x1 = int(i * tileWidth)
            x2 = int((i+1)*tileWidth) if i != columns-1 else width
            cropped = image.crop((x1, y1, x2, y2))
            avgLuminance = int(get_average_luminance(cropped))
            if moreLevels:
                greyScaleValue = gscale1[avgLuminance*69//255]
            else:
                greyScaleValue = gscale2[avgLuminance*9//255]
            result[j] += greyScaleValue
    return result

def init_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", required=False)
    parser.add_argument("-c", required=False)
    parser.add_argument("-s", required=False)
    parser.add_argument("-ml", required=False)
    args = parser.parse_args()
    file = args.f if args.f else "Capture.jpg"
    columns = 165 if not args.c else int(args.c)
    scale = 0.4 if not args.s else float(args.s)
    moreLevels = False if not args.ml else args.ml
    return (file, columns, scale, moreLevels)

def main():
    """
    Argument list:
    -f FILENAME
    -c COLUMNS
    -s SCALE
    -ml ADD_MORE_LEVELS
    """
    file, columns, scale, moreLevels = init_arguments()
    result = convert_image_to_ascii(file, columns, scale, moreLevels)
    with open("awsome.txt", "w") as file:
        for row in result:
            file.write("%s\n" % row)

if __name__ == '__main__':
    main()
