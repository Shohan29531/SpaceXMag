import cv2

img = cv2.imread("Output.jpg")

def draw_circle(event, x, y, flags, param):
    
    if event == cv2.EVENT_LBUTTONDOWN:
        print("hello")
        cv2.circle(img, (x, y), 100, (0, 255, 0), -1)
        
cv2.namedWindow(winname = "Title of Popup Window")
cv2.setMouseCallback("Title of Popup Window", draw_circle)


while True:
    cv2.imshow("Title of Popup Window", img)

    k = cv2.waitKey(1)
    
    if k == 27:
        break
    elif k == 32:
        cv2.circle(img, (200, 200), 100, (0, 255, 0), -1)
        print("inside")



        
cv2.destroyAllWindows()