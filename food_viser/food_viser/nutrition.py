import os
import cv2
import easyocr
import pytesseract
import torch

yolo_path = '..\label_localization\yolov5_label_localization_runs'
best_weights = os.path.join(yolo_path, 'weights', 'best.pt')
localization_model = torch.hub.load('ultralytics/yolov5', 'custom', best_weights, force_reload=True)

reader = easyocr.Reader(['en'], gpu=False)


# pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'

def nutrients_classifier(nutrition_dict):
    """
    Function to classify the amount of nutrients as healthy or not
    """

    class_dict = {
        'cal': [], 'fat': [],
        'carbs': [], 'sugars': [],
        'cholesterol': []
    }
    total_fat, saturated_fat, sugar = 0, 0, 0

    for nutrient in nutrition_dict.keys():
        val = nutrition_dict[nutrient]
        if not val:
            nutrition_dict[nutrient] = 0.0

        else:
            if val.endswith('g') or val.endswith('9'):
                val = val[:-1]

                if val.endswith('m'):
                    val = val[:-1]
                    if val == 'o' or val == 'O':
                        val = 0.0
                    else:
                        val = float(val) * 1000

                else:
                    if val == 'o' or val == 'O':
                        val = 0.0
                    else:
                        val = float(val)

            val = float(val)

            if nutrient == 'calories':
                val = val / 9
                if val > 100:
                    val = 100
                class_dict['cal'] = val

            elif nutrient == 'total_fat':
                total_fat = val

            elif nutrient == 'total_carbs':
                class_dict['carbs'] = val

            elif nutrient == 'fiber':
                class_dict['carbs'] -= val

            elif nutrient == 'saturated_fat':
                saturated_fat = val

            elif nutrient == 'trans_fat':
                continue

            elif nutrient == 'total_sugar':
                sugar = val

            elif nutrient == 'protein':
                class_dict['carbs'] -= val

            elif nutrient == 'sodium':
                val = val / 2.5
                if val > 100:
                    val = 100
                class_dict['sodium'] = val

            elif nutrient == 'potassium':
                val = val / 5
                if val > 100:
                    val = 100
                class_dict['potassium'] = val

            elif nutrient == 'cholesterol':
                val = val / 300
                if val > 100:
                    val = 100
                class_dict['cholesterol'] = val

    total_fat = (total_fat - 3.0) * 8
    saturated_fat = ((saturated_fat - 1.5) * 1000) / 350

    if total_fat > 100:
        total_fat = 100

    if saturated_fat > 100:
        saturated_fat = 100
    class_dict['fat'] = (total_fat + saturated_fat) / 2
    sugar = ((sugar - 5) * 1000) / 175

    if sugar > 100:
        sugar = 100

    class_dict['sugars'] = sugar
    carbs = class_dict['carbs']
    carbs = (carbs - 20) * 100

    if carbs > 100:
        carbs = 100
    class_dict['carbs'] = carbs

    return class_dict


def extract_nutrients(text):
    """
    Function to extract the nutrients from text while iterating through it
    """

    nutrition_dict = {
        'calories': [], 'total_fat': [],
        'total_carbs': [], 'protein': [],
        'total_sugar': [], 'cholesterol': [], 'fiber': [],
        'saturated_fat': [], 'trans_fat': [],
        'sodium': [], 'potassium': []
    }

    text = text.lower()
    text = text.split()

    for j, i in enumerate(text):

        if i == 'calories':
            nutrition_dict['calories'] = text[text.index(i) + 1]

        elif i == 'total':
            if text[j + 1] == 'fat':
                nutrition_dict['total_fat'] = text[j + 2]

            elif text[j + 1] == 'carbohydrate' or text[j + 1] == 'carbohydrates':
                nutrition_dict['total_carbs'] = text[j + 2]

            elif text[j + 1] == 'fiber':
                nutrition_dict['fiber'] = text[j + 2]

            elif text[j + 1] == 'sugars' or text[j + 1] == 'sugar':
                nutrition_dict['total_sugar'] = text[j + 2]

            elif text[j + 1] == 'cholesterol':
                nutrition_dict['total_cholestrol'] = text[j + 2]

        elif i == 'cholesterol':
            nutrition_dict['cholesterol'] = text[j + 1]

        elif i == 'saturated':
            nutrition_dict['saturated_fat'] = text[j + 2]

        elif i == 'trans':
            nutrition_dict['trans_fat'] = text[j + 2]

        elif i == 'sodium':
            nutrition_dict['sodium'] = text[j + 1]

        elif i == 'potassium':
            nutrition_dict['potassium'] = text[j + 1]

        elif i == 'dietary':
            nutrition_dict['fiber'] = text[j + 2]

        elif i == 'fiber':
            nutrition_dict['fiber'] = text[j + 1]

        elif i == 'protein':
            nutrition_dict['protein'] = text[j + 1]

        elif i == 'sugars' or i == 'sugar':
            if not nutrition_dict['total_sugar']:
                nutrition_dict['total_sugar'] = text[j + 1]

    return nutrients_classifier(nutrition_dict)


def nutrients_recognition(img, method='easyocr'):
    """
    Function to recognize the text in the image and extract the nutrition facts
    """

    if method == 'easyocr':
        detections = reader.readtext(img)

        text = ""
        for i in detections:
            text += i[1] + " "

        return extract_nutrients(text)

    elif method == 'pytesseract':
        return extract_nutrients(pytesseract.image_to_string(img))


def get_nutrition(img, confidence_threshold=0.1, ocr='easyocr'):
    """
    Function to localize the labels in the image and extract nutrition facts
    """

    nutrients_list = []
    output = localization_model(img)
    output_df = output.pandas().xyxy[0]
    output_df = output_df[output_df['confidence'] > confidence_threshold]
    len = output_df.shape[0]

    for i in range(len):
        bb = output_df.loc[i]
        x1, x2, y1, y2 = int(bb['xmin']), int(bb['xmax']), int(bb['ymin']), int(bb['ymax'])
        cropped_image = img[y1:y2, x1:x2]

        label_info = nutrients_recognition(cropped_image, method=ocr)
        nutrients_list.append(label_info)

    return nutrients_list


if __name__ == '__main__':
    img = cv2.imread(r'food_viser\static\images\label_examples\nutrition-facts-label-download-image1.jpg')
    list = get_nutrition(img, ocr='easyocr')
    print(list)
