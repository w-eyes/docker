import torch
import time

if torch.cuda.is_available():
    dtype = torch.float16
    device = 'cuda'
    a = torch.randn(4096, 4096, dtype=dtype, device=device)
    b = torch.randn(4096, 4096, dtype=dtype, device=device)
    torch.cuda.synchronize()
    start = time.time()
    c = a @ b
    torch.cuda.synchronize()
    print('Tensor Core time:', time.time() - start)
else:
    print('CUDA not available!')

print(''' 
 
 Must be small

''')