#include <iostream>
#include <assert.h>
#include "/usr/local/cuda/include/cuda.h"
#include "/usr/local/cuda/include/cuda_runtime.h"

int main(void)
{
    CUresult a;
    CUcontext pctx;
    cudaSetDevice(0); // runtime API creates context here
    a = cuCtxGetCurrent(&pctx);
    std::cout << "GetContext : " << a << std::endl;
    assert(a == CUDA_SUCCESS);
    a = cuCtxPopCurrent(&pctx);
    std::cout << "cuCtxPopCurrent : " << a << std::endl;
    assert(a == CUDA_SUCCESS);
    std::cout << "Initialized CUDA" << std::endl;

    return 0;
}
