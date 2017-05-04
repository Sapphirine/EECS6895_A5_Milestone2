import dlib
import cv2
import argparse as ap
import motionkalm



def Initialization(box)

## Get the initialized bounding box for the selected target

	p_left_list = []
	p_right_list = []

	box_list = []
	box_target = box.copy()
	mousebutton = False

	ix,iy = -1,-1

	cv2.namedWindow("box_target", cv2.WINDOW_NORMAL)
	cv2.imshow("box_target", box_target)
# Creating mouse callback function
	def draw_rect(event, x, y, flags, param):
		
		global p_left,p_right,mousebutton

		if event == cv2.EVENT_LBUTTONDOWN:
			mousebutton = True
			ix,iy = x,y
			p_left_list.append((ix,iy))

		elif event == cv2.EVENT_MOUSEMOVE:
			if mousebutton == True:
				cv2.rectangle(img,p_left_list[-1],(x,y),(0,255,0),1) 

		elif event == cv2.EVENT_LBUTTONUP:
			if mousebutton == False:
				ix,iy = x,y
				p_right_list.append((ix, iy))

		print "Get target object initialization at [{}, {}]".format(p_left_list[-1], p_right_list[-1])


# handle mouse events in OpenCV
	cv2.setMouseCallback("Inibox", draw_rect)

	key = cv2.waitKey(30)
	if key == ord('t'):
		cv2.destroyAllWindows()
		return zip(p_right_list, p_left_list)

	cv2.destroyAllWindows()
	return zip(p_right_list, p_left_list)


def VideoRead(videopath)

	cam = cv2.VideoCapture(videopath)

    # If Camera Device is not opened, exit the program
	if not cam.isOpened():
		print "Video device or file couldn't be opened"
		exit()
	
	print "Press key `p` to pause the video to start tracking"
	while True:
        
		retval, img = cam.read()
		if not retval:
			print "Cannot capture frame device"
			exit()
		if(cv2.waitKey(10)==ord('p')):
			break
		cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
		cv2.imshow("Image", img)
	cv2.destroyWindow("Image")



	cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
	cv2.imshow("Image", img)

	obj_box = Initialization(img)

	return obj_box

    

def Tracking(videopath)


	obj = VideoRead(videopath)

    tracker = [dlib.correlation_tracker() for _ in xrange(len(obj))]
   
    [tracker[i].start_track(img, dlib.rectangle(*rect)) for i, rect in enumerate(obj)]

    while True:
        
        retval, img = cam.read()
        if not retval:
            print "Cannot capture frame device | CODE TERMINATION :( "
            exit()
        
        for i in xrange(len(tracker)):
            tracker[i].update(img)
            
            rect = tracker[i].get_position()

           
            radio = tracker[i].update(img, rect)
            #print radio
            pt1 = (int(rect.left()), int(rect.top()))
            pt2 = (int(rect.right()), int(rect.bottom()))
            
            if radio > best_radio:
                best_radio = radio
                print "New highest match!"
            
            else:
                if radio < 0.2*best_radio:
                   #print "Object is exiting or being occluded"
                   # pt1 = (int(rect.left()), int(rect.top()))
                   # pt2 = (int(rect.right()), int(rect.bottom()))
        
                   # kf = kf.em(measurements, n_iter=5)
                   # (filtered_state_means, filtered_state_covariances) = kf.filter(measurements)
                   kalmanfilter = motionkalm()

                   Px, Py = kalmanfilter.ComputeMotion(x,y)

                   
                   print "Object is exiting or being occluded, the next prediction position 1s later is:"
                   print Px
    
                   break
                   exit()

            pt1 = (int(rect.left()), int(rect.top()))
            pt2 = (int(rect.right()), int(rect.bottom()))
            cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
            print "Object {} tracked at [{}, {}] \r".format(i, pt1, pt2),
            if dispLoc:
                loc = (int(rect.left()), int(rect.top()-20))
	        txt = "Object tracked at [{}, {}]".format(pt1, pt2)
	        cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1)
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
      
        if cv2.waitKey(1) == 27:
            break

    
    cam.release()


def main(data):
    Tracking(data)

if __name__ == "__main__":
	videopath = "/Users/lingyuzhang/Spring17/5AdvancedBigdata/task_milestone/videofile/people.avi" 
    main(videopath)


















