---
display_name: "Codex"
summary: "在用户电脑上执行 Clash/X链式修复与渲染的执行者，Super OS 圆桌中为执行位不是 API 参与方；2026-11-18 按五个视频 Skill 用真实素材重做 22 号切片画面获用户认可；2026-11-23 GeekFaka 演示站交他做成可用站；2026-11-25 代码动效风格蒸馏工具 V1.1 归 Codex 侧。"
rank: 37
updated: "2026-11-25"
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
- 2026-11-12 用户把一个卡死的 Cursor/Grok/X 账户关联页面交给 Codex 去处理：该流程声称关联「永久生效、无法撤销」，弹窗按钮点不动、刷新与关标签页都没用，用户已新开窗口绕出；交给 Codex 的红线是不许点任何「连接/继续绑定」类按钮、不许替用户购买或续订、不许动 X 的 Premium 订阅（官网已直购，有效期至 2026-12-12、续订已取消），处理后须先报告结果（memory/2026-11-12.md Verified extraction 03:52 UTC 第二条，quote「我交给codex去吧」）。
- 2026-11-13 用户 Super OS「AI 圆桌会议」需求将 Codex 与 ChatGPT、Claude、Muse 并列为拟拉进同一会议室的 AI（message:eda1edd5-46c2-4b4e-af17-922f8576e9d5）；同日圆桌试点口径明确 Codex 在用户电脑上是执行位、不是 API 参与方，ChatGPT、Claude 的 API 密钥与预算授权尚未接入，圆桌 v1 先用本系统多 Agent 扮演各方讨论（message:assistant-msg-185beab8-d09c-469a-81ea-e297c25b4682）。
- 2026-11-18 用户拿 Muse 的 22 号 GPT-6.2 切片（稿＋1.2 倍速配音）打底，在本机用 Codex 换上真实素材、按五个开源 Skill 的方法重做画面，成品获用户认可（原话「我想要的视频终于能够做出来了，codex 帮我做的」）；分工为 Muse 出稿与配音、Codex 本机做素材画面合成；成片文件尚未到 Muse 手里，未验收（memory/2026-11-18.md#L804、MEMORY.md）。
- 2026-11-18 12:18 用户补明 Muse 本人可直接用这五个 Skill 做片，不必只经 Codex；五仓代码在本地 ~/workspace/jiayisha/视频Skill学习-2026-11-17/repos/（memory/2026-11-18.md#L807、MEMORY.md）。
- 2026-11-22 用户的套餐为 Pro 100：只有每周限额、没有 5 小时限额，当时每周限额剩余 95%、约 5 天 23 小时后重置；额外购买的付费 credits 余额为 0，用户没买过，与套餐用量无关；连续长时间跑 Codex 不会被 5 小时窗口卡住，只需盯每周额度（message:fb8c56b2-7507-4bb2-97b3-18111a1418c0、message:assistant-msg-3f80b180-d045-4387-875b-81db3a993764、message:assistant-msg-5a550173-ba4c-4268-ac88-3a7142f56b8b）。
- 2026-11-23 用户把 GeekFaka 代充演示站交给 Codex 做成可用站：Muse 已打包交接（1.7MB、168 个文件，含完整源码、演示数据库与《HANDOVER-交接说明.md》）；离能用还差部署、真实商品与卡密、接支付、改演示配置，外观方向待用户定（用户此前已判该演示站「太丑了」）；同日用户发来 Craft Anything（storytold/craft-anything）问能做什么，Muse 建议可拿 NIUB 自营店作原版给 GeekFaka 换皮，是否补进 Codex 交接说明待用户决定（message:4b725375-fdcd-4af3-b0cb-a4ba6bec63ac、message:assistant-msg-a45700c4-39f8-47f3-b908-6c84f7454c85、message:assistant-msg-c341c2c2-cbd2-4815-a631-a44c62120b2f）。
- 2026-11-25 用户发来 code-video-style-distill V1.1（2026-11-24）：专项技术工具，已退出默认创作流程，仅在明确需要复刻代码动效风格时调用，其输出进正式创作前仍须按 video-distill-master V1.2 核验；精确运镜、数据动画、标题卡、要点列表、图表、时间线、对比双栏、流程图这类代码生成的画面归 Codex 侧，不归 Muse 的电影感镜头、人物、环境、视觉隐喻；文档所写工具路径 /workspace/ip-team/tools/code-video-style-distill/ 经 2026-11-25 实查在本机不存在，Muse 这边不能直接跑，须先落实本地路径；文档自述局限为测试参考片是工具自渲、真实外部视频未测过，Lemo 后端在入场时长 M6 一项卡住判停滞，Motion Canvas 后端只支持 9 种段落中的 5 种（message:d768ed60-a7d5-4a38-9454-7dde4d9b51d8、message:assistant-msg-03817b45-7f08-4943-911a-a3c79a68a43e）。

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
- 2026-11-18：用户在本机用 Codex 按五个视频 Skill 的方法重做 22 号 GPT-6.2 切片的画面（换上真实素材），成品获用户认可；同日用户补明 Muse 本人也可直接用这五个 Skill 做片，不必只经 Codex（memory/2026-11-18.md#L804、L807）。
- 2026-11-22：用户确认其 Pro 100 套餐只有每周限额、无 5 小时限额，当时每周限额剩余 95%；2026-11-12 的额度耗尽状态至此已恢复，连续长时间跑 Codex 不再受 5 小时窗口限制（message:assistant-msg-3f80b180-d045-4387-875b-81db3a993764）。
- 2026-11-23：用户把 GeekFaka 代充演示站交给 Codex 做成可用站（Muse 打包 1.7MB、168 个文件含交接说明）；同日用户发来 Craft Anything 仓库，Muse 建议用它对照 NIUB 给 GeekFaka 换皮，是否补进交接说明待用户决定（message:4b725375-fdcd-4af3-b0cb-a4ba6bec63ac、message:assistant-msg-c341c2c2-cbd2-4815-a631-a44c62120b2f）。
- 2026-11-25：用户发来 code-video-style-distill V1.1 并由 Muse 登记：代码动效风格蒸馏归 Codex 侧，Muse 的电影感镜头不往该工具送；文档所写工具路径在本机实查不存在，Muse 不能直接跑（message:d768ed60-a7d5-4a38-9454-7dde4d9b51d8、message:assistant-msg-03817b45-7f08-4943-911a-a3c79a68a43e）。

