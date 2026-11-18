---
display_name: "Codex"
summary: "在用户电脑上执行 Clash/X链式修复与渲染的执行者，Super OS 圆桌中为执行位不是 API 参与方；2026-11-12 卡死的 Cursor 关联页交他关闭，结果待报。"
rank: 38
updated: "2026-11-13"
---

# Codex

## Facts
- 用户 2026-11-11 把 Clash Verge「X链式」的修复交给在他自己电脑上的 Codex，边界是不得动他当前在用的节点，修好后由用户自己尝试激活测试（memory/2026-11-11.md#L879、L868）。
- 2026-11-11 Codex 修好 X链式，用户自查出口为 64.50.132.248（纽约静态 IP），X 固定出口环境定版（memory/2026-11-11.md#L889）。
- Codex 已建好「X链式v2」（X前置池，含 29 个日美前置节点）且当前启用的是 v2；完整备份与 Restore-Clash.cmd 由 Codex 建好（MEMORY.md#L66）。
- 2026-11-12 05:15（北京时间）Codex 做 PC 环境只读审计，Muse 已验收：链路顺序正确（MATCH→Exit→LinkStatic-NY→dialer-proxy X前置池）；WebRTC 泄漏根因坐实——出口 socks5 节点 udp:false，STUN 的 UDP 19 条全部 DIRECT 直出、真实 IP 125.71.94.10 暴露；系统/浏览器时区实为 Asia/Shanghai（MEMORY.md#L69、memory/2026-11-12.md#L665）。
- Codex 按批清单写入 Chrome 机器级策略 `WebRtcIPHandlingPolicy=disable_non_proxied_udp`（待 Chrome 完全重启生效），建好专用配置文件「用户1」，清掉 Firefox 残留 claude/anthropic Cookie 12 条，备份复制到 D:\Clash-备份-2026-11-12\ 且 SHA256 一致（memory/2026-11-12.md#L676 一带「Codex 按批清单执行完毕」）。
- 上述策略名后被证实在 Chrome 157 不存在：2026-11-12 07:57（北京时间）DeepSeek 复查 `chrome://policy` 状态为「错误」，查 `chrome.dll` 确认 `WebRtcIPHandlingPolicy` count=0、`WebRtcIPHandling` count=2；已删旧值改写为 `WebRtcIPHandling = disable_non_proxied_udp`、状态「正常」，双站验证无泄漏（message:02078c79-99d0-441a-815d-b9f785ef46fb、MEMORY.md「策略名纠正」条）。
- 工作室重制作（转写、渲染）由 Codex 在用户自己电脑（RTX 4060）上执行，Muse 出制作规格单（MEMORY.md 算力分工条）。
- 2026-11-12 05:40 前后用户称 Codex 没有额度了，提出让 DS（DeepSeek）顶班（memory/2026-11-12.md#L681）。
- 2026-11-12 用户把一个卡死的 Cursor/Grok/X 账户关联页面交给 Codex 去处理：该流程声称关联「永久生效、无法撤销」，弹窗按钮点不动、刷新与关标签页都没用，用户已新开窗口绕出；交给 Codex 的红线是不许点任何「连接/继续绑定」类按钮、不许替用户购买或续订、不许动 X 的 Premium 订阅（官网已直购，有效期至 2026-12-12、续订已取消），处理后须先报告结果（memory/2026-11-12.md Verified extraction 03:52 UTC 第二条，quote「我交给codex去吧」）。
- 2026-11-13 用户 Super OS「AI 圆桌会议」需求将 Codex 与 ChatGPT、Claude、Muse 并列为拟拉进同一会议室的 AI（message:eda1edd5-46c2-4b4e-af17-922f8576e9d5）；同日圆桌试点口径明确 Codex 在用户电脑上是执行位、不是 API 参与方，ChatGPT、Claude 的 API 密钥与预算授权尚未接入，圆桌 v1 先用本系统多 Agent 扮演各方讨论（message:assistant-msg-185beab8-d09c-469a-81ea-e297c25b4682）。

