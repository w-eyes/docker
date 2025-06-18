import torch
import time

# Создаем большой тензор
x = torch.randn(10000, 10000)

# Вычисляем на CPU
start_time = time.time()
y_cpu = x @ x
print('CPU time:', time.time() - start_time)

# Переносим данные на GPU (если CUDA доступна)
if torch.cuda.is_available():
    x_gpu = x.cuda()
    start_time = time.time()
    y_gpu = x_gpu @ x_gpu
    print('GPU time:', time.time() - start_time)
else:
    print('CUDA not available!')


print(''' 
NOTE! GPU time must be lower than CPU

''')