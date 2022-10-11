#include <iostream>
#include <assert.h>
#include <cuda.h>
#include <cuda_runtime.h>

int main(void)
{
    CUresult a;
    CUcontext pctx;
    CUdevice device;
    cuInit(0);
    cuDeviceGet(&device, 0);
    std::cout << "DeviceGet : " << a << std::endl;
    cuCtxCreate(&pctx, CU_CTX_SCHED_AUTO, device ); // explicit context here
    std::cout << "CtxCreate : " << a << std::endl;
    assert(a == CUDA_SUCCESS);
    a = cuCtxPopCurrent(&pctx);
    std::cout << "cuCtxPopCurrent : " << a << std::endl;
    assert(a == CUDA_SUCCESS);
    std::cout << "Initialized CUDA" << std::endl;

    return 0;
}
