#include "conv.h"

void conv_baseline(float* in, float* weight, float* out) {
    int out_size = IMG_SIZE - KERNEL_SIZE + 1;
    
    for (int f = 0; f < FILTERS; f++) {
        for (int h = 0; h < out_size; h++) {
            for (int w = 0; w < out_size; w++) {
                float sum = 0;
                for (int c = 0; c < CHANNELS; c++) {
                    for (int kh = 0; kh < KERNEL_SIZE; kh++) {
                        for (int kw = 0; kw < KERNEL_SIZE; kw++) {
                            int in_idx = (c * IMG_SIZE * IMG_SIZE) + 
                                         ((h + kh) * IMG_SIZE) + 
                                         (w + kw);
                            int w_idx = (f * CHANNELS * KERNEL_SIZE * KERNEL_SIZE) + 
                                        (c * KERNEL_SIZE * KERNEL_SIZE) + 
                                        (kh * KERNEL_SIZE) + 
                                        kw;
                            sum += in[in_idx] * weight[w_idx];
                        }
                    }
                }
                int out_idx = (f * out_size * out_size) + (h * out_size) + w;
                out[out_idx] = sum;
            }
        }
    }
}
