# importing required libraries
import requests
from bs4 import BeautifulSoup
import os
import time

def get_directory(url):
    return "URL_" + str(url.replace("/","_"))

#return the path of folder created for scraped URL
def get_path(url):
    return "static/URL_" + str(url.replace("/","_"))


headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }

# define the function to scrape images and store it in a directory
def get_images(url):
    # get the directory path
    path = get_path(url)
    try:
        os.mkdir(path)
    except:
        pass
    # request the source code from the URL
    response = requests.request("GET", url, headers=headers)
    # parse the data through the Beautiful Soup
    data = BeautifulSoup(response.text, 'html.parser')
    # find the image tag in the source code
    images = data.find_all('img', src=True)
    print('Number of Images: ', len(images))
    # select src tag: extract the source from all the image tags
    image_src = [x['src'] for x in images]
    # select only jpeg format images
    image_src = [x for x in image_src if x.endswith('.jpeg') ]
    image_count = 1
    # store the image in the specified directory
    for image in image_src:
        print(image)
        image_file_name = path+'/'+str(image_count)+'.jpeg' 
        print(image_file_name)
        # open the file in write binary form and add the image content to store it
        with open(image_file_name, 'wb') as f:
            res = requests.get(image)
            f.write(res.content)
        image_count = image_count+1

