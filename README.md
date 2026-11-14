<div align="center">

# dsh-skin-anthropic

**给 DeepSeek Harness Web GUI 换上温润的 Anthropic 纸感皮肤与 Claude 级交互质感**

*Editorial Warmth · Surface 0–3 纸面微对比 · 15 阶弹簧手感 · Zero-JS 滚动渐隐 · 暗色防光渗字重补偿*

[![License: MIT](https://img.shields.io/badge/License-MIT-d97757.svg)](LICENSE)
[![DSH Plugin](https://img.shields.io/badge/DeepSeek%20Harness-Web%20Skin-141413.svg)](https://github.com/Tieboyh/dsh-skin-anthropic)
[![Zero Build Deps](https://img.shields.io/badge/Runtime-Pure%20CSS%20%2B%20Tiny%20Effect-788c5d.svg)](#架构与文件)

</div>

---

## ✨ 为什么做这个皮肤？

不只是换一层主题色。`dsh-skin-anthropic` 基于 `anthropic.com` 公开调色板与 Claude Design System (CDS) 的桌面端工程细节，从**色彩阶梯、表面微对比、光学排版、交互物理**四个维度重构 DeepSeek Harness 的视觉体验：

### 🎨 1. 温润纸感与 Surface 0–3 微对比层次
* **浅色纸面**：`#f5f4ed`（侧栏 Surface 0）→ `#faf9f5`（主画布 Surface 1）→ `#fcfbf8`（一级抬升）→ `#ffffff`（卡片与输入框 Surface 2/3），温和不刺眼。
* **暗色黑纸**：`#111110` → `#161514` → `#1c1b19` / `#22211f` / `#282725`，告别冷蓝灰暗底；浮层与卡片自动叠加极细的 `0.5px` **顶部内高光（`inset`）**，深色纸面叠层依然清晰锐利。
* **macOS Vibrancy 暖色适配**：覆盖 DSH 原生在 `darwin` 下偏冷蓝紫的侧栏洗色与半透明菜单底色，让毛玻璃透出干净的暖纸感。
* **品牌与焦点角色分离**：发送按钮、推理呼吸、陶土扫光使用经典的 **Clay 陶土橙（`#d97757` / `#c6613f`）**；键盘焦点环（Focus Ring）保留克制的 **Focus Blue（`#2a78d6` / `#6da7ec`）**，兼顾辨识度与克制感。

### ⚡ 2. 桌面级微交互物理学
* **15 阶 CSS 弹簧按钮手感**：利用独立 `scale` 属性实现按下 `60ms` 轻陷至 `0.975`、松手 `450ms` 弹性复位的物理回弹（不破坏原有 `transform` 定位，且遵循 `prefers-reduced-motion`）。
* **Composer 双环漫反射阴影**：输入框在静息、悬停与聚焦时呈现三段细腻的柔光扩散与内发丝描边过渡。
* **Zero-JS 7 档非线性滚动渐隐**：基于 `@property` + `animation-timeline: scroll(self)` 的纯 CSS 边缘消隐遮罩，在侧边栏与会话列表可滚动时自动激活，即使叠加在 macOS 毛玻璃上也能透明融化边缘。
* **窗口失焦自动降饱和**：监听窗口 `focus` / `blur`，切换后台时自动将主操作按钮与强调色退化为中性暖灰，回到前台时重新点亮陶土橙。

### 👁️ 3. 光学排版与细节克制
* **暗色模式字重逆补偿（Anti-Halation）**：针对深底浅字的视网膜光渗现象，在暗色模式下通过 `--dsw-font-*` 将 `400 / 500 / 600 / 700` 字重微调为 `385 / 465 / 560 / 660`，搭配 `Anthropic Serif Variable` 可变字体不发胀、不糊边。
* **等宽数字防抖动**：代码块、计时器与统计数字启用 `tabular-nums`，流式刷新时不左右跳位。
* **精简差异化暗色样式**：暗色模式仅生成差异 Token，CSS 体积轻量且可维护。

---

## 📦 安装

### 从 GitHub 安装

```bash
dsh plugin --profile desktop add github:Tieboyh/dsh-skin-anthropic
```

### 本地开发链接

```bash
dsh plugin --profile desktop add link:/path/to/dsh-skin-anthropic
```

安装后重启（或刷新）DSH，在 **设置 → 外观** 中即可看到字体栈已自动接管为 Anthropic 排版栈。

> **关于字体文件**：本仓库**不包含任何专有字体二进制文件**。`cordis.patch.yml` 仅在配置层写入 `font-family` 名称（如 `Anthropic Serif Variable` / `Anthropic Mono`），若本机未安装对应字体，会自动平滑回退到 `PingFang SC` / `Georgia` / `SF Mono`，界面排版不会错位；你也可以随时在「设置 → 外观」中自由覆盖字体与字号。

---

## 🎨 色板映射一览

| 角色 / 用途 | DSH Token | 浅色值 | 暗色值 | 设计来源 |
|---|---|---|---|---|
| 侧栏基底（Surface 0） | `--dsw-specific-sidebar-fill` | `#f5f4ed` | `#111110` | Paper Gray 100 / Obsidian |
| 主画布（Surface 1） | `--dsw-alias-bg-base` | `#faf9f5` | `#161514` | Paper Gray 050 / Dark Paper |
| 输入框（Surface 3） | `--dsw-specific-input-major` | `#ffffff` | `#201f1d` | Crisp Card Surface |
| 正文 / 主按钮 | `neutral-bluish-1000` | `#141413` | `#f0eee6` | Ink / Warm Bone |
| 次要 / 说明文字 | `neutral-bluish-700 / 600` | `#73726c / #87867f` | `#9c9a92 / #87867f` | Warm Stone |
| 品牌强调 / 发送 / 扫光 | `blue-500 / deepseek-500` | `#d97757` (`#c6613f` hover) | `#d97757` (`#e08b6e` shimmer) | Clay Terracotta |
| 键盘焦点环 | `--dsw-focus-ring-color` | `#2a78d6` | `#6da7ec` | Focus Blue |
| 成功 / Diff Added | `green-*` | `#788c5d` | `#8ea56e` | Olive |
| 错误 / Diff Deleted | `red-*` | `#bf4d43` | `#d16156` | Error |
| 警告 | `amber-*` | `#c08a3e` | `#e2ab55` | Oat / Ochre |
| 完成态 / 特殊状态 | `violet-*` | `#7a68c6` | `#b4a9e6` | Iris |

---

## 🛠️ 架构与文件

```text
dsh-skin-anthropic/
├── client.js                 # 预构建的 Client Bundle（已内联全部 CSS 与窗口失焦监听）
├── index.js                  # Host 侧空壳（维持 Fiber 生命周期）
├── cordis.patch.yml          # Bundle Patch：挂载皮肤并配置 ui-theme 默认字体栈
├── scripts/
│   └── build-tokens.py       # Token 生成与样式打包脚本（暗色差异生成 + 内联打包）
└── src/
    ├── client.template.js    # Client 入口模板（CSS 挂载、focus/blur 监听与干净卸载）
    ├── tokens.css            # 自动生成的色板、Surface 0–3、macOS Vibrancy 与焦点环规则
    ├── sidebar.css           # 侧栏紧凑布局微调 + Scroll-Driven 7 档边缘渐隐
    └── ergonomics.css        # Composer 阴影、15 阶弹簧手感、失焦降饱和与暗色字重补偿
```

---

## 🎛️ 自定义与二次开发

修改 `scripts/build-tokens.py` 中的色带（`CLAY / ERROR / OLIVE / OCHRE / IRIS`）、`EXPLICIT` 映射或 `src/sidebar.css` / `src/ergonomics.css` 后，重新构建即可：

```bash
python3 scripts/build-tokens.py   # 重新生成 src/tokens.css 并打包 client.js
node --check client.js            # 校验 bundle 语法
```

开启本地链接开发时，DSH 的 HMR 会自动感知 `client.js` 变更，刷新页面即可看到效果。

---

## 🔌 启停与卸载

* **临时禁用**：在 profile 的 `cordis.patch.yml` 中添加：
  ```yaml
  - id: skin-anthropic
    disabled: true
  ```
* **彻底卸载**：
  ```bash
  dsh plugin --profile desktop remove dsh-skin-anthropic
  ```

所有样式均严格作用域限定在 `body[data-dsh-skin="anthropic"]` 下，停用或卸载时会自动清理 `<style>` 标签、DOM 属性与事件监听器，不留任何残留。

---

## 🙏 致谢与声明

* 调色板取自 `anthropic.com` 公开样式表；交互物理参数、Surface 0–3 层次与暗色光学补偿理念参考了 [open-claude-ui](https://github.com/Caho1/open-claude-ui) 对 Claude Desktop (CDS) 的逆向研究。
* `Anthropic` 与 `Claude` 的名称、品牌标识及专有字体归 Anthropic PBC 所有；本仓库仅包含 CSS / JS 配置实现，不包含任何字体或音频二进制文件。
