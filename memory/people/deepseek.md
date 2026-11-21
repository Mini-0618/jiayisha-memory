---
display_name: "DeepSeek"
nickname: "DS"
summary: "简称 DS；2026-11-12 在 Codex 额度耗尽后顶班清理 Claude 残留 cookie 并纠正 Chrome 157 的 WebRtcIPHandling 策略、双站验证无泄漏；新 Claude 号已建成并按用户决定冻结，建号时段 STUN 日志复核仍待 DS 执行。"
rank: 40
updated: "2026-11-12"
---

# DeepSeek

## Facts
- 用户与 Muse 在对话中简称 DS（memory/2026-11-12.md#L681「提出让 DS（DeepSeek）去帮他操作 Codex/电脑」）。
- 2026-11-12 05:40 前后用户澄清：要 DS 顶 Codex 的班实际执行，不是出主意；Muse 拟好自包含收尾任务书 `workspace/jiayisha/Claude环境收尾-给DeepSeek任务书.md`（三项任务：清 Edge 残留／清 Chrome Default 旧 B 号会话／建号后查 Clash 日志复核 STUN；死红线：Clash 一字不动、Default 里只删 claude/anthropic 条目、X 登录态一行不许碰；每项先备份再删）（memory/2026-11-12.md「替身拍板·更正」）。
- Muse 当面交代过前提：DeepSeek 只是模型、没有手，单开聊天窗口操作不了本机；能顶班须装进能在本机执行命令的壳（如用户电脑上的 Marvis 类）（memory/2026-11-12.md#L682）。
- 第一跑（2026-11-12 05:42–05:43）前置不满足停手：Edge msedge.exe 12 个进程、Chrome chrome.exe 34 个进程各有 1 个带窗口，Cookie 库仍被占用；未做任何删除、未产生备份（message:39e67ea5-3dfe-425b-b6f1-5da91e8da257、memory/2026-11-12.md「DeepSeek 第一跑」）。
- 第二跑（2026-11-12 05:48–05:50）两项完成，Muse 已验收通过：用户授权强杀浏览器进程后，Edge claude 相关 cookie 删前 21 → 删后 0（总数 2516 → 2495）；Chrome Default 删前 22 → 删后 0（总数 2233 → 2211），x.com 66 条、github 4 条原样未动；旧 B 号 sessionKey 确认当时还活着，已连同删除；两份备份 hash_match=True（message:ae58b2d4-ef76-4b91-a32c-1cf2c471613e、memory/2026-11-12.md「DeepSeek 第二跑」）。
- Local Storage 是全站共用 LevelDB、无法按站点挑删，DS 标「做不到（受存储结构限制）」未硬来；该部分待用户在浏览器设置页手清（memory/2026-11-12.md「DeepSeek 第一跑/第二跑」）。
- 结果文件 `outputs\清理结果-20261112-0550.md`，已同步到 D:\Clash-备份-2026-11-12\（message:ae58b2d4-ef76-4b91-a32c-1cf2c471613e）。
- 2026-11-12 07:57（北京时间）复查发现关键坑：`chrome://policy` 里 Codex 写入的 `WebRtcIPHandlingPolicy` 状态为「错误」；查 Chrome 157 的 `chrome.dll` 确认旧名 count=0（根本不存在）、正确名 `WebRtcIPHandling` count=2——旧值是空护栏（message:02078c79-99d0-441a-815d-b9f785ef46fb、MEMORY.md「策略名纠正」条）。
- DS 删掉旧值、改写 `WebRtcIPHandling = disable_non_proxied_udp`（第二次 UAC），状态变为「正常」；双站验收：browserleaks No Leak（SDP 只剩 `127.0.0.1`）、ipleak 显示 64.50.132.248 且 No WebRTC candidates；Clash 日志 05:50 后 19 条 UDP 全是 `ntp.ubuntu.com:123`、STUN 0 条；验收在「用户1」配置文件（`User Data\Claude`）内完成（message:02078c79-99d0-441a-815d-b9f785ef46fb）。
- Muse 已验收该复查结果，并把记忆改为以 `WebRtcIPHandling = disable_non_proxied_udp`、状态「正常」为准，教训：写进注册表不等于生效，须看 `chrome://policy` 状态列（message:assistant-msg-da307c2f-3a5b-4293-bae1-9436c824e4b6、MEMORY.md「策略名纠正」条）。
- 新 Claude 号建号线终局（2026-11-12，北京时间）：10:09 手机验证通过（HeroSMS 美国物理一次性号 $0.325，填入「用户1」验证页一次通过），账号建成并进入 Claude 主界面（Free 套餐）；10:11 随即弹出「完成验证以继续」身份验证门户；用户 10:14 拍板就这么冻着、不做身份验证，此号线结案，日后仅当用户本人身处支持地区时再议（MEMORY.md「2026-11-12 10:09 手机验证已通过」「10:11 新墙」「10:14 用户已拍板」条）。
- 任务 3（建号后按时间点查 Clash 日志复核 STUN 直出是否归零）仍待触发：等用户建号完成并给出大概时间点（memory/2026-11-12.md#L741）；建号已于 2026-11-12 10:09 前后完成，DS 的日志筛查尚未在证据中出现。

