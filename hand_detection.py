import cv2
import datetime
import argparse
import imutils
from imutils.video import VideoStream
from utils import detector_utils as detector_utils

detection_graph, sess = detector_utils.load_inference_graph()

if __name__ == '__main__':
    # Detection confidence threshold to draw bounding box
    score_thresh = 0.60

    # Get stream from webcam and set parameters)
    vs = VideoStream().start()

    # max number of hands we want to detect/track
    num_hands_detect = 1
    color = (0, 255, 0)
    im_height, im_width = (None, None)
    try:
        while True:
            # Read Frame and process
            frame = vs.read()
            frame = cv2.resize(frame, (640, 480))

            if im_height == None:
                im_height, im_width = frame.shape[:2]

            # Convert image to rgb since opencv loads images in bgr, if not accuracy will decrease
            try:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except:
                print("Error converting to RGB")

            # Run image through tensorflow graph
            boxes, scores, classes = detector_utils.detect_objects(
                frame, detection_graph, sess)
                 
            for i in range(num_hands_detect):
                if scores[i] > score_thresh:
                    (left, right, top, bottom) = (boxes[i][1] * im_width, boxes[i][3] * im_width,
                                                      boxes[i][0] * im_height, boxes[i][2] * im_height)					
                    if classes[i] == 1: hlabel = 'open'
                    if classes[i] == 2: hlabel='close'
                    cv2.putText(frame, hlabel+str("{0:.2f}".format(scores[i])), (int(left), int(top) - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,1)
            # Draw bounding boxeses and text
            detector_utils.draw_box_on_image(
                num_hands_detect, score_thresh, scores, boxes, classes, im_width, im_height, frame)

            cv2.imshow('Detection', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                vs.stop()
                break
    except KeyboardInterrupt:
        pass#print("Average FPS: ", str("{0:.2f}".format(fps)))
