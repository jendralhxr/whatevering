// run it like: ./matrixmul 8192 10

#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <math.h>
#include <time.h> // For clock() on host, though we mainly rely on CUDA events

// Custom error checking function (replaces checkCudaErrors)
static void CheckCudaError(cudaError_t err, const char *file, int line) {
    if (err != cudaSuccess) {
        fprintf(stderr, "CUDA Error: %s in file %s at line %d\n", 
                cudaGetErrorString(err), file, line);
        exit(EXIT_FAILURE);
    }
}

// Macro to simplify calling the error check
#define CHECK_CUDA_ERROR(err) CheckCudaError(err, __FILE__, __LINE__)

// Define a default matrix size and iteration count
#define DEFAULT_N 1024
#define DEFAULT_ITERATIONS 10

// Define the thread block size
#define BLOCK_SIZE 32


// CUDA Kernel: Matrix multiplication C = A * B
// Each thread computes one element of the resulting matrix C(row, col)
__global__ void MatMulKernel(const float* A, const float* B, float* C, int n) {
    // Calculate the row and column index of the C element to be computed
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < n && col < n) {
        float sum = 0.0f;
        for (int k = 0; k < n; ++k) {
            // C[row][col] = sum(A[row][k] * B[k][col]) for k = 0 to n-1
            sum += A[row * n + k] * B[k * n + col];
        }
        C[row * n + col] = sum;
    }
}

// Main host function
int main(int argc, char *argv[]) {
    // --- 1. Parse Command-Line Arguments ---
    int N = DEFAULT_N;
    int iterations = DEFAULT_ITERATIONS;

    if (argc > 1) {
        N = atoi(argv[1]);
        if (N <= 0) {
            fprintf(stderr, "Invalid matrix size N. Using default: %d\n", DEFAULT_N);
            N = DEFAULT_N;
        }
    }
    if (argc > 2) {
        iterations = atoi(argv[2]);
        if (iterations <= 0) {
            fprintf(stderr, "Invalid iteration count. Using default: %d\n", DEFAULT_ITERATIONS);
            iterations = DEFAULT_ITERATIONS;
        }
    }

    long long size_bytes = (long long)N * N * sizeof(float);
    printf("--- CUDA Matrix Multiplication Benchmark ---\n");
    printf("Matrix Size (N): %d x %d\n", N, N);
    printf("Total Elements: %lld\n", (long long)N * N);
    printf("Iterations: %d\n", iterations);
    printf("Total Host Memory for one matrix: %.2f MB\n", (float)size_bytes / (1024.0f * 1024.0f));

    if (N % BLOCK_SIZE != 0) {
        fprintf(stderr, "Warning: N is not a multiple of BLOCK_SIZE (%d). Kernel padding is active.\n", BLOCK_SIZE);
    }

    float *h_A, *h_B, *h_C; // Host matrices
    float *d_A, *d_B, *d_C; // Device (GPU) matrices
    
    // --- 2. Host Memory Allocation and Initialization ---
    // Use calloc to initialize to zero and check for allocation failure
    h_A = (float*)calloc(N * N, sizeof(float));
    h_B = (float*)calloc(N * N, sizeof(float));
    h_C = (float*)calloc(N * N, sizeof(float));

    if (h_A == NULL || h_B == NULL || h_C == NULL) {
        fprintf(stderr, "Failed to allocate host memory (%.2f MB per matrix)!\n", (float)size_bytes / (1024.0f * 1024.0f));
        exit(EXIT_FAILURE);
    }

    // Initialize matrices A and B
    for (int i = 0; i < N * N; i++) {
        h_A[i] = 1.0f; 
        h_B[i] = 2.0f; 
    }

    // --- 3. Device Memory Allocation ---
    CHECK_CUDA_ERROR(cudaMalloc((void**)&d_A, size_bytes));
    CHECK_CUDA_ERROR(cudaMalloc((void**)&d_B, size_bytes));
    CHECK_CUDA_ERROR(cudaMalloc((void**)&d_C, size_bytes));

    // --- 4. Host to Device (H2D) Data Transfer (Only done once) ---
    CHECK_CUDA_ERROR(cudaMemcpy(d_A, h_A, size_bytes, cudaMemcpyHostToDevice));
    CHECK_CUDA_ERROR(cudaMemcpy(d_B, h_B, size_bytes, cudaMemcpyHostToDevice));
    
    // --- 5. Define Grid and Block Dimensions ---
    dim3 dimBlock(BLOCK_SIZE, BLOCK_SIZE);
    // Calculate the grid size needed to cover N x N elements
    dim3 dimGrid((N + dimBlock.x - 1) / dimBlock.x, 
                 (N + dimBlock.y - 1) / dimBlock.y);

    // --- 6. CUDA Event Setup for Timing ---
    cudaEvent_t start, stop;
    CHECK_CUDA_ERROR(cudaEventCreate(&start));
    CHECK_CUDA_ERROR(cudaEventCreate(&stop));
    
    // --- 7. Iterative Kernel Execution and Timing ---
    float totalTime_ms = 0;
    
    // Warm-up run (optional, but recommended for consistent timings)
    MatMulKernel<<<dimGrid, dimBlock>>>(d_A, d_B, d_C, N);
    CHECK_CUDA_ERROR(cudaGetLastError());
    CHECK_CUDA_ERROR(cudaDeviceSynchronize()); // Wait for warm-up to finish

    for (int i = 0; i < iterations; ++i) {
        // Record the start event
        CHECK_CUDA_ERROR(cudaEventRecord(start, 0)); 
        
        // Launch the CUDA Kernel
        MatMulKernel<<<dimGrid, dimBlock>>>(d_A, d_B, d_C, N);
        
        // Record the stop event
        CHECK_CUDA_ERROR(cudaEventRecord(stop, 0));

        // Wait for the stop event to complete
        CHECK_CUDA_ERROR(cudaEventSynchronize(stop)); 

        // Calculate the elapsed time for this iteration
        float elapsedTime_ms = 0;
        CHECK_CUDA_ERROR(cudaEventElapsedTime(&elapsedTime_ms, start, stop));
        totalTime_ms += elapsedTime_ms;
    }
    
    float averageTime_ms = totalTime_ms / iterations;

    printf("\n--- Results ---\n");
    printf("Average Kernel Execution Time over %d runs: %.3f ms\n", iterations, averageTime_ms);
    printf("-----------------\n");
    
    // --- 8. Device to Host (D2H) Data Transfer for verification ---
    CHECK_CUDA_ERROR(cudaMemcpy(h_C, d_C, size_bytes, cudaMemcpyDeviceToHost));

    // --- 9. Verification ---
    float expected = 2.0f * N;
    if (fabs(h_C[0] - expected) < 1e-5) {
        printf("Verification: PASS (Expected value: %.1f)\n", expected);
    } else {
        printf("Verification: FAIL (Example C[0] is %.1f, expected %.1f)\n", h_C[0], expected);
    }

    // --- 10. Cleanup ---
    cudaEventDestroy(start);
    cudaEventDestroy(stop);
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    free(h_A);
    free(h_B);
    free(h_C);

    return 0;
}
