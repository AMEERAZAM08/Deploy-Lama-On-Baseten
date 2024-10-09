import gradio as gr
import base64
import requests
import os 
from PIL import Image
from io import BytesIO


def process(input_image_editor):
    image = input_image_editor['background']
    mask = input_image_editor['layers'][0]
    lama_result = call_api(image, mask)
    return lama_result



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

MARKDOWN = """
# LAMA Inpainting API Baseten 🔥
"""


with gr.Blocks() as demo:
    gr.Markdown(MARKDOWN)
    with gr.Row():
        with gr.Column():
            input_image_editor_component = gr.ImageEditor(
                label='Image',
                type='pil',
                sources=["upload", "webcam"],
                image_mode='RGB',
                layers=False,
                brush=gr.Brush(colors=["#FFFFFF"], color_mode="fixed"))
            submit_button_component = gr.Button(
                    value='Submit', variant='primary', scale=0)
        with gr.Column():
            output_image_component = gr.Image(
                type='pil', image_mode='RGB', label='Generated image', format="png")

    submit_button_component.click(
        fn=process,
        inputs=[
            input_image_editor_component,
        ],
        outputs=[
            output_image_component,
        ]
    )

demo.launch(debug=False, show_error=True,share=True)