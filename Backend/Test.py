import urllib.request
import numpy as np
import cv2

f = open("api_key.txt", "r")
api_key = f.read()
start_point = np.array([57.588179, 12.113134])
end_point = np.array([57.580574, 12.156631])
size = abs(start_point-end_point)

zoom = 19
pixel_size = size * 2**zoom

patch = np.array([640, 640])
n_patch = np.ceil(pixel_size/patch)
print(n_patch)

tot_map = np.zeros((int(pixel_size[0]*2)+2000, int(pixel_size[1]*2)+1000, 3))

gap = patch/(2**zoom)
gap[1] *= 1.4
gap[0] *= 0.7
n_patch = np.ceil(size/gap)


start_point -= np.array([320, -320])/(2**zoom)

point = [0, 0]
patch *= 2
patch[0] -= 90
patch[1] -= 5

for j in range(int(n_patch[0])):
    for i in range(int(n_patch[1])):
        point[0] = start_point[0] - gap[0] * j
        point[1] = start_point[1] + gap[1] * i

        request = 'https://maps.googleapis.com/maps/api/staticmap?' \
                  f'center={point[0]},{point[1]}' \
                  f'&zoom={zoom}' \
                  '&size=640x640' \
                  '&scale=2' \
                  '&maptype=satellite' \
                  '&key=' + api_key

        urllib.request.urlretrieve(request, 'testing.png')

        temp = cv2.imread('testing.png')
        tot_map[patch[0]*j:patch[0]*(j+1), patch[1]*i:patch[1]*(i+1), :] = temp[0:1190, 0:1275, :]

cv2.imwrite('done.png', tot_map)
