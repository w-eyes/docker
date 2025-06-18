import torch
print('PyTorch version:', torch.__version__)
print('CUDA available:', torch.cuda.is_available())
print('CUDA device count:', torch.cuda.device_count())
print('Current CUDA device:', torch.cuda.current_device())
print('Device name:', torch.cuda.get_device_name(0))

print(''' 
NOTE! Expected:

PyTorch version: 1.7.1+cu110
CUDA available: True
CUDA device count: 1
Current CUDA device: 0
Device name: NVIDIA GeForce RTX 4090

''')