"""
The `Model` class is an interface between the ML model that you're packaging and the model
server that you're running it on.

The main methods to implement here are:
* `load`: runs exactly once when the model server is spun up or patched and loads the
   model onto the model server. Include any logic for initializing your model, such
   as downloading model weights and loading the model into memory.
* `predict`: runs every time the model server is called. Include any logic for model
  inference and return the model output.

See https://truss.baseten.co/quickstart for more.


Code done By AMEER AZAM
for more contact at https://linktr.ee/ameerazam22

"""
import base64
from PIL import Image
from io import BytesIO
from simple_lama_inpainting import SimpleLama
from PIL import Image

class Model:
    def __init__(self, **kwargs):
        #Basten Simple file 
        # Uncomment the following to get access
        # to various parts of the Truss config.
        # self._data_dir = kwargs["data_dir"]
        # self._config = kwargs["config"]
        # self._secrets = kwargs["secrets"]
        self.simple_lama = None 

    def load(self):
        # Load model here and assign to self._model.
        self.simple_lama = SimpleLama()


    def preprocess(self, request):
        encoded_image = request.get('input_img', None)
        encoded_mask = request.get('input_mask', None)
        print("Encoded image received:", encoded_image is not None)
        if encoded_image is not None or encoded_mask is None:
            try:
                image_data = base64.b64decode(encoded_image)
                input_img = Image.open(BytesIO(image_data))
                print("Input image loaded successfully:")

                mask_data = base64.b64decode(encoded_mask)
                mask_image = Image.open(BytesIO(mask_data))
                print("Input Mask loaded successfully:")
            except Exception as e:
                print("Error decoding or loading the image:", e)
                mask_image = None
        else:
            print("No image data found in the request.")
            input_img = None
            mask_image = None

        generate_args = {
            "input_img": input_img,
            "mask_img": mask_image,
        }
        print("Generate arguments:", generate_args)
        request["generate_args"] = generate_args
        return request

    def predict(self, request):
        # Run model inference here
        model_input = request.pop("generate_args")
        print("Model input received in predict method:", model_input)

        input_img = model_input['input_img']
        mask_img = model_input['mask_img']
        try:

            mask_img = mask_img.convert('L')
            result = self.simple_lama(input_img, mask_img)
            print("Lama done successfully.")
        except Exception as e:
            print("Error during model inference:", e)
            return {'error': str(e)}

        # Encode the images
        encoded_output_images = None
    
        try:
            buffered = BytesIO()
            result.save(buffered, format='PNG')
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            encoded_output_images = encoded_image

        except Exception as e:
            print(f"Error encoding image with label '{label}':", e)

        return {'output_images': encoded_output_images}
