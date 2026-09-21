---
title: "On Organizational Structure in the AI Era"
source: "https://zartbot.github.io/blog/misc/on_org_struct/"
author:
published:
created: 2026-09-21
description: "Why has the resource advantage of the tech giants not been steadily converted into an innovation advantage? A first-hand essay on departmental boundaries vs. knowledge boundaries, competition among high-density talent, the leader's technical taste, and organizational structure as a technical capability."
tags:
  - "clippings"
---
A very interesting topic: in this wave of AI, why is it that the traditional tech giants — with their ample capital, enormous compute, and large pools of outstanding talent — did not, as a matter of course, sweep up the most important innovations? Microsoft, Meta, Apple, AWS, and Google all have deep technical accumulation, yet the emergence of OpenAI, Anthropic, and some domestic foundation-model companies shows that the correspondence between the scale of resources and the capacity for innovation is far less direct than one might imagine.

Why has the resource advantage not been steadily converted into an innovation advantage, and what determines how these resources can be used? `Organizational structure` is very likely one of the underestimated variables among them. In an interview <sup>[1]</sup>, Liang Wenfeng remarked: **"What we lack in innovation is certainly not capital, but rather a lack of confidence and not knowing how to organize high-density talent to achieve effective innovation."** This sentence pushes a problem that is often reduced to technical roadmaps and resource investment up to the level of organizational capability. After recruiting a group of smart people, how to get them to understand problems together, to try and err together, and to convert their individual knowledge into progress for the whole system is a matter of an entirely different kind of difficulty.

## 1\. In the AI Era, Organizational Structure Is Itself a Technical Capability

Over the past few decades, large enterprises have developed a fairly mature way of organizing: dividing departments by specialty, defining boundaries by responsibility, coordinating cooperation through interfaces, and then measuring output by each department's own metrics. The compute team is responsible for compute, the network team for the network, and the storage team for storage. The upper-layer algorithm team raises requirements, the data team provides data, and the Infra team delivers infrastructure. When the technical path is relatively stable and problems can be decomposed in advance, this structure can support an enormous business scale.

But frontier AI R&D has one troublesome feature: **a great many key problems simply cannot be accurately decomposed before they are solved.**

The model architecture changes the communication pattern; communication capability affects the parallelization strategy; the parallelization strategy affects memory footprint and training efficiency. The length distribution of the data changes the compute load, and the data mixture in turn affects model convergence. A problem that looks like it belongs to algorithms may, in the end, need to be solved by adjusting the communication implementation; a problem that looks like it belongs to storage may only be solvable by changing the way data is organized. Between algorithms, data, and infrastructure, there exist a great many mutually influencing relationships.

When technical problems need to be solved as a whole, yet the organization requires each department to be responsible only for its own local metrics, the crack between the local optimum and the global optimum appears.

Imagine that the efficiency of a large-scale training run is unsatisfactory. The compute team produces its reports: GPU utilization is not low. The network team inspects the links: average bandwidth and packet-loss rate show no obvious anomalies. The storage team completes its tests: throughput meets the established standards. Every team can prove that it delivered a qualified service, yet the time the model needs to complete one round of experiments remains very long.

The problem may be hidden at the junctions of these reports. The network's average performance is normal, yet the tail latency of a few nodes may stall synchronous training. The storage system's sequential-read throughput is excellent, yet the actual data pipeline involves a great deal of small-file access and preprocessing waits. The GPUs are very busy, yet a considerable portion of that time may be consumed by redundant computation or inefficient data movement. Departmental metrics provide useful information, but only by putting them back into the same training process can one judge what is actually happening to the whole system.

Compute, network, and storage will also generate different yet reasonable demands around the same problem. To improve resource utilization, the scheduling system may tend to stuff tasks into scattered idle GPUs, but distributed training may instead need a set of machines with an appropriate topology. To reduce storage costs, the platform may restrict the use of high-performance storage, but faster checkpoint saving can support a higher saving frequency, reducing recomputation after failures, while faster recovery can shorten downtime. The cost saved by one department may reappear, at a higher price, in another.

If model researchers can only hand a fully finalized design to the Infra team and then ask them to "make it run as fast as possible," many optimization opportunities are already lost before the handoff. The two sides need to jointly judge, at an earlier stage: which algorithmic choices are worth changing the infrastructure for, and which system constraints should be fed back into the model design.

## 1.1 Departmental Boundaries vs. Knowledge Boundaries

