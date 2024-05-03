from openai import AzureOpenAI
import os
import requests
import json

import datetime




def Text_to_image(text,user_id):
    

    client = AzureOpenAI(
        api_version="api_version",  
        api_key="azure_openai_api_key",
        azure_endpoint = 'azure_endpoint'
        
    )



    result = client.images.generate(
        model="dalle_bot", 
        prompt=text,
        n=1
        
    )

    json_response = json.loads(result.model_dump_json())

    # Set the directory for the stored image
    image_dir = os.path.join(os.curdir, user_id)

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Initialize the image path (note the filetype should be png)
    image_path = os.path.join(image_dir, str(datetime.datetime.now()))

    # Retrieve the generated image
    image_url = json_response["data"][0]["url"]  # extract image URL from response
    generated_image = requests.get(image_url).content  # download the image
    with open(image_path, "wb") as image_file:
        image_file.write(generated_image)



    return image_path


