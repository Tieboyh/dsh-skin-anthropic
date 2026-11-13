# dsh-skin-anthropic

Anthropic 纸感皮肤，给 DeepSeek Harness Web GUI 用。底色和语义色取自 anthropic.com 公开的调色板（`gray-000…1000`、`clay`、`olive`、`oat`、`iris`、`error`），映射到 DSH 的设计 token 层；同时接管三处字体栈，装一个插件就得到完整的 Anthropic 外观。

## 安装

从 GitHub 装：

```bash
dsh plugin --profile desktop add github:Tieboyh/dsh-skin-anthropic
```

或用本地目录（开发时）：

```bash
dsh plugin --profile desktop add link:/path/to/dsh-skin-anthropic
```

装完重启 DSH，设置 → 外观里能看到字体栈已指向 Anthropic。

**字体文件需要自己装。** 插件只写 `font-family` 名称，不包含任何字体二进制——Anthropic Sans / Serif / Mono 是 Anthropic 的专有字体，没有公开授权。没装字体时后面的 PingFang SC / Georgia 会接手，界面不会坏，只是没有 Anthropic 的字形。

## 怎么工作的

DSH 的组件不直接写颜色，而是引用 `--dsw-alias-*`；这些 alias 又全部指向一层原子阶梯 `--dsw-static-*`（neutral、bluish、blue、red、green、amber、violet）。皮肤只重写这一层：

```
body[data-dsh-skin="anthropic"]                     → 82 个 static + 30 个字面色 alias
body[data-dsh-skin="anthropic"][data-ds-dark-theme] → 同 82 个 static（暗色尾段加深）+ 28 个 alias
```

于是 surface / label / border / button / bubble / 弹层全部跟着变，不需要逐个组件适配。所有声明带 `!important`，因为 theme presenter 把 token 写成 body 内联样式，普通样式表压不住它。

字体走的是 bundle patch 里的 `ui-theme` config（`textFontFamily` / `codeFontFamily` / `terminalFontFamily`），属于配置层而不是 CSS，所以在设置界面里仍可被用户覆盖。

## 色板

| 用途 | DSH token | 值 | 来源 |
|---|---|---|---|
| 页面 / 卡片 / layer | `neutral-bluish-00` | `#faf9f5` | gray-050 |
| 侧栏、登录输入 | `neutral-bluish-50` | `#f5f4ed` | gray-100 |
| 模块平台、选择器、tip | `neutral-bluish-60` | `#f0eee6` | gray-150 |
| 遮罩层 | `neutral-bluish-150` | `#e2e0d5` | gray-200/250 之间 |
| 正文 | `neutral-bluish-1000` | `#141413` | gray-950 |
| 次要文字 | `neutral-bluish-700` | `#73726c` | gray-550 |
| 说明文字 | `neutral-bluish-600` | `#87867f` | gray-500 |
| 品牌 / 主按钮 | `neutral-bluish-1000` | `#141413` | 官网按钮就是黑底白字 |
| 强调 / 焦点 / 链接 | `blue-500` / `deepseek-500` | `#d97757` | clay |
| 强调 hover | `blue-600` | `#c6613f` | clay-interactive |
| 用户气泡 | `deepseek-50` / `-200` | `#fdf3ef` / `#f6d2c3` | clay 淡化 |
| 成功 / diff-added | `green-*` | `#788c5d` | olive |
| 错误 / diff-deleted | `red-*` | `#bf4d43` | Anthropic error |
| 警告 | `amber-*` | `#c08a3e` | oat 加深 |
| 特殊状态 | `violet-*` | `#4a3aa7` | iris-deep |

暗色模式下 alias 引用的阶梯反向（底取 950、文字取 50），所以同一套 static 自动得到对的反差；暗色块另外把尾段压到 `#141413 / #1a1918 / #1f1e1d / #262624`，贴近 Anthropic 自己的暗色纸面。

弹层、hairline 边框、遮罩这些字面量 alias 单独覆盖过，用的是 `#141413` 的透明度而非纯黑，避免暖底上出现冷灰边。

## 字体

```yaml
textFontFamily:     '"Anthropic Serif Web", "Anthropic Serif Web Text", "PingFang SC", Georgia, serif'
codeFontFamily:     '"Anthropic Mono Web", "Anthropic Mono", "SF Mono", Menlo, monospace'
terminalFontFamily: '"Anthropic Mono Web", "Anthropic Mono", "SF Mono", Menlo, monospace'
```

中文没有 Anthropic 字体可用——官方三套只有拉丁字形（各约 700 个 glyph），中文一律由 PingFang SC 兜底。想换中文观感，把 `PingFang SC` 换成 Noto Sans SC 或思源黑体即可。

## 文件

```
client.js                预构建的 client bundle（CSS 已内联，ModuleLoader 拿不到文件）
index.js                 host 侧空壳，只为让 fiber 存在
cordis.patch.yml         bundle patch：insert 皮肤 + 覆盖 ui-theme 的字体栈
src/tokens.css           生成的样式表，便于阅读 diff
src/client.template.js   bundle 模板（含 CSS 占位）
scripts/build-tokens.py  生成器：改色只改这里的表
```

## 改色

改 `scripts/build-tokens.py` 里的 `EXPLICIT`（中性阶梯与强调色的落点）或 `CLAY / ERROR / OLIVE / OCHRE / IRIS` 色带，然后：

```bash
python3 scripts/build-tokens.py   # 同时生成 src/tokens.css 与 client.js
node --check client.js
```

DSH 的 HMR 会重新加载 client bundle，界面即变，不用重启。

## 开关

- 临时关：在 profile 的 `cordis.patch.yml` 加 `- id: skin-anthropic` + `disabled: true`；
- 彻底删：`dsh plugin --profile desktop remove dsh-skin-anthropic`。

皮肤通过 `body[data-dsh-skin="anthropic"]` 作用域生效，卸载时属性与 `<style>` 一起被移除，不会留残留。

## 说明

配色取自 anthropic.com 的公开样式表，用于个人界面定制；Anthropic 的名称与字体归 Anthropic PBC 所有，本仓库不包含任何字体文件。
