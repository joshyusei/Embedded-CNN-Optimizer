# Low-Level CNN Inference

這是一個專注於純 C 語言實作的高效能卷積神經網絡 (CNN) 推論引擎。主要針對資源受限的嵌入式系統進行優化，特別著重於記憶體存取模式與運算效率。

## 開發環境設定

### 前置作業
1.  **安裝編譯器**：下載並安裝 [MinGW-w64](https://www.mingw-w64.org/)。
2.  **設定環境變數**：將 MinGW 的 `bin` 資料夾路徑（例如：`D:\apps\MinGW\bin`）加入系統的環境變數 `Path` 中。
3.  **VS Code 擴充功能**：安裝 [C/C++ (Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)。

### 專案配置
本專案已配置 VS Code 的工作設定（`.vscode/tasks.json`），支援直接使用編譯器進行建置。

## 目前進度
- [x] 環境建置與 Hello World 測試
- [ ] 基礎張量運算實作
- [ ] 卷積層優化
