#include <iostream>
#include <vector>
#include <cuda_runtime.h>

// Kernel for Matrix Multiplication and Addition: D = (A * B) + C
__global__ void matMulAddKernel(float* A, float* B, float* C, float* D, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < N && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < N; k++) {
            sum += A[row * N + k] * B[k * N + col];
        }
        D[row * N + col] = sum + C[row * N + col];
    }
}

void runBenchmark(int N, int iterations) {
    size_t size = N * N * sizeof(float);

    // Host memory
    std::vector<float> h_A(N * N, 1.0f);
    std::vector<float> h_B(N * N, 2.0f);
    std::vector<float> h_C(N * N, 3.0f);
    std::vector<float> h_D(N * N, 0.0f);

    // Device memory
    float *d_A, *d_B, *d_C, *d_D;
    cudaMalloc(&d_A, size);
    cudaMalloc(&d_B, size);
    cudaMalloc(&d_C, size);
    cudaMalloc(&d_D, size);

    cudaMemcpy(d_A, h_A.data(), size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B.data(), size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_C, h_C.data(), size, cudaMemcpyHostToDevice);

    // Define grid and block size
    dim3 threadsPerBlock(16, 16);
    dim3 blocksPerGrid((N + threadsPerBlock.x - 1) / threadsPerBlock.x,
                       (N + threadsPerBlock.y - 1) / threadsPerBlock.y);

    // CUDA Events for timing
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    std::cout << "Starting benchmark: " << N << "x" << N << " matrix, " << iterations << " iterations..." << std::endl;

    cudaEventRecord(start);

    for (int i = 0; i < iterations; i++) {
        matMulAddKernel<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, d_D, N);
    }

    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);

    std::cout << "Total Time: " << milliseconds << " ms" << std::endl;
    std::cout << "Avg Time per Iteration: " << milliseconds / iterations << " ms" << std::endl;

    // Cleanup
    cudaFree(d_A); cudaFree(d_B); cudaFree(d_C); cudaFree(d_D);
    cudaEventDestroy(start); cudaEventDestroy(stop);
}

int main() {
    int matrixSize = 1024; // 1024x1024
    int iters = 1000;       // Number of loops
    
    runBenchmark(matrixSize, iters);
    
    return 0;
}