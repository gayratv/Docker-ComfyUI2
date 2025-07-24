import torch
import sys

print(torch.__version__, '+cu' + torch.version.cuda if torch.version.cuda else ' (CPU)')

print("python version:", sys.version.split()[0])
print("torch version:", torch.__version__)
print("cuda version (torch):", torch.version.cuda)
print("cuda available:", torch.cuda.is_available())
