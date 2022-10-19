import os
import torch
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'
yolo_path = 'label_localization\yolov5_label_localization_runs'
best_weights = os.path.join(yolo_path, 'weights', 'best.pt')
localization_model = torch.hub.load('ultralytics/yolov5', 'custom', best_weights)

def nutrients(text):
    
    '''
    Function to extract the nutritients from text while iterating through it
    '''
    
    nutrition_dict = {
        'calories' : [],
        'total_fat' : [],
        'total_calories' : [],
        'total_carbs':[],
        'total_protein':[],
        'total_sugar':[],
        'sodium':[],
        'cholesterol':[],
        'total_fiber':[],
        'saturated_fat':[],
        'trans_fat':[],
        'sodium':[],
        'potassium':[]
        
    }
    text = text.split()
    for i in text:
        if i == 'calories':
            nutrition_dict['calories'] = text[text.index(i)+1]
            
        if i == 'total':
            if text[text.index(i)+1] == 'Fat':
                nutrition_dict['total_fat'] = text[text.index(i)+2]
                
            elif text[text.index(i)+1] == 'Carbohydrate':
                nutrition_dict['total_carbs'] = text[text.index(i)+2]
                
            elif text[text.index(i)+1] == 'Protein':
                nutrition_dict['total_protein'] = text[text.index(i)+2]
                
            elif text[text.index(i)+1] == 'Fiber':
                nutrition_dict['total_fiber'] = text[text.index(i)+2]
                
            elif text[text.index(i)+1] == 'sugars' or text[text.index(i)+1] == 'sugar':
                nutrition_dict['total_sugar'] = text[text.index(i)+2]
                
            elif text[text.index(i)+1] == 'Cholesterol':
                nutrition_dict['total_cholestrol'] = text[text.index(i)+2]
                
        if i == 'Cholesterol':
            nutrition_dict['cholesterol'] = text[text.index(i)+1]
            
        if i == 'Saturated':
            nutrition_dict['saturated_fat'] = text[text.index(i)+2]
            
        if i == 'Trans':
            nutrition_dict['trans_fat'] = text[text.index(i)+2]
            
        if i == 'Sodium':
            nutrition_dict['sodium'] = text[text.index(i)+1]
            
        if i == 'Potassium':
            nutrition_dict['potassium'] = text[text.index(i)+1]

    return nutrition_dict
            

def get_nutrition(img,confidence_threshold=0.1):
    
    '''
    Function to localize the labels in the image and extract nutrition facts
    '''
    
    output = localization_model(img)
    output_df = output.pandas().xyxy[0]
    output_df = output_df[output_df['confidence'] > confidence_threshold]
    len = output_df.shape[0]
    
    for i in range(len):

        bb = output_df.loc[i]
        x1,x2,y1,y2 = int(bb['xmin']), int(bb['xmax']), int(bb['ymin']), int(bb['ymax'])
        cropped_image = img[y1:y2,x1:x2]
        
        label_info = nutrients((pytesseract.image_to_string(cropped_image)))
            
# img = cv2.imread(r'food_viser\food_viser\nutrition-facts-label-download-image1.jpg')
# get_nutrition(img)         








