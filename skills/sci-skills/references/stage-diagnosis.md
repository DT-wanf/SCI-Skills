# Stage Diagnosis

## Rule

The actual stage is the earliest essential stage that has not met its acceptance criteria. A manuscript draft, code repository, dataset, figure, or partial result does not automatically validate preceding stages.

## Procedure

1. Record the user's self-reported stage and available artifacts.
2. Select the likely paper family and scan that family's compact matrix from stage 1 onward.
3. Compare artifacts with each stage's core outputs and minimum pass evidence; mark `passed`, `partially_passed`, `failed`, or `not_assessed`.
4. Stop at the earliest critical non-passed stage and load that authoritative stage module.
5. If the boundary is ambiguous, load only that stage and the immediately adjacent candidate, then decide.
6. Preserve usable downstream materials as provisional assets and explain the missing evidence in Chinese.

The matrix is a diagnosis index, not a replacement for the selected stage module. A matrix match identifies the candidate stage; formal acceptance uses the full module.

<!-- BEGIN GENERATED 35-STAGE MATRIX -->
## Compact 35-stage diagnosis matrix

### Empirical / 实证类

#### E1 — Research Topic and Problem Definition

Core outputs: 候选选题清单; 核心研究问题表述; 研究对象与边界说明; 初步题目 3 个版本

Minimum pass evidence: 研究问题可转化为变量、对象、关系、机制或效果; 研究对象、时间范围和场景边界清楚; 能够说明使用何种证据回答问题; 至少一个题目具备三个月内完成最小可行版本的可能

#### E2 — Literature Search and Review Construction

Core outputs: 关键词与检索式; 核心文献清单; 文献分类矩阵; 研究空白初步陈述; 文献综述结构框架

Minimum pass evidence: 能够说明研究所依托的文献基础; 综述按问题组织而不是逐篇堆砌; 研究空白直接连接后续假设、理论框架或方法; 核心文献真实且可核查

#### E3 — Theoretical Framework and Research Hypotheses

Core outputs: 理论框架图或文字版框架; 变量关系说明; 研究假设列表; 核心概念定义; 变量与假设对应表

Minimum pass evidence: 每个假设有明确理论依据; 变量原则上可测量、编码或通过材料识别; 理论框架能够指导研究设计; 假设与研究空白直接对应; 若制作理论框架图，图位和关系边界已由用户确认，且图中没有把假设关系冒充为已验证因果机制

#### E4 — Research Design and Method Route

Core outputs: 研究设计方案; 变量操作化表; 数据收集计划; 分析方法路线图; 伦理与质量控制说明

Minimum pass evidence: 方法能够回答研究问题并检验假设; 数据来源和样本标准清楚; 变量定义可操作且分析步骤可复现; 主要偏差、混淆因素和伦理问题已识别; 已有数据充足性已经基于字段、样本、范围、来源和研究问题完成判断; 仅当数据为 `INSUFFICIENT` 或 `ABSENT` 时才设计新增数据方案; 如计划爬取，已记录所有非爬虫路线不适用的理由并将 `crawl_necessity` 标为 `JUSTIFIED`

#### E5 — Data Collection, Execution, and Analysis

Core outputs: 原始数据与清洗后数据; 数据字典或编码表; 统计/编码/实验结果; 核心图表; 核心图表对应的Python/R源码、真实输入映射与运行证据; 结果解释草稿; 假设检验对应表; 数据源与权限记录; 试采集报告和全量采集日志; 用户审核结论; 数据清洗交接 Prompt

Minimum pass evidence: 每个核心结论有数据或材料支撑; 分析方法与研究设计一致; 结果和图表清楚可读; 没有将相关关系误写为因果关系; 每个假设有明确结果对应; 数据充足性结论与实际执行分支一致; 新获取的网络数据在清洗前已完成来源、范围、字段、质量、偏差和权限审核，并获得用户明确通过; 现有数据若被判定为 `SUFFICIENT`，没有误触发新增数据获取或爬虫; 每张实验结论图均来自真实数据或已核实结果，经Python/R实际运行生成，并具有输入、源码、运行证据和输出之间的可追溯链; 没有使用AI图片生成、手填数值或模拟数据制作正式实验结论图

#### E6 — Paper Writing and Structural Optimization

Core outputs: 完整论文提纲; 各章节初稿; 图表与结果说明; 修改记录或问题清单; 章节衔接检查表; 论文图位建议与用户选择记录

Minimum pass evidence: 引言问题在结论中得到回应; 方法、结果和讨论逻辑闭合; 语言规范且不夸大贡献; 引用、图表和附录相互对应; 所有核心结论来自真实文献、数据和结果; 实验结论图通过真实输入与Python/R运行证据审核；解释性和增强图均在制作前确认图位与拆图方案

#### E7 — Finalization, Submission, and Dissemination

Core outputs: 终稿文件; 投稿前检查清单; 投稿信或封面信; 审稿回复框架; 补充材料清单; 传播版摘要或汇报提纲