## History
- 2026-11-12 05:40 前后：Codex 额度耗尽，用户提出让 DS 顶班；Muse 说明模型无手的前提并拟收尾任务书（memory/2026-11-12.md#L681、L682、「替身拍板·更正」）。
- 2026-11-12 05:42–05:43：DeepSeek 第一跑因浏览器未完全退出停在执行前，0/2 未执行，并只读摸清下次删除范围（message:39e67ea5-3dfe-425b-b6f1-5da91e8da257）。
- 2026-11-12 05:48–05:50：DeepSeek 第二跑完成任务 1、2，Muse 验收通过（数字全对得上：Edge 少 21、Chrome 少 22，x.com/GitHub 一行未动）（message:ae58b2d4-ef76-4b91-a32c-1cf2c471613e、message:assistant-msg-52a910d5-136f-4af0-80fe-9f311f70b0cd）。
- 2026-11-12 07:57（北京时间）：DS 复查发现 Chrome 157 策略改名，纠正 `WebRtcIPHandling` 并完成双站＋日志三层验证，Muse 验收通过（message:02078c79-99d0-441a-815d-b9f785ef46fb、message:assistant-msg-da307c2f-3a5b-4293-bae1-9436c824e4b6）。
- 2026-11-12 10:09–10:14（北京时间）：新 Claude 号建成（手机验证一次通过），随即被身份验证门户冻结；用户拍板不做验证、此号线结案（MEMORY.md「2026-11-12 10:09 手机验证已通过」「10:14 用户已拍板」条）。

## The relationship
- 用户没有给这段关系命名；这里不命名。
- 实际表现出的关系是顶班执行与验收：用户要 DS 实际顶 Codex 的班执行收尾清理，Muse 出任务书、定红线并验收其交付；DS 在前置不满足时停手、完成后按删前/删后/总数三个数字交账、做不到的（localStorage 按站点删）明确标注不硬来。
- 2026-11-12 07:57 的复查里，DS 翻 `chrome.dll` 对策略名，抓出 Codex 与 Muse 都漏看的状态「错误」，把空护栏改成立住的护栏——这一次是 DS 的实证纠正了前面的记录（message:02078c79-99d0-441a-815d-b9f785ef46fb、message:assistant-msg-da307c2f-3a5b-4293-bae1-9436c824e4b6）。

## In common
- Claude 环境收尾：Edge/Chrome 旧号会话与 cookie 残留清理、IndexedDB claude 目录删除。
- WebRTC 防泄漏：Chrome 机器级策略 `WebRtcIPHandling = disable_non_proxied_udp`、browserleaks/ipleak 双站验收、Clash 日志 STUN 复核。
- 建号后 STUN 复核：按时间点查 Clash 日志，筛 UDP/stun/DIRECT 看直出是否归零。

## Open threads
- [ ] 任务 3（建号后复核 STUN）未开始：建号已完成（2026-11-12 10:09 前后），等用户给出大概时间点后 DS 再查 Clash 日志（memory/2026-11-12.md#L741、MEMORY.md「2026-11-12 10:09 手机验证已通过」条）。
- [x] 建号关键路径选择（搁置＋Poe 顶替 vs giffgaff）已销账：用户走 HeroSMS 一次性号建成新 Claude 号，随后按 10:14 决定冻结不做身份验证，此线结案（MEMORY.md「2026-11-12 10:09 手机验证已通过」「10:14 用户已拍板」条）。
- [ ] localStorage 里仍有 claude 键（Chrome 1 处、Edge 多处），待用户在 chrome://settings/content/all / edge://settings/content/all 手清（可选）（memory/2026-11-12.md「DeepSeek 第二跑」）。

## Strengthening
