import os
import torch
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'
yolo_path = 'label_localization\yolov5_label_localization_runs'
best_weights = os.path.join(yolo_path, 'weights', 'best.pt')
localization_model = torch.hub.load('ultralytics/yolov5', 'custom', best_weights)

def ocr(image):
    
    '''
    Function to extract the text from the image
    '''
    return pytesseract.image_to_string(image)

def nutrition(text):
    '''
    Function to extract the nutrition facts from the text
    '''
    print(text)
    pass


def get_nutrition(img,confidence_threshold=0.1):
    
    '''
    Function to localize the labels in the image and extract nutrition facts
    '''
    output = localization_model(img)
    output_df = output.pandas().xyxy[0]
    
    cropped_images = []
    len = output_df.shape[0]
    
    for i in range(len):
        
        if output_df['confidence'][i] < confidence_threshold:
            
            output_df.drop(i, inplace=True)
            
        else:
            
            k = output_df.loc[i]
            x1,x2,y1,y2 = int(k['xmin']),int(k['xmax']),int(k['ymin']), int(k['ymax'])
            cropped_image = img[y1:y2,x1:x2]
            nutrition((ocr(cropped_image)))
            








