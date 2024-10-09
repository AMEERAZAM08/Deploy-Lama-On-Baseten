import base64
import requests

# Function to encode an image file to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# Paths to your input image and mask image
input_image_path = "./input_image.png"
input_mask_path = "./mask_image.png"

# Encode the images in base64
encoded_input_image = encode_image_to_base64(input_image_path)
encoded_mask_image = encode_image_to_base64(input_mask_path)

# Prepare the payload for the POST request
payload = {
    'input_img': encoded_input_image,
    'input_mask': encoded_mask_image
}

# URL of the model server (replace with your actual endpoint)
url = 'http://your-model-server-url/predict'




# Send the POST request
payload

response = requests.post(
    basten_url,
    headers={"Authorization": f"Api-Key {BASTEN_KEY}"},
    json=payload,
)

print("response ",response)

# Print the server's response
if response.status_code == 200:
    result = response.json()
    output_images = result.get('output_images', [])
    for idx, output in enumerate(output_images):
        # Each output image is in base64 format, decode and save it
        output_image_data = base64.b64decode(output['lama_result'])
        output_image_path = f"lama_output_{idx}.png"
        with open(output_image_path, "wb") as output_file:
            output_file.write(output_image_data)
        print(f"Output image saved to {output_image_path}")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(f"Error message: {response.text}")
