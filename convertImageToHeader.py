import imageio
import sys
import numpy as np
import matplotlib.pyplot as plt

## Number of pixel updates per revolution
pixelUpdatesPerRevolution = 50

## Number of pixels
numberPixels = 72

## Angle in degrees between each pixel update
pixelUpdateAngleIncrement = 180//pixelUpdatesPerRevolution


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

for name in sys.argv[1:]:
    arr = imageio.imread(name)

    ## Finding the minimum length for the image
    length = 0
    if arr.shape[0] < arr.shape[1]:
        length = arr.shape[0]
    else:
        length = arr.shape[1]

    points = []
    polarData = []
    for phi in range(0, 180, pixelUpdateAngleIncrement):
        ledStrip = []
        for rho in range(int(-length/2), int(length/2), int(length/numberPixels)):
            [x, y] = pol2cart(rho, phi)
            x = int(x + length/2)
            y = int(y + length/2)

            ## making sure bounds work
            if x < 0: x = 0
            if x >= length: x = length - 1
            if y < 0: y = 0
            if y >= length: y = length - 1

            points.append({
            "rho":rho,
            "phi":phi,
            "rgb":[arr[x, y, 0], arr[x, y, 1], arr[x, y, 2]]
            })
            ledStrip.append([arr[x, y, 0], arr[x, y, 1], arr[x, y, 2]])
        polarData.append(ledStrip)


    ## File Write
    file = open("pov/graphics.h", "w")
    file.write("//Don't edit this file, it's code-gen!!\n")
    file.write("//Modify convertImageToHeader.py if you wanna do anything.\n\n")

    file.write("const uint8_t PROGMEM red[][72] = {\n")
    for i in range(len(polarData)):
        colors = []
        for j in range(numberPixels):
            colors.append(polarData[i][j][0])
        file.write("{" + ",".join(map(str, colors)) + "},\n")
    file.write("};\n\n")

    file.write("const uint8_t PROGMEM green[][72] = {\n")
    for i in range(len(polarData)):
        colors = []
        for j in range(numberPixels):
            colors.append(polarData[i][j][1])
        file.write("{" + ",".join(map(str, colors)) + "},\n")
    file.write("};\n\n")

    file.write("const uint8_t PROGMEM blue[][72] = {\n")
    for i in range(len(polarData)):
        colors = []
        for j in range(numberPixels):
            colors.append(polarData[i][j][2])
        file.write("{" + ",".join(map(str, colors)) + "},\n")
    file.write("};\n\n")

    '''
    for i in range(len(polarData)):
        file.write("const uint8_t PROGMEM stripColors" + str(i) + "[][3] = {\n")
        for j in range(numberPixels):
            file.write("{" + ",".join(map(str, polarData[i][j])) + "},\n")
        print(polarData[i])
        file.write("};\n\n")

    stripColorArrNames = []
    for i in range(len(polarData)):
        stripColorArrNames.append("stripColors" + str(i))
    file.write("const char *const[] stripTable[] PROGMEM = {" + ", ".join(stripColorArrNames) + "};")
    '''




    print(arr.shape)
    print(length)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    i = 0
    for phi in range(0, 180, pixelUpdateAngleIncrement):
        ledStrip = []
        j = 0
        for rho in range(int(-length/2), int(length/2), int(length/numberPixels)):
            [x, y] = pol2cart(rho, phi)
            x = int(x + length/2)
            y = int(y + length/2)
            rgb = [val/255 for val in polarData[i][j]]
            ax.scatter(x, y, color=rgb)
            j+=1
        i+=1

    ax1 = fig.add_subplot(121)

    for point in points:
        [x, y] = pol2cart(point["rho"], point["phi"])
        x = int(x + length/2)
        y = int(y + length/2)
        rgb = [val/255 for val in point["rgb"]]
        ax.scatter(x, y, color=rgb)
    plt.show()
