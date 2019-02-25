# Serveix per posicionar objectes tridimensionals en els eixos que definim del taulell d'escacsself.
import numpy as np
import cv2
import yaml
import glob

# Servix per pintar els eixo des del corner 0 en aquest fins imgpts quadrats per l'eix x y i z.
def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5) # eix Z
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5) # eix Y
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5) # eix X
    return img

def drawCube(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)

    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)

    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)

    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

    return img

# Primerament carreguem el calibratge que hem fet anteriorment dins del fitxer calibration.yaml
#  Per carregar els valors de un fitxer : Descomentar aixó!
# with open('calibration.yaml') as f:
#     loadeddict = yaml.load(f)
# mtx = loadeddict.get('camera_matrix')
# dist = loadeddict.get('dist_coeff')

# Load previously saved data
with np.load('calibration.z.npz') as X:
    mtx, dist = [X[i] for i in ('mtx','dist')]

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 0.001)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Per pintar els eixos 3D
# axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

# Per pintar el cub 3D
axis = np.float32([[0,0,0],[0,3,0],[3,3,0],[3,0,0],[0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3]])

for fname in glob.glob('left*.jpg'):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

    if ret == True:

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        # Find the rotation and translation vectors.
        _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)

        # project 3D points to image plane
        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

        img = drawCube(img,corners2,imgpts)
        cv2.imshow('img',img)
        k = cv2.waitKey(0) & 0xff
        if k == 's':
            cv2.imwrite(fname[:6]+'.png', img)

cv2.destroyAllWindows()