## History
- 2026-11-10：用户让 Muse 在云电脑上装 Codex，实测已预装 codex-cli 0.164.0-alpha.9、Node 24 齐备，未登录，待用户选 ChatGPT 账号登录或 API key（memory/2026-11-10.md#L128、L125）。
- 2026-11-11 约 20:20–20:40：用户改派 Codex 在他电脑上修 Clash 链式；Muse 交付交接总结，约束写明别动在用节点、Codex 只改配置（memory/2026-11-11.md#L864、L868）。
- 2026-11-11 约 21:09：Codex 修好 X链式，用户确认出口已是 64.50.132.248（memory/2026-11-11.md#L889）。
- 2026-11-12 04:25：Codex 检查说明书确认已建好并启用「X链式v2」（MEMORY.md#L66）。
- 2026-11-12 05:15–05:50：Codex 只读审计完成并按批清单执行（WebRTC 策略、专用配置文件、Firefox 清理、备份异盘），Muse 验收通过；执行进度 05:39 Codex、收尾 05:50 DeepSeek（MEMORY.md#L69）。
- 2026-11-12 05:40 前后：Codex 额度耗尽，收尾清理改由 DeepSeek 顶班（memory/2026-11-12.md#L681）。
- 2026-11-12 07:57（北京时间）：DeepSeek 复查发现 Codex 写入的 `WebRtcIPHandlingPolicy` 在 Chrome 157 无效（状态「错误」），纠正为 `WebRtcIPHandling` 并验证通过，Muse 验收（message:02078c79-99d0-441a-815d-b9f785ef46fb、message:assistant-msg-da307c2f-3a5b-4293-bae1-9436c824e4b6）。
- 2026-11-12：用户把卡死的 Cursor 账户关联旧页面交给 Codex 关闭，红线为勿点绑定、勿动 X 订阅；窗口内尚无 Codex 的处理结果回报（memory/2026-11-12.md Verified extraction 03:52 UTC 第二条）。
- 2026-11-13：Codex 被列入 Super OS AI 圆桌拟参与名单，试点中定位为用户电脑上的执行位而非 API 真身参与方（message:eda1edd5-46c2-4b4e-af17-922f8576e9d5、message:assistant-msg-185beab8-d09c-469a-81ea-e297c25b4682）。

## The relationship
- 用户没有给这段关系命名；这里不命名。
- 实际表现出的关系是任务交接与验收：用户把本机修复与审计交给 Codex 执行，Muse 出任务书/交接总结并验收其交付（链路、WebRTC 根因、时区纠正均以 Codex 的系统级证据为准，覆盖 Muse 早前错报）。
- 2026-11-12 起 Codex 额度耗尽，同一条收尾线改由 DeepSeek 顶班执行，Muse 继续验收；Codex 写入的 WebRTC 策略名其后被 DeepSeek 证实在 Chrome 157 无效并纠正（message:02078c79-99d0-441a-815d-b9f785ef46fb）。
- 2026-11-12 用户仍直接把卡死的 Cursor 关联页交回 Codex 处理（而非 DeepSeek），并坚持「我要让他去帮我解决呀」——交接时 Muse 已提醒其额度昨晚耗尽、必要时 DeepSeek 顶上（memory/2026-11-12.md Verified extraction 03:52 UTC 第二条）。
- 2026-11-13 起，Codex 同时是 Super OS 圆桌拟参与 AI 之一，但试点定位是用户电脑上的执行位、不是 API 真身参与方（message:eda1edd5-46c2-4b4e-af17-922f8576e9d5、message:assistant-msg-185beab8-d09c-469a-81ea-e297c25b4682）。

## In common
- X 固定出口与 Clash 链式（X链式v2、LinkStatic 纽约出口 64.50.132.248、29 个前置节点）。
- PC 环境与浏览器卫生（WebRTC 策略、Chrome 专用配置文件、Claude 账号残留清理）。
- 加伊莎重制作管线中 Codex 在用户电脑上渲染、Muse 出规格单的分工。

## Open threads
- [ ] 卡死的 Cursor/Grok/X 账户关联旧页面已交 Codex 关闭（2026-11-12）：窗口内无处理结果回报；红线为不点任何绑定按钮、不动 X Premium 订阅（有效期至 2026-12-12、续订已取消），发现已误关联先报告用户（memory/2026-11-12.md Verified extraction 03:52 UTC 第二条）。
- [ ] 29 个前置节点逐个验收表用户尚未提供（验收＝切过去后 ipify 显示 64.50.132.248 且 x.com 可打开）；截至 2026-11-12 04:33 记录未完项不变（memory/2026-11-12.md#L557）。
- [ ] 开机自启仍未启用（MEMORY.md#L66，截至 2026-11-12 04:25 状态）。
- [ ] Codex 额度耗尽后何时恢复未知；截至 2026-11-12 05:40 前后最后支持状态是 DeepSeek 顶班收尾（memory/2026-11-12.md#L681）。

## Strengthening
