import torch
import torch.nn as nn
import time

# --- Config from include/conv.h ---
IMG_SIZE = 224
KERNEL_SIZE = 3
CHANNELS = 3
FILTERS = 16

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

class StandardConv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, padding=0, bias=False)
    
    def forward(self, x):
        return self.conv(x)

class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3):
        super().__init__()
        self.depthwise = nn.Conv2d(in_channels, in_channels, kernel_size, groups=in_channels, padding=0, bias=False)
        self.pointwise = nn.Conv2d(in_channels, out_channels, 1, bias=False)
    
    def forward(self, x):
        return self.pointwise(self.depthwise(x))

def benchmark(model, input_size=(1, CHANNELS, IMG_SIZE, IMG_SIZE), iterations=100):
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device("cpu")
    model.to(device)
    model.eval()
    x = torch.randn(input_size).to(device)
    
    # Warm up
    with torch.no_grad():
        for _ in range(10):
            model(x)
    
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    
    start_time = time.time()
    with torch.no_grad():
        for _ in range(iterations):
            model(x)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
    end_time = time.time()
    
    return (end_time - start_time) / iterations * 1000  # ms

if __name__ == "__main__":
    # Base configuration from main.c: 3 channels -> 16 filters, 3x3 kernel
    base_params = CHANNELS * FILTERS * KERNEL_SIZE * KERNEL_SIZE
    print(f"Target Parameter Count (based on main.c): {base_params}")
    
    # Configurations to target ~base_params
    # 1. Standard 3x3: 3 -> 16 => 3*16*3*3 = 432
    # 2. Standard 5x5: 3 -> 6 => 3*6*5*5 = 450
    # 3. DW-Sep 3x3: 3 -> 135 => (3*3*3) + (3*135) = 27 + 405 = 432
    # 4. Bottleneck: 3 -> 12 -> 25 => (3*12) + (12*12*9) + (12*25) = 36 + 1296 + 300 = 1632 (Too many)
    #    Let's use 3 -> 4 -> 25 => (3*4) + (4*4*9) + (4*25) = 12 + 144 + 100 = 256 (Closer)
    #    Let's use 3 -> 6 -> 25 => (3*6) + (6*6*9) + (6*25) = 18 + 324 + 150 = 492 (Closer)

    configs = [
        ("Standard 3x3 (C-like)", StandardConv(CHANNELS, FILTERS, kernel_size=3)),
        ("Standard 5x5", StandardConv(CHANNELS, 6, kernel_size=5)),
        ("Depthwise Separable", DepthwiseSeparableConv(CHANNELS, 135, kernel_size=3)),
        ("Bottleneck (1x1-3x3-1x1)", nn.Sequential(
            nn.Conv2d(CHANNELS, 6, 1, bias=False),
            nn.Conv2d(6, 6, 3, padding=1, bias=False),
            nn.Conv2d(6, 25, 1, bias=False)
        ))
    ]
    
    input_size = (1, CHANNELS, IMG_SIZE, IMG_SIZE)
    
    print(f"Benchmarking with input size: {input_size}\n")
    print(f"{'Architecture':<25} | {'Params':<10} | {'Latency (ms)':<15}")
    print("-" * 55)
    
    results = []
    for name, model in configs:
        params = count_parameters(model)
        latency = benchmark(model, input_size=input_size)
        print(f"{name:<25} | {params:<10} | {latency:<15.4f}")
        results.append({"Architecture": name, "Params": params, "Latency (ms)": latency})

    try:
        import pandas as pd
        df = pd.DataFrame(results)
        print("\nSummary (DataFrame):")
        print(df)
    except ImportError:
        print("\nSummary (List):")
        for res in results:
            print(res)
