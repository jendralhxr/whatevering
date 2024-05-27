def find_peaks(arr, threshold):
    peaks = []
    for i in range(1, len(arr) - 1):
        if arr[i] > arr[i - 1] and arr[i] > arr[i + 1] and arr[i] > threshold:
            peaks.append((i, arr[i]))
    return peaks

# Example usage:
arr = [1.5, 2.0, 1.8, 3.2, 2.7, 2.9, 2.6, 1.2]
threshold = 2.5
peaks = find_peaks(arr, threshold)
print("Peaks found at indices and values above threshold:", peaks)


def f(x):
    # Define your function here
    return x**2 - 4*x + 3  # Example function: f(x) = x^2 - 4x + 3

def find_minimum():
    left, right = -5, 5  # Define the range to search within
    epsilon = 1e-6  # Define the desired precision

    while abs(right - left) > epsilon:
        mid1 = left + (right - left) / 3
        mid2 = right - (right - left) / 3

        if f(mid1) < f(mid2):
            right = mid2
        else:
            left = mid1

    min_x = (left + right) / 2
    min_value = f(min_x)
    
    # Print the minimum value and corresponding x
    print("Minimum value:", min_value)
    print("Corresponding x:", min_x)

# Call the function to find the minimum
find_minimum()


--------

def f(x):
    # Define your function here
    return x**2 - 4*x + 3  # Example function: f(x) = x^2 - 4x + 3

def find_minimum():
    min_value = float('inf')  # Initialize min_value to positive infinity
    min_x = None  # Initialize min_x as None
    
    # Iterate over the range of x values from -5 to 5
    for x in range(-5, 6):
        # Evaluate the function at the current x value
        fx = f(x)
        
        # Check if the current function value is less than the minimum found so far
        if fx < min_value:
            min_value = fx  # Update min_value
            min_x = x  # Update min_x
    
    # Print the minimum value and corresponding x
    print("Minimum value:", min_value)
    print("Corresponding x:", min_x)

# Call the function to find the minimum
find_minimum()




