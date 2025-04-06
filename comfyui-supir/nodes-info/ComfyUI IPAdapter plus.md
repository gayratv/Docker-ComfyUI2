https://github.com/cubiq/ComfyUI_IPAdapter_plus

/ComfyUI/models/clip_vision
![Снимок экрана 2025-04-03 133622.png](assets/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-04-03%20133622.png)


/ComfyUI/models/clip_vision
CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors, download and rename
https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors
CLIP-ViT-bigG-14-laion2B-39B-b160k.safetensors, download and rename
https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/image_encoder/model.safetensors
clip-vit-large-patch14-336.bin, download and rename only for Kolors models
https://huggingface.co/Kwai-Kolors/Kolors-IP-Adapter-Plus/resolve/main/image_encoder/pytorch_model.bin

/ComfyUI/models/ipadapter, create it if not present
ip-adapter_sd15.safetensors, Basic model, average strength
ip-adapter_sd15_light_v11.bin, Light impact model
ip-adapter-plus_sd15.safetensors, Plus model, very strong
ip-adapter-plus-face_sd15.safetensors, Face model, portraits
ip-adapter-full-face_sd15.safetensors, Stronger face model, not necessarily better
ip-adapter_sd15_vit-G.safetensors, Base model, requires bigG clip vision encoder
ip-adapter_sdxl_vit-h.safetensors, SDXL model
ip-adapter-plus_sdxl_vit-h.safetensors, SDXL plus model
ip-adapter-plus-face_sdxl_vit-h.safetensors, SDXL face model
ip-adapter_sdxl.safetensors, vit-G SDXL model, requires bigG clip vision encoder

<ul dir="auto">
<li><a href="https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15.safetensors" rel="nofollow">ip-adapter_sd15.safetensors</a>, Basic model, average strength</li>
<li><a href="https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15_light_v11.bin" rel="nofollow">ip-adapter_sd15_light_v11.bin</a>, Light impact model</li>
<li><a href="https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.safetensors" rel="nofollow">ip-adapter-plus_sd15.safetensors</a>, Plus model, very strong</li>
<li><a href="https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus-face_sd15.safetensors" rel="nofollow">ip-adapter-plus-face_sd15.safetensors</a>, Face model, portraits</li>
<li><a href="https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-full-face_sd15.safetensors" rel="nofollow">ip-adapter-full-face_sd15.safetensors</a>, Stronger face model, not necessarily better</li>
<li><a href="https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15_vit-G.safetensors" rel="nofollow">ip-adapter_sd15_vit-G.safetensors</a>, Base model, <strong>requires bigG clip vision encoder</strong></li>
<li><a href="https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter_sdxl_vit-h.safetensors" rel="nofollow">ip-adapter_sdxl_vit-h.safetensors</a>, SDXL model</li>
<li><a href="https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors" rel="nofollow">ip-adapter-plus_sdxl_vit-h.safetensors</a>, SDXL plus model</li>
<li><a href="https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors" rel="nofollow">ip-adapter-plus-face_sdxl_vit-h.safetensors</a>, SDXL face model</li>
<li><a href="https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter_sdxl.safetensors" rel="nofollow">ip-adapter_sdxl.safetensors</a>, vit-G SDXL model, <strong>requires bigG clip vision encoder</strong></li>
<li><strong>Deprecated</strong> <a href="https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15_light.safetensors" rel="nofollow">ip-adapter_sd15_light.safetensors</a>, v1.0 Light impact model</li>
</ul>