Minimum pass evidence: 格式符合目标要求; 图表、引用、附录和声明齐全; 审稿意见逐条回应且标明修改位置; 终稿无明显错字、格式混乱或证据缺口; 投稿材料与目标要求一致

### Interpretive / 阐释类

#### I1 — Interpretive Object and Research Question Definition

Core outputs: 阐释对象说明; 核心研究问题; 材料范围; 题目版本

Minimum pass evidence: 问题具体且可通过材料分析回答; 研究对象边界清楚; 不是简单主题赏析或读后感

#### I2 — Textual Materials and Context Collection

Core outputs: 原始材料清单; 文本摘录表; 背景资料清单; 已有研究简表

Minimum pass evidence: 材料能直接支撑阐释问题; 文本证据有出处和页码; 背景资料没有喧宾夺主; 现有材料充足性已先行判断，充分时没有误触发新增采集; 新获取的网络材料，其范围、版本、权限、缺失和选择偏差已经说明并经用户审核

#### I3 — Theoretical Lens and Interpretive Path

Core outputs: 理论视角选择说明; 核心理论概念; 阐释路径图; 理论与文本对应表

Minimum pass evidence: 理论与问题高度匹配; 理论概念有清楚定义; 能够回到具体材料展开分析

#### I4 — Close Reading, Coding, and Material Analysis

Core outputs: 文本细读笔记; 材料分析表; 关键证据链; 初步阐释判断

Minimum pass evidence: 每个解释都有具体材料支撑; 细读不是摘抄而有分析推进; 能够呈现文本复杂性或矛盾

#### I5 — Interpretive Thesis and Chapter Structure

Core outputs: 中心论点; 详细提纲; 章节材料分配表; 题目修订版

Minimum pass evidence: 中心论点清晰且可争论; 各章节共同服务主论点; 材料分配不重复、不空泛

#### I6 — Drafting and Interpretive Deepening

Core outputs: 正文初稿; 核心段落修改稿; 证据与论点对应表; 过渡句和章节结论

Minimum pass evidence: 文本证据和解释紧密对应; 理论使用适度; 章节之间有递进关系; 没有把主观感受当作学术结论

#### I7 — Finalization, Format, and Submission

Core outputs: 终稿; 版本与引用检查清单; 摘要与关键词; 修改计划

Minimum pass evidence: 文本版本和引用清楚; 摘要说明对象、问题、方法和贡献; 格式符合要求; 没有明显证据缺口

### Method-Application / 方法应用类

#### M1 — Application Problem and Need Definition

Core outputs: 问题定义; 需求场景说明; 现有痛点清单; 评价目标

Minimum pass evidence: 问题真实具体; 应用场景清楚; 评价标准初步明确

#### M2 — Existing Methods and Competing Solutions

Core outputs: 现有方法对比表; 不足分析; 改进方向; 相关文献清单

Minimum pass evidence: 能够明确本文相对谁改进; 不足具体而非泛泛; 改进方向与后续方案一致

#### M3 — New Method, Model, or Solution Design

Core outputs: 方法框架图文字版; 方法图位、全览与模块拆图建议及用户选择记录; 模块说明; 操作流程; 资源与条件清单

Minimum pass evidence: 方案结构清楚; 每个模块有明确功能; 能够说明相对现有方法的改进点; 具备实施条件; 复杂方法没有被强行压缩成单张拥挤图片；若制作图件，已先获得用户对图位和拆图方案的确认

#### M4 — Implementation Route and Prototype Construction

Core outputs: 实施计划; 原型功能清单; 流程文档; 测试准备材料; 实施/实验流程图建议、对标图适配方案与用户选择记录（如适用）

Minimum pass evidence: 实施步骤可执行; 资源需求明确; 原型能支撑验证目标; 风险有备选方案; 若制作流程图，步骤、模块和输入输出均来自已确认方案，并在制作前完成图位与用户确认

#### M5 — Effect Validation and Evaluation Design

Core outputs: 验证方案; 评价指标表; 实验/案例结果; 对比分析表; 结果图Python/R源码、真实输入映射、运行证据与审核状态

Minimum pass evidence: 验证方式与目标一致; 有清楚基线或评价标准; 结果能支撑核心主张; 局限被说明; 所有验证结果图由真实输入经Python/R实际运行生成并可追溯；没有AI生成或手工拼接的实验结论图

#### M6 — Paper Writing and Application Value

Core outputs: 论文提纲; 方法章节初稿; 验证结果说明; 应用价值段落

Minimum pass evidence: 方法描述足以让他人理解和复现; 验证结果对应核心问题; 贡献具体而非只说有价值; 局限和适用范围明确

#### M7 — Finalization, Translation, and Submission

Core outputs: 终稿; 投稿检查清单; 代码/数据/原型说明; 修改计划; 展示或传播材料

Minimum pass evidence: 格式符合要求; 图表清晰且编号一致; 补充材料齐全; 方法边界和安全伦理说明完整

### Theoretical / 理论类

