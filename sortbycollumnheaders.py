import csv
import sys

def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

def sort_csv_columns_based_on_header(csv_file_path):
    # Read the CSV file
    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        data = list(csv_reader)

    # Transpose the data
    transposed_data = transpose(data)

    # Sort the transposed data based on the values of the headers
    transposed_data_sorted = sorted(transposed_data, key=lambda x: x[0])

    # Transpose the sorted data back
    sorted_data = transpose(transposed_data_sorted)

    # Write back the sorted data to a new CSV file
    sorted_csv_file_path = csv_file_path.replace('.csv', '_sorted.csv')
    with open(sorted_csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(sorted_data)

    print(f"Sorted columns written to {sorted_csv_file_path}")

# Call the function to sort the columns based on the values of the headers
sort_csv_columns_based_on_header(sys.argv[1])
