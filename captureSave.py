import cv2, time

# Create an object. Zero for external camera
video=cv2.VideoCapture(0)


a=0
img_counter=0
while True:
    a = a + 1
    # Create a frame object
    check, frame = video.read()
    frame = cv2.flip(frame, 1)
    #print(check)
    #print(frame) #Representing image

    #time.sleep(0.5)
    #cv2.rectangle(frame, (x, y), (x+width,y+height), (0,255,0), 2)
    cv2.rectangle(frame, (50, 50), (400, 400), (0,255,0), 2)

	# Show the frame
    cv2.imshow("Capturing", frame)
    img_name = "images/img_{}.png".format(img_counter)
    #crop_img = frame[y:y+h, x:x+w]
    crop_img = frame[52:398, 52:398]
	
	#cv2.imwrite(img_name, frame)
    cv2.imwrite(img_name, crop_img)
    img_counter+=1
    
    # For playing
    key=cv2.waitKey(1)
    
    if key == ord('q'):
        break

print(a)
# Shut down the camera
video.release()
cv2.destroyAllWindows