**Knowledge boundaries are often more stubborn than departmental boundaries.** This is also the reason I have, in recent years, kept insisting on **full-stack "artificial/hand-crafted" intelligence** — many optimizations in fact lie exactly at the knowledge boundaries...

Departmental boundaries are at least visible; they can be changed by adjusting reporting relationships or setting up joint projects. Knowledge boundaries, by contrast, are often hidden within everyday communication. When an algorithm researcher says "we need a larger batch," what the Infra engineer receives is a scaling-up request, without necessarily knowing what training hypothesis is being validated behind it. When an engineer feeds back "this design's communication overhead is too high," what the researcher receives is a constraint, without necessarily knowing that switching to a different data layout or expert-placement scheme might make the design viable again.

Both sides are working conscientiously, but what gets passed across is only the conclusion; the assumptions and context that support the conclusion do not.

Tickets are good at conveying problems that have already been clearly defined. Frontier research, however, often requires a group of people to sit down and first figure out what the problem actually is. Once collaboration is compressed into "file a request, evaluate, schedule, deliver," Infra easily becomes a service department that passively takes orders, and the algorithm team easily mistakes the limitations of the existing platform for the limitations of the technology itself.

The same holds between the data team and the algorithm team. The data team may measure its work by delivery volume, cleaning progress, and processing cost, whereas the algorithm team runs experiments around final model metrics. If the two sides lack continuous feedback, data easily becomes a one-off delivered raw material. On which capabilities the model performs weakly, which samples are truly effective, and which cleaning rules mistakenly deleted valuable content — these then struggle to form a continuous validation process.

A complete improvement process should be able to start from model failure cases, form data hypotheses, adjust the data, run controlled experiments, and then feed the conclusions back into the next round of training. If these links belong separately to several teams, each with different schedules and assessment cycles, then an exploration that could originally have advanced quickly may end up waiting repeatedly during handoffs.

More thorny still, the organization sometimes requires that responsibility be assigned first before troubleshooting resources can be committed. When a loss anomaly suddenly appears in a training run, the cause may come from a data change, numerical precision, an operator implementation, or a hardware fault. When evidence is insufficient, any single team finds it very hard to localize the cause on its own. But if every team wants to first see proof that "the problem belongs to it" before it is willing to step in, troubleshooting falls into a loop. AI R&D often requires joint diagnosis first, in order to know who should solve the problem.

The impact of departmental boundaries goes beyond execution efficiency. It gradually changes what questions researchers are willing to raise.

If one idea must simultaneously coordinate the data pipeline, the training framework, and the network implementation in order to complete even its initial validation, while another idea only requires modifying a small piece of code within one's own department, then within the same performance cycle the latter is naturally more attractive. Over time, people will actively choose research directions in which resources are easy to obtain, delivery is easy, and results are easy to attribute. Those ideas with very high potential value but which require crossing multiple boundaries may not even get a first experiment.

At this point, the organizational structure has already entered the technical roadmap itself. On the surface, the company enjoys ample research freedom; in reality, which directions are easy to attempt and which are abandoned in advance have already been filtered once through budget attribution, interface constraints, and collaboration costs.

> So I quite agree with Weng Jiayi's view: "What the current AI race competes on is not algorithmic innovation, but engineering capability and iteration speed. Every company has bugs to varying degrees; whoever fixes more bugs trains a better model."
> 
> What truly hides behind this is, in fact, a great mass of details, and these details are in turn hidden within the knowledge boundaries; what is exposed to management is only the one-sided departmental boundaries, so they assume a few organizational reshuffles can solve it — but the knowledge barriers have not been broken...

## 2\. The Competition Among Smart People

From childhood on, I always studied in various pilot/experimental classes, so I can very well understand what **"competition among high-density talent"** means — and this further amplifies the organization's problems.

Smart people respond to incentives too. When promotion requires proving independent contribution, budgets require proving departmental value, and a manager's influence is tied to team size, people become motivated to build their own projects, defend their own boundaries, and emphasize their ownership of results.

Helping another team solve a key problem may be very valuable to the company, yet for the individual it does not necessarily translate easily into a clear promotion case. Distilling one's experience into a shared tool can spare many people detours, but the contribution may be scattered across others' results. By contrast, building anew a platform bearing a clear team label is, instead, more easily recognized and rewarded. Redundant construction, information hoarding, and the scramble for credit may thus become rational choices under a given evaluation system.

