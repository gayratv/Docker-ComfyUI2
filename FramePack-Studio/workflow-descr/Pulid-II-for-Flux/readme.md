https://www.patreon.com/posts/forget-loras-ii-120974622

git clone https://github.com/lldacing/ComfyUI_PuLID_Flux_ll.git || true

# Download PuLID model
curl -L -o "$PULID_MODEL_DIR/pulid_flux_v0-9-1.safetensors" "https://huggingface.co/guozinan/PuLID/resolve/main/pulid_flux_v0.9.1.safetensors?download=true"
https://huggingface.co/guozinan/PuLID/

# Download and extract Antelopev2 model
tmp_zip="/tmp/antelopev2.zip"
curl -L -o "$tmp_zip" "https://huggingface.co/MonsterMMORPG/tools/resolve/main/antelopev2.zip"
unzip -o "$tmp_zip" -d "$INSIGHTFACE_DIR"
https://huggingface.co/MonsterMMORPG/tools/




Hello, I can't find
flux-canny-controlnet-v3.safetensors
depth_anything_vitl14.pth
FLUX\REAL\amateurphotov2.safetensors

12gb
models / diffusion_models
https://huggingface.co/OreX/ControlNet/resolve/main/FLUX%20ControlNet/Flux-Tools-Canny/flux1-canny-dev-FP8.safetensors
https://huggingface.co/OreX/ControlNet/resolve/main/FLUX%20ControlNet/Flux-Tools-Depth/flux1-depth-dev-FP8.safetensors
