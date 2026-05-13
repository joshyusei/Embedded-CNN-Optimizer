#define IMG_SIZE 224
#define KERNEL_SIZE 3
#define CHANNELS 3
#define FILTERS 16

// 卷積函數宣告
void conv_baseline(float* in, float* weight, float* out);
void conv_optimized(float* in, float* weight, float* out);
