import torch
torch.cuda.is_available()

# x = torch.rand(5, 3)
# print(x)

#####

import torch
import time

def sum_of_squares(start, end, device='cpu'):
    """
    Computes the sum of squares of numbers from start to end.
    Runs on either CPU or GPU (based on the `device` argument).

    Args:
    - start (int): starting number of the range.
    - end (int): ending number of the range.
    - device (str): 'cpu' or 'cuda'. Specifies the device to run on.

    Returns:
    - sum_of_squares (tensor): The computed sum of squares.
    """
    # Create a tensor of numbers in the range [start, end]
    numbers = torch.arange(start, end, device=device)
    
    # Compute sum of squares
    sum_of_squares = torch.sum(numbers ** 2)
    
    return sum_of_squares

def run_demo(start=0, end=100000000):
    """
    Runs the sum of squares demo on either CPU or GPU, and times the computation.
    """

    # Check if CUDA is available and select the device
    if torch.cuda.is_available():
        device = 'cuda'
        print(f"Running on GPU ({torch.cuda.get_device_name(0)})")
    else:
        device = 'cpu'
        print("Running on CPU")
    
    device='cpu'
    start_time = time.time()
    for i in range(1,100):
        result = sum_of_squares(start, end, device=device)
    elapsed_time = time.time() - start_time
    
    # Output results
    print(f"Sum of squares from {start} to {end}: {result.item()}")
    print(f"Elapsed time: {elapsed_time:.4f} seconds")

if __name__ == "__main__":
    run_demo()