## The relationship
- 用户没有给这段关系命名；这里不命名。
- 实际表现出的关系是任务交接与验收：用户把本机修复与审计交给 Codex 执行，Muse 出任务书/交接总结并验收其交付（链路、WebRTC 根因、时区纠正均以 Codex 的系统级证据为准，覆盖 Muse 早前错报）。
- 2026-11-12 起 Codex 额度耗尽，同一条收尾线改由 DeepSeek 顶班执行，Muse 继续验收；Codex 写入的 WebRTC 策略名其后被 DeepSeek 证实在 Chrome 157 无效并纠正（message:02078c79-99d0-441a-815d-b9f785ef46fb）。
- 2026-11-12 用户仍直接把卡死的 Cursor 关联页交回 Codex 处理（而非 DeepSeek），并坚持「我要让他去帮我解决呀」——交接时 Muse 已提醒其额度昨晚耗尽、必要时 DeepSeek 顶上（memory/2026-11-12.md Verified extraction 03:52 UTC 第二条）。
- 2026-11-13 起，Codex 同时是 Super OS 圆桌拟参与 AI 之一，但试点定位是用户电脑上的执行位、不是 API 真身参与方（message:eda1edd5-46c2-4b4e-af17-922f8576e9d5、message:assistant-msg-185beab8-d09c-469a-81ea-e297c25b4682）。
- 2026-11-18 五 Skill 画面路线经用户实证跑通，分工为 Muse 出稿与配音、Codex 本机做素材画面合成；同日用户补明 Muse 本人可直接用这五个 Skill 做片，不必只经 Codex（memory/2026-11-18.md#L804、L807）。
- 2026-11-23 用户再次直接派活给 Codex：把 GeekFaka 代充演示站交给他做成可用站，Muse 打包交接说明，用户须另定外观方向（message:4b725375-fdcd-4af3-b0cb-a4ba6bec63ac）。
- 2026-11-25 代码动效风格蒸馏（code-video-style-distill V1.1）划归 Codex 侧：精确运镜、数据动画与代码生成的标题卡、要点、图表、时间线、对比双栏、流程图归 Codex，Muse 的电影感镜头、人物、环境、视觉隐喻不往该工具送；该工具在本机无本地安装，须先落实路径才能调用（message:assistant-msg-03817b45-7f08-4943-911a-a3c79a68a43e）。

