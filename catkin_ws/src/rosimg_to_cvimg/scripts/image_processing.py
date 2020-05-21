import cv2


def process_frame(fgMask):

    img = fgMask

    #print('Original Dimensions : ',img.shape)

    scale_percent = 1 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    right=0
    left=0
    #print('Resized Dimensions : ',resized.shape)
    for i in range (width):
        for j in range (height):
            if resized[i][j]>0:
                if j>3:
                    right+=1
                else:
                    left+=1



    regions = {
    'right': right,
    'left': left,
    }
    cv2.imshow('resized',resized)
    cv2.waitKey(30)
    return regions
