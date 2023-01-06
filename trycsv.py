import csv
import sys

steps= 60

x_start=0; y_start=4;
x_stop=200; y_stop=48;
x_interval= (x_stop-x_start)/steps
y_interval= (y_stop-y_start)/steps

f = open(sys.argv[1], 'w', newline='')

writer = csv.writer(f)
header= ['framenum','x1','x2','x3','x4','x5','x6','x7','x8','x9','x10']
writer.writerow(header);
writer.writerow(['cip', 'cup', 'cep', 'cop']);
writer.writerow(['cap', 'cip', 'cup', 'cep', 'cop']);
writer.writerow(['kepkop', 'cip', 'cup', 'cep', 'cop']);
writer.writerow(['cup', 'cep', 'cop']);

numlist= [];

for i in range(0,steps+1):
    numlist.append(i)
    print("{} - {}".format(x_start+ i*x_interval, y_start+i*y_interval))

writer.writerow(numlist);

