import os
import torch
import cv2
import  easyocr, pytesseract

yolo_path = 'label_localization\yolov5_label_localization_runs'
best_weights = os.path.join(yolo_path, 'weights', 'best.pt')
localization_model = torch.hub.load('ultralytics/yolov5', 'custom', best_weights)

reader = easyocr.Reader(['en'], gpu=False)
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'

def extract_nutrients(text):
    
    '''
    Function to extract the nutritients from text while iterating through it
    '''
    
    nutrition_dict = {
        'calories' : [],'total_fat' : [],
        'total_carbs':[],'protein':[],
        'total_sugar':[],'sodium':[],
        'cholesterol':[],'fiber':[],
        'saturated_fat':[],'trans_fat':[],
        'sodium':[],'potassium':[]
    }

    text = text.lower()
    text = text.split()

    for j,i in enumerate(text):
        
        if i == 'calories':
            nutrition_dict['calories'] = text[text.index(i)+1]
            
        elif i == 'total':
            if text[j+1] == 'fat':
                nutrition_dict['total_fat'] = text[j+2]
                
            elif text[j+1] == 'carbohydrate' or text[j+1] == 'carbohydrates':
                nutrition_dict['total_carbs'] = text[j+2]
                
            elif text[j+1] == 'fiber':
                nutrition_dict['fiber'] = text[j+2]
                
            elif text[j+1] == 'sugars' or text[j+1] == 'sugar':
                nutrition_dict['total_sugar'] = text[j+2]
                
            elif text[j+1] == 'cholesterol':
                nutrition_dict['total_cholestrol'] = text[j+2]
                
        elif i == 'cholesterol':
            nutrition_dict['cholesterol'] = text[j+1]
            
        elif i == 'saturated':
            nutrition_dict['saturated_fat'] = text[j+2]
            
        elif i == 'trans':
            nutrition_dict['trans_fat'] = text[j+2]
            
        elif i == 'sodium':
            nutrition_dict['sodium'] = text[j+1]
            
        elif i == 'potassium':
            nutrition_dict['potassium'] = text[j+1]
            
        elif i == 'dietary':
            nutrition_dict['fiber'] = text[j+2]
        
        elif i == 'fiber':
            nutrition_dict['fiber'] = text[j+1]
            
        elif i == 'protein':
            nutrition_dict['protein'] = text[j+1]
            
        elif i == 'sugars' or i == 'sugar':
            if nutrition_dict['total_sugar'] == []:
                nutrition_dict['total_sugar'] = text[j+1]
                
    return nutrition_dict

def nutrients_recognition(img,method = 'easyocr'):
    
    '''
    Function to recognize the text in the image and extract the nutrition facts
    '''
    
    if(method == 'easyocr'):
        detections = reader.readtext(img)
        
        text = ""
        for i in detections:
            text += i[1] + " "
            
        return extract_nutrients(text)
    
    elif(method == 'pytesseract'):
        return extract_nutrients(pytesseract.image_to_string(img))
            
def get_nutrition(img,confidence_threshold=0.1,ocr = 'easyocr'):
    
    '''
    Function to localize the labels in the image and extract nutrition facts
    '''
    
    nutrients_list = []
    output = localization_model(img)
    output_df = output.pandas().xyxy[0]
    output_df = output_df[output_df['confidence'] > confidence_threshold]
    len = output_df.shape[0]
    
    for i in range(len):

        bb = output_df.loc[i]
        x1,x2,y1,y2 = int(bb['xmin']), int(bb['xmax']), int(bb['ymin']), int(bb['ymax'])
        cropped_image = img[y1:y2,x1:x2]
        
        label_info = nutrients_recognition(cropped_image,method = ocr)
        nutrients_list.append(label_info)
    
    return nutrients_list
            
img = cv2.imread(r'food_viser\static\images\label_examples\nutrition-facts-label-download-image1.jpg')
list = get_nutrition(img,ocr = 'easyocr')
print(list)