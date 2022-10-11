#include <stdio.h>
#include <stdlib.h>

/* The calling function takes a single callback as a parameter. */
void PrintTwoNumbers(int (*numberSource)(void)) {
    int val1 = numberSource();
    int val2 = numberSource();
    int val3 = numberSource();
    int val4 = numberSource();
    printf("%d %d %d %d\n", val1, val2, val4, val3);
}

/* A possible callback */
int overNineThousand(void) {
    return (rand()%1000) + 9001;
}

/* Another possible callback. */
int meaningOfLife(void) {
    return 42;
}

/* Here we call PrintTwoNumbers() with three different callbacks. */
int main(void) {
    time_t t;
    srand((unsigned)time(&t)); // Init seed for random function
    PrintTwoNumbers(&rand);
    PrintTwoNumbers(&overNineThousand);
    PrintTwoNumbers(&meaningOfLife);
    return 0;
}