The stronger a person's technical ability, the more capable they are of providing a complete and persuasive justification for their own choices. A debate can be full of jargon and technical detail while at the same time being deeply shaped by resource allocation and credit attribution. When admitting that another design is better means one's own project loses its budget, technical judgment struggles to stay open.

Internal competition can help an organization explore different routes, but it requires shared evaluation standards, reproducible experimental results, and clear mechanisms for reallocating resources. If every team maintains its own evaluation criteria, stays silent about failures, and shows successes selectively, the company will find it hard to know which directions are worth continuing to invest in.

For talent density to convert into innovation density depends on one concrete condition: **sharing knowledge, exposing problems, and helping others succeed must also be worthwhile for the individual.** In fact, I have always been asking myself one question: "If you were the only person left in the whole world, would you want money or fame?" So for many years now I have kept myself in a harmless, unassuming state: for some things, it is enough that I myself know I made them succeed, and credit and the like do not matter; and I often, under the banner of "technical poverty alleviation," share knowledge with others — which brings to mind an article from a few years ago, [*Technical Poverty Alleviation and Public Intellectuals*](https://mp.weixin.qq.com/s/LYEgdBtrlTe_MgL1NEvVBw).

So where does the whole problem lie? **From an organizational standpoint, an enterprise may not lack people who understand this equation; what it lacks is the opportunity for such knowledge to meet real system problems.** It reveals a class of organizational risk: when a problem spans algorithmic assumptions and system implementation, there can always be someone responsible for local fixes, while the re-examination of the shared assumptions may go unowned for a long time. What is most worth discussing is whether the organization has the ability to recognize this vacancy and to organize the corresponding people and resources.

## 3\. The Leader's Taste

Even if a team gains the freedom to cross departmental boundaries, there is still one question to answer: what will the team use that freedom to pursue? Faced with training instability, some tend to keep tuning parameters, some hope to add a correction, and some will stop to examine what assumptions the gradient estimate is actually built upon. These choices all require time and resources, and the organization cannot try all directions at once. The core leader's taste begins to play its role precisely in such choices.

Taste can be understood as a judgment calibrated through practice. It helps a leader discern which problems are worth long-term investment, which anomalies may expose a more fundamental mechanism, which complexities genuinely come from the problem itself, and which come from the accumulation of past decisions. When the technical roadmap is not yet clear, this judgment influences where the team first places its attention, and also influences what kinds of people and ideas can gain support.

This taste must ultimately turn into resource arrangements. Adding a mechanism, besides the immediate development work, also increases the later burden of parameter tuning, troubleshooting, and maintenance. A project that has already absorbed a lot of manpower may likewise need to be scaled back or ended. The leader needs to help the team face such trade-offs, letting past investment serve as the background for decisions while placing greater weight on how much effective progress can still be gained in the future.

To make these judgments, the core leader needs to maintain sufficient technical depth. The function of depth is to raise the quality of the questions and the evidence; the concrete derivations and implementations should still be advanced by those closest to the facts. And yet in the AI era such technical depth is very difficult, and leaders often have to face being forced to make decisions in a great many domains they do not understand so well...

On the other hand, taste in choosing people also influences the organization along the same direction. Beyond professional depth, one must also recognize whether a person is willing to understand adjacent fields, whether they can explain their own judgments to colleagues of different backgrounds, and whether they will proactively revise a design into which they have already poured effort. A researcher who can connect algorithmic assumptions with system behavior may help several teams redefine a problem. This kind of contribution does not necessarily correspond to a standalone module, yet it may change the way the entire project advances.

The reward mechanism must be able to see these contributions. Finding the root cause and then deleting several layers of useless logic, proving that an expensive experiment need not be continued, turning one's own experience into a tool that other teams can reuse — all of these should enter the basis for evaluation. If the organization mainly rewards the number of projects, the volume of code, and team expansion, members will tend to add work that can be attributed to themselves. Recognizing the removal of complexity makes people more willing to put their attention on the actual improvement of the whole system.

Leaders also need to allow evidence to overturn their own preferences. A concise explanation may miss a real numerical problem, and **a measure that looks clumsy may also be irreplaceable under specific conditions**. When a researcher produces a counterexample, whether resources and direction can be adjusted accordingly is more telling than whether discussion is permitted in the meeting. When a core figure is willing to revise their judgment in public, it lowers the cost for others to expose mistakes and makes failed experiments more easily become shared knowledge.

## 4\. The Team's Problems

As a team grows, these judgments must also gradually become a basis that can be discussed and transmitted. Recording the assumptions on which important decisions depend, making clear what evidence would trigger an adjustment, and cultivating people who can take independent responsibility for problems — all of these can reduce the dependence on any individual's presence.

Concretely, in organizational design, one important starting point is to configure stably collaborating algorithm, data, and Infra members around a research goal — for example, improving long-context training efficiency, raising a certain class of reasoning capability, or lowering the inference cost of meeting an established quality requirement. The team works together starting from the goal and the hypotheses, possesses the necessary experiment quota and technical-modification privileges, and has a clearly designated owner to coordinate the trade-offs among quality, time, and cost.

Professional departments still bear the responsibilities of talent development, technical standards, and long-term infrastructure construction. Networking, storage, and training stability all require continuous professional accumulation, and making everyone responsible for everything would also dilute this capability. What needs adjusting is the mode of cooperation and the decision-making authority on key problems, so that the team can, when necessary, jointly modify implementations that cross professional boundaries.

Joint projects must have clear decision rights, avoiding the need to go back to multiple departments to seek support at every step. The members' time commitment to the project, their resource quota, and the basis for their evaluation also need to be clarified in advance. A project owner who has responsibility but no ability to mobilize resources easily becomes a meeting coordinator; and members who simultaneously shoulder several conflicting goals also find it hard to sustain their investment in the shared problem.

The organization also needs to consciously cultivate people who can cross knowledge boundaries. System engineers who understand model training, algorithm researchers who understand hardware constraints, and data engineers who can judge the value of data through model evaluation — all of these can reduce the loss of critical context during handoffs. When Anthropic introduced its interpretability team, it described a way of working in which members switch between research and engineering, and it emphasized cross-domain engineering capability and close collaboration among teams. This case illustrates one concrete way of working. Anthropic's introduction to interpretability research engineering <sup>[2]</sup>.

## 5\. Conclusion

For large enterprises, the changes of the AI era also involve the priorities of existing businesses. Mature products need stability, predictable costs, and clear delivery commitments, whereas frontier research needs to bear more uncertainty. Both are reasonable, but they require different budget rhythms and evaluation methods. If exploratory projects must always justify themselves by the quarterly-return standard of mature businesses, the organization more easily chooses improvements that can be delivered quickly, and it continuously compresses the space for fundamental innovation.

A company's size does not determine whether these problems exist. Small companies can equally suffer from information monopoly, over-centralized decision-making, and the overloading of key figures. Large companies are also fully capable of building efficient research teams by clarifying goals, adjusting authority, and changing incentives. What is worth observing is whether, after a key problem appears, the relevant people can see the evidence in time, can judge it together, and can mobilize resources to turn that judgment into experiments.

As AI tools further increase the speed of writing code, processing data, and analyzing experiments, these organizational capabilities may become even more important. If individuals execute tasks faster and faster, while the speed of acquiring context and making cross-team decisions does not change, then waiting and coordination will take up an ever-larger proportion. More output will converge before the same decision bottleneck, exposing the problems that were originally masked by execution cost.

So, discussing organizational structure in the AI era must ultimately come down to some very concrete matters: after a researcher discovers an anomaly, whom can they directly find; how long does a cross-disciplinary idea take to get its first validation; can a single failure help all the relevant teams avoid detours; when a person helps others achieve a breakthrough, can they be recognized just the same; and can a judgment put forward by the core leader be changed by new evidence.

Capital can buy machines, and salaries can attract talent. The organization needs to go further and create the conditions for these people to understand one another's work, to revise shared judgments, and to turn scattered professional capabilities into collective knowledge that accumulates continuously. When the most valuable problems keep appearing at the junctions between departments, the organization must let knowledge, resources, and decisions cross these boundaries in time. The core leader's taste, in turn, must enable more people to gain the ability to make reliable judgments independently. In this sense, organizational structure itself has already become part of AI's technical capability.

References

\[1\]

Liang Wenfeng interview: [https://finance.sina.com.cn/roll/2024-07-22/doc-inceypaf4744158.shtml](https://finance.sina.com.cn/roll/2024-07-22/doc-inceypaf4744158.shtml)

\[2\]

Anthropic's introduction to interpretability research engineering: [https://www.anthropic.com/research/engineering-challenges-interpretability](https://www.anthropic.com/research/engineering-challenges-interpretability)