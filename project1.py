import PIL, sys, argparse
from PIL import Image
parser = argparse.ArgumentParser()
parser.add_argument('-e', action="store", help="Enrypt message", dest="msg")
parser.add_argument('-d', action='store', help="decrypt message", dest='dImage')
parser.add_argument('-i', action="store", help="image to lay message into", dest="image")
parser.add_argument('-o', action='store', help='output image', dest='finalImage')
args = parser.parse_args()

def main():
    if (sys.argv[1] == '-e'):
        #convert string message into binary
        msgBuff = [0] * (len(args.msg) * 8)
        i = 0
        for char in args.msg:
            #convert letter from msg to unicode representation
            #of that letter then convert it to binary
            letter = format(ord(char), '08b')
            for num in letter:
                #convert that 1 or 0 char to unicode,
                #subtract 48 to get actual number
                #store it into the msgBuff
                msgBuff[i] = ord(num) - 48
                i = i + 1

        img = Image.open(args.image)
        x, y = img.size
        #check if image is too big for picture
        if (len(msgBuff) >= x*y):
            print("ERROR: Message too big")
        else:
            encrypt(img, msgBuff, x, y)
        img.close()
    elif(sys.argv[1] == '-d'):
        decrypt()

    sys.exit()



# def encrypt - gets the number of pixels within a JPG file
# @param picture - the picture to determine pixel count
# @param message - binary message to put into picture
# @param width - width of picture
# @param height - length of picture
def encrypt(picture, message, width, height):
    #store length of message
    length = len(message)
    #convert length of message to binary
    msgLenBin = format(length, '032b')

    # get pixel rgb values
    rgbImg = picture.convert('RGB')
    pix = picture.load()

    #store message length in first 11 pixels
    msgPos = 0
    j = width-1
    while j > (width-1) - 11:
        #get rgb binary of pixel
        r, g, b = rgbImg.getpixel((j, height-1))
        red = list(format(r, '08b'))
        green = list(format(g, '08b'))
        blue = list(format(b, '08b'))

        if msgPos < len(msgLenBin):
            red[7] = msgLenBin[msgPos]
            msgPos += 1
        else:
            red[7] = 0
        if msgPos < len(msgLenBin):
            green[7] = msgLenBin[msgPos]
            msgPos += 1
        else:
            green[7] = 0
        if msgPos < len(msgLenBin):
            blue[7] = msgLenBin[msgPos]
            msgPos += 1
        else:
            blue[7] = 0

        #convert from list to string
        red = ''.join(map(str, red))
        green = ''.join(map(str, green))
        blue = ''.join(map(str, blue))

        #change rgb value of pixel
        pix[j, height-1] = (int(red, 2), int(green, 2), int(blue, 2))
        j -= 1

    #store message in rest of pixels
    i = width-1-11
    j = height-1
    msgPos = 0
    done = False
    while not done:
        #get rgb binary of pixel
        r, g, b = rgbImg.getpixel((i, j))
        red = list(format(r, '08b'))
        green = list(format(g, '08b'))
        blue = list(format(b, '08b'))

        if msgPos < len(message):
            red[7] = message[msgPos]
            msgPos += 1
        if msgPos < len(message):
            green[7] = message[msgPos]
            msgPos += 1
        if msgPos < len(message):
            blue[7] = message[msgPos]
            msgPos += 1


        #convert from list to string
        red = ''.join(map(str, red))
        green = ''.join(map(str, green))
        blue = ''.join(map(str, blue))

        #change rgb value of pixel
        pix[i, j] = (int(red, 2), int(green, 2), int(blue, 2))
        i-=1

        if i == 0:
            j -= 1
            i = width - 1

        if msgPos == len(message):
            done = True
    picture.save(args.finalImage)

#def decrypt() - decrypt message in image
def decrypt():
    # open image and get width and length
    img = Image.open(args.dImage)
    width, height = img.size

    # get pixel rgb values
    rgbImg = img.convert('RGB')

    #get message length
    msgLen = []
    for i in range(width-1, width-12, -1):
        r, g, b = rgbImg.getpixel((i, height-1))
        red = list(format(r, '08b'))
        green = list(format(g, '08b'))
        blue = list(format(b, '08b'))

        msgLen.insert(len(msgLen), red[7])
        msgLen.insert(len(msgLen), green[7])
        msgLen.insert(len(msgLen), blue[7])

    msgLen = ''.join(map(str, msgLen))
    msgLen = msgLen[:len(msgLen)-1]

    #get message
    i = width-12
    j = height-1
    done = False
    msg = []
    while not done:
        r, g, b = rgbImg.getpixel((i, j))
        red = list(format(r, '08b'))
        green = list(format(g, '08b'))
        blue = list(format(b, '08b'))

        if (len(msg) < int(msgLen, 2)):
            msg.insert(len(msg), red[7])
        if (len(msg) < int(msgLen, 2)):
            msg.insert(len(msg), green[7])
        if (len(msg) < int(msgLen, 2)):
            msg.insert(len(msg), blue[7])

        i-=1
        if i == 0:
            j -= 1
            i = width - 1

        if(len(msg) == int(msgLen,2)):
            done = True
    msg = ''.join(map(str, msg))
    temp = ''.join(map(str, msg))

    i = 0
    j = 8
    msg = ''
    while j <= len(temp):
        msg += chr(int(temp[i:j], 2))
        i = j
        j+=8
    img.close()
    print(msg)

if __name__ == "__main__":
    main()
