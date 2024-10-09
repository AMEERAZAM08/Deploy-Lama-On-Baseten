import base64
import requests
import os 
from PIL import Image

from io import BytesIO
def encode_image_to_base64(pil_image):
    """Encodes a PIL image to base64 format."""
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def call_api(image, mask):
    # Paths to your input image and mask image
    # Encode the images in base64
    encoded_input_image = encode_image_to_base64(image)
    encoded_mask_image = encode_image_to_base64(mask)

    # Prepare the payload for the POST request
    payload = {
        'input_img': encoded_input_image,
        'input_mask': encoded_mask_image
    }

    basten_url= os.getenv("url")
    BASTEN_KEY = os.getenv("KEY")

    response = requests.post(
        basten_url,
        headers={"Authorization": f"Api-Key {BASTEN_KEY}"},
        json=payload,
    )

    print("response ",response)

    # Print the server's response
    if response.status_code == 200:
        result = response.json()
        output_images = result.get('output_images')
        # Each output image is in base64 format, decode and save it
        output_image_data = base64.b64decode(output_images)
        output_image = Image.open(BytesIO(output_image_data))
        return output_image
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Error message: {response.text}")
        return None


input_image = Image.open("./input_image.png")
input_mask = Image.open("./mask_image.png")

lama_result = call_api(input_image, input_mask)

lama_result.save("lama_output.png")