#### T1 — Theoretical Problem and Core Concept Definition

Core outputs: 理论问题表述; 核心概念清单; 初步论点版本; 研究边界说明

Minimum pass evidence: 问题指向理论争议或概念困难; 核心概念有明确边界; 能够说明本文不是简单介绍而是提出判断

#### T2 — Theoretical Genealogy and Literature Lineage

Core outputs: 理论谱系表; 核心文献分类表; 主要争议清单; 可进入的理论缺口

Minimum pass evidence: 能够说明理论问题从哪里来; 不同理论立场之间差异清楚; 文献综述服务于后续论证

#### T3 — Theoretical Gap and Author Position

Core outputs: 核心论点; 理论缺口陈述; 论证对象与反驳清单; 修正后的题目

Minimum pass evidence: 本文立场明确且可争论; 论点不是常识判断; 论点能被后续章节层层支撑

#### T4 — Argument Framework and Chapter Design

Core outputs: 详细论文提纲; 章节论证任务表; 关键概念安排表; 可能反驳位置; 理论图位建议、内容边界与用户选择记录（如适用）

Minimum pass evidence: 每章有明确论证功能; 章节顺序推动主论点; 没有把文献介绍误当成理论论证; 若制作理论图，图中没有把概念关系或作者主张伪装成已验证的实验机制

#### T5 — Conceptual Analysis and Theoretical Argument

Core outputs: 核心章节初稿; 概念辨析段落; 理论比较表; 反驳与回应段落

Minimum pass evidence: 每个判断有理论依据或文本依据; 推理链条清楚; 对被批判理论的呈现不过度简化

#### T6 — Theoretical Contribution, Limits, and Conclusion

Core outputs: 理论贡献表述; 局限性说明; 结论初稿; 未来研究方向

Minimum pass evidence: 结论回答引言问题; 贡献表述具体而克制; 局限说明不削弱核心论点

#### T7 — Finalization and Submission Preparation

Core outputs: 终稿; 格式检查清单; 投稿信/答辩说明; 修改计划

Minimum pass evidence: 术语统一; 引用准确可查; 摘要清楚表达问题、方法和贡献; 审稿回复逐条对应

### Review / 综述类

#### R1 — Review Topic and Scope Definition

Core outputs: 综述主题; 范围说明; 综述类型判断; 核心综述问题

Minimum pass evidence: 主题不大不空; 边界可检索、可执行; 综述问题能指导后续文献筛选

#### R2 — Search Strategy and Literature Screening

Core outputs: 检索式; 数据库清单; 纳入/排除标准; 筛选记录表

Minimum pass evidence: 检索过程可复述; 筛选标准前后一致; 最终文献来源真实可查

#### R3 — Literature Reading, Coding, and Evidence Matrix

Core outputs: 文献编码表; 核心文献摘要; 主题标签; 资料矩阵

Minimum pass evidence: 每篇文献信息完整; 编码字段能够支持综述问题; 可以横向比较不同文献

#### R4 — Classification Framework and Research Trajectory

Core outputs: 分类框架; 研究脉络图; 主题板块说明; 发展阶段总结; 研究脉络/分类图位方案与用户选择记录

Minimum pass evidence: 分类标准明确且不重叠; 能够解释领域发展逻辑; 不是简单按年份罗列; 定量脉络图来自真实文献矩阵和Python/R运行证据；解释性脉络图的图位与结构已经用户确认

#### R5 — Comparative Evaluation and Research Limitations

Core outputs: 研究评价表; 主要不足清单; 争议与矛盾总结; 研究空白陈述

Minimum pass evidence: 评价有依据而不泛泛; 不足能够导向未来研究; 没有贬低已有研究或过度概括

#### R6 — Review Writing and Knowledge Map Presentation

Core outputs: 综述论文提纲; 正文初稿; 文献分类表; 研究脉络图/未来方向图; 全文图件地图、图位建议与用户审核状态

Minimum pass evidence: 正文按问题组织; 图表帮助理解领域结构; 评价与未来方向相互对应; 所有定量图可追溯到真实文献矩阵和Python/R运行；所有解释性或增强图均经过制作前图位确认和制作后用户审核

#### R7 — Finalization, Citation Audit, and Submission

Core outputs: 终稿; 检索与筛选附录; 引用核查清单; 修改计划

Minimum pass evidence: 检索和筛选过程透明; 核心文献无明显遗漏; 引用格式统一; 未来方向具体可研究

<!-- END GENERATED 35-STAGE MATRIX -->

## Confidence

- High: direct artifacts support every earlier pass decision.
- Medium: sufficient descriptions exist but some source files are missing.
- Low: the user description is sparse, contradictory, or cannot support earlier-stage acceptance.

Low confidence does not authorize skipping. Ask no more than three critical questions, retain the earliest plausible stage, and label downstream help provisional.

## Skip handling

If the user requests downstream writing before upstream validation, provide provisional assistance, label upstream dependencies, and keep stage status unchanged.
