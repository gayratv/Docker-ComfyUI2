# check_cuda.py
import torch

def check_cuda():
    available = torch.cuda.is_available()
    print("CUDA доступна:" , available)
    if not available:
        return

    num = torch.cuda.device_count()
    print("Количество устройств CUDA:", num)
    for i in range(num):
        name = torch.cuda.get_device_name(i)
        props = torch.cuda.get_device_properties(i)
        print(f"Устройство {i} — {name}, память: {props.total_memory/1024**3:.1f} GB")

    # небольшая проверка вычислений на GPU
    a = torch.randn(5, 5, device="cuda")
    b = torch.randn(5, 5, device="cuda")
    c = a @ b  # матричное умножение на GPU
    print("Результат вычисления на GPU:", c[0,0].item())

if __name__ == "__main__":
    check_cuda()
