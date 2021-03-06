from sys import exit
import math

import numpy as np
import cv2

import re
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


ARC_LENGTH_ADJUST = 0.015
SCREEN_WIDTH = 500




def resize_img(img, width):
    dimensions = img.shape
    fx = width/dimensions[0]
    fy = fx
    img = cv2.resize(img, None, fx=fx, fy=fy)
    dimensions = img.shape
    return img








def ocr_read_with_many_filters(img):
    '''
    there are many cases that the tool can not detect the text on the screen because noise
    this function will create many filters and apply to the image and return a list of result
    for other function to compare
    '''
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #for x in xrange(1,10):
    #    pass
    mask_dark_red = cv2.inRange(hsv, (150, 50, 10), (179, 255, 255)) # dark red
    mask_light_red = cv2.inRange(hsv, (0, 70, 100), (15, 255, 200)) # dark red
    mask_dark = cv2.inRange(hsv, (0, 1, 1), (170, 200, 100)) # dark red
    mask = cv2.bitwise_or(mask_dark_red, mask_light_red, mask_dark)
    mask = cv2.bitwise_not(mask)

    img_show('',imgThreshold)
    print(ocr_read(imgThreshold))




def img_show(img_name, img):
    if isinstance(img, list):
        for each_img in img:
            cv2.imshow(img_name, each_img)
    else:
        cv2.imshow(img_name, img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()





def find_contours(img):
    try: # if the img is BGR
        # convert image to gray scale. This will remove any color noise
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # use threshold to convert the image to black and white with less noise
        img = cv2.bilateralFilter(img, 11, 17, 17)
        img = cv2.Canny(img, 30, 200)
    except Exception as e: # if others (gray, BW)
        pass
    
    # find all contours
    contours,h = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours










def draw_bounding_box(img, contour, shape='rectangle'):
    '''
    draw a bounding box of the contour
    shape = 'rectangle' or 'circle'
    '''
    img = img.copy()

    if shape=='circle':
        center, radius = cv2.minEnclosingCircle(contour)
        cv2.circle(img, center, radius, (255,0,0),2)
    else:
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
    return img




def draw_all_contours(img, contours, edge_num=None, minimun_area=None):
    img_contour = img.copy()
    for cnt in contours:

        # shape of contour # 0.015 need to adjust to find the best number for rectangle
        approx = cv2.approxPolyDP(cnt,ARC_LENGTH_ADJUST*cv2.arcLength(cnt,True),True)

        # calculate area of contour
        area = cv2.contourArea(cnt)

        # check proper contours
        if edge_num==None: 
            pass
        else:
            if len(approx)==edge_num:
                pass
            else:
                continue

        if minimun_area==None:
            pass
        else:
            if area>minimun_area:
                pass
            else:
                continue

        x,y,w,h = cv2.boundingRect(cnt)
        cv2.drawContours(img_contour,[cnt],0,(0,255,0),2)
        #cv2.putText(img_contour, str(len(approx)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1)
        
    return img_contour










def find_screen_contour(img):
    '''
    detect white screen of the tool, the img trasfer should be a totally white screen (no content)
    the return value is a contour of the frame detected
    '''
    img = img.copy()
    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # select range of specific colors
    mask = cv2.inRange(hsv, (0, 0, 100), (179, 255, 255)) # detect white screen
    #img_show('', mask)
  
    # find contours
    contours = find_contours(mask)

    screen_contour = sorted(contours, key = cv2.contourArea, reverse = True)[0]

    return screen_contour







def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result





def get_screen_with_canvas(img):
    '''
    get screen in put it in the center of an image, 
    put the image onto a canvas which is large enough for the image to rotate
    '''
    OFFSET_SCREEN = 3
    OFFSET_CANVAS_EDGE = 20
    # find screen contour
    screen_contour = find_screen_contour(img)
    #img_show('screen_contour', draw_all_contours(img, [screen_contour]))
    #img_show('screen_contour', draw_bounding_box(img, screen_contour))

    # getting the screen with offset
    x,y,w,h = cv2.boundingRect(screen_contour)
    screen = img[y-OFFSET_SCREEN:y+h+OFFSET_SCREEN, x-OFFSET_SCREEN:x+w+OFFSET_SCREEN]

    #img_show('screen', screen)
    # calculating canvas_edge
    canvas_edge = int(math.sqrt((screen.shape[0])**2 + (screen.shape[1])**2)) + OFFSET_CANVAS_EDGE

    #Creating a dark square with NUMPY  
    canvas = np.zeros((canvas_edge,canvas_edge,3),np.uint8)

    #Getting the centering position
    ax,ay = (canvas_edge - screen.shape[1])//2,(canvas_edge - screen.shape[0])//2

    #Pasting the 'image' in a centering position
    canvas[ay:screen.shape[0]+ay,ax:ax+screen.shape[1]] = screen

    return canvas





def find_rotate_degree(img):
    '''
    find the exact degree to rotate the img with screen to  right
    algorithm:
    - use 3 point [-thres_num, 0, thres_num] to check the ratio 
    between contour_area and bounding_area
    and get the the best_point which correspoding to the highest ratio
    - continue to create 3 new point with half range as the previous still
    we get the correct degree
    '''
    screen = get_screen_with_canvas(img)
    screen = resize_img(screen, 600) # reduce size to reduce time
    thres_num = 45
    correct_deg = 0
    for i in range(0,15): # maximun number of bindary counting
        max_ratio = 0
        best_deg = 0
        check_points = [-thres_num , 0, thres_num]
        for deg in check_points:
            img = rotate_image(screen, deg)

            # calculate ratio
            ratio = find_correction_percentage(img)

            #print(ratio)
            if ratio>max_ratio:
                max_ratio = ratio
                best_deg = deg

        thres_num = thres_num/2
        screen = rotate_image(screen, best_deg)
        correct_deg +=best_deg
        #print(correct_deg)

    return round(correct_deg,4)


def find_correction_percentage(img):
    # calculate ratio
    screen_contour = find_screen_contour(img)
    contour_area = cv2.contourArea(screen_contour)
    x,y,w,h = cv2.boundingRect(screen_contour)
    bounding_area = w*h
    percentage = contour_area/bounding_area
    return round(percentage,4)






def get_screen(img):
    '''
    get screen image of the tool only
    '''
    #rotate_degree = find_rotate_degree(img)
    #img = rotate_image(get_screen_with_canvas(img), rotate_degree)

    # draw a bounding box
    screen_contour = find_screen_contour(img)
    img_with_screen_bounding_box = draw_bounding_box(img, screen_contour)

    x,y,w,h = cv2.boundingRect(screen_contour)
    screen = img[y:y+h, x:x+w]
    screen = resize_img(screen, SCREEN_WIDTH)
    return screen








def filter_red_box(img):
    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # select range of specific colors
    mask1 = cv2.inRange(hsv, (170, 200, 100), (179, 255, 255)) # dark red
    #mask2 = cv2.inRange(hsv, (0, 60, 50), (10, 255, 255)) # ligh red
    #mask = cv2.bitwise_or(mask1, mask2)
    mask = mask1
    # background white, foreground black
    inversed_mask = cv2.bitwise_not(mask)
    return inversed_mask


#img = cv2.imread('reference_box.png')
#img = filter_red_box(img)
#img_show('aaa',img)
#cv2.imwrite('check.png', img)
#exit()




   


def find_red_box_contours(img):
    dimensions = img.shape
    img_area = dimensions[0]*dimensions[1]
    img_frame_contour_area = (dimensions[0]-1)*(dimensions[1]-1)

    smallest_area = img_area/2222 # ratio when a box is acceptable
    result_contours = []


    # find all contours
    img = filter_red_box(img)
    contours = find_contours(img)

    # a list containing all contour centers
    centers = {'cx':[], 'cy':[]} 
    # loop through each contour, determine the red boxes
    for cnt in contours:
        # shape of contour
        approx = cv2.approxPolyDP(cnt, ARC_LENGTH_ADJUST*cv2.arcLength(cnt,True),True)
        # calculate area of contour
        area = cv2.contourArea(cnt)

        # if contour is rectangle 
        # and area is larger than minimun area then get the contour
        # and is the frame contour
        if len(approx)==4 and area>smallest_area and area!=img_frame_contour_area:

            # compute the center of the contour
            x,y,w,h = cv2.boundingRect(cnt)
            cx = int((x+w-1)/2)
            cy = int((y+h-1)/2)

            # check if contour having the same center as others => cancel
            if cx in centers['cx'] and cy in centers['cy']:
                pass
            else:
                result_contours.append(cnt)
                centers['cx'].extend(range(cx,cx+6))
                centers['cy'].extend(range(cy,cy+6))

    # sort the result contours by coordinate y
    result_contours = sorted(result_contours, key=lambda cnt: cv2.boundingRect(cnt)[1])
    return result_contours


#img = cv2.imread('reference_box.png')
#contours = find_red_box_contours(img)
#img = draw_all_contours(img, contours, 4, None)
#img_show('find_red_box_contours_187',img)
#exit()



from PIL import Image
from PIL import ImageFilter

def ocr_read(img):
    #start = time.time()
    if isinstance(img, str):
        img = cv2.imread(img)

    #img = cv2.resize(img, None, fx=0.75, fy=0.75)

    # sharpen
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    for i in range(0,3):
        im_pil = im_pil.filter(ImageFilter.SHARPEN);
        #im_pil.show();
    


    img = cv2.cvtColor(np.array(im_pil), cv2.COLOR_RGB2BGR)



    # Convert image to grayscale
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        print(e)
        pass

    

    # blur image to get text easier
    img = cv2.bilateralFilter(img,5,100,100)
    # threshold
    #img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #img_show('',img)

    img_show('img_name', img)

    # get text from image, use many different config to get the best result
    for config in ('--psm 3', '--psm 7', '--psm 8', '--psm 10'):
        text = pytesseract.image_to_string(img, config=config)
        if text!='': break

    # process text after to have unique format
    text = re.sub(r'^\|', '', text, flags=re.MULTILINE) # remove "|" at the beginning
    text = re.sub(r'\n+','\n',text) # replace many line feeds by one
    text = text.replace('“','"').replace('”','"')
    #text = text.replace('.','')
    #print(time.time()-start)
    return text





def post_process_compared_strings(text_cur, text_ref):
    curs = text_cur.split('\n')
    refs = text_ref.split('\n')

    # check and fix first character
    if text_cur!=text_ref:
        for i in range(0, len(refs)):
            if curs[i]!=refs[i] and len(curs)==len(refs):
                initial = refs[i][0]
                fix_initial_0 = curs[i]
                fix_initial_1 = initial + curs[i]
                fix_initial_2 = initial + curs[i][1:]
                fix_initial_3 = curs[i][1:]
                for fix_initial in (fix_initial_0, fix_initial_1, fix_initial_2, fix_initial_3):
                    final = refs[i][-1]
                    fix_final_0 = fix_initial
                    fix_final_1 = fix_initial + final
                    fix_final_2 = fix_initial[:-1] + final
                    fix_final_3 = fix_initial[:-1]
                    for fix_final in (fix_final_0, fix_final_1, fix_final_2, fix_final_3):
                        if fix_final==refs[i]:
                            curs[i] = fix_final
                            break

    text_cur='\n'.join(curs)
    # todo: kiểm tra dấu chấm cuối câu

    return text_cur, text_ref



#text_cur = 'his is an example\nan example is this'
#text_ref = 'this is an example\nan example is this.'
#text_cur, text_ref = post_process_compared_strings(text_cur, text_ref)
#print(text_cur)
#exit()




def compare_screens(cur_screen, 
                    ref_screen):
    # read current screen if a path is transfered
    if isinstance(cur_screen, str):
        cur_screen = cv2.imread(cur_screen)
        
    # read ref_screen if a path is transfered
    if isinstance(ref_screen, str):
        ref_screen = cv2.imread(ref_screen)
        
    cur_screen_root = cur_screen.copy()
    ref_screen_root = ref_screen.copy()

    # result
    results =[]
    contours = find_red_box_contours(ref_screen)
    #img_show('draw_all_contours', draw_all_contours(cur_screen.copy(),contours))

    result_flag = True
    for cnt in contours:
        #img_contour = cur_screen.copy()
        #cv2.drawContours(img_contour,[cnt],0,(0,0,255),2)
        #img_show('red box', resize_img(img_contour, 500))

        x,y,w,h = cv2.boundingRect(cnt)

        cur_crop = cur_screen_root[y:y+h, x:x+w]
        text_cur = ocr_read(cur_crop)
        #img_show('cur_crop',cur_crop)

        ref_crop = ref_screen_root[y:y+h, x:x+w]
        text_ref = ocr_read(ref_crop)
        #img_show('ref_crop',ref_crop)
        
        text_cur, text_ref = post_process_compared_strings(text_cur, text_ref)

        result = {}
        result['contour'] = cnt
        result['current text image'] = cur_crop
        result['reference text image'] = ref_crop
        result['current text'] = text_cur
        result['reference text'] = text_ref

        if text_cur == text_ref:
            #print('pass')
            result['status'] = 'Pass'
        else:
            result_flag = False
            result['status'] = 'Fail'
        results.append(result)

    return results





# => test function
def check_reference(fp):
    # load reference image => find all red rectangle contours
    ref_screen = cv2.imread(fp)
    ref_screen_root = ref_screen.copy()
    contours = find_red_box_contours(ref_screen)

    cnt_order = 0 # for ordering text objects
    result = fp + '\n\n' # text to print out

    # loop all contours
    for cnt in contours:
        cnt_order += 1
        x,y,w,h = cv2.boundingRect(cnt)
        ref_screen_with_contours = cv2.drawContours(ref_screen,[cnt],0,(0,255,0),2)
        ref_screen_with_contours = cv2.putText(ref_screen_with_contours, str(cnt_order), (x, y), 
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        crop = ref_screen_root[y:y+h, x:x+w]
        text = ocr_read(crop)
        result += '{ord}\n{text}\n\n'.format(ord=str(cnt_order),text=text) # add the text found and its object order to result
    
    # if there are no contours found => show the original image
    if 'ref_screen_with_contours' not in locals():
        ref_screen_with_contours = ref_screen
        result += 'NO RED RECTANGLES FOUND'

    # convert color and put img, text to the GUI
    ref_screen_with_contours = cv2.cvtColor(ref_screen_with_contours, cv2.COLOR_BGR2RGB)
    print(result)



def word_boxes():
    img = cv2.imread(r"reference\menu.png")
    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img) 
    print(boxes)
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    


if __name__ == '__main__':

    #img = capture_camera()
    #cur_screen = r"G:\Google Drive\3. Coding\Auto Test Tool Project\reference\demo\oil3.png"
    #result = check_reference(cur_screen)
    #print('result', result)
    word_boxes()
    exit()


