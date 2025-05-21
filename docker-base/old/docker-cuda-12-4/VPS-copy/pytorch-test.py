import torch

print("CUDA доступен:", torch.cuda.is_available())
print("cuDNN доступен:", torch.backends.cudnn.enabled)
print("Версия cuDNN:", torch.backends.cudnn.version())
print("Версия torch:",torch.__version__)