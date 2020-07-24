import json
import pandas as pd
import io
import glob
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models

#This method takes the image data in bytes
#and applies a series of ‘transform’ functions on it and returns a tensor
def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

# define the function to get the class predicted of image
# it takes the parameter: image path and provide the output as the predicted class
def get_category(model, imagenet_class_mapping, image_path):
    # read the image in binary form
    with open(image_path, 'rb') as file:
        image_bytes = file.read()
    # transform the image
    transformed_image = transform_image(image_bytes=image_bytes)
    # use the model to predict the class
    outputs = model.forward(transformed_image)
    
    _, category = outputs.max(1)
    # return the value,get a python number from a tensor
    predicted_idx = str(category.item())
    return imagenet_class_mapping[predicted_idx]
    #get_category(image_path='static/sample_1.jpeg')
    #['n02089973', 'English_foxhound']

def get_prediction(model, imagenet_class_mapping, path_to_directory):
    #return file list in the directory
    files = glob.glob(path_to_directory+'/*')
    image_with_tags = {}
    for image_file in files:
        image_with_tags[image_file] = get_category(model, imagenet_class_mapping, image_path=image_file)[1]
    return image_with_tags

#image_with_tags = {"../static/URL_https:.../1.jpeg":"English foxhound"}