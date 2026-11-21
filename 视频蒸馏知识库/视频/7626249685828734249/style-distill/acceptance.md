# 验收清单（预先声明）— fastcut-doc-narration

- 创建：2026-11-20T19:11:12+00:00（在第一次渲染之前）
- 出处分级：must 只对 seen 字段生效；inferred → should；unknown → should + not-testable。
- 基准冻结：主色/强调色/元件基准来自参考片分析（不带 overrides 的 distill），建清单时冻结在各项 baseline 字段，之后不随 style-tokens 改动。
- 完成规则：降级后剩下的所有 must 项，在连续两轮、两个不同成片文件（sha256 不同）的 compare 中都为 pass 才算完成；not-testable 不算 pass；同一文件重复比较不计新一轮；两轮总分不动就停下来问人
- 出处：Tier/gap/ledger 结构改编自 Speedrunlab/reverse-engineer-anything-self-learning-loop (MIT)；'不可比较即 unknown/not-testable' 规则参考 morluto/rea 视觉主张合同 (MIT)；seen/inferred/unknown 分级参考 aicodeking/leanrea (MIT)。

| ID | 档位 | 原定档位 | 出处等级 | 来源字段 | 项目 | 指标 | 阈值 | 方法 |
|---|---|---|---|---|---|---|---|---|
| M1 | must | must | seen | canvas.width, canvas.height, canvas.fps | 画布尺寸与帧率一致 | canvas_equal | == True | ffprobe width/height/fps |
| M2 | must | must | seen | palette.bg | 背景色一致 | bg_delta_e | <= 3.0 | CIEDE2000(ref bg, replica bg)；bg=边框像素众数 |
| M3 | must | must | seen | palette.measured_swatches | 整体色板接近 | palette_weighted_delta_e | <= 6.0 | 参考色板每个色块(占比≥0.5%)到复刻色板最近色的 ΔE2000，按占比加权平均 |
| M4 | should (not-testable) | must | unknown | palette.primary, palette.accent | 主色/强调色出现在复刻片 | role_colors_max_delta_e | <= 8.0 | 基准=参考片分析测得的 primary/accent（建清单时冻结）到复刻前景色板最近色的最大 ΔE2000 |
| M5 | should (not-testable) | must | unknown | motion.easing.enter | 入场速度曲线形状一致（缓动） | entrance_profile_corr | >= 0.8 | 非转场运动事件的光流速度曲线重采样到 20 点、归一化后取平均，Pearson r |
| M6 | should (not-testable) | must | unknown | motion.durations_s | 入场动画时长接近 | entrance_duration_ratio_err | <= 0.25 | |median(rep)/median(ref) - 1| |
| M7 | must | must | seen | layout.margins_pct.left | 左边距一致 | margin_left_diff_pct | <= 2.0 | 左边距百分点差 |
| M8 | should | must | inferred | layout.alignment | 对齐方式一致 | alignment_match | == True | dominant_alignment 相同 |
| M9 | should | must | inferred | layout.safe_area_pct | 安全区接近 | safe_area_diff_pct | <= 3.0 | 四边安全区百分点差的最大值 |
| M10 | should | must | inferred | layout.radius_px | 面板圆角接近 | radius_diff_px | <= 6.0 | 面板圆角像素差（按画布高度归一） |
| C1 | should | must | inferred | components:title_card | 元件 title_card 在复刻片中被检测到 | component_detected | == True | 对复刻片跑 analyze+distill 的元件检测，要求出现 title_card |
| C2 | should (not-testable) | must | unknown | components:bullet_list | 元件 bullet_list 在复刻片中被检测到 | component_detected | == True | 对复刻片跑 analyze+distill 的元件检测，要求出现 bullet_list |
| C3 | should (not-testable) | must | unknown | components:number_counter | 元件 number_counter 在复刻片中被检测到 | component_detected | == True | 对复刻片跑 analyze+distill 的元件检测，要求出现 number_counter |
| C4 | should (not-testable) | must | unknown | components:bar_chart | 元件 bar_chart 在复刻片中被检测到 | component_detected | == True | 对复刻片跑 analyze+distill 的元件检测，要求出现 bar_chart |
| C5 | should (not-testable) | must | unknown | components:subtitle_bar | 元件 subtitle_bar 在复刻片中被检测到 | component_detected | == True | 对复刻片跑 analyze+distill 的元件检测，要求出现 subtitle_bar |
| U1 | must | must | seen | components_style.subtitle | 字幕底条色一致 | subtitle_bar_delta_e | <= 8.0 | 复刻片字幕行局部底色（components_style.subtitle.bg，需复刻侧 seen）与冻结基准 ΔE2000 |
| U2 | must | must | seen | components_style.subtitle | 字幕字号接近 | subtitle_size_ratio_err | <= 0.15 | 底部居中 OCR 行的墨迹字号中位数比 |rep/ref - 1|（按画布高度归一；任一侧无 OCR → not-testable） |
| U3 | must | must | seen | components_style.subtitle | 单条字幕 ≤18 字（一屏一行） | subtitle_max_line_chars | <= 18 | 复刻片底部居中 OCR 行去空格/标点后的字数最大值（无 OCR → not-testable）；模板按 ≤18 字自动拆条 |
| S1 | should (not-testable) | should | unknown | typography.scale_px.body | 正文字号接近 | body_size_ratio_err | <= 0.15 | OCR 墨迹高度估计的正文字号比（任一侧无 OCR 或默认值 → not-testable） |
| S2 | should (not-testable) | should | unknown | typography.scale_px.h1 | 标题字号接近 | h1_size_ratio_err | <= 0.2 | OCR 标题层字号比（任一侧无 OCR 或默认值 → not-testable） |
| S3 | should | should | inferred | motion.transition.type, motion.transition.duration_s | 转场类型一致且时长接近 | transition_match | == True | 光流方向判类型 + 核心时长误差≤30% |
| S4 | should | should | seen | rhythm.shot_mean_s | 镜头节奏接近 | shot_mean_ratio_err | <= 0.35 | 平均镜头时长比（受脚本时长影响） |
| S5 | should (not-testable) | should | unknown | motion.stagger_s | 错峰间隔接近 | stagger_ratio_err | <= 0.35 | 镜头内入场间隔中位数比 |
| S6 | should | should | inferred | layout.decor.grid_lines | 装饰元素一致（背景网格） | decor_match | == True | 背景网格线检测结果相同 |
| S7 | should | should | seen | rhythm.av_sync | 音画卡点比例接近（双方都有音轨时） | av_sync_ratio_diff | <= 0.2 | 视觉事件落在 80ms 内音频起音点的比例差 |
| S10 | should | should | seen | rhythm.entrance_events_per_min | 入场事件密度接近（次/分钟） | entrance_density_ratio_err | <= 0.35 | 非转场运动事件数/分钟之比 |rep/ref - 1|（受脚本内容量影响，故为 should） |
| O1 | out | out | seen | — | 整条运动能量曲线相关（仅同内容复刻有意义） | timeline_energy_corr | >= 0.6 | 两条运动能量曲线按归一化时间重采样 200 点后 Pearson r |
| O2 | out | out | seen | — | 同时间点画面结构相似（仅同内容） | mean_ssim | >= 0.85 | 并排帧灰度 SSIM 平均 |
| O3 | out | out | seen | — | 使用原片字体文件 | — | — | 政策排除：只用免费可商用替代字体 |
| O4 | out | out | seen | — | 原片素材 / logo / 角色 / 商标 | — | — | 政策排除：不搬运受保护资产 |
| O5 | out | out | seen | — | 像素级完全一致 | — | — | 不承诺；尺寸/字体/编码不同则视觉主张记为 not-testable |

- 降级后 must：M1, M2, M3, M7, U1, U2, U3
- 被降级：M4（unknown）, M5（unknown）, M6（unknown）, M8（inferred）, M9（inferred）, M10（inferred）, C1（inferred）, C2（unknown）, C3（unknown）, C4（unknown）, C5（unknown）, S1（unknown）, S2（unknown）, S5（unknown）
