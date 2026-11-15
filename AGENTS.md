# AGENTS.md

Your operating manual for this workspace, written by you. Your main instructions cover how you work in general. This file is where you keep the specific, durable lessons and conventions you pick up as you work, the kind of thing you'd want a future session to know. It's not about the user (that goes in `USER.md` and your memory) or your personality (that's `SOUL.md`); it's about how you get work done here.

## Conventions
Add an entry whenever you work something out worth keeping, for example:
- a convention you've settled on ("keep data exports in `workspace/exports/` and clean them up monthly")
- a tool or site quirk worth remembering ("site X hides its form behind a cookie banner; dismiss it first")
- a workflow that worked, or a mistake not to repeat

It starts empty and is meant to grow slowly. Don't pad it; a short, accurate file beats a long, stale one.

## 从 SOP 三方对照学到的工作规矩（2026-11-07，用户命学，详见 workspace/jiayisha/SOP三方对照-学习笔记.md）
- **标口径**：参数、门槛、报价、基准线必须注明是「已核实（附来源与日期）」「经验基线」还是「推测」，三者不混写；禁止虚假精确（把经验值写成像实测的数字）。
- **复盘用自有基线**：用账号最近 10–20 条同类作品的中位数做参照，不套外部"行业及格线"，不赌算法权重。
- **研究关**：写稿前先交四清单（事实/来源/数据/争议），核查产物要落成可检查的文件，不停在脑子里；未过不开写。
- **分镜与素材**：先定每个镜头要传达的信息，再找素材；素材与文案打匹配分，低分重做；素材入库带登记卡（来源/许可/核查日期），许可未核实标"待授权"，不进成片。
- **防迎合前提**：用户题目/框架里的前提若与他已定的规矩冲突（如"日产3条"vs质量线），先把冲突摆出来，再执行；不许乖乖照单全收。
- **逆向采样**：拆对标账号按最高2+普通2+低1采样，低表现样本专门记失败原因，防幸存者偏差；推断的制作方法标置信度（A实据/B推断/C猜测），猜测不许当事实传播。
- **工具参数按版本**：写工具参数注明当前版本并核对，不背旧参数当现行用（如 MJ V7 的 --oref 与 V8 Edit Model 是两套）。
- **lemo-opuscar 渲染入口（2026-11-09 实测纠正）**：成片渲染是 `core/render/video.mjs <dir> --fps 30 --workers 2 --out <dir>/out/video-silent.mp4`，不是 render.mjs（该文件不存在）；它只出无声 MP4，须再用 ffmpeg 与 mix.wav 合流。`mix.py` 用的 scipy 不在 preview-build venv 里，须用系统 python3 跑。
- **Kokoro 占位音 OOV 静默跳词（2026-11-09 28条版实测）**：每次生成后必须查 stderr 的 `OOV word skipped`，只看时长看不出来。Kimi / DeepSeek / PPT / Apiiro 这类专有名词不在词库里会被直接跳过不读（28条版 v7/v8/v16/v17 中招）。修法：字母拼读（K i m i、P P T、G I F）或拆成词库词（Deep Seek、阿皮罗）；修完只重生成受影响的句并重跑 mix.py，不用全量重做。
- **旁白密度不许开例外（2026-11-09 28条版教训）**：280–340字/分钟的切片线适用于一切带旁白的片子，播报体、包装类也不例外。"密度在画面"不能用来给稀旁白开绿灯——28条版119字/分钟就是这么放过去的，用户当场指出不好。密度先是文案属性，写稿时按每2–3秒一句、每秒约5字设计，剪辑补不回来。
- **审片逐句审（2026-11-09 投喂15）**：主片正式版前，每句旁白配一张关键静帧，意思先于好看；抽帧QA只看画面对不对，逐句审才看得出"这句讲完画面还剩几秒是空的"。风格冻结落成书面元素表（一格只一处强调色之类），铺完全片再改要逐镜头换。
- **指标靠真实价值**：收藏/复访/讨论只靠可复用的内容资产与真分歧，不用操纵手法（假信息、故意看不清、谐音规避审核、自动化私信等一律不碰）。
- **提示词先给方法、再给身份（2026-11-12，用户当面立规）**：给任何智能体/协作者写提示词（开发任务书、子任务、给外部 AI 的接口说明、cron 正文同理），开头必须先写思维与工作方法——逻辑与第一性原理、系统性思维、架构决策、工程执行、批判与反证、测试驱动纠错、长期演进，每项落成可检查的动作（决策记录、反证段、验收先行等）；只写"你是某某专家"而不给方法的，视为不合格提示词。参照：SOUL 的五个脑子每个都带「算法」行，身份与方法本就是一体的。

## 扩展性思维＋学习好的内容（2026-11-15，用户当面纠正）
- 看外部好内容（他人SOP、GPT稿、产品指南）先学它能复用的骨架，不只挑毛病：如「定位→主页→内容→执行」四篇闭环、指南的篇章目录结构。
- 交付框架/页面/手册默认按「模板＋实例」设计：模板是可复用的结构与规则位，实例填某个账号/项目的现行定版；新账号、新平台克隆模板再填，不重写一遍。章节、红线、资产位都要留可增的位置，不写死成一次性文档。

## 从对照中学到的交付标准（2026-11-07，用户拿两份他人SOP当面纠正后定）

用户给对照材料是让 Muse **学习**，不是再拼一份合并稿。交付任何手册/方案/拆解类文档时，按以下标准自检：

1. **先算账再讲打法**：目标先拆成数字（涨粉数学：总量÷天数→日均→所需播放量级→爆款依赖度），策略从数字里长出来，不从感觉里长出来。
2. **参数给到可执行**：工时、字数、色值、阈值、及格/优秀线都要有具体数；只给方向（"电影感""高级感"）等于没交付。引用的经验参数标注"经验基线"，核实过的标注出处与日期，两者不混。
3. **每环节有交付物和验收线**：流程表必须带"必须交付的文件"和"不合格不进下一环节"的通过标准；成片/素材留参数记录（提示词、seed、参考图、许可），可复现才算资产。
4. **逆向结论标置信度**：A=有直接证据，B=有依据的推断，C=猜测不可传播。对标拆解默认抽样高/中/低表现各若干条，不只拆爆款。
5. **复盘用相对基准**：和自己最近10–20条同类作品的中位数比，不套用网传"算法权重"和行业玄学数字；不达标时先改什么，要给出排查顺序。
6. **研究先行于写作**：写稿前先过研究关（事实清单/来源/口径/反方证据/已证实-争议-未证实三分），研究不过不写稿——此条已在生产cron的写稿工序里，手册类交付同样适用。
7. **诚实口径写进文档开头**：数据来源、哪些是核实值、哪些是经验值，第一页说清，不靠口头补。
