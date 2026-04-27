---
title: "Chapter 3 Contribution 1: Improving Read Alignment by Exploring a Sequence Transformation Space | From sequences to knowledge, improving and learning from sequence alignments"
source: "https://thesis.lucblassel.com/HPC-paper.html"
author:
  - "[[Luc Blassel]]"
published:
created: 2026-04-26
description: "Chapter 3 Contribution 1: Improving Read Alignment by Exploring a Sequence Transformation Space | From sequences to knowledge, improving and learning from sequence alignments"
tags:
---
## Chapter 3 Contribution 1: Improving Read Alignment by Exploring a Sequence Transformation Space

Recall that, when using long-read sequencing technologies, sequencing errors are more frequent than when using short-read sequencing. The most common of these sequencing errors are linked to homopolymers ([1.4.2](https://thesis.lucblassel.com/what-is-sequence-data.html#homopolymers-and-long-reads)). In read-mapping analyses, a short sequence is globally aligned to a much longer reference sequence. Mapping long-reads can help bridge some gaps in knowledge and solve problems impossible to solve with shorter reads, however sequencing errors complicate an already complicated task ([2.3](https://thesis.lucblassel.com/aligning-sequence-data.html#the-specificities-of-read-mapping)). Homopolymer compression ([1.4.3.2](https://thesis.lucblassel.com/what-is-sequence-data.html#hpc-trick)) has been successfully used to mitigate some of the effects of these errors and improve long-read mapping analyses. There might, however, be rooom for improvement and alternative sequence transformation procedures that improve long-read mapping more than homopolymer compression.

This chapter was written as an article titled: **“Mapping-friendly sequence reductions: going beyond homopolymer compression”**. It is currently in press for the iScience proceedings of the RECOMB-SEQ 2022 conference and is presented as is, without any modification from the submitted version. The author list, complete with affiliations is given below:  

Luc Blassel <sup><strong>1</strong>,<strong>2</strong> *</sup>, Paul Medvedev <sup><strong>3</strong>,<strong>4</strong>,<strong>5</strong></sup>, Rayan Chikhi <sup><strong>1</strong></sup>

**1** Sequence Bioinformatics, Department of Computational Biology, Institut Pasteur, Paris, France  
**2** Sorbonne Université, Collège doctoral, Paris, France  
**3** Department of Computer Science and Engineering, Pennsylvania State University, University Park, Pennsylvania, United States of America  
**4** Department of Biochemistry and Molecular Biology, Pennsylvania State University, University Park, Pennsylvania, United States of America  
**5** Center for Computational Biology and Bioinformatics, Pennsylvania State University, University Park, Pennsylvania, United States of America  

## Highlights

- Mapping-friendly sequence reductions (MSRs) are functions that transform DNA sequences.
- They are a generalization of the concept of homopolymer compression.
- We show that some well-chosen MSRs enable more accurate long read mapping.

## Graphical abstract

![](https://thesis.lucblassel.com/figures/HPC-MSRs/abstract.png)

## Abstract

Sequencing errors continue to pose algorithmic challenges to methods working with sequencing data. One of the simplest and most prevalent techniques for ameliorating the detrimental effects of homopolymer expansion/contraction errors present in long reads is homopolymer compression. It collapses runs of repeated nucleotides, to remove some sequencing errors and improve mapping sensitivity. Though our intuitive understanding justifies why homopolymer compression works, it in no way implies that it is the best transformation that can be done. In this paper, we explore if there are transformations that can be applied in the same pre-processing manner as homopolymer compression that would achieve better alignment sensitivity. We introduce a more general framework than homopolymer compression, called mapping-friendly sequence reductions. We transform the reference and the reads using these reductions and then apply an alignment algorithm. We demonstrate that some mapping-friendly sequence reductions lead to improved mapping accuracy, outperforming homopolymer compression.

## 3.1 Introduction

Sequencing errors continue to pose algorithmic challenges to methods working with read data. In short-read technologies, these tend to be substitution errors, but in long reads, these tend to be short insertions and deletions; most common are expansions or contractions of homopolymers (i.e. reporting 3 As instead of 4) [^2]. Many algorithmic problems, such as alignment, become trivial if not for sequencing errors [^10]. Error correction can often decrease the error rate but does not eliminate all errors. Most tools therefore incorporate the uncertainty caused by errors into their underlying algorithms. The higher the error rate, the more detrimental its effect on algorithm speed, memory, and accuracy. While the sequencing error rate of any given technology tends to decrease over time, new technologies entering the market typically have high error rates (e.g. Oxford Nanopore Technologies). Finding better ways to cope with sequencing error therefore remains a top priority in bioinformatics.

One of the simplest and most prevalent techniques for ameliorating the detrimental effects of homopolymer expansion/contraction errors is *homopolymer compression* (abbreviated HPC). HPC simply transforms runs of the same nucleotide within a sequence into a single occurrence of that nucleotide. For example, HPC applied to the sequence AAAGGTTA yields the sequence AGTA. To use HPC in an alignment algorithm, one first compresses the reads and the reference, then aligns each compressed read to the compressed reference, and finally reports all alignment locations, converted into the coordinate system of the uncompressed reference. HPC effectively removes homopolymer expansion/contraction errors from the downstream algorithm. Though there is a trade-off with specificity of the alignment (e.g. some of the compressed alignments may not correspond to true alignments) the improvement in mapping sensitivity usually outweighs it [^8].

The first use of HPC that we are aware of was in 2008 as a pre-processing step for 454 pyrosequencing data in the Celera assembler [^5]. It is used by a wide range of error-correction algorithms, e.g. for 454 data [^13], PacBio data [^7], and Oxford Nanopore data [^14]. HPC is used in alignment, e.g. by the widely used minimap2 aligner [^8]. HPC is also used in long-read assembly, e.g. HiCanu [^3], SMARTdenovo [^15], or mdBG [^4]. HPC is also used for clustering transcriptome reads according to gene family of origin [^6]. Overall, HPC has been widely used, with demonstrated benefits.

Though our intuitive understanding justifies why HPC works, it in no way implies that it is the best transformation that can be done. Are there transformations that can be applied in the same pre-processing way as HPC that would achieve better alignment sensitivity? In this work, we define a more general notion which we call *mapping-friendly sequence reductions*. In order to efficiently explore the performance of all reductions, we identify two heuristics to reduce the search space of reductions. We then identify a number of mapping-friendly sequence reductions which are likely to yield better mapping performance than HPC. We evaluate them using two mappers (`minimap2` and `winnowmap2`) on three simulated datasets (whole human genome, human centromere, and whole *Drosophila* genome). We show that some of these functions provide vastly superior performance in terms of correctly placing high mapping quality reads, compared to either HPC or using raw reads. For example, one function decreased the mapping error rate of `minimap2` by an order of magnitude over the entire human genome, keeping an identical fraction of reads mapped.

We also evaluate whether HPC sensitivity gains continue to outweigh the specificity cost with the advent of telomere-to-telomere assemblies [^1]. These contain many more low-complexity and/or repeated regions such as centromeres and telomeres. HPC may increase mapping ambiguity in these regions by removing small, distinguishing, differences between repeat instances. Indeed, we find that neither HPC nor our mapping-friendly sequence reductions perform better than mapping raw reads on centromeres, hinting at the importance of preserving all sequence information in repeated regions.

## 3.2 Results

### 3.2.1 Streaming sequence reductions

We wish to extend the notion of homopolymer compression to a more general function while maintaining its simplicity. What makes HPC simple is that it can be done in a streaming fashion over the sequence while maintaining only a local context. The algorithm can be viewed simply as scanning a string from left to right and, at each new character, outputting that character if and only if it is different from the previous character. In order to prepare for generalizing this algorithm, let us define a function gHPC:Σ2→Σ∪{ε} $gHPC:Σ2→Σ∪{ε}$ $g^\text{HPC} : \Sigma^2\rightarrow\Sigma\cup\{\varepsilon\}$ where Σ $Σ$ $\Sigma$ is the DNA alphabet, ε $ε$ $\varepsilon$ is the empty character, and

gHPC(x1⋅x2)={x2if x1≠x2εif x1=x2 
$$
gHPC(x1⋅x2)={x2if x1≠x2εif x1=x2
$$
 
$$
\begin{align*}
    & g^\text{HPC}(x_1\cdot x_2) =
    \begin{cases}
        x_2 & \text{if } x_1 \neq x_2 \\
        \varepsilon & \text{if } x_1 = x_2
    \end{cases}
\end{align*}
$$

Now, we can view HPC as sliding a window of size 2 over the sequence and at each new window, applying gHPC $gHPC$ $g^\text{HPC}$ to the window and concatenating the output to the growing compressed string. Formally, let x $x$ $x$ be a string, which we index starting from 1. Then, the HPC transformation is defined as

f(x)=x\[1,ℓ−1\]⋅g(x\[1,ℓ\])⋅g(x\[2,ℓ+1\])⋯g(x\[|x|−ℓ+1,|x|\])(3.1) 
$$
(3.1)f(x)=x[1,ℓ−1]⋅g(x[1,ℓ])⋅g(x[2,ℓ+1])⋯g(x[|x|−ℓ+1,|x|])
$$
 
$$
\begin{equation}
  f(x) = x[1,\ell-1]\cdot g(x[1,\ell]) \cdot g(x[2, \ell+1])\cdots g(x[|x|-\ell+1,|x|])
  \tag{3.1}
\end{equation}
$$

where ℓ=2 $ℓ=2$ $\ell = 2$ and g=gHPC $g=gHPC$ $g=g^\text{HPC}$. In other words, f $f$ $f$ is the concatenation of the first ℓ−1 $ℓ−1$ $\ell-1$ characters of x $x$ $x$ and the sequence of outputs of g $g$ $g$ applied to a sliding window of length ℓ $ℓ$ $\ell$ over x $x$ $x$. The core of the transformation is given by g $g$ $g$ and the size of the context ℓ $ℓ$ $\ell$, and f $f$ $f$ is simply the wrapper for g $g$ $g$ so that the transformation can be applied to arbitrary length strings.

With this view in mind, we can generalize HPC while keeping its simplicity by 1) considering different functions g $g$ $g$ that can be plugged into Equation [(3.1)](https://thesis.lucblassel.com/HPC-paper.html#eq:MSR) increasing the context that g $g$ $g$ uses (i.e. setting ℓ>2 $ℓ>2$ $\ell>2$). Formally, for a given alphabet Σ $Σ$ $\Sigma$ and a context size ℓ $ℓ$ $\ell$, a function T $T$ $T$ mapping strings to strings is said to be an *order-* ℓ $ℓ$ $\ell$ Streaming sequence reduction (abbreviated *SSR*) if there exists some g:Σℓ→Σ∪{ε} $g:Σℓ→Σ∪{ε}$ $g : \Sigma^\ell\rightarrow\Sigma\cup\{\varepsilon\}$ such that T=f $T=f$ $T=f$.

Figure [3.1](https://thesis.lucblassel.com/HPC-paper.html#fig:countingMSRs) A shows how an SSR can be visualized as a directed graph. Observe that an order- ℓ $ℓ$ $\ell$ SSR is defined by a mapping between |Σ|ℓ $|Σ|ℓ$ $|\Sigma|^\ell$ inputs and |Σ|+1 $|Σ|+1$ $|\Sigma| + 1$ outputs. For example, for ℓ=2 $ℓ=2$ $\ell=2$, there are n=16 $n=16$ $n=16$ inputs and k=5 $k=5$ $k=5$ outputs. Figure [3.1](https://thesis.lucblassel.com/HPC-paper.html#fig:countingMSRs) B visualizes HPC in this way.

 $**Representing and counting Streaming sequence reductions.**  
**A**: General representation of an order-2 Streaming sequence
reduction as a mapping of 16 input dinucleotides, to the 4 nucleotide
outputs and the empty character $\varepsilon$. **B**: Homopolymer
compression is an order-2 SSR. All dinucleotides except those that
contain the same nucleotide twice map to the second nucleotide of the
pair. The 4 dinucleotides that are the two same nucleotides map to the
empty character $\varepsilon$. **C**: Our RC-core-insensitive order-2
SSRs are mappings of the 6 representative dinucleotide inputs to the 4
nucleotide outputs and the empty character $\varepsilon$. The 4
dinucleotides that are their own reverse complement are always mapped to
$\varepsilon$. The remaining 6 dinucleotides are mapped to the
complement of the mapped output of the reverse complement dinucleotide
input. For example, if AA is mapped to C, then TT (the reverse
complement of AA) will be mapped to G (the complement of C). **D**:
Number of possible SSR mappings under the different restrictions
presented in the main text. All mappings from 16 dinucleotide inputs to
5 outputs (as in panel A) are represented by the outermost circle. All
RC-core-insensitive mappings (as in panel C) are represented by the
medium circle. All RC-core-insensitive mappings with only one
representative of each equivalence class are represented by the
innermost circle.$

Figure 3.1: **Representing and counting Streaming sequence reductions.**  
**A**: General representation of an order-2 Streaming sequence reduction as a mapping of 16 input dinucleotides, to the 4 nucleotide outputs and the empty character ε $ε$. **B**: Homopolymer compression is an order-2 SSR. All dinucleotides except those that contain the same nucleotide twice map to the second nucleotide of the pair. The 4 dinucleotides that are the two same nucleotides map to the empty character ε $ε$. **C**: Our RC-core-insensitive order-2 SSRs are mappings of the 6 representative dinucleotide inputs to the 4 nucleotide outputs and the empty character ε $ε$. The 4 dinucleotides that are their own reverse complement are always mapped to ε $ε$. The remaining 6 dinucleotides are mapped to the complement of the mapped output of the reverse complement dinucleotide input. For example, if AA is mapped to C, then TT (the reverse complement of AA) will be mapped to G (the complement of C). **D**: Number of possible SSR mappings under the different restrictions presented in the main text. All mappings from 16 dinucleotide inputs to 5 outputs (as in panel A) are represented by the outermost circle. All RC-core-insensitive mappings (as in panel C) are represented by the medium circle. All RC-core-insensitive mappings with only one representative of each equivalence class are represented by the innermost circle.

Since we aim to use SSRs in the context of sequencing data, we need to place additional restrictions on how they handle reverse complements. For example, given two strings x $x$ $x$ (e.g. a read) and y $y$ $y$ (e.g. a substring of the reference), a mapper might check if x=RC(y) $x=RC(y)$ $x = RC(y)$. When strings are pre-processed using an SSR f $f$ $f$, it will end up checking if f(x)=RC(f(y)) $f(x)=RC(f(y))$ $f(x) = RC(f(y))$. However, x=RC(y) $x=RC(y)$ $x = RC(y)$ only implies that f(x)=f(RC(y)) $f(x)=f(RC(y))$ $f(x) = f(RC(y))$. In order to have it also imply that f(x)=RC(f(y)) $f(x)=RC(f(y))$ $f(x) = RC(f(y))$, we need f $f$ $f$ to be commutative with RC, i.e. applying SSR then RC needs to be equivalent to applying RC then SSR. We say that f $f$ $f$ is *RC-insensitive* if for all x $x$ $x$, f(RC(x))=RC(f(x)) $f(RC(x))=RC(f(x))$ $f(RC(x))= RC(f(x))$. Observe that HPC is RC-insensitive.

### 3.2.2 Restricting the space of streaming sequence reductions

To discover SSRs that improve mapping performance, our strategy is to put them all to the test by evaluating the results of an actual mapping software over a simulated test dataset reduced by each SSR. However, even with only 16 $16$ $16$ inputs and 5 $5$ $5$ outputs, the number of possible g $g$ $g$ mappings for order-2 SSRs is 516≈1.5⋅1011 $516≈1.5⋅1011$ $5^{16}\approx 1.5\cdot10^{11}$, which is prohibitive to enumerate. In this section, we describe two ideas for reducing the space of SSRs that we will test. In subsection [3.2.2.1](https://thesis.lucblassel.com/HPC-paper.html#sec:rc-insensitive), we show how the restriction to RC-insensitive mappings can be used to reduce the search space. In subsection [3.2.2.2](https://thesis.lucblassel.com/HPC-paper.html#sec:equiv), we exploit the natural symmetry that arises due to Watson-Crick complements to further restrict the search space.

These restrictions reduce the number of order-2 SSRs to only, making it feasible to test all of them. Figure [3.1](https://thesis.lucblassel.com/HPC-paper.html#fig:countingMSRs) D shows an overview of our restriction process.

#### 3.2.2.1 Reverse complement-core-insensitive streaming sequence reductions

Consider an SSR defined by a function g $g$ $g$, as in Equation [(3.1)](https://thesis.lucblassel.com/HPC-paper.html#eq:MSR). Throughout this paper we will consider SSRs that have a related but weaker property than RC-insensitive. We say that an SSR is *RC-core-insensitive* if the function g $g$ $g$ that defines it has the property that for every ℓ $ℓ$ $\ell$ -mer x $x$ $x$ and its reverse complement y $y$ $y$, we have that either g(x) $g(x)$ $g(x)$ is the reverse complement of g(y) $g(y)$ $g(y)$ or g(x)=g(y)=ε $g(x)=g(y)=ε$ $g(x) = g(y) = \varepsilon$. We will restrict our SSR search space to RC-core-insensitive reductions in order to reduce the number of SSRs we will need to test.

Let us consider what this means for the case of ℓ=2 $ℓ=2$ $\ell=2$, which will be the focal point of our experimental analysis. There are 16 ℓ $ℓ$ $\ell$ -mers(i.e. dinucleotides) in total. Four of them are their own reverse complement: AT, TA, GC, CG. The RC-core-insensitive restriction forces g $g$ $g$ to map each of these to ε $ε$ $\varepsilon$, since a single nucleotide output cannot be its own reverse complement. This leaves 12 ℓ $ℓ$ $\ell$ -mers, which can be broken down into 6 pairs of reverse complements. For each pair, we can order them in lexicographical order and write them as (AA,TT),(AC,GT),(AG,CT),(CA,TG),(CC,GG),$(AA,TT),(AC,GT),(AG,CT),(CA,TG),(CC,GG),$ $(AA,TT), (AC,GT), (AG,CT), (CA,TG), (CC,GG),$ and (GA,TC) $(GA,TC)$ $(GA,TC)$. Defining g $g$ $g$ can then be done by assigning an output nucleotide to the first ℓ $ℓ$ $\ell$ -mer in each of these pairs (Figure [3.1](https://thesis.lucblassel.com/HPC-paper.html#fig:countingMSRs) C). For example, we can define an SSR by assigning g(AA)=C $g(AA)=C$ $g(AA) = C$, g(AC)=C $g(AC)=C$ $g(AC) = C$, g(AG)=A $g(AG)=A$ $g(AG) = A$, g(CA)=A $g(CA)=A$ $g(CA) = A$, g(CC)=T $g(CC)=T$ $g(CC) = T$, and g(GA)=G $g(GA)=G$ $g(GA) = G$. As an example, let us apply the corresponding SSR to an example read r $r$ $r$:

r=TAAGTTGAf(RC(r))=TCACCTGf(r)=TCAGGTGRC(f(r))=CACCTGARC(r)=TCAACTTA 
$$
r=TAAGTTGAf(RC(r))=TCACCTGf(r)=TCAGGTGRC(f(r))=CACCTGARC(r)=TCAACTTA
$$
 
$$
\begin{align*}
    r & = \text{TAAGTTGA}    & f(RC(r)) &=\color{red}{\text{T}}\color{green}{\text{CACCTG}} \\
    f(r) & =\text{TCAGGTG}   & RC(f(r)) &=\;\;\;\color{green}{\text{CACCTG}}\color{red}{\text{A}} \\
    RC(r) & =\text{TCAACTTA} & &
\end{align*}
$$

Observe that the first ℓ−1 $ℓ−1$ $\ell-1$ nucleotides of r $r$ $r$ (shown in red) are copied as-is, since we do not apply g $g$ $g$ on them (as per Equation [(3.1)](https://thesis.lucblassel.com/HPC-paper.html#eq:MSR)). As we see in this example, this implies that f(RC(r)) $f(RC(r))$ $f(RC(r))$ is not necessarily equal to RC(f(r)) $RC(f(r))$ $RC(f(r))$; thus an RC-core-insensitive SSR is not necessarily an RC-insensitive SSR. However, an RC-core-insensitive SSR has the property that for all strings r $r$ $r$, we have f(RC(r))\[ℓ,|r|\])=RC(f(r))\[1,|r|−ℓ+1\] $f(RC(r))[ℓ,|r|])=RC(f(r))[1,|r|−ℓ+1]$ $f(RC(r))[\ell, |r|]) = RC(f(r))[1, |r| - \ell + 1]$. In other words, if we drop the ℓ−1 $ℓ−1$ $\ell - 1$ prefix of f(RC(r)) $f(RC(r))$ $f(RC(r))$ and the ℓ−1 $ℓ−1$ $\ell - 1$ suffix of RC(f(r)) $RC(f(r))$ $RC(f(r))$, then the two strings are equal. Though we no longer have the strict RC-insensitive property, this new property suffices for the purpose of mapping long reads. Since the length of the read sequences will be much greater than ℓ $ℓ$ $\ell$ (in our results we will only use ℓ=2 $ℓ=2$ $\ell=2$), having a mismatch in the first or last nucleotide will be practically inconsequential.

It is important to note though that there may be other RC-insensitive functions not generated by this construction. For instance, HPC cannot be derived using this method (as it does not map the di-nucleotides AT,TA,GC and CG to ε $ε$ $\varepsilon$), and yet it is RC-insensitive.

We can count the number of RC-core-insensitive SSRs. Let us define i(ℓ) $i(ℓ)$ $i(\ell)$ the number of input assignments necessary to fully determine the RC-core-insensitive SSR; one can think of this as the degrees-of-freedom in choosing g $g$ $g$. As we showed, for ℓ=2 $ℓ=2$ $\ell=2$, we have i(ℓ)=6 $i(ℓ)=6$ $i(\ell)=6$. The number of RC-core-insensitive SSRs is then 5i(ℓ) $5i(ℓ)$ $5^{i(\ell)}$. Therefore, for ℓ=2 $ℓ=2$ $\ell=2$, instead of 516 $516$ $5^{16}$ possible mappings we have at most 56≈1.5⋅104 $56≈1.5⋅104$ $5^{6}\approx1.5\cdot10^{4}$ RC-core-insensitive mappings (Figure [3.1](https://thesis.lucblassel.com/HPC-paper.html#fig:countingMSRs) D). For an odd ℓ>2 $ℓ>2$ $\ell>2$, there are no ℓ $ℓ$ $\ell$ -mers that are their own reverse complements, hence i(ℓ)=4ℓ/2 $i(ℓ)=4ℓ/2$ $i(\ell)=4^\ell/2$. If ℓ $ℓ$ $\ell$ is even then there are 4ℓ/2 $4ℓ/2$ $4^{\ell/2}$ inputs that are their own reverse complements (i.e. we take all possible sequences of length ℓ/2 $ℓ/2$ $\ell/2$ and reconstruct the other half with reverse complements). Thus, i(ℓ)=(4ℓ−4ℓ/2)/2 $i(ℓ)=(4ℓ−4ℓ/2)/2$ $i(\ell)=(4^\ell- 4^{\ell/2})/2$.

#### 3.2.2.2 Equivalence classes of SSRs

Non mapping-related preliminary tests led us to hypothesize that swapping A↔T $A↔T$ $A\leftrightarrow T$ and/or C↔G $C↔G$ $C\leftrightarrow G$, as well as swapping the whole A/T $A/T$ $A/T$ pair with the C/G $C/G$ $C/G$ pair in the SSR outputs would have a negligible effect on performance. In other words, we could exchange the letters of the output in a way that preserves the Watson-Crick complementary relation. Intuitively, this can be due to the symmetry induced by reverse complements in nucleic acid strands, though we do not have a more rigorous explanation for this effect. In this section, we will formalize this observation by defining the notion of SSR equivalence. This will reduce the space of SSRs that we will need to consider by allowing us to evaluate only one SSR from each equivalence class.

Consider an RC-core-insensitive SSR defined by a function g $g$ $g$, as in Equation [(3.1)](https://thesis.lucblassel.com/HPC-paper.html#eq:MSR). An ℓ $ℓ$ $\ell$ -mer is canonical if it is the not lexicographically larger than its reverse complement. Let I $I$ $I$ be the set of all ℓ $ℓ$ $\ell$ -mers that are canonical. Such an SSR’s *dimension* k $k$ $k$ is the number of distinct nucleotides that can be output by g $g$ $g$ on inputs from I $I$ $I$ (not counting ε $ε$ $\varepsilon$). The dimension can range from 1 $1$ $1$ to 4 $4$ $4$. Next, observe that g $g$ $g$ maps all elements of I $I$ $I$ to one of k+1 $k+1$ $k+ 1$ values (i.e. Σ∪ε $Σ∪ε$ $\Sigma \cup \varepsilon$). The output of g $g$ $g$ on ℓ $ℓ$ $\ell$ -mers not in I $I$ $I$ is determined by its output on ℓ $ℓ$ $\ell$ -mers in I $I$ $I$, since we assume the SSR is RC-core-insensitive. We can therefore view it as a partition of I $I$ $I$ into k+1 $k+1$ $k+1$ sets S0 $S0$ $S_0$, …, Sk $Sk$ $S_k$, and then having a function t $t$ $t$ that is an injection from {1,…,k} ${1,…,k}$ $\{1, \ldots, k\}$ to Σ $Σ$ $\Sigma$ that assigns an output letter to each partition. Further, we permanently assign the output letter for S0 $S0$ $S_0$ to be ε $ε$ $\varepsilon$. Note that while S0 $S0$ $S_0$ could be empty, S1,…,Sk $S1,…,Sk$ $S_1, \ldots, S_k$ cannot be empty by definition of dimension. For example, the SSR used in Section [3.2.2.1](https://thesis.lucblassel.com/HPC-paper.html#sec:rc-insensitive) has dimension four and corresponds to the partition S0={},S1={AG,CA} $S0={},S1={AG,CA}$ $S_0 = \{\}, S_1=\{AG,CA\}$, S2={CC} $S2={CC}$ $S_2=\{CC\}$, S3={AA,AC} $S3={AA,AC}$ $S_3=\{AA,AC\}$, S4={GA} $S4={GA}$ $S_4=\{GA\}$, and to the injection t(1)=A $t(1)=A$ $t(1) = A$, t(2)=T $t(2)=T$ $t(2) =T$, t(3)=C $t(3)=C$ $t(3) = C$, and t(4)=G $t(4)=G$ $t(4) = G$.

Let IsComp(x,y) $IsComp(x,y)$ $IsComp(x,y)$ be a function that returns true if two nucleotides x,y∈Σ∪{ε} $x,y∈Σ∪{ε}$ $x, y \in \Sigma \cup \{\varepsilon\}$ are Watson-Crick complements, and false otherwise. Consider two SSRs of dimension k $k$ $k$ defined by S0,…,Sk,t $S0,…,Sk,t$ $S_0, \ldots, S_k, t$ and S′0,,S′k,t′ $S0′,,Sk′,t′$ $S'_0, , S'_k, t'$, respectively. We say that they are equivalent iff all the following conditions are met:

- S0=S′0 $S0=S0′$ $S_0 = S'_0$,
- there exists a permutation π $π$ $\pi$ of {1,…,k} ${1,…,k}$ $\{1,\ldots, k\}$ such that for all 1≤i≤k $1≤i≤k$ $1 \leq i \leq k$, we have Si=S′π(i) $Si=Sπ(i)′$ $S_i = S'_{\pi(i)}$,
- for all 1≤i<j≤k $1≤i<j≤k$ $1 \leq i < j \leq k$, we have IsComp(t(i),t(j))=IsComp(t′(π(i)),t′(π(j))) $IsComp(t(i),t(j))=IsComp(t′(π(i)),t′(π(j)))$ $IsComp(t(i), t(j)) = IsComp(t'(\pi(i)), t'(\pi(j)))$.

One can verify that this definition is indeed an equivalence relation, i.e. it is reflexive, symmetric, and transitive. Therefore, we can partition the set of all SSRs into equivalence classes based on this equivalence relation. One caveat is that a single SSR defined by a function g $g$ $g$ may correspond to multiple SSRs of the form S0,…,Sk,t $S0,…,Sk,t$ $S_0,\ldots,S_k,t$. However, these multiple SSRs are equivalent, hence the resulting equivalence classes are not affected. Furthermore, we can assume that there is some rule to pick one representative SSR for its equivalence class; the rule itself does not matter in our case.

Figure [3.2](https://thesis.lucblassel.com/HPC-paper.html#fig:figMSRConfigs) shows the equivalence classes for ℓ=2 $ℓ=2$ $\ell=2$, for a fixed partition. An equivalence class can be defined by which pair of classes Si $Si$ $S_i$ and Sj $Sj$ $S_j$ have complementary outputs under t $t$ $t$ and t′ $t′$ $t'$. Let us define o(k) $o(k)$ $o(k)$ as the number of equivalence classes for a given partition and a given k $k$ $k$. Then Figure [3.2](https://thesis.lucblassel.com/HPC-paper.html#fig:figMSRConfigs) shows that o(1)=1 $o(1)=1$ $o(1)=1$, o(2)=2 $o(2)=2$ $o(2)=2$ and o(3)=o(4)=3 $o(3)=o(4)=3$ $o(3) = o(4) = 3$. There are thus only 9 equivalence classes for a given partition.

 $**SSR equivalence classes for a fixed partition of the inputs.**  
$S_0$ is always assigned $\varepsilon$, so it is represented by a gray
node. A blue link between $S_i$ and an $S_j$ denotes that
$\textsc{IsComp}(t(i), t(j))=\text{true}$. The equivalence classes are
determined by the Watson-Crick complementary relationships between the
rest of the parts, i.e. by all the possible ways to draw the blue links.$

Figure 3.2: **SSR equivalence classes for a fixed partition of the inputs.**  
S0 $S0$ is always assigned ε $ε$, so it is represented by a gray node. A blue link between Si $Si$ and an Sj $Sj$ denotes that IsComp(t(i),t(j))=true $IsComp(t(i),t(j))=true$. The equivalence classes are determined by the Watson-Crick complementary relationships between the rest of the parts, i.e. by all the possible ways to draw the blue links.

#### 3.2.2.3 Counting the number of restricted SSRs

In this section, we derive a formula for the number of restricted SSRs, i.e. SSRs that are RC-core-insensitive and that are representative for their equivalence class. Consider the class of RC-core-insensitive SSRs with dimension k $k$ $k$. In subsection [3.2.2.1](https://thesis.lucblassel.com/HPC-paper.html#sec:rc-insensitive), we derived that the degrees-of-freedom in assigning ℓ $ℓ$ $\ell$ -mers to an output is i(ℓ)=4ℓ/2 $i(ℓ)=4ℓ/2$ $i(\ell) = 4^\ell/2$ if ℓ $ℓ$ $\ell$ is odd and i(ℓ)=(4ℓ−4ℓ/2)/2 $i(ℓ)=(4ℓ−4ℓ/2)/2$ $i(\ell) = (4^\ell - 4^{\ell / 2})/2$ if ℓ $ℓ$ $\ell$ is even. Let C(ℓ,k) $C(ℓ,k)$ $C(\ell,k)$ be the number of ways that i(ℓ) $i(ℓ)$ $i(\ell)$ ℓ $ℓ$ $\ell$ -mers can be partitioned into k+1 $k+1$ $k+1$ sets S0,…,Sk $S0,…,Sk$ $S_0, \ldots, S_k$, with S1,…,Sk $S1,…,Sk$ $S_1, \ldots, S_k$ required to be non-empty. Then, in subsection [3.2.2.2](https://thesis.lucblassel.com/HPC-paper.html#sec:equiv), we have derived o(k) $o(k)$ $o(k)$, the number of SSR equivalence classes for each such partition. The number of restricted SSRs can then be written as

N(ℓ)=4∑k=1C(ℓ,k)⋅o(k)(3.2) 
$$
(3.2)N(ℓ)=∑k=14C(ℓ,k)⋅o(k)
$$
 
$$
\begin{equation}
N(\ell) = \sum_{k=1}^{4} C(\ell, k) \cdot o(k)
\tag{3.2}
\end{equation}
$$

To derive the formula for C(ℓ,k) $C(ℓ,k)$ $C(\ell, k)$, we first recall that the number of ways to partition n $n$ $n$ elements into k $k$ $k$ non-empty sets is known as the Stirling number of the second kind and is denoted by {nk} ${nk}$ $\tiny\bigg\{%
\begin{matrix}
    n \\
    k
\end{matrix}
\bigg\}$ [^16]. It can be computed using the formula

{nk}=1k!k∑i=0(−1)i(ki)(k−i)n 
$$
{nk}=1k!∑i=0k(−1)i(ki)(k−i)n
$$
 
$$
\begin{equation*}
    \bigg\{%
\begin{matrix}
    n \\
    k
\end{matrix}
\bigg\}  = \frac{1}{k!}\sum_{i=0}^k(-1)^i\bigg(
\begin{matrix}
    k \\
    i
\end{matrix}
\bigg) (k-i)^n
\end{equation*}
$$

Let j $j$ $j$ be the number of the i(ℓ) $i(ℓ)$ $i(\ell)$ ℓ $ℓ$ $\ell$ -mers that are assigned to S0 $S0$ $S_0$. Note this does not include the ℓ $ℓ$ $\ell$ -mers that are self-complementary that are forced to be in S0 $S0$ $S_0$. Let C(ℓ,k,j) $C(ℓ,k,j)$ $C(\ell,k,j)$ be the number of ways that i(ℓ) $i(ℓ)$ $i(\ell)$ ℓ $ℓ$ $\ell$ -mers can be partitioned into k+1 $k+1$ $k+1$ sets S0,…,Sk $S0,…,Sk$ $S_0, \ldots, S_k$, such that j $j$ $j$ of the ℓ $ℓ$ $\ell$ -mers go into |S0| $|S0|$ $|S_0|$ and S1,…,Sk $S1,…,Sk$ $S_1, \ldots, S_k$ to are non-empty. We need to consider several cases depending on the value of j $j$ $j$:

- In the case that j=0 $j=0$ $j = 0$, we are partitioning the i(ℓ) $i(ℓ)$ $i(\ell)$ inputs among non-empty sets S1,…,Sk $S1,…,Sk$ $S_1, \ldots, S_k$. Then C(ℓ,k,j)={i(ℓ)k} $C(ℓ,k,j)={i(ℓ)k}$ $C(\ell, k,j) = \tiny{\bigg\{%
	\begin{matrix}
	    i(\ell) \\
	    k
	\end{matrix}
	\bigg\} }$.
- In the case that 1≤j≤i(ℓ)−k $1≤j≤i(ℓ)−k$ $1 \leq j \leq i(\ell) - k$, there are (i(ℓ)j) $(i(ℓ)j)$ $\tiny{\bigg(
	\begin{matrix}
	    i(\ell) \\
	    j
	\end{matrix}
	\bigg) }$ ways to choose which j $j$ $j$ ℓ $ℓ$ $\ell$ -mers are in S0 $S0$ $S_0$, and {i(ℓ)−jk} ${i(ℓ)−jk}$ $\tiny{\bigg\{%
	\begin{matrix}
	    i(\ell) - j \\
	    k
	\end{matrix}
	\bigg\} }$ ways to partition the remaining ℓ $ℓ$ $\ell$ -mers into S1,…,Sk $S1,…,Sk$ $S_1, \ldots, S_k$. Hence, C(ℓ,k,j)=(i(ℓ)j){i(ℓ)−jk} $C(ℓ,k,j)=(i(ℓ)j){i(ℓ)−jk}$ $C(\ell, k,j) = \tiny{\bigg(
	\begin{matrix}
	    i(\ell) \\
	    j
	\end{matrix}
	\bigg) }\tiny{\bigg\{%
	\begin{matrix}
	    i(\ell) - j \\
	    k
	\end{matrix}
	\bigg\} }$.
- In the case that j>i(ℓ)−k $j>i(ℓ)−k$ $j > i(\ell) - k$, it is impossible to partition the remaining k $k$ $k$ (or fewer) ℓ $ℓ$ $\ell$ -mers into S1,…,Sk $S1,…,Sk$ $S_1, \ldots, S_k$ such that the sets are non-empty. Recall that as we assume the dimension is k $k$ $k$, each set must contain at least one element. Hence, C(ℓ,k,j)=0 $C(ℓ,k,j)=0$ $C(\ell, k,j) = 0$.

Putting this together into Equation [(3.2)](https://thesis.lucblassel.com/HPC-paper.html#eq:N), we get

N(ℓ)=4∑k=1o(k)({i(ℓ)k}+i(ℓ)−k∑j=1(i(ℓ)j){i(ℓ)−jk}) 
$$
N(ℓ)=∑k=14o(k)({i(ℓ)k}+∑j=1i(ℓ)−k(i(ℓ)j){i(ℓ)−jk})
$$
 
$$
\begin{equation*}
    N(\ell) = \sum_{k=1}^4 o(k) \bigg( \bigg\{%
\begin{matrix}
    i(\ell) \\
    k
\end{matrix}
\bigg\}  + \sum_{j=1}^{i(\ell) - k}\bigg(
\begin{matrix}
    i(\ell) \\
    j
\end{matrix}
\bigg) \bigg\{%
\begin{matrix}
    i(\ell)-j \\
    k
\end{matrix}
\bigg\}   \bigg)
\end{equation*}
$$

For ℓ=2 $ℓ=2$ $\ell=2$, we have N(2)=2,135 $N(2)=2,135$ $N(2)=2,135$ restricted SSRs, which is several orders of magnitude smaller than the initial 516 $516$ $5^{16}$ possible SSRs and allows us to test the performance of all of them. For order-3 SSRs we get N(3)=2.9⋅1021 $N(3)=2.9⋅1021$ $N(3)=2.9\cdot10^{21}$ which much smaller than the full search space of 543≈5.4⋅1044 $543≈5.4⋅1044$ $5^{4^3}\approx5.4\cdot10^{44}$, for order-4 SSRs we get a similar reduction in search space with N(4)=9.4⋅1084 $N(4)=9.4⋅1084$ $N(4)=9.4\cdot10^{84}$ as opposed to the full search space of 544≈8.6⋅10178 $544≈8.6⋅10178$ $5^{4^4}\approx8.6\cdot10^{178}$. For these higher order SSRs, although the restricted search space is much smaller than the full original one, it is still too large to exhaustively search.

### 3.2.3 Selection of mapping-friendly sequence reductions

We selected a set of “promising” SSRs starting from all of the SSRs enumerated in Section [3.2.2](https://thesis.lucblassel.com/HPC-paper.html#sec:enum), that we call *mapping-friendly sequence reductions* (abbreviated *MSR*). The selection was performed on a 0.5x coverage read set, simulated from a whole human genome assembly [^1].The transformed reads were mapped to the transformed reference using `minimap2` and `paftools mapeval` [^8] was used to compute a mapping error rate. Note that overfitting SSRs to a particular genome is acceptable in applications where a custom SSR can be used for each genome. Yet in this work, the same set of selected SSR will be used across all genomes.

![**Illustration of how a respective mapq threshold is chosen for each
of our evaluated MSRs.**  
The orange dot shows the error rate and
fraction of reads mapped for HPC at mapq threshold 60. Anything below
and to the right of this point is strictly better than HPC 60, i.e. it
has both a lower error rate and higher fraction of reads mapped. If an
evaluated MSR does not pass through this region, then it is discarded
from further consideration. In the figure, the blue MSR does pass
through this region, indicating that it is better than HPC 60. We
identify the leftmost point (marked as a blue dot) and use the mapq
threshold at that point as the respective threshold.](https://thesis.lucblassel.com/figures/HPC-MSRs/threshold_selection-v2.png)

Figure 3.3: **Illustration of how a respective mapq threshold is chosen for each of our evaluated MSRs.**  
The orange dot shows the error rate and fraction of reads mapped for HPC at mapq threshold 60. Anything below and to the right of this point is strictly better than HPC 60, i.e. it has both a lower error rate and higher fraction of reads mapped. If an evaluated MSR does not pass through this region, then it is discarded from further consideration. In the figure, the blue MSR does pass through this region, indicating that it is better than HPC 60. We identify the leftmost point (marked as a blue dot) and use the mapq threshold at that point as the respective threshold.

For each evaluated SSR, we selected, if it exists, the highest mapq threshold for which the mapped read fraction is higher and the mapping error rate is lower than HPC at mapq 60 (0.93 $0.93$ $0.93$ and 2.1⋅10−3 $2.1⋅10−3$ $2.1\cdot10^{-3}$ respectively), Figure [3.3](https://thesis.lucblassel.com/HPC-paper.html#fig:thresholdChoice) illustrates the idea. Then we identified the 20 SSRs that have the highest fraction of reads mapped at their respective thresholds. Similarly we identified the 20 SSRs with the lowest mapping error rate. Finally we select the 20 SSRs that have the highest percentage of thresholds “better” than HPC at mapq 60; i.e. the number of mapq thresholds for which the SSR has both a higher fraction of reads mapped and lower mapping error rate than HPC at a mapq threshold of 60, divided by the total number of thresholds (=60).

The union of these 3 sets of 20 SSRs resulted in a set of 58 “promising” MSRs. Furthermore, we will highlight three MSRs that are “best in their category”, i.e.

- **MSR** <sub>F</sub>: The MSR with the highest fraction of mapped reads at a mapq threshold of 0.
- **MSR** <sub>E</sub>: The MSR with the lowest mapping error rate at its respective mapq threshold.
- **MSR** <sub>P</sub>: The MSR with the highest percentage of mapq thresholds for which it is “better” than HPC at mapq 60.

Figure [3.4](https://thesis.lucblassel.com/HPC-paper.html#fig:topMSRs) shows the actual functions MSR <sub>F</sub>, MSR <sub>E</sub>, MSR <sub>P</sub>. An intriguing property is that they output predominantly As and Ts, with MSR <sub>P</sub> assigning only 2 input pairs to the G/C output whereas MSR <sub>E</sub> and MSR <sub>F</sub> assign only one. Additionally, MSR <sub>E</sub> and MSR <sub>P</sub> both assign the {CC,GG} input pair to the deletion output ε $ε$ $\varepsilon$ removing any information corresponding to repetitions of either G or C from the reduced sequence. Overall this means the reduced sequences are much more AT-rich than their raw counterparts, but somehow information pertinent to mapping is retained

![**Graph representations of our highlighted MSRs: MSR~E~,
MSR~F~, and MSR~P~.**  
MSR~E~ has the lowest error rate of among MSRs at the highest
mapq threshold for which it performs better than HPC at mapq 60,
MSR~F~ has the highest fraction of reads mapped at mapq 60 and
MSR~P~ has the highest percentage of mapq thresholds for which
it outperforms HPC at mapq 60. The grayed out nodes represent the
reverse complement of input dinucleotides and outputs, as in
Figure \@ref(fig:countingMSRs)C. For example for MSR~E~, AA is
mapped to T, so TT is mapped to
A.](https://thesis.lucblassel.com/figures/HPC-MSRs/Top_MSRs.png)

Figure 3.4: **Graph representations of our highlighted MSRs: MSR <sub>E</sub>, MSR <sub>F</sub>, and MSR <sub>P</sub>.**  
MSR <sub>E</sub> has the lowest error rate of among MSRs at the highest mapq threshold for which it performs better than HPC at mapq 60, MSR <sub>F</sub> has the highest fraction of reads mapped at mapq 60 and MSR <sub>P</sub> has the highest percentage of mapq thresholds for which it outperforms HPC at mapq 60. The grayed out nodes represent the reverse complement of input dinucleotides and outputs, as in Figure [3.1](https://thesis.lucblassel.com/HPC-paper.html#fig:countingMSRs) C. For example for MSR <sub>E</sub>, AA is mapped to T, so TT is mapped to A.

The 58 selected MSRs, as well as HPC and the identity transformation (denoted as *raw*), were then evaluated on larger read-sets simulated from 3 whole genome references: a whole human genome assembly [^1], a whole *Drosophila melanogaster* genome assembly [^17] and a synthetic centromeric sequence [^12] (see [STAR Methods](https://thesis.lucblassel.com/HPC-paper.html#sec:methods) for more details).

### 3.2.5 Mapping-friendly sequence reductions increase mapping quality on repeated regions of the human genome

To evaluate the performance of our MSRs specifically on repeats, we extracted the reads for which the generating region overlapped with the repeated region of the whole human genome by more than 50% $50%$ $50\%$ of the read length. We then evaluated the MSRs on these reads only. Repeated regions were obtained from [https://t2t.gi.ucsc.edu/chm13/hub/t2t-chm13-v1.1/rmsk/rmsk.bigBed](https://t2t.gi.ucsc.edu/chm13/hub/t2t-chm13-v1.1/rmsk/rmsk.bigBed).

We obtained similar results as on the whole human genome, with MSRs E, F and P performing better than HPC at mapq 50 (Figure [3.5](https://thesis.lucblassel.com/HPC-paper.html#fig:mapeval) B). At a mapq threshold of 50, the mapping error rate is 53% $53%$ $53\%$, 31% $31%$ $31\%$, and 39% $39%$ $39\%$ lower than HPC at mapq 60 for MSRs E, F and P respectively, while the fraction of mapped reads remains slightly higher. At mapq=60, raw has an mapping error rate 40% $40%$ $40\%$ lower than HPC but the mapped fraction is also 17% $17%$ $17\%$ lower.

### 3.2.6 Raw mapping improves upon HPC on centromeric regions

On the “TandemTools” centromeric reference, HPC consistently maps a smaller fraction of reads than raw, across all mapping quality thresholds (Figure [3.5](https://thesis.lucblassel.com/HPC-paper.html#fig:mapeval) C). Additionally, the mapping error rate for raw is often inferior to that of HPC. The same is true for our selected MSRs: most of them have comparable performance to HPC, but none of them outperform raw mapping (Figure [3.5](https://thesis.lucblassel.com/HPC-paper.html#fig:mapeval) C).

We conjecture this is due to the highly repetitive nature of centromeres. HPC likely removes small unique repetitions in the reads and the reference that might allow mappers to better match reads to a particular occurrence a centromeric pattern. Mapping raw reads on the other hand preserves all bases in the read and better differentiates repeats. Therefore it seems inadvisable to use HPC when mapping reads to highly repetitive regions of a genome, such as a centromere.

### 3.2.7 Positions of incorrectly mapped reads across the entire human genome

To study how MSRs E, F, and P improve over HPC and raw mapping in terms of mapping error rate on the human genome, we selected all the primary alignments that `paftools mapeval` reported as incorrectly mapped. For HPC and raw, only alignments of mapping quality equal to 60 were considered. To report a comparable fraction of aligned reads, we selected alignments of mapping quality ≥50 $≥50$ $\geq50$ for MSRs. We then reported the origin of those incorrectly mapped reads on whole human genome reference, shown per-chromosome in Figure [3.6](https://thesis.lucblassel.com/HPC-paper.html#fig:errorHists).

 $**Histogram of the original simulated positions for the incorrectly
mapped reads using `minimap2` at high mapping qualities across the whole
human genome, for several transformation methods.**  
For a given chromosome, each row represents the number of simulated
reads starting at that particular region. The dark gray rectangle
represents the position of the centromere for that chromosome, obtained
from annotations provided by the T2T consortium
(<http://t2t.gi.ucsc.edu/chm13/hub/t2t-chm13-v1.1/>). Similarly for
chromosomes 13, 14, 15, 21 and 22, a lighter gray rectangle represents
the position of the "stalk" satellites also containing repetitive
regions. For HPC and raw reads only alignments of mapping quality 60
were considered. To provide a fair comparison, alignments with mapping
qualities $\geq 50$ were considered for MSRs E, F and P.$

Figure 3.6: **Histogram of the original simulated positions for the incorrectly mapped reads using `minimap2` at high mapping qualities across the whole human genome, for several transformation methods.**  
For a given chromosome, each row represents the number of simulated reads starting at that particular region. The dark gray rectangle represents the position of the centromere for that chromosome, obtained from annotations provided by the T2T consortium ([http://t2t.gi.ucsc.edu/chm13/hub/t2t-chm13-v1.1/](http://t2t.gi.ucsc.edu/chm13/hub/t2t-chm13-v1.1/)). Similarly for chromosomes 13, 14, 15, 21 and 22, a lighter gray rectangle represents the position of the “stalk” satellites also containing repetitive regions. For HPC and raw reads only alignments of mapping quality 60 were considered. To provide a fair comparison, alignments with mapping qualities ≥50 $≥50$ were considered for MSRs E, F and P.

We observe that erroneously mapped reads are not only those from centromeres, and instead originate from many other genomic regions. MSRs E and P have a markedly lower number of these incorrect mappings than either HPC or raw, with 1118 incorrect mappings for raw mappings and 1130 for HPC as opposed to 549, 970 and 361 for MSRs E, F and P respectively. This stays true even for difficult regions of the genome such as chromosome X, where raw and HPC have 70 incorrect mappings as opposed MSRs E and P that have 39, and 27 errors respectively.

We also investigated where all simulated reads were mapped on the whole human genome assembly, for raw, HPC and MSRs E,F and P in Figures [A.1](https://thesis.lucblassel.com/HPC-appendix.html#fig:hist-raw) through [A.5](https://thesis.lucblassel.com/HPC-appendix.html#fig:hist-msr-f). The correctly mapped reads are, as expected, evenly distributed along each chromosome. The incorrectly mapped reads are however unevenly distributed. For most chromosomes there is a sharp peak in the distribution of incorrectly mapped reads, located at the position of the centromere. For the acrocentric chromosomes, there is a second peak corresponding to the “stalk” satellite region, with an enrichment of incorrectly mapped reads. This is expected since both centromeres and “stalks” are repetitive regions which are a challenge for mapping. For chromosomes 1, 9 and 16 however the majority of incorrectly mapped reads originate in repeated regions just after the centromere.

## 3.4 Limitations of this study

Our proposed MSRs improve upon HPC at mapq 60, both in terms of fraction of reads mapped and mapping error rate on whole human, *Drosophila melanogaster*, and *Escherichia coli* genomes. We chose these sequences because they were from organisms that we deemed different enough, however it would be interesting to verify if our proposed MSRs are still advantageous on even more organisms, e.g. more bacterial or viral genomes. This would allow us to assess the generalizability of our proposed MSRs.

We made the choice of using simulated data to be able to compute a mapping error rate. Some metrics, such as fraction of reads mapped might still be informative with regards to the mapping performance benefits of MSRs, even on real data. Evaluating the MSRs on real data might be more challenging but would offer insight into real-world usage of such pre-processing transformations.

The hypothesis we made in subsection [3.2.2.2](https://thesis.lucblassel.com/HPC-paper.html#sec:equiv) was derived from non mapping-related tests, it helped us reduce the search space and find MSRs. Testing if this hypothesis holds true on mapping tasks would help us make sure we are not missing some potentially well-performing SSRs by discarding them at this stage.

Finally, the restrictions we imposed to define RC-core-insensitive MSRs though intuitively understandable are somewhat arbitrary, so exploring a larger search space might be beneficial. Alternatively for higher order MSRs, even with our restrictions, the search spaces remain much too large to be explored exhaustively. To mitigate this problem, either further restrictions need to be found, or an alternative, optimization-based exploration method should be implemented.

## Acknowledgements

The authors thank Kristoffer Sahlin for feedback on the manuscript.

R.C was supported by ANR Transipedia, SeqDigger, Inception and PRAIRIE grants (ANR-18-CE45-0020, ANR-19-CE45-0008, PIA/ANR16-CONV-0005, ANR-19-P3IA-0001). This method is part of projects that have received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreements No 956229 and 872539. L.B was also supported by the ANR PRAIRIE grant (ANR-19-P3IA-0001). This material is based upon work supported by the National Science Foundation under Grant No. 1453527 and 1931531.

## Author contributions

Conceptualization, P.M. and R.C.; Methodology, L.B., P.M. and R.C.; Software, L.B.; Validation, L.B. and R.C.; Formal Analysis, L.B.; Investigation, L.B.; Resources, R.C.; Writing – Original Draft, L.B., P.M. and R.C.; Writing – Review & Editing, L.B., P.M. and R.C.; Visualization, L.B.; Supervision, R.C.; Project Administration, R.C.; Funding Acquisition, R.C.;

## Declaration of interests

The authors declare no competing interests.

## STAR Methods

### Lead contact

Further information and requests for resources should be directed to and will be fulfilled by the lead contact, Rayan Chikhi ([rayan.chikhi@pasteur.fr](mailto:rayan.chikhi@pasteur.fr))

### Materials availability

This study did not generate new unique reagents.

### Data and code availability

This paper analyzes existing, publicly available data. These accession numbers for the datasets are listed in the key resources table

All original code has been deposited at a github backed zenodo repository and is publicly available as of the date of publication. DOIs are listed in the key resources table, and the backing github repository is available at [github.com/lucblassel/MSR\_discovery](https://github.com/lucblassel/MSR_discovery).

Any additional information required to reanalyze the data reported in this paper is available from the lead contact upon request.

### Method details

#### 3.4.0.1 Datasets

The following three reference sequences were used for evaluation:

1. **Whole human genome:** This reference sequence is a whole genome assembly of the CHM13hTERT human cell line by the Telomere-to-Telomere consortium [^1]. We used the 1.1 assembly release (Genbank Assembly ID [GCA\_009914755.3](https://www.ncbi.nlm.nih.gov/assembly/GCA_009914755.3/)).
2. **Whole *Drosophila* genome:** This reference sequence is a whole genome assembly of a *Drosophila melanogaster*, release 6.35 (Genbank Assembly ID [GCA\_000001215.4](https://www.ncbi.nlm.nih.gov/assembly/GCF_000001215.4/)) [^17].
3. **Synthetic centromeric sequence:** This sequence was obtained from the `TandemTools` mapper test data [^12]. It is a simulated centromeric sequence that is inherently difficult to map reads to. Appendix [A.1](https://thesis.lucblassel.com/HPC-appendix.html#appendix:tandemtools) describes how it was constructed, and it is downloadable from [https://github.com/lucblassel/TandemTools/blob/master/test\_data/simulated\_del.fasta](https://github.com/lucblassel/TandemTools/blob/master/test_data/simulated_del.fasta)

#### 3.4.0.2 Simulation pipeline

Given a reference sequence, simulated reads were obtained using `nanosim` [^21] with the `human_NA12878_DNA_FAB49712_guppy_flipflop` pre-trained model, mimicking sequencing with an Oxford Nanopore instrument. The number of simulated reads was chosen to obtain a theoretical coverage of whole genomes around 1.5x, this resulted in simulating ≈6.6⋅105 $≈6.6⋅105$ $\approx 6.6\cdot10^5$ reads for the whole human genome and ≈2.6⋅104 $≈2.6⋅104$ $\approx 2.6\cdot10^4$ reads for the whole Drosophila genome. Since the centromeric sequence is very short, we aimed for a theoretical coverage of 100x which resulted in ≈1.3⋅104 $≈1.3⋅104$ $\approx 1.3\cdot10^4$ simulated reads.

For each evaluated SSR, the reads as well as the reference sequence were reduced by applying the SSR to them. The reduced reads were then mapped to the reduced reference using `minimap2` [^8] with the `map-ont` preset and the `-c` flag to generate precise alignments. Although HPC is an option in `minimap2` we do not use it and we evaluate HPC as any of the other SSRs by transforming the reference and reads prior to mapping. The starting coordinates of the reduced reads on the reduced reference were translated to reflect deletions incurred by the reduction process. The mapping results with translated coordinates were filtered to keep only the primary alignments. This process was done for each of our SSRs as well as with HPC and the original untransformed reads (denoted as *raw*).

#### 3.4.0.3 Evaluation pipeline

We use two metrics to evaluate the quality of a mapping of a simulated read set. The first is the *fraction of reads mapped*, i.e. that have at least one alignment. The second is the *mapping error rate*, which is the fraction of mapped reads that have an incorrect location as determined by `paftools mapeval` [^8]. This tool considers a read as correctly mapped if the intersection between its true interval of origin, and the interval where it has been mapped to, is at least 10% of the union of both intervals.

Furthermore, we measure the mapping error rate as a function of a given *mapping quality threshold*. Mapping quality (abbreviated mapq) is a metric reported by the aligner that indicates its confidence in read placement; the highest value (60) indicates that the mapping location is likely correct and unique with high probability, and a low value (e.g. 0) indicates that the read has multiple equally likely candidate mappings and that the reported location cannot be trusted. The mapping error rate at a mapq threshold t $t$ $t$ is then defined as the mapping error rate of reads whose mapping quality is t $t$ $t$ or above. For example, the mapping error rate at t=0 $t=0$ $t=0$ is the mapping error rate of the whole read set, while the mapping error rate at t=60 $t=60$ $t=60$ is the mapping error rate of only the most confident read mappings. Observe that the mapping error rate decreases as t $t$ $t$ increases.

All experiments performed for this article are implemented and documented as nextflow workflows available in this project’s repository ([https://github.com/lucblassel/MSR\_discovery](https://github.com/lucblassel/MSR_discovery)). These workflows may be used to rerun experiments and reproduce results. The repository also contains a Rmarkdown notebook to generate all figures and tables in the main text and supplemental information from the pipeline outputs.

## Supplementary information

Supporting Information can be found in Appendix [A](https://thesis.lucblassel.com/HPC-appendix.html#HPC-appendix)

### References

[^1]: 4.

Nurk, S. *et al.* [The complete sequence of a human genome](https://doi.org/10.1126/science.abj6987). *Science* **376**, 44–53 (2022).

[^2]: 101.

Dohm, J. C., Peters, P., Stralis-Pavese, N. & Himmelbauer, H. [Benchmarking of long-read correction methods](https://doi.org/10.1093/nargab/lqaa037). *NAR Genomics and Bioinformatics* **2**, (2020).

[^3]: 112.

Nurk, S. *et al.* [HiCanu: Accurate assembly of segmental duplications, satellites, and allelic variants from high-fidelity long reads](https://doi.org/10.1101/gr.263566.120). *Genome Res.* **30**, 1291–1305 (2020).

[^4]: 113.

Ekim, B., Berger, B. & Chikhi, R. [Minimizer-space de Bruijn graphs: Whole-genome assembly of long reads in minutes on a personal computer](https://doi.org/10.1016/j.cels.2021.08.009). *Cell Systems* **12**, 958–968.e6 (2021).

[^5]: 115.

Miller, J. R. *et al.* [Aggressive assembly of pyrosequencing reads with mates](https://doi.org/10.1093/bioinformatics/btn548). *Bioinformatics* **24**, 2818–2824 (2008).

[^6]: 116.

Sahlin, K. & Medvedev, P. [De Novo Clustering of Long-Read Transcriptome Data Using a Greedy, Quality Value-Based Algorithm](https://doi.org/10.1089/cmb.2019.0299). *Journal of Computational Biology* **27**, 472–484 (2020).

[^7]: 117.

Au, K. F., Underwood, J. G., Lee, L. & Wong, W. H. [Improving PacBio Long Read Accuracy by Short Read Alignment](https://doi.org/10.1371/journal.pone.0046679). *Plos One* **7**, e46679 (2012).

[^8]: 119.

Li, H. [Minimap2: Pairwise alignment for nucleotide sequences](https://doi.org/10.1093/bioinformatics/bty191). *Bioinformatics* **34**, 3094–3100 (2018).

[^9]: 120.

Jain, C. *et al.* [Weighted minimizer sampling improves long read mapping](https://doi.org/10.1093/bioinformatics/btaa435). *Bioinformatics* **36**, i111–i118 (2020).

[^10]: 129.

Gusfield, D. *Algorithms on Strings, Trees, and Sequences: Computer Science and Computational Biology*. (Cambridge University Press, 1997). doi:[10.1017/cbo9780511574931](https://doi.org/10.1017/cbo9780511574931).

[^11]: 261.

Prodanov, T. & Bansal, V. [Sensitive alignment using paralogous sequence variants improves long-read mapping and variant calling in segmental duplications](https://doi.org/10.1093/nar/gkaa829). *Nucleic Acids Research* **48**, e114 (2020).

[^12]: 263.

Mikheenko, A., Bzikadze, A. V., Gurevich, A., Miga, K. H. & Pevzner, P. A. [TandemTools: Mapping long reads and assessing/improving assembly quality in extra-long tandem repeats](https://doi.org/10.1093/bioinformatics/btaa440). *Bioinformatics* **36**, i75–i83 (2020).

[^13]: 310.

Bragg, L., Stone, G., Imelfort, M., Hugenholtz, P. & Tyson, G. W. [Fast, accurate error-correction of amplicon pyrosequences using Acacia](https://doi.org/10.1038/nmeth.1990). *Nat Methods* **9**, 425–426 (2012).

[^14]: 311.

Sahlin, K. & Medvedev, P. [Error correction enables use of Oxford Nanopore technology for reference-free transcriptome analysis](https://doi.org/10.1038/s41467-020-20340-8). *Nat Commun* **12**, 2 (2021).

[^15]: 312.

Liu, H. *et al.* [SMARTdenovo: A de novo assembler using long noisy reads](https://doi.org/10.46471/gigabyte.15). *Gigabyte* **2021**, 1–9 (2021).

[^16]: 313.

Graham, R. L., Knuth, D. E. & Patashnik, O. *Concrete mathematics: A foundation for computer science*. (Addison-Wesley, 1994).

[^17]: 314.

Adams, M. D. *et al.* [The genome sequence of Drosophila melanogaster](https://doi.org/10.1126/science.287.5461.2185). *Science* **287**, 2185–2195 (2000).

[^18]: 315.

Rhie, A., Walenz, B. P., Koren, S. & Phillippy, A. M. [Merqury: Reference-free quality, completeness, and phasing assessment for genome assemblies](https://doi.org/10.1186/s13059-020-02134-9). *Genome Biology* **21**, 245 (2020).

[^19]: 316.

Li, H. [New strategies to improve Minimap2 alignment accuracy](https://doi.org/10.1093/bioinformatics/btab705). *Bioinformatics* **37**, 4572–4574 (2021).

[^20]: 317.

Li, H. *et al.* [A synthetic-diploid benchmark for accurate variant-calling evaluation](https://doi.org/10.1038/s41592-018-0054-7). *Nat Methods* **15**, 595–597 (2018).

[^21]: 318.

Yang, C., Chu, J., Warren, R. L. & Birol, I. [NanoSim: Nanopore sequence read simulator based on statistical characterization](https://doi.org/10.1093/gigascience/gix010). *GigaScience* **6**, (2017).