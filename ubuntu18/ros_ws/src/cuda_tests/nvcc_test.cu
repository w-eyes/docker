//nvidia-toolkit need to be installed
//run^
//RUN: nvcc nvcc_test.cu -o test && ./nvcc_test 

#include <stdio.h>
#include <cuda_runtime.h>

__global__ void kernel() {
    printf("Hello from GPU thread %d!\n", threadIdx.x);
}

int main() {
    kernel<<<1, 5>>>();
    cudaDeviceSynchronize();
    return 0;
}