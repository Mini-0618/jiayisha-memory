# 风格蒸馏运行报告 — code-video-style-distill × 《别做梦了，AI风口，与你无关》

- 日期：2026-11-21（本地时间）
- 技能：GitHub 仓库 Mini-0618/motion-resource-center- 的 `skills/code-video-style-distill`（当日 clone，入口 cvsd.py）
- 参考片：`../别做梦了，AI风口，与你无关.mp4`（1920×1080 @30fps，756.0s，117MB）
- 风格名：`fastcut-doc-narration`
- 权利口径：公开视频、仅内部风格学习（技能范围门第 1 条），运行时设 RIGHTS_OK=1

## 走了哪几步

| 步 | 命令 | 结果 |
|---|---|---|
| 0 预检 | `cvsd.py precheck` | **verdict = live_ai_3d**（score 0.33；抽样 68.8% 实拍/AI/3D、18.8% 代码模板、12.5% 混合）。技能口径：只能蒸馏包装层 |
| 1 拆解 | `cvsd.py analyze --sample-fps 2` | 317 个镜头、63 个运动事件（全部被归为转场类）；产物在 `ref_analysis/`（analysis.json、scenes.csv、951 张关键帧、contact_sheet.png、motion_energy、色板、音频包络/起音点、videomd/VIDEO.md） |
| 1.5 目测 | Read contact_sheet.png、motion_energy.png、scene253/308 全分辨率 settled 帧 | 写入 `overrides.json`（见下） |
| 2 蒸馏 | `cvsd.py distill fastcut-doc-narration --overrides overrides.json` | `style/style-tokens.json`，**schema 校验通过**；风格资产已存技能仓库 `styles/fastcut-doc-narration/`（含 README、refs、attribution 模板） |
| 3 验收清单 | `cvsd.py checklist script.json` | `acceptance.json/.md` 已生成并冻结（在任何渲染之前）：降级后 **7 must / 19 should / 5 out** |
| 4–6 静帧预检/渲染/对比 | — | **未执行，停在闸门处**，理由见文末 |

## 环境偏差（如实记录）

1. **采样率降到 2fps**：默认 30fps 与 4fps 两次运行均被系统 OOM 杀掉（analyze 把全片帧＋float32 灰度栈＋两份 diff 数组同时驻留，本机共享内存 6GB）。2fps 峰值约 3GB 才跑通。代价：切点定位 ±0.5s、运动事件时间粒度 0.5s；关键帧、色板、版式仍是全分辨率提取，不受影响。
2. **无 OCR**：本机未装 Tesseract，analyze 自动跳过 OCR 并在 analysis.json 注明。后果：字号阶梯、字幕文字证据、元件文字证据全部降级 unknown（tokens 的 unknowns 清单里有）。
3. Node v24.22.1 在位，但模板 `template/node_modules` 未安装、本机无 Chrome——渲染路径未走到，未验证。

## overrides（目测纠正，均带 _provenance）

- `components_style.subtitle`（seen，证据 scene253/308 settled 帧）：底部居中、白色填充＋黑色粗描边、**无底条**（bg_opacity 0.0）。脚本因无 OCR 本会记 unknown，目测纠正为实测在位。
- `typography.vibe`（inferred）：粗黑无衬线（黑体气质），中英双行字幕（中文大、英文字小）。字体身份按技能规则保持 unknown。
- `layout.radius_px = 24`（inferred）：画面内容置于圆角矩形画框内（浅灰描边、外侧虚化背景），圆角目测约 24–30px。
- `motion.transition.type = cut`、`duration_s = 0`（inferred）：脚本给出的「转场中位 3.0s」是 2fps 采样在实拍上的伪影；能量图上切点为单采样宽尖峰。
- `motion.easing.family_guess = "unknown"`（unknown，置信度 0.1）：**占位符而非测量值**。首轮 distill 因该字段为 None 未过 schema（字段要求 string），按技能自带的 overrides 通道补入并明确标注 unknown，schema 随后通过。

## style-tokens 盘点

- provenance 共 95 个字段：**seen 47 / inferred 21 / unknown 27**。
- 真实可用的包装层结论：画布 1920×1080@30；镜头节奏平均 2.385s / 中位 2.0s（seen）；音频 BPM 61.5、音画卡点匹配率 0.696（seen）；字幕样式如上（seen）；转场为硬切（inferred）；圆角画框（inferred）。
- **不可当设计参数用的字段**：palette 的 bg/surface/primary/accent 是实拍画面内容的像素统计（边框众数灰 #838384、画面棕 #8D673E），本片没有设计底色，这些值只对「内容题材」有意义，拿去做模板底色是误用。
- 元件检测（像素启发式，置信度 0.6–0.75）：title_card ×1、evidence_frame ×23、timeline ×5、transition ×1。注意 evidence_frame 的大量命中主要来自「圆角画框＋有纹理内容」这一包装形态本身，不等于 23 处独立证据图元件。
- 模板表达不了的签名元件（只记此处，不硬塞 tokens）：①顶部章节选项卡导航条（浅灰分段、当前章白色圆角高亮）；②右下角白色人物剪影水印（logo 类资产，按技能政策不搬运）；③中英双行字幕的英文字号比（无 OCR 未测到）。

## checklist 生成中的一处透明说明

checklist 内部要跑一遍无 overrides 的基准 distill 做基准冻结；该基准 distill 同样因 family_guess=None 在写出 tokens 后以 schema 错误退出（exit 1）。`ref_analysis/_distill/style-tokens.json` 已按其设计落盘，第二次运行 checklist 时按其自带缓存规则直接采用该文件并成功生成清单。基准取的色板/几何值与主 tokens 一致，此事不改变任何阈值。

## 停在哪一步、为什么

**停在第 3 步之后（验收清单已冻结），未做 stillcheck 静帧预检、未做 Remotion 复刻渲染、未做 compare。** 三个理由：

1. **技能闸门**：precheck 判定 live_ai_3d。技能的一键流程在此判定下直接停机（exit 4，需 --force 才继续），且明示「主体画面需要其它工具或自有素材」。本次按任务授权只走了技能为该类视频定义的包装层蒸馏路径（analyze→distill→checklist），没有用 --force 绕闸。
2. **比对无意义**：stillcheck/compare 的色板与版式基准取自参考片分析——对实拍片即画面内容统计量；拿模板段落的静帧去和实拍帧比 ΔE 与边距，得分不携带任何包装风格信息，通过或失败都是假信号。
3. **环境未就绪（次要）**：模板依赖未安装、本机无 Chrome，Remotion 首渲需下载无头 Chrome。

后续如要继续：需要用户明确点头 --force 等效授权，并先装模板依赖与 Chrome；且验收预期应改按包装层口径（字幕、画框、章节条、节奏），而不是现清单里对实拍帧的 M2/M3/M7。

## attribution

`styles/fastcut-doc-narration/attribution.json` 仍为模板值 UNSPECIFIED（来源标注与权利声明应由用户填写），export-index 时会照实标记。
