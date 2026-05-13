#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "conv.h"

// 定義輸出的維度，方便靜態陣列使用
#define OUT_SIZE (IMG_SIZE - KERNEL_SIZE + 1)

// 在嵌入式系統中，通常會預先分配好靜態記憶體 (Static Allocation)
// 使用 static 宣告在全域，避免佔用 stack 空間導致 overflow
static float input_buffer[CHANNELS * IMG_SIZE * IMG_SIZE];
static float weight_buffer[FILTERS * CHANNELS * KERNEL_SIZE * KERNEL_SIZE];
static float output_buffer[FILTERS * OUT_SIZE * OUT_SIZE];

void init_data(float* data, int size) {
    for (int i = 0; i < size; i++) {
        data[i] = (float)rand() / (float)RAND_MAX;
    }
}

int main() {
    printf("--- Low-Level CNN Inference Project (Static Memory Mode) ---\n");
    printf("Config: Input %dx%dx%d, Filters %d, Kernel %dx%d\n", 
           CHANNELS, IMG_SIZE, IMG_SIZE, FILTERS, KERNEL_SIZE, KERNEL_SIZE);
    
    int in_total = CHANNELS * IMG_SIZE * IMG_SIZE;
    int w_total = FILTERS * CHANNELS * KERNEL_SIZE * KERNEL_SIZE;

    // 初始化隨機資料
    srand(time(NULL));
    init_data(input_buffer, in_total);
    init_data(weight_buffer, w_total);

    printf("Starting baseline convolution...\n");
    clock_t start = clock();
    
    // 直接傳入靜態陣列的指標
    conv_baseline(input_buffer, weight_buffer, output_buffer);
    
    clock_t end = clock();
    
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Total parameter count: %d\n", w_total);
    printf("Baseline Execution Time: %f ms\n", time_spent * 1000);

    return 0;
}
