
import numpy as np
import cv2
import glob

cap = cv2.VideoCapture(0)

images = glob.glob('*.png') 
currentImage=0  

replaceImg=cv2.imread(images[currentImage])
rows,cols,ch = replaceImg.shape
pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])    

zoomLevel = 0   
processing = True   
maskThreshold=10

while(True):
    
    ret, img = cap.read()
   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

    
    if ret == True and processing:
        
        pts2 = np.float32([corners[0,0],corners[8,0],corners[len(corners)-1,0],corners[len(corners)-9,0]])
        
        M = cv2.getPerspectiveTransform(pts1,pts2)
        rows,cols,ch = img.shape
        
        dst = cv2.warpPerspective(replaceImg,M,(cols,rows))

        ret, mask = cv2.threshold(cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY),maskThreshold, 1, cv2.THRESH_BINARY_INV)     
 
        mask = cv2.erode(mask,(3,3))
        mask = cv2.dilate(mask,(3,3))         
       
        for c in range(0,3):
            img[:, :, c] = dst[:,:,c]*(1-mask[:,:]) + img[:,:,c]*mask[:,:]

    cv2.imshow('img',img)  
    
   
    key = cv2.waitKey(1)
    if key == ord('q'): # quit
        print 'Quit'
        break
    if key == ord('p'): # processing
        processing = not processing
        if processing: 
            print 'Activated image processing'
        else: 
            print 'Deactivated image processing'
    if key == ord('z'): #  zoom in
        zoomLevel=zoomLevel+0.05
        rows,cols,ch = replaceImg.shape
        pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
        pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])
        print 'Zoom in'
    if key == ord('x'): #  zoom out
        zoomLevel=zoomLevel-0.05
        rows,cols,ch = replaceImg.shape
        pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
        pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])
        print 'Zoom in'
        print 'Zoom out'
    if key == ord('s'): #  next image
        if currentImage<len(images)-1:
            currentImage=currentImage+1
            replaceImg=cv2.imread(images[currentImage])
            rows,cols,ch = replaceImg.shape
            pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
            pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])
            print 'Next image'
        else:
            print 'No more images on the right'
    if key == ord('a'): #  previous image
        if currentImage>0:
            currentImage=currentImage-1
            replaceImg=cv2.imread(images[currentImage])
            rows,cols,ch = replaceImg.shape
            pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
            pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])

            print 'Previous image'
        else:
            print 'No more images on the left'
            
    if key == ord('d'): # increase threshold
        if maskThreshold<255:
            maskThreshold=maskThreshold+1
            print 'Increase Mask Threshold'
        else:
            print 'maximun value Reached'
    if key == ('f'): # decrease threshold
        if maskThreshold>0:
            maskThreshold=maskThreshold-1
            print 'Decrease Mask Threshold'
        else:
            print 'Mask Threshold at the minimun value'

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