## In common
- X 固定出口与 Clash 链式（X链式v2、LinkStatic 纽约出口 64.50.132.248、29 个前置节点）。
- PC 环境与浏览器卫生（WebRTC 策略、Chrome 专用配置文件、Claude 账号残留清理）。
- 加伊莎重制作管线中 Codex 在用户电脑上渲染、Muse 出规格单的分工。
- 五个视频 Skill 的画面方法（2026-11-18 经 Codex 在本机实证跑通）：Muse 出稿与配音、Codex 换真实素材重做画面。
- GeekFaka 代充演示站（2026-11-23 交 Codex 做成可用站）。
- 代码动效风格蒸馏 code-video-style-distill V1.1（2026-11-25 划归 Codex 侧，专项工具、仅在明确需要复刻代码动效风格时调用）。

## Open threads
- [ ] 卡死的 Cursor/Grok/X 账户关联旧页面已交 Codex 关闭（2026-11-12）：窗口内无处理结果回报；红线为不点任何绑定按钮、不动 X Premium 订阅（有效期至 2026-12-12、续订已取消），发现已误关联先报告用户（memory/2026-11-12.md Verified extraction 03:52 UTC 第二条）。
- [ ] 29 个前置节点逐个验收表用户尚未提供（验收＝切过去后 ipify 显示 64.50.132.248 且 x.com 可打开）；截至 2026-11-12 04:33 记录未完项不变（memory/2026-11-12.md#L557）。
- [ ] 开机自启仍未启用（MEMORY.md#L66，截至 2026-11-12 04:25 状态）。
- [x] Codex 额度耗尽后何时恢复未知（2026-11-12 05:40 前后，memory/2026-11-12.md#L681）——2026-11-22 已确认恢复：用户为 Pro 100，当时每周限额剩余 95%、无 5 小时限额（message:assistant-msg-3f80b180-d045-4387-875b-81db3a993764）。
- [ ] 22 号切片重做版成片文件尚未到 Muse 手里，未验收（2026-11-18，memory/2026-11-18.md#L804）。
- [ ] GeekFaka 代充演示站已交 Codex 做成可用站（2026-11-23）：部署、真实库存与卡密、接支付、改演示配置待完成；外观换不换皮、换成什么样待用户定方向（message:4b725375-fdcd-4af3-b0cb-a4ba6bec63ac、message:assistant-msg-a45700c4-39f8-47f3-b908-6c84f7454c85）。
- [ ] 是否把 Craft Anything（对照 NIUB 换皮的用法）补进给 Codex 的交接说明，待用户决定（2026-11-23，message:assistant-msg-c341c2c2-cbd2-4815-a631-a44c62120b2f）。
- [ ] 等 Codex 送第一个具体镜头（2026-11-25）：若其中含代码动效段落，在路线判定里明确标出走 code-video-style-distill V1.1，触发条件为明确需要复刻代码动效风格，不默认调用；该工具在本机无本地安装，调用前须先落实路径（message:assistant-msg-03817b45-7f08-4943-911a-a3c79a68a43e）。

## Strengthening
