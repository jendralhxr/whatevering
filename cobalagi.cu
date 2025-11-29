#include <iostream>
#include <chrono>
#include <cuda_runtime.h>

struct LongLong {
    int low;
    int high;
};

// Kernel to accumulate sum of squares into two 32-bit parts (low and high)
__device__ void atomicAddLongLong(LongLong* address, long long value) {
    // Split value into high and low 32-bit parts
    int low_part = static_cast<int>(value & 0xFFFFFFFF);
    int high_part = static_cast<int>(value >> 32);

    // Add low part using atomic add
    atomicAdd(&(address->low), low_part);

    // Add high part using atomic add
    atomicAdd(&(address->high), high_part);
}

// Kernel to compute the sum of squares
__global__ void sum_of_squares_kernel(int* d_numbers, LongLong* d_result, int start, int end) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (idx >= start && idx < end) {
        int val = d_numbers[idx];
        long long square = (long long)(val) * val;
        atomicAddLongLong(d_result, square);  // Use atomicAddLongLong for 64-bit accumulation
    }
}

long long sum_of_squares_cpu(int start, int end) {
    long long result = 0;
    for (int i = start; i < end; i++) {
        result += (long long)i * i;
    }
    return result;
}

void run_demo(int start = 0, int end = 1000000) {
    // Measure the time for the CPU version
    auto start_time = std::chrono::high_resolution_clock::now();
    long long cpu_result=0;
	for (int i = start; i < 1000; i++) {
    	long long cpu_result = sum_of_squares_cpu(start, end);
		}
	auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed_cpu = end_time - start_time;
    std::cout << "CPU Result: " << cpu_result << "\n";
    std::cout << "Elapsed Time (CPU): " << elapsed_cpu.count() << " seconds\n";

    // Now, measure the time for the GPU version (only if CUDA is available)
    int* d_numbers;
    LongLong* d_result;
    int num_elements = end - start;
    size_t size = num_elements * sizeof(int);

    // Allocate memory on the device
    cudaMalloc(&d_numbers, size);
    cudaMalloc(&d_result, sizeof(LongLong));

    // Initialize result on the device to zero
    cudaMemset(d_result, 0, sizeof(LongLong));

    // Copy the numbers from the host to the device
    int* h_numbers = new int[num_elements];
    for (int i = 0; i < num_elements; i++) {
        h_numbers[i] = start + i;
    }
    cudaMemcpy(d_numbers, h_numbers, size, cudaMemcpyHostToDevice);

    // Launch the kernel
    int blockSize = 256;  // Number of threads per block
    int numBlocks = (num_elements + blockSize - 1) / blockSize;
    
    start_time = std::chrono::high_resolution_clock::now();
    for (int i = start; i < 1000; i++) {
    	sum_of_squares_kernel<<<numBlocks, blockSize>>>(d_numbers, d_result, start, end);
    }
    // Check for kernel launch errors
    cudaDeviceSynchronize();
    
    // Copy the result back to the host
    LongLong gpu_result;
    cudaMemcpy(&gpu_result, d_result, sizeof(LongLong), cudaMemcpyDeviceToHost);

    // Combine the low and high parts into a 64-bit result
    long long final_gpu_result = static_cast<long long>(gpu_result.high) << 32 | (gpu_result.low & 0xFFFFFFFF);

    // Measure elapsed time for the GPU computation
    end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed_gpu = end_time - start_time;

    std::cout << "GPU Result: " << final_gpu_result << "\n";
    std::cout << "Elapsed Time (GPU): " << elapsed_gpu.count() << " seconds\n";

    // Free device memory
    cudaFree(d_numbers);
    cudaFree(d_result);

    delete[] h_numbers;
}

int main() {
    // Call the demo
    run_demo();
    return 0;
}
