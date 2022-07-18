#include <stdio.h>

class Node {
    public:
        int test_num;
};

int generate_maze(int width, int height, int cycles) {
    int* nodes = new int [width * height];
    delete[] nodes;
    return 0;
}

int main(int argc, char* argv[]) {
    fprintf(stdout, "Hello World\n");
    generate_maze(10, 10, 0);
    return 0;
}

// TODO: actually implement this bad boy
// TODO: get some cpp extensions