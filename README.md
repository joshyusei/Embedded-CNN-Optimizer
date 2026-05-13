# Low-Level CNN Inference

這是一個專注於純 C 語言實作的高效能卷積神經網絡 (CNN) 推論引擎。主要針對資源受限的嵌入式系統進行優化，特別著重於記憶體存取模式與運算效率。

## 開發環境設定

### 前置作業
1.  **安裝編譯器**：下載並安裝 [MinGW-w64](https://www.mingw-w64.org/)。
2.  **設定環境變數**：將 MinGW 的 `bin` 資料夾路徑（例如：`D:\apps\MinGW\bin`）加入系統的環境變數 `Path` 中。
3.  **VS Code 擴充功能**：安裝 [C/C++ (Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)。

### 專案配置與自動化建置
本專案已配置 VS Code 的 `tasks.json`，讓開發者可以直接在編輯器中一鍵編譯並執行。

#### `tasks.json` 運作邏輯：
1.  **全案編譯 (`編譯並執行 CNN 專案`)**：
    *   **指令**：使用 PowerShell 呼叫 `gcc`。
    *   **參數**：
        *   `-I'${workspaceFolder}/include'`：指定包含路徑。
        *   `(Get-Item '${workspaceFolder}/src/*.c')`：**動態搜尋** `src` 資料夾下所有 `.c` 檔案並傳給編譯器。這避免了每次新增檔案都要手動修改設定。
        *   `-o 'cnn_inference.exe'`：指定輸出檔名。
    *   **自動執行**：編譯成功後會自動執行產出的 `.exe`。
2.  **單檔測試 (`編譯並執行單一 C 檔案`)**：
    *   針對當前開啟的單一 `.c` 檔案進行快速編譯與測試，適合用於測試 `hello.c` 或獨立的小工具。

#### 如何使用：
*   按下 `Ctrl + Shift + B` 即可觸發預設建置工作。
*   或透過選單：`Terminal` -> `Run Task...` 選擇特定任務。

### 疑難排解 (Troubleshooting)
*   **VS Code IntelliSense 找不到標頭檔 (.h)**：
    若出現紅色波浪線，請至 VS Code 的 `C/C++: Edit Configurations (UI)`，在 **包含路徑 (Include path)** 區塊加入 `${workspaceFolder}/**`。這會讓 VS Code 自動搜尋專案下所有子資料夾的標頭檔。

## 專案結構 (Project Structure)

*   **`include/`**：存放標頭檔 (`.h`)。
    *   `conv.h`：定義全域常數（如 `IMG_SIZE`, `FILTERS`）與函式宣告。
*   **`src/`**：存放原始碼 (`.c`)。
    *   `main.c`：程式進入點，負責資料初始化與效能測量。
    *   `baseline.c`：基礎卷積演算法實作。
*   **`.vscode/`**：開發環境配置。
    *   `tasks.json`：定義編譯指令。支援「編譯並執行全案」以及「編譯當前單一檔案」。

## CNN 實作細節

### 1. 靜態記憶體管理 (Static Memory Management)
本專案**不使用 `malloc`**，改用 `static` 全域陣列進行記憶體分配。
*   **原因**：
    *   **資源受限環境**：嵌入式系統通常記憶體有限，且不一定有完整的堆積 (Heap) 管理機制。
    *   **避免記憶體碎片化**：頻繁分配與釋放堆積空間會導致碎片化，影響系統穩定性。
    *   **效能預測性**：靜態分配在編譯時期即決定記憶體佈局，避免執行時期的分配開銷。
    *   **防止 Stack Overflow**：大型張量若放在局部變數 (Stack) 容易導致溢位，改用全域 `static` 會存放在 Data Segment。

### 2. 基礎卷積 (Baseline Convolution)
目前的卷積實作採用標準的六層巢狀迴圈：
- 遍歷輸出通道 (Filters)
- 遍歷輸出特徵圖高度 (Height)
- 遍歷輸出特徵圖寬度 (Width)
- 遍歷輸入通道 (Channels)
- 遍歷卷積核高度 (Kernel Height)
- 遍歷卷積核寬度 (Kernel Width)

此版本作為效能比較的基準點。

## 目前進度
- [x] 環境建置與 Hello World 測試
- [x] 基礎張量運算與卷積實作
- [ ] 卷積層優化 (SIMD/Loop Unrolling)
- [ ] 支援更多層別 (Pooling, Activation)
