---
display_name: "Groq"
summary: "开源模型高速推理平台；用户 2026-11-14 提供其 API，Muse 当日验活并登记为 Super OS API 第 5 条、Agent 第 5 号，定位快速推理/转写短任务；同日实测其声音模型被条款阻断、无中文与克隆入口，生成用户声音此路不通。"
rank: 43
updated: "2026-11-14"
---

# Groq

## Facts
- Groq（q）与 Grok（k，xAI）是两家不同的公司，密钥不通用；用户 2026-11-14 发来 https://console.groq.com/docs/rate-limits（message:1a8f0904-1a09-4447-87a1-b79c72132644），Muse 回复先分清字（message:assistant-msg-8fcc7ba8-72d9-4aab-960b-08cafd38dcf0）。
- Groq 是开源模型高速推理平台，OpenAI 兼容接口 api.groq.com；文档页汇总口径：gpt-oss-120b 约 30 次/分钟、1000 次/天、20 万 token/天；Whisper whisper-large-v3 约 20 次/分钟、2000 次/天（message:assistant-msg-8fcc7ba8-72d9-4aab-960b-08cafd38dcf0、MEMORY.md「Groq API」条）。
- 2026-11-14 验活实测（真跑调用）：模型列表 200 共 11 个模型（gpt-oss-120b/20b、qwen3.8-27b、whisper-large-v3 与 turbo、orpheus 英/阿 TTS 等，无 llama-3.3）；gpt-oss-20b 与 qwen 对话 200（总耗时 0.03–0.13 秒级）；Whisper 转写 Kokoro 占位音 200 识别正确（未传用户真声样本）（message:assistant-msg-52210eb4-b735-4d10-b5fc-cc605bbcf2aa、MEMORY.md「Groq API」条）。
- 已登记进超级中心：API 连接第 5 条＋Agent 第 5 号，定位写死「快速推理／转写，只派短任务」（message:assistant-msg-52210eb4-b735-4d10-b5fc-cc605bbcf2aa）。
- 限额与阵容的实测结论：gpt-oss 按 1000 次/天、20 万 token/天量级只配初筛、摘要、转写短活；没有 Llama 3.3，Qwen 只有一个 27B 版；自带配音只有英文和阿拉伯语，中文配音帮不上忙（message:assistant-msg-52210eb4-b735-4d10-b5fc-cc605bbcf2aa）。
- 2026-11-14 声音模型实测（真调用，非功能列表）：给 groq.py 新增 speech 命令，调用 canopylabs/orpheus-v1-english 返回 400 model_terms_required，须组织管理员先去 Groq 控制台接受该模型条款，本次未接受、未生成；Orpheus 只有预置嗓子、无克隆入口，两个声音模型仅英文/阿拉伯语，生成不了中文、更生成不了用户本人的声音（memory/2026-11-14.md#L99、message:b998c243-05bd-467a-a69d-248f34fc0c13、message:assistant-msg-f4ca7a5c-4811-47c5-98c7-ca17b922a61e）。
- 2026-11-14 用量口径：调用 Groq 烧 Groq 自己的额度（对话按 token、转写按音频秒数，文档汇总约 20 万 token/天、28800 音频秒/天，真实限额以控制台 Limits 页为准），Muse 派活、看结果、汇报仍走本对话；同日「巫师向」声音是本地 ffmpeg 处理，零 API、零 token（message:0b8c834e-057b-458b-8666-0ea2522d2595、message:assistant-msg-cec5df72-08a8-400d-af01-09036dbfead2、memory/2026-11-14.md#L67）。

## History
- 2026-11-14：用户提供 Groq API 文档链接，Muse 区分 Groq/Grok 并说明密钥经安全录入、验活后登记进 Super OS（message:1a8f0904-1a09-4447-87a1-b79c72132644、message:assistant-msg-8fcc7ba8-72d9-4aab-960b-08cafd38dcf0）。
- 2026-11-14：Groq 验活通过并登记为 Super OS API 第 5 条、Agent 第 5 号（message:assistant-msg-52210eb4-b735-4d10-b5fc-cc605bbcf2aa）。
- 2026-11-14：用户随后提出「你先那他的声音模型去帮我生成我的声音 巫师那样的」（message:b998c243-05bd-467a-a69d-248f34fc0c13），指代与执行路径待确认。
- 2026-11-14：Groq 声音模型实测受阻——speech 调用返回 400 model_terms_required，本次未接受条款、未生成；账号 11 个模型无中文语音模型、只有英/阿预置音色且无克隆入口，生成用户声音此路不通；替代为本地对 Voicebox 8 秒试听原声做「巫师向」处理（memory/2026-11-14.md#L89、memory/2026-11-14.md#L99）。

## The relationship
- 用户没有给这段关系命名；这里不命名。现有证据只支持：用户把 Groq 的 API 交给 Muse 接入 Super OS，Muse 完成验活与登记，并把 Groq 定位为只派短任务的快速推理/转写一路。

## In common
- Super OS 快速推理与转写：Groq 的高速对话与 Whisper 转写对标视频批量转写、热点初筛这类短活（message:assistant-msg-52210eb4-b735-4d10-b5fc-cc605bbcf2aa）。

## Open threads
- [ ] Groq 首件真活待用户点选：对标视频批量转写，还是热点初筛（2026-11-14，message:assistant-msg-52210eb4-b735-4d10-b5fc-cc605bbcf2aa）。
- [x] 用户提出用「他的声音模型」生成巫师财经质感的声音（2026-11-14，message:b998c243-05bd-467a-a69d-248f34fc0c13）：2026-11-14 已实测——Groq 声音调用返回 400 model_terms_required，预置嗓子无克隆入口、仅英文/阿拉伯语，此路不通；已改本地处理用户本人声音，用户声音未出本机（memory/2026-11-14.md#L99）。

## Strengthening
