import torch

print("CUDA доступна:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
a = torch.randn(3, 3, device="cuda")
b = torch.randn(3, 3, device="cuda")
c = a @ b
print("Пример вычисления на GPU, c[0,0] =", c[0, 0].item())
