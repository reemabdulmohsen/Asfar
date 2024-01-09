import torch
from diffusers import DiffusionPipeline
import cv2

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float32, use_safetensors=True, variant="fp16")


def getImage(prompt):
    # Can be set to 1~50 steps. LCM support fast inference even <= 4 steps. Recommend: 1~8 steps.
    num_inference_steps = 4

    images = pipe(prompt=prompt, num_inference_steps=num_inference_steps, guidance_scale=8.0, output_type="pil").images[0]

    images.save("image.png")
    img = cv2.imread("image.png")
    print(img.shape)
    img = cv2.resize(img, (1350, 1000))
    print(img.shape)
    cv2.imwrite("image.png", img)
    return images[0]


