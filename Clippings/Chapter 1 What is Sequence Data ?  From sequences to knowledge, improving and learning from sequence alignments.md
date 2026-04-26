---
title: "Chapter 1 What is Sequence Data ? | From sequences to knowledge, improving and learning from sequence alignments"
source: "https://thesis.lucblassel.com/what-is-sequence-data.html#conclusion"
author:
  - "[[Luc Blassel]]"
published:
created: 2026-04-26
description: "Chapter 1 What is Sequence Data ? | From sequences to knowledge, improving and learning from sequence alignments"
tags:
---
## Chapter 1 What is Sequence Data?

## 1.1 Biological sequences, a primer

To fully understand the work that was done during this thesis, as well as the choices that were made, some basic knowledge of molecular biology and genetics is needed. If you are already familiar with biological sequences, feel free to skip ahead to section [1.2](https://thesis.lucblassel.com/what-is-sequence-data.html#obtaining-sequence-data).

### 1.1.1 What is DNA?

**D** esoxyribo **N** ucleic **A** cid (DNA) is one of the most important molecules there is, without it complex life as we know it is impossible. It contains all the genetic information of a given organism, that is to say all the information necessary for the organism to: 1) function as a living being and 2) make a perfect copy of itself. This is the case for the overwhelming majority of living organisms on planet earth, from elephants to potatoes, to micro-organisms like bacteria.

DNA is a polymer, composed of monomeric units called nucleotides. Each nucleotide is composed of ribose (a five carbon sugar) on which are attached a phosphate group as well as one of four nucleobases: Adenine (A), Cytosine (C), Guanine (G) of Thymine (T). These four types of nucleotide monomers link up with one-another, through phosphate-sugar bonds, creating a single strand of DNA. The ordered sequence of these four types of nucleotides in strand encodes all the genetic information necessary for the organism to function. Nucleotides in a strand form strong complementary bonds with nucleotides from another strand, A with T and C with G. These bonds allow two strands of DNA to form the double-helix structure of DNA <sup><a href="#ref-watsonStructureDna1953" role="doc-biblioref">1</a></sup> shown in Figure [1.1](https://thesis.lucblassel.com/what-is-sequence-data.html#fig:figDNA). The specificity of nucleotide bonds ensure that the two strands of the double helix are complementary and that the information contained in one strand can be recovered from the other. This ensures a certain structural stability to the DNA molecule and a way to recover the important information that could be lost due to a damaged strand.

![**Double-helix structure of DNA.**  
Each strand of DNA has a phosphate-sugar backbone on which are attached nucleobases. The two strands are linked by complementary bonds between the nucleobases of different strands (A bonding with T and C bonding with G), encoding the same information of both strands.](https://thesis.lucblassel.com/figures/Sequence-Intro/DNA.png)

Figure 1.1: **Double-helix structure of DNA.**  
Each strand of DNA has a phosphate-sugar backbone on which are attached nucleobases. The two strands are linked by complementary bonds between the nucleobases of different strands (A bonding with T and C bonding with G), encoding the same information of both strands.

The amount of DNA necessary to encode the information varies greatly from organism to organism: 5400 base pairs (5.4kBp) for the φX174 $φX174$ $\varphi X174$ phage <sup><a href="#ref-sangerNucleotideSequenceBacteriophage1977" role="doc-biblioref">2</a></sup>, 4.9MBp for *Escherichia coli* <sup><a href="#ref-archerGenomeSequenceColi2011" role="doc-biblioref">3</a></sup>, 3.1GBp for *Homo sapiens* <sup><a href="#ref-nurkCompleteSequenceHuman2022" role="doc-biblioref">4</a></sup> all the way up to almost 150GBp for *Paris japonica,* a Japanese mountain flowering plant <sup><a href="#ref-pellicerLargestEukaryoticGenome2010" role="doc-biblioref">5</a></sup>. While very small genome size tend to occur in smaller, simpler organisms, genome size does not correlate with organism complexity <sup><a href="#ref-macgregorCValueParadox2001" role="doc-biblioref">6</a></sup>.

### 1.1.2 From Information to action

#### 1.1.2.1 Proteins, their structure and their role

The double stranded DNA molecules present in the cells of a living organism contain information only; in order for the organism to live, this information must be read and translated into actions. Most of the actions necessary for “life” are taken by large molecules called proteins, they have a very wide range of functions from catalyzing reactions in the cell to giving it structure <sup><a href="#ref-albertsMolecularBiologyCell2002" role="doc-biblioref">7</a></sup>.

Proteins are macromolecules that are made up of one or several chains of amino acids. These chains then link together and fold up in a specific three dimensional structure, giving the protein the shape it needs to fulfill its goal. This structure is determined by the sequence of amino acids, and a given protein can be identified by this amino acid sequence <sup><a href="#ref-albertsMolecularBiologyCell2002" role="doc-biblioref">7</a></sup>.

This sequence is directly dependent on the information contained in the DNA. First the DNA is transcribed in a similar, but single stranded, molecule called RNA (Ribonucleic Acid) which encodes the same sequence. This RNA molecule is then translated into a protein by the following process <sup><a href="#ref-crickGeneralNatureGenetic1961" role="doc-biblioref">8</a></sup>:

1. Nucleotides in the RNA sequence are read in groups of three called codons.
2. These codons are read sequentially along the RNA molecule.
3. Each codon corresponds to an amino acid, according to the genetic code.
4. The sequence of codons in RNA *(and by extension DNA)* determines the sequence of amino acids.
5. The translation process is stopped when a specific type of codon *(a “Stop” codon)* is read.

With four types of nucleotides and codons grouping three nucleotides there are 43=64 $43=64$ $4^3=64$ possible codons. However, as stated above, proteins are only made up of 20 different amino acids, meaning that several different codons correspond to the same amino acid. This gives the translation process a certain robustness to errors that can occur when the DNA is copied to create a new cell, or when it is transformed into RNA prior to protein translation.

The portion of DNA that is read to create the protein is said to be “coding”, and is called a gene. There are several thousands of genes in the human genome <sup><a href="#ref-internationalhumangenomesequencingconsortiumFinishingEuchromaticSequence2004" role="doc-biblioref">9</a></sup> resulting in proteins executing thousands of different functions in a cell. In human beings, coding DNA represents only 1% to 2% of the total genome <sup><a href="#ref-elkonCharacterizationNoncodingRegulatory2017" role="doc-biblioref">10</a>,<a href="#ref-omennReflectionsHUPOHuman2021" role="doc-biblioref">11</a></sup>. The large majority of the DNA in a human being is not translated into proteins, a portion of it has a regulatory role, controlling transcription and translation, but the role remains unknown for the rest of the human genome <sup><a href="#ref-shabalinaMammalianTranscriptomeFunction2004" role="doc-biblioref">12</a>,<a href="#ref-theencodeprojectconsortiumIntegratedEncyclopediaDNA2012" role="doc-biblioref">13</a></sup>.

#### 1.1.2.2 Making mistakes

Going from DNA sequence to protein is quite a complicated process involving several steps, it is therefore possible for a mistake to happen. There are several mechanisms to avoid mistakes and alteration of the genetic information: the complementary nature of the two strands of DNA, the redundant nature of the genetic code as well as error correction mechanisms in the molecules *(called “polymerases”)* that read and write DNA and RNA being some of them. Despite all that, some errors in the nucleic acid (DNA and RNA) or protein sequences still make it through, these are called mutations.

##### 1.1.2.2.1 Where can mistakes happen?

There are several sources of error that can alter genetic information <sup><a href="#ref-chatterjeeMechanismsDNADamage2017" role="doc-biblioref">14</a></sup>:

While RNA transcription and protein translation are much more error prone processes than DNA replication, the errors induced only alter the expression of the genetic information. The effects of these errors are localized to the cells where they happen and are not transmitted to offspring. However these transcription errors are not unimportant and increased transcription error rates have been hypothesized to cause severe neurological symptoms in pediatric cohorts <sup><a href="#ref-anagnostouTranscriptionErrorsAging2021" role="doc-biblioref">26</a></sup>.

##### 1.1.2.2.3 What effect can mutations have?

As we stated above, some mutations in DNA may have no repercussions, some others can lead to non-functional proteins. In some cases mutations can be associated with a trait in the mutated individual. For example a single mutation in a gene linked with coagulation can lead to pathological Leiden thrombophilia <sup><a href="#ref-kujovichFactorLeidenThrombophilia2011" role="doc-biblioref">28</a></sup>, a single amino acid deletion in the CFTR protein leads to *(the very deadly)* cystic fibrosis <sup><a href="#ref-cuttingCysticFibrosisGenetics2015" role="doc-biblioref">29</a></sup>, and many mutations have been linked to complex diseases like type 2 diabetes <sup><a href="#ref-fuchsbergerGeneticArchitectureType2016" role="doc-biblioref">30</a>,<a href="#ref-morrisLargescaleAssociationAnalysis2012" role="doc-biblioref">31</a></sup>. All mutational effects are not necessarily bad for the organism though, and mutations are essential for bacteria <sup><a href="#ref-woodfordEmergenceAntibioticResistance2007" role="doc-biblioref">32</a></sup> or viruses like HIV <sup><a href="#ref-rheeHumanImmunodeficiencyVirus2003" role="doc-biblioref">33</a></sup> to develop resistance to treatment *(more on that in Chapters* [5](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#viruses-hiv-and-drug-resistance) *and* [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper)*).*

While some mutations, have had their mechanisms and consequences thoroughly studied, in many cases mutations are simply linked to a trait. Since it is easier to show correlation than causation, and that the former does not necessarily imply the latter, it is important to further study mutations of notice to understand their potential consequences.

## 1.2 Obtaining sequence data

In many fields, especially in computational biology, we need to know what genetic information the studied organism has. That is to say: what is the exact sequence of nucleotides that make up its DNA? The process of figuring out this sequence is, perhaps unsurprisingly, called sequencing. A sequence that is produced by this process is called a *sequencing read* or, more commonly, just a *read*.

### 1.2.1 Sanger sequencing, a breakthrough

The first widely used sequencing method was developed in 1977 <sup><a href="#ref-sangerDNASequencingChainterminating1977" role="doc-biblioref">34</a></sup>. Sanger *et al.* devised a simple method to read the sequence of nucleotides that make up a DNA sequence known as *chain termination sequencing* or simply *Sanger sequencing* *(represented in Figure* [1.3](https://thesis.lucblassel.com/what-is-sequence-data.html#fig:sanger)*)*. Although this method is now mostly obsolete, it established some key concepts in sequencing, some of which are in action in the most modern sequencers.

To understand Sanger sequencing, one must first understand how to synthesize DNA. As we stated in Section [1.1.1](https://thesis.lucblassel.com/what-is-sequence-data.html#what-is-dna), DNA is built up from building blocks that we called nucleotides, more specifically deoxynucleotide triphosphates or dNTPs. These dNTPs are made up of a sugar (deoxyribose), a nucleobase (A, T, G or C) and 3 phosphate groups. By successively adding these dNTPs at the end of an existing DNA molecule, we extend it, linking one of the phospates of the dNTP to an oxygen atom on the last nucleotide of the DNA molecule. Let us now consider a dideoxynucleotide triphosphate (ddNTP), which is identical to a dNTP except we remove a specific oxygen atom. This ddNTP can be added to the growing molecule of DNA like regular dNTPs, but since it is missing that one oxygen atom no more dNTPs or ddNTPs can be added to the DNA molecule after this one. The elongation is terminated and we call these ddNTPs chain-terminators. This combination of DNA synthesis followed by termination are at the heart of Sanger sequencing.

It is important to note that dNTPs and ddNTPs refer to nucleotides with any nucleobase. We can refer to specific dNTPs by replacing the “N” with the base of choice. For example, dATP refers to the dNTP that has adenine as a base. Similarly we have dCTP, dGTP and dTTP (as well as ddATP, ddCTP, ddGTP and ddTTP).

1. The first step of Sanger sequencing (and most sequencing methods) is to amplify the DNA molecule we wish to sequence, *i.e.* make many copies of it (usually through a process called PCR). These clones of the sequence are then separated into their two complementary strands one of which will be used as a template for the sequencing steps.
2. The second step is to prepare 4 different sequencing environments *(think of it as 4 test tubes)*. In each environment we introduce an equal mix of the 4 dNTPs, that will be used to elongate new DNA molecules from the amplified templates, and a single type of ddNTP. So in the first test tube we will have only ddATP, ddCTP in the second, *et cetera.* In addition, these ddNTP are marked, at first with radioactive isotopes, and later on, as the technology matured, with dyes. This marking means that we can observe the location of these ddNTPs later on.
3. Then an equal portion of the template is introduced in each environment with DNA polymerases (that will add the nucleotides to elongate a sequence that is complementary to the template), and short specific DNA molecules called primers that are necessary for the polymerases to start synthesizing new DNA.
4. During synthesis the chain is elongated with dNTPs by the polymerase and the reaction stops once a ddNTP is incorporated. At the end of this process we have plenty of fragments of DNA in each test tube, and we know that these fragments end with a specific base in a given environment. For example, in the test tube where we added ddATP, we know that all the fragments end with an A, and that we have all the possible fragments that start at the beginning of the template and end with an A. If the template is AACTA, then the fragments we would get in the ddATP test tube would be A, AA, and AACTA.
5. Then, a sample from each environment is taken and deposited on a gel, each in its own lane. A process called electrophoresis is then used to separate the fragments according to their weight. By applying an electrical current to the gel, the fragments of DNA will migrate away from where they were deposited along their lane in the gel. Lighter, shorter DNA fragments will travel further than heavier ones. We then get clusters of fragments ordered by weight (and therefore by length) called bands. With the marked ddNTP we can reveal these bands in the gel.
6. We know that: 1) bands are ordered by length; 2) consecutive bands correspond to the addition of a single nucleotide; 3) in a specific lane fragments corresponding to a band end with a specific base. This knowledge is enough to deduce the sequence of the template. An example gel is shown in Figure [1.3](https://thesis.lucblassel.com/what-is-sequence-data.html#fig:sanger).

This process allowed Sanger *et al.* to sequence the first genome, of a φX174 $φX174$ $\varphi X174$ bacteriophage, in 1977 <sup><a href="#ref-sangerNucleotideSequenceBacteriophage1977" role="doc-biblioref">2</a></sup>. Although revolutionary, this method was costly, time consuming and labor intensive. Adjustments to this method were made in order to make it faster and less expensive. An important step was to change the way ddNTPs were marked. By using fluorescent markers, each base having a distinct “color”, we can eliminate the need to have 4 different environments and lanes in the gel <sup><a href="#ref-smithSynthesisOligonucleotidesContaining1985" role="doc-biblioref">35</a>,<a href="#ref-smithFluorescenceDetectionAutomated1986" role="doc-biblioref">36</a></sup>. This also paved the way for automating sequencing, each fluorescently marked band can be excited with a laser, and the resulting specific wavelength can be recorded by optical systems and the corresponding base automatically deduced <sup><a href="#ref-ansorgeAutomatedDNASequencing1987" role="doc-biblioref">37</a></sup> (Also see Figure [1.3](https://thesis.lucblassel.com/what-is-sequence-data.html#fig:sanger)). Other improvements were made such as using capillary electrophoresis instead of gel electrophoresis.

![**Overview of the sanger sequencing protocol.**  
**A)** The sequence to read and all the generated fragments, with highlighted ddNTP chain terminators, ordered by molecular weight (i.e. length). **B)** Classical Sanger sequencing. The fragments are separated by electrophoresis and the lighter fragments travel further from the wells at the botom of the gel. Each lane in the gel correpsonds to a specific ddNTP. The radioactivly marked ddNTPs appear as black band in the gel and we can reconstruct the sequence by reading the bands from top to bottom, the column in wich the band appears indicating which base is at each position. **C)** Automated Sanger sequencing. The fragments are also separated by electrophoresis, as in panel B. Chain terminators are marked with fluorescent markers. When excited by a laser, each ddNTP emits a specific wavelength. This is read by an optical sensor and the corresponding ddNTP is recorded. By exciting each band we can quickly deduce the sequence. 
](https://thesis.lucblassel.com/figures/Sequence-Intro/Sanger.png)

Figure 1.3: **Overview of the sanger sequencing protocol.**  
**A)** The sequence to read and all the generated fragments, with highlighted ddNTP chain terminators, ordered by molecular weight (i.e. length). **B)** Classical Sanger sequencing. The fragments are separated by electrophoresis and the lighter fragments travel further from the wells at the botom of the gel. Each lane in the gel correpsonds to a specific ddNTP. The radioactivly marked ddNTPs appear as black band in the gel and we can reconstruct the sequence by reading the bands from top to bottom, the column in wich the band appears indicating which base is at each position. **C)** Automated Sanger sequencing. The fragments are also separated by electrophoresis, as in panel B. Chain terminators are marked with fluorescent markers. When excited by a laser, each ddNTP emits a specific wavelength. This is read by an optical sensor and the corresponding ddNTP is recorded. By exciting each band we can quickly deduce the sequence.

These gradual improvements to the Sanger sequencing protocol made it possible to sequence longer and more accurate reads, with the latest technologies resulting in reads reaching 1,000 base pairs with an accuracy of 99.999% <sup><a href="#ref-shendureNextgenerationDNASequencing2008" role="doc-biblioref">38</a></sup>. These improvements also resulted in a lower cost for sequencing, which was greatly decreased from around $1000 per base-pair <sup><a href="#ref-collinsHumanGenomeProject2003" role="doc-biblioref">39</a></sup> to only $0.5 per kilobase <sup><a href="#ref-shendureNextgenerationDNASequencing2008" role="doc-biblioref">38</a></sup>. Finally these technological improvements also increased the throughput of sequencing machines from around 1 kilobase per day <sup><a href="#ref-collinsHumanGenomeProject2003" role="doc-biblioref">39</a></sup> to 120 kilobases per hour <sup><a href="#ref-liuComparisonNextGenerationSequencing2012" role="doc-biblioref">40</a></sup>.

Despite these improvements, for ambitious endeavors such as the human genome project, sequencing was a massive undertaking: the first human genome is estimated to have cost between 500 million and 1 billion US dollars to sequence <sup><a href="#ref-CostSequencingHuman" role="doc-biblioref">41</a></sup>.

### 1.2.3 Long read sequencing

Although NGS technologies revolutionized the sequencing world, recent efforts have been made to get longer reads. These third-generation methods generate reads of tens of kilobases and are commonly called *long-read sequencing* method. Long reads have a host of applications <sup><a href="#ref-pollardLongReadsTheir2018" role="doc-biblioref">48</a></sup> for which short NGS reads might not be well suited: *De novo* assembly of large complex genomes, studying complex repetitive regions such as centromeres or telomeres or detection of structural variants. They have recently been used to assemble the first truly complete human genome, including telomeric and centromeric regions <sup><a href="#ref-nurkCompleteSequenceHuman2022" role="doc-biblioref">4</a></sup>.

The two available long read technologies are: Single Molecule Real Time sequencing (SMRT), commercialized by Pacific Biosciences (PacBio) and Nanopore sequencing, commercialized by Oxford Nanopore Technologies (ONT). While these technologies are quite different, they both result in much longer reads than even Sanger sequencing in real time, without the need for chain terminators or separate sequencing reactions, all with a high throughput and at a reasonably low cost.

SMRT sequencing was first developed in 2009 <sup><a href="#ref-eidRealTimeDNASequencing2009" role="doc-biblioref">49</a></sup>, before being commercialized and furthered by PacBio. The basic principle is as follows:

1. Fragment and amplify DNA to obtain a very large number of DNA templates.
2. Link both strands of each DNA template together with known sequences called *bell adapters*. Denature the DNA to create a single stranded, circular DNA molecule.
3. Primers and polymerases are attached to the circular molecule specifically on one of the bell adapters.
4. Add the circular DNA template, primer, polymerases complexes to a SMRT chip. This chip is essentially a large aluminium surface with hundreds of thousands of microscopic wells called *Zero-Mode Waveguides* (ZMWs) only 100nm in diameter <sup><a href="#ref-leveneZeroModeWaveguidesSingleMolecule2003" role="doc-biblioref">50</a></sup>. The polymerases are chemically bonded to the bottom of each of these ZMWs so we effectively get a single DNA template and polymerase per well.
5. Fluorescently marked dNTPs are incorporated progressively in each of the wells. When a marked dNTP is incorporated in the newly synthesized DNA brand, light of a specific wavelength is emitted.
6. The size of these ZMWs make the detection of the fluorescence possible with an optical system. Incorporation of dNTPs in each ZMW can be detected simultaneously in a parallel fashion and the resulting sequences deduced.

Nanopore sequencing, thought of in the eighties, further developed along the years <sup><a href="#ref-clarkeContinuousBaseIdentification2009" role="doc-biblioref">51</a></sup> and first commercialized by ONT in 2014 <sup><a href="#ref-deamerThreeDecadesNanopore2016" role="doc-biblioref">52</a></sup>, is completely different from all the sequencing technologies previously mentioned. Where all the other ones are based on synthesizing a complementary DNA strand and detecting specific dNTP incorporation in some way or another, there is no synthesis in nanopore sequencing. The principle relies on feeding a single strand of a DNA template through a small hole in a membrane, a *nanopore*, at a controlled speed. As the nucleotides go through the nanopore, an electric current is formed between both sides of the membrane. This current can be measured and is specific to the succession of 5 to 6 nucleotides inside the nanopore channel at any given time. By looking at the evolution of the electric current as the DNA strand goes through the nanopore, we can deduce the sequence of nucleotides through a process called *base calling.* Base calling is usually done with machine learning methods, mainly artificial neural networks <sup><a href="#ref-wickPerformanceNeuralNetwork2019" role="doc-biblioref">53</a></sup>. In the flow cells used in ONT sequencers, there are hundreds of thousands of nanopores, spread out over a synthetic membrane, allowing for massively parallel sequencing as well. Theoretically, since this method is not based on synthesis, the upper limit for read length is only limited by the length of the template, and in practice ONT sequencing produces the longest reads.

Both technologies yield long reads, the median and highest read lengths being 10 kilobases and 60 kilobases respectively for PacBio sequencing <sup><a href="#ref-rhoadsPacBioSequencingIts2015" role="doc-biblioref">54</a></sup>. For nanopore the median read lengths of 10 to 12 kilobases <sup><a href="#ref-ipMinIONAnalysisReference2015" role="doc-biblioref">55</a>,<a href="#ref-logsdonLongreadHumanGenome2020" role="doc-biblioref">56</a></sup> are similar to PacBio, but in it can also yield ultra-long reads of 1 up to 2.3 megabases long <sup><a href="#ref-jainNanoporeSequencingAssembly2018" role="doc-biblioref">57</a> – <a href="#ref-payneBulkVisGraphicalViewer2019" role="doc-biblioref">59</a></sup>. The length of the reads and parallel nature of these two technologies allow these sequencers to have truly massive throughputs. PacBio sequencers can sequence between 2 and 11 gigabases per hour and ONT from 12.5 gigabases per hour, up to a staggering 260 gigabases per hour using the latest ONT PromethION machines <sup><a href="#ref-logsdonLongreadHumanGenome2020" role="doc-biblioref">56</a></sup>. The cost of sequencing with these machines, while higher than for Illumina sequencers, remains reasonably affordable at $0.32 and $0.13 per megabase for PacBio and ONT respectively <sup><a href="#ref-murigneuxComparisonLongreadMethods2020" role="doc-biblioref">60</a></sup>. These characteristics are summarized in Table [1.1](https://thesis.lucblassel.com/what-is-sequence-data.html#tab:sequencing) along with other sequencing technologies.

The length, throughput and sequencing cost of both these technologies paint a pretty picture, and indeed they have proved useful in many settings, but sequencing accuracy is a problem with these technologies. The per-base sequencing accuracy has been estimated to be between 85% and 92% for PacBio sequencers and 87% to 98% for ONT machines <sup><a href="#ref-logsdonLongreadHumanGenome2020" role="doc-biblioref">56</a>,<a href="#ref-chaissonResolvingComplexityHuman2015" role="doc-biblioref">61</a>,<a href="#ref-jainOxfordNanoporeMinION2016" role="doc-biblioref">62</a></sup>. This accuracy is much lower than either Sanger sequencing or Illumina reads. Characterizing, correcting and accounting for these errors is widely studied and it will be discussed in more detail in Sections [1.3](https://thesis.lucblassel.com/what-is-sequence-data.html#sequencing-errors-how-to-account-for-them) and [1.4](https://thesis.lucblassel.com/what-is-sequence-data.html#the-special-case-of-homopolymers).

| technology | read length (nt) | throughput (nt/hour) | cost ($/Mb) | accuracy |
| --- | --- | --- | --- | --- |
| Sanger | 1000 | 120 103 | $500 | 99.999% |
| Illumina | 150 | 2.5-12.5 109 | $0.07 | 99.9% |
| Pyrosequencing | 400 | 30 106 | $10 | 99.9% |
| PacBio SMRT | 10000 (up to 60000) | 2-11 109 | $0.32 | 85-92% |
| Nanopore | 12000 (up to 2.5 106) | 12.5-260 109 | $0.13 | 87-98% |

Table 1.1: **Comparison of sequencing technology characteristics.**  
Characteristics for the latest sequencers were used for the Sanger sequencing entry. The length is given in nucleotides, throughputs in sequenced nuctleotides per hour and cost in US dollars per megabase.

While most of the mentioned technologies can also be adapted and used to sequence RNA instead of DNA <sup><a href="#ref-hongRNASequencingNew2020" role="doc-biblioref">63</a>,<a href="#ref-ozsolakRNASequencingAdvances2011" role="doc-biblioref">64</a></sup>, directly sequencing proteins remains a challenge. The sequence of amino acids making up a protein is usually deduced from the codons in sequenced DNA or RNA after detection of potentially coding regions called open reading frames (ORFs). Development of methods to directly sequence protein molecules using mass spectrometry was started not very long after Sanger sequencing <sup><a href="#ref-huntProteinSequencingTandem1986" role="doc-biblioref">65</a></sup> and improved <sup><a href="#ref-smithProteinSequencingProtocols2002" role="doc-biblioref">66</a></sup>. New methods are still being developed <sup><a href="#ref-restrepo-perezPavingWaySinglemolecule2018" role="doc-biblioref">67</a></sup> but protein sequencing remains a challenge.

## 1.4 The special case of homopolymers

Despite improvement in error correction methods and sequencing technologies, certain genetic patterns are particularly difficult to process, homopolymers are one such pattern.

### 1.4.1 Homopolymers and the human genome

*Homopolymers* consist of a stretch of repeated nucleotides (i.e. ≥2 $≥2$ $\geq 2$) occurring at some point in the genome. For example, the sequence AAAA is a length 4 adenine homopolymer. In the complete human genome assembly (CHM13 v1.1 from the T2T consortium <sup><a href="#ref-nurkCompleteSequenceHuman2022" role="doc-biblioref">4</a></sup>), 50% of its three gigabases are in homopolymers of size 2 or more, and 10% are in homopolymers of length equal or greater than 4. As can be seen in Figure [1.4](https://thesis.lucblassel.com/what-is-sequence-data.html#fig:HPpercent), short and medium length homopolymers make up a significant part of the genome. In a previous GRCh38 human genome assembly, more than 1.9 megabases are in homopolymers of length 8 or higher <sup><a href="#ref-booeshaghiPseudoalignmentFacilitatesAssignment2022" role="doc-biblioref">98</a></sup>, representing about 1‰ of that assembly. The longest homopolymer run in the CHM13 v1.1 assembly is 86 *(90 in GRCh38 <sup><a href="#ref-booeshaghiPseudoalignmentFacilitatesAssignment2022" role="doc-biblioref">98</a></sup>)*.

![**Homopolymer fraction of the whole human genome by homopolymer length.**  
The homopolymer counts were calculated from the T2T consortium full human genome assembly CHM13 v1.1. This figure was inspired by Figure 3b of reference [@booeshaghiPseudoalignmentFacilitatesAssignment2022].](https://thesis.lucblassel.com/_main_files/figure-html/HPpercent-1.png)

Figure 1.4: **Homopolymer fraction of the whole human genome by homopolymer length.**  
The homopolymer counts were calculated from the T2T consortium full human genome assembly CHM13 v1.1. This figure was inspired by Figure 3b of reference <sup><a href="#ref-booeshaghiPseudoalignmentFacilitatesAssignment2022" role="doc-biblioref">98</a></sup>.

In the human genome, homopolymers tend to occur more often in adenine and thymine runs than guanine and cytosine. There are are approximately twice as many nucleotides within A or T homopolymers (481 Mb and 484 Mb) than G or C (278 Mb and 279 Mb). This discrepancy is even more pronounced when looking at homopolymers longer than four nucleotides (c.f. Figure [1.5](https://thesis.lucblassel.com/what-is-sequence-data.html#fig:HPdistrib)).

 $**Distribution of homopolymer lengths per base in the human genome, for homopolymers of length $\geq$ 4.**  
The homopolymer counts were calculated from the T2T consortium full human genome assembly CHM13 v1.1.$

Figure 1.5: **Distribution of homopolymer lengths per base in the human genome, for homopolymers of length ≥ $≥$ 4.**  
The homopolymer counts were calculated from the T2T consortium full human genome assembly CHM13 v1.1.

### 1.4.2 Homopolymers and long reads

Unfortunately, homopolymers are a source of errors in sequencing, particularly for long-read technologies. While substitutions seem to be randomly distributed along the reads for PacBio and ONT, the main error mode seems to be indels in homopolymeric sections, *i.e.* reading the same nucleotide several times or skipping over one of the repeated nucleotides. Many studies show that homopolymeric indels are the main type of error for PacBIO SMRT and ONT long-read sequencing <sup><a href="#ref-weiratherComprehensiveComparisonPacific2017" role="doc-biblioref">68</a>,<a href="#ref-delahayeSequencingDNANanopores2021" role="doc-biblioref">99</a> – <a href="#ref-dohmBenchmarkingLongreadCorrection2020" role="doc-biblioref">101</a></sup>. This is even the case for PacBio HiFi reads, while the circular consensus approach eliminates the randomly distributed substitutions but homopolymer indels remain <sup><a href="#ref-wengerAccurateCircularConsensus2019" role="doc-biblioref">87</a></sup>. It seems that ONT reads are more prone to this type of error than PacBIo <sup><a href="#ref-logsdonLongreadHumanGenome2020" role="doc-biblioref">56</a></sup>. The rate of these errors is independent of the length of the homopolymer for ONT, but it rises with homopolymer length for short-read and PacBio technologies <sup><a href="#ref-fooxPerformanceAssessmentDNA2021" role="doc-biblioref">102</a></sup>.

### 1.4.3 Accounting for homopolymers

The fact that they make up a significant part of the human genome, and that they are a source of errors for long read technologies means that homopolymers warrant special attention and care. Methods have been devised and implemented, specifically to counter homopolymer-linked errors.

#### 1.4.3.2 Homopolymer compression, a nifty trick

Homopolymer-errors can be harmful for downstream analyses such as read-mapping (c.f. Chapter [3](https://thesis.lucblassel.com/HPC-paper.html#HPC-paper)). However, in many cases, reads cannot be re-sequenced with newer technologies, or base-called with better base callers. Only the read sequences potentially containing homopolymer errors, are available for usage. In order to account for this sort of error, a simple pre-processing trick was developed: *homopolymer compression* (HPC).

The idea is very simple: for any sequence, replace a repeated run of any nucleotide (i.e. homopolymers) by a single occurrence of that nucleotide. This means that after going through HPC the sequence AAACTGGG will yield the sequence ACTG. This simple pre-processing step, applied to all the reads and sequences to analyze, removes all indels in homopolymers, and can resolve some ambiguities (c.f. Figure [1.6](https://thesis.lucblassel.com/what-is-sequence-data.html#fig:hpcSchema)). It can also remove legitimate information contained in homopolymers, but the trade-off with the reduced error rate has been deemed advantageous.

HPC has been implemented in many sequence bioinformatics software tools. The `HiCanu` <sup><a href="#ref-nurkHiCanuAccurateAssembly2020" role="doc-biblioref">112</a></sup>, `MDBG` <sup><a href="#ref-ekimMinimizerspaceBruijnGraphs2021" role="doc-biblioref">113</a></sup>, `wtdbg2` <sup><a href="#ref-ruanFastAccurateLongread2020" role="doc-biblioref">75</a></sup>, `shasta` <sup><a href="#ref-shafinNanoporeSequencingShasta2020" role="doc-biblioref">114</a></sup> assemblers all use HPC under the hood to provide better assemblies, and HPC was used to assemble the complete human genome sequence <sup><a href="#ref-nurkCompleteSequenceHuman2022" role="doc-biblioref">4</a></sup>. The first published usage of HPC, was actually in the `CABOG` assembler <sup><a href="#ref-millerAggressiveAssemblyPyrosequencing2008" role="doc-biblioref">115</a></sup> developed for pyrosequencing reads. HPC has also been implemented for other tasks, like clustering <sup><a href="#ref-sahlinNovoClusteringLongRead2020" role="doc-biblioref">116</a></sup>, long read error correction with `LSC` <sup><a href="#ref-auImprovingPacBioLong2012" role="doc-biblioref">117</a></sup> and `LSCPlus` <sup><a href="#ref-huLSCplusFastSolution2016" role="doc-biblioref">118</a></sup>, alignment with `minimap2` <sup><a href="#ref-liMinimap2PairwiseAlignment2018" role="doc-biblioref">119</a></sup> and `winnowmap2` <sup><a href="#ref-jainWeightedMinimizerSampling2020" role="doc-biblioref">120</a></sup>, or specific analysis pipelines for satellite tandem repeats <sup><a href="#ref-vannesteForensicSTRAnalysis2012" role="doc-biblioref">121</a></sup>.

![**Homopolymer compression can help resolve ambiguities due to sequencing errors.**  
A read with homopolymer related sequencing errors can be homologous to two different regions of the reference genome, with one discrepancy for each region. After applying HPC, this ambiguity is properly accounted for and the read is homologous to only one region. This figure, however, only shows one way homopolymers can be detrimental and others are possible^[Homopolymer indels can be harmful in opposite circumstances as well. Let us consider, for example, a read that should correspond to several repetitions of a conserved motif. Homopolymer indels can artificially resolve an ambiguity by making the read unique and prefer a specific repetition of the motif or entirely misplace the read.].
](https://thesis.lucblassel.com/figures/Sequence-Intro/Hpc.png)

Figure 1.6: **Homopolymer compression can help resolve ambiguities due to sequencing errors.**  
A read with homopolymer related sequencing errors can be homologous to two different regions of the reference genome, with one discrepancy for each region. After applying HPC, this ambiguity is properly accounted for and the read is homologous to only one region. This figure, however, only shows one way homopolymers can be detrimental and others are possible [^1].

## 1.5 Conclusion

I hope, after reading this chapter, you will agree with me that sequencing is fundamental for furthering our knowledge of biological processes, organisms and Life in general. And as such, the sequencing field is still very active with new technologies being developed to improve the current technologies in various aspects. Illumina promises high accuracy long reads with Infinity <sup><a href="#ref-HighPerformanceLong" role="doc-biblioref">97</a></sup> and PacBio is developing its own short read sequencing technology, moving away from sequencing by synthesis <sup><a href="#ref-ShortreadSequencingBinding" role="doc-biblioref">122</a>,<a href="#ref-cetinPlasmonicSensorCould2018" role="doc-biblioref">123</a></sup>. Finally, efforts are also being made to make sequencing more affordable and available in a greater number settings with Ultima genomics promising accurate short reads for as low as $1 per gigabase <sup><a href="#ref-almogyCostefficientWholeGenomesequencing2022" role="doc-biblioref">124</a></sup>.

With all these technological improvements we are approaching an era where sequencing is easy and quick, opening the door for massive projects like Tara Oceans <sup><a href="#ref-sunagawaTaraOceansGlobal2020" role="doc-biblioref">125</a></sup> or the BioGenome project <sup><a href="#ref-lewinEarthBioGenomeProject2018" role="doc-biblioref">126</a></sup> to better understand biodiversity. Routine whole-genome sequencing could also usher in an era personalized medicine <sup><a href="#ref-lightbodyReviewApplicationsHighthroughput2019" role="doc-biblioref">127</a></sup>.

Despite all these advancements, sequencing errors remain an obstacle to certain analyses. This is particularly true for the ever more used and useful long reads, and the important fraction of genomes made up of homopolymers. Detecting, removing or accounting for these errors in some way is a crucial step to improve any analysis based on sequencing data, and to make sure that no theory or conclusion are built upon erroneous sequence data.

Finally, it is important to note (at least for the remainder of this thesis) that, from a computational standpoint, a biological sequence is simply a succession of letters and a set of reads is simply a text file. Therefore, many analyses and data processing methods are inspired or directly transposed from the field of text algorithmics.

### References

1.

Watson, J. D. & Crick, F. H. C. [The Structure of Dna](https://doi.org/10.1101/sqb.1953.018.01.020). *Cold Spring Harb Symp Quant Biol* **18**, 123–131 (1953).

2.

Sanger, F. *et al.* [Nucleotide sequence of bacteriophage φX174 DNA](https://doi.org/10.1038/265687a0). *Nature* **265**, 687–695 (1977).

3.

Archer, C. T. *et al.* [The genome sequence of E. Coli W (ATCC 9637): Comparative genome analysis and an improved genome-scale reconstruction of E. coli](https://doi.org/10.1186/1471-2164-12-9). *BMC Genomics* **12**, 9 (2011).

4.

Nurk, S. *et al.* [The complete sequence of a human genome](https://doi.org/10.1126/science.abj6987). *Science* **376**, 44–53 (2022).

5.

Pellicer, J., Fay, M. F. & Leitch, I. J. [The largest eukaryotic genome of them all?](https://doi.org/10.1111/j.1095-8339.2010.01072.x) *Botanical Journal of the Linnean Society* **164**, 10–15 (2010).

6.

Macgregor, H. C. C-Value Paradox. in *Encyclopedia of Genetics* (eds. Brenner, S. & Miller, J. H.) 249–250 (Academic Press, 2001). doi:[10.1006/rwgn.2001.0301](https://doi.org/10.1006/rwgn.2001.0301).

7.

Alberts, B. *et al.* *[Molecular Biology of the Cell. 4th edition](https://www.ncbi.nlm.nih.gov/books/NBK26916/)*. (Garland Science, 2002).

8.

Crick, F. H. C., Barnett, L., Brenner, S. & Watts-Tobin, R. J. [General Nature of the Genetic Code for Proteins](https://doi.org/10.1038/1921227a0). *Nature* **192**, 1227–1232 (1961).

9.

International Human Genome Sequencing Consortium. [Finishing the euchromatic sequence of the human genome](https://doi.org/10.1038/nature03001). *Nature* **431**, 931–945 (2004).

10.

Elkon, R. & Agami, R. [Characterization of noncoding regulatory DNA in the human genome](https://doi.org/10.1038/nbt.3863). *Nat Biotechnol* **35**, 732–746 (2017).

11.

Omenn, G. S. [Reflections on the HUPO Human Proteome Project, the Flagship Project of the Human Proteome Organization, at 10Ỹears](https://doi.org/10.1016/j.mcpro.2021.100062). *Mol Cell Proteomics* **20**, 100062 (2021).

12.

Shabalina, S. A. & Spiridonov, N. A. [The mammalian transcriptome and the function of non-coding DNA sequences](https://doi.org/10.1186/gb-2004-5-4-105). *Genome Biol* **5**, 105 (2004).

13.

Consortium, T. E. P. [An Integrated Encyclopedia of DNA Elements in the Human Genome](https://doi.org/10.1038/nature11247). *Nature* **489**, 57–74 (2012).

14.

Chatterjee, N. & Walker, G. C. [Mechanisms of DNA damage, repair, and mutagenesis: DNA Damage and Repair](https://doi.org/10.1002/em.22087). *Environ. Mol. Mutagen.* **58**, 235–263 (2017).

15.

Fijalkowska, I. J., Schaaper, R. M. & Jonczyk, P. [DNA replication fidelity in Escherichia coli: A multi-DNA polymerase affair](https://doi.org/10.1111/j.1574-6976.2012.00338.x). *FEMS Microbiol Rev* **36**, 1105–1121 (2012).

16.

Pray, L. [DNA replication and causes of mutation](https://www.nature.com/scitable/topicpage/dna-replication-and-causes-of-mutation-409/). *Nature education* **1**, 214 (2008).

17.

Gout, J.-F., Thomas, W. K., Smith, Z., Okamoto, K. & Lynch, M. [Large-scale detection of in vivo transcription errors](https://doi.org/10.1073/pnas.1309843110). *Proceedings of the National Academy of Sciences* **110**, 18584–18589 (2013).

18.

Gout, J.-F. *et al.* [The landscape of transcription errors in eukaryotic cells](https://doi.org/10.1126/sciadv.1701484). *Sci Adv* **3**, e1701484 (2017).

19.

Shcherbakov, D. *et al.* [Ribosomal mistranslation leads to silencing of the unfolded protein response and increased mitochondrial biogenesis](https://doi.org/10.1038/s42003-019-0626-9). *Commun Biol* **2**, 1–16 (2019).

20.

Desouky, O., Ding, N. & Zhou, G. [Targeted and non-targeted effects of ionizing radiation](https://doi.org/10.1016/j.jrras.2015.03.003). *Journal of Radiation Research and Applied Sciences* **8**, 247–254 (2015).

21.

Kiefer, J. Effects of Ultraviolet Radiation on DNA. in *Chromosomal Alterations: Methods, Results and Importance in Human Health* (eds. Obe, G. & Vijayalaxmi) 39–53 (Springer, 2007). doi:[10.1007/978-3-540-71414-9\_3](https://doi.org/10.1007/978-3-540-71414-9_3).

22.

Bennett, J. W. & Klich, M. [Mycotoxins](https://doi.org/10.1128/cmr.16.3.497-516.2003). *Clin Microbiol Rev* **16**, 497–516 (2003).

23.

Kantidze, O. L., Velichko, A. K., Luzhin, A. V. & Razin, S. V. [Heat Stress-Induced DNA Damage](https://www.ncbi.nlm.nih.gov/pmc/articles/Pmc4947990). *Acta Naturae* **8**, 75–78 (2016).

24.

Gregory, C. D. & Milner, A. E. [Regulation of cell survival in Burkitt lymphoma: Implications from studies of apoptosis following cold-shock treatment](https://doi.org/10.1002/ijc.2910570321). *Int J Cancer* **57**, 419–426 (1994).

25.

Gafter-Gvili, A. *et al.* [Oxidative Stress-Induced DNA Damage and Repair in Human Peripheral Blood Mononuclear Cells: Protective Role of Hemoglobin](https://doi.org/10.1371/journal.pone.0068341). *PLoS One* **8**, e68341 (2013).

26.

Anagnostou, M. E. *et al.* [Transcription errors in aging and disease](https://doi.org/10.1016/j.tma.2021.05.002). *Translational Medicine of Aging* **5**, 31–38 (2021).

27.

Roth, J. R. [Frameshift mutations](https://doi.org/10.1146/annurev.ge.08.120174.001535). *Annu Rev Genet* **8**, 319–346 (1974).

28.

Kujovich, J. L. [Factor V Leiden thrombophilia](https://doi.org/10.1097/GIM.0b013e3181faa0f2). *Genetics in Medicine* **13**, 1–16 (2011).

29.

Cutting, G. R. [Cystic fibrosis genetics: From molecular understanding to clinical application](https://doi.org/10.1038/nrg3849). *Nat Rev Genet* **16**, 45–56 (2015).

30.

Fuchsberger, C. *et al.* [The genetic architecture of type 2 diabetes](https://doi.org/10.1038/nature18642). *Nature* **536**, 41–47 (2016).

31.

Morris, A. P. *et al.* [Large-scale association analysis provides insights into the genetic architecture and pathophysiology of type 2 diabetes](https://doi.org/10.1038/ng.2383). *Nat Genet* **44**, 981–990 (2012).

32.

Woodford, N. & Ellington, M. J. [The emergence of antibiotic resistance by mutation](https://doi.org/10.1111/j.1469-0691.2006.01492.x). *Clinical Microbiology and Infection* **13**, 5–18 (2007).

33.

Rhee, S.-Y. *et al.* [Human immunodeficiency virus reverse transcriptase and protease sequence database](https://doi.org/10.1093/nar/gkg100). *Nucleic Acids Res* **31**, 298–303 (2003).

34.

Sanger, F., Nicklen, S. & Coulson, A. R. [DNA sequencing with chain-terminating inhibitors](https://doi.org/10.1073/pnas.74.12.5463). *Proceedings of the National Academy of Sciences* **74**, 5463–5467 (1977).

35.

Smith, L. M., Fung, S., Hunkapiller, M. W., Hunkapiller, T. J. & Hood, L. E. [The synthesis of oligonucleotides containing an aliphatic amino group at the 5′ terminus: Synthesis of fluorescent DNA primers for use in DNA sequence analysis](https://doi.org/10.1093/nar/13.7.2399). *Nucleic Acids Research* **13**, 2399–2412 (1985).

36.

Smith, L. M. *et al.* [Fluorescence detection in automated DNA sequence analysis](https://doi.org/10.1038/321674a0). *Nature* **321**, 674–679 (1986).

37.

Ansorge, W., Sproat, B., Stegemann, J., Schwager, C. & Zenke, M. [Automated DNA sequencing: Ultrasensitive detection of fluorescent bands during electrophoresis](https://doi.org/10.1093/nar/15.11.4593). *Nucleic Acids Research* **15**, 4593–4602 (1987).

38.

Shendure, J. & Ji, H. [Next-generation DNA sequencing](https://doi.org/10.1038/nbt1486). *Nat Biotechnol* **26**, 1135–1145 (2008).

39.

Collins, F. S., Morgan, M. & Patrinos, A. [The Human Genome Project: Lessons from Large-Scale Biology](https://doi.org/10.1126/science.1084564). *Science* **300**, 286–290 (2003).

40.

Liu, L. *et al.* [Comparison of Next-Generation Sequencing Systems](https://doi.org/10.1155/2012/251364). *Journal of Biomedicine and Biotechnology* **2012**, e251364 (2012).

41.

The Cost of Sequencing a Human Genome. [https://www.genome.gov/about-genomics/fact-sheets/Sequencing-Human-Genome-cost](https://www.genome.gov/about-genomics/fact-sheets/Sequencing-Human-Genome-cost).

42.

Metzker, M. L. [Sequencing technologies — the next generation](https://doi.org/10.1038/nrg2626). *Nat Rev Genet* **11**, 31–46 (2010).

43.

Canard, B. & Sarfati, R. S. [DNA polymerase fluorescent substrates with reversible 3′-tags](https://doi.org/10.1016/0378-1119\(94\)90226-7). *Gene* **148**, 1–6 (1994).

44.

Nyren, P., Pettersson, B. & Uhlen, M. [Solid Phase DNA Minisequencing by an Enzymatic Luminometric Inorganic Pyrophosphate Detection Assay](https://doi.org/10.1006/abio.1993.1024). *Analytical Biochemistry* **208**, 171–175 (1993).

45.

Mardis, E. R. [A decade’s perspective on DNA sequencing technology](https://doi.org/10.1038/nature09796). *Nature* **470**, 198–203 (2011).

47.

Sequencing Technology | Sequencing by synthesis. [https://www.illumina.com/science/technology/next-generation-sequencing/sequencing-technology.html](https://www.illumina.com/science/technology/next-generation-sequencing/sequencing-technology.html).

48.

Pollard, M. O., Gurdasani, D., Mentzer, A. J., Porter, T. & Sandhu, M. S. [Long reads: Their purpose and place](https://doi.org/10.1093/hmg/ddy177). *Human Molecular Genetics* **27**, R234–r241 (2018).

49.

Eid, J. *et al.* [Real-Time DNA Sequencing from Single Polymerase Molecules](https://doi.org/10.1126/science.1162986). *Science* **323**, 133–138 (2009).

50.

Levene, M. J. *et al.* [Zero-Mode Waveguides for Single-Molecule Analysis at High Concentrations](https://doi.org/10.1126/science.1079700). *Science* **299**, 682–686 (2003).

51.

Clarke, J. *et al.* [Continuous base identification for single-molecule nanopore DNA sequencing](https://doi.org/10.1038/nnano.2009.12). *Nature Nanotech* **4**, 265–270 (2009).

52.

Deamer, D., Akeson, M. & Branton, D. [Three decades of nanopore sequencing](https://doi.org/10.1038/nbt.3423). *Nat Biotechnol* **34**, 518–524 (2016).

53.

Wick, R. R., Judd, L. M. & Holt, K. E. [Performance of neural network basecalling tools for Oxford Nanopore sequencing](https://doi.org/10.1186/s13059-019-1727-y). *Genome Biol* **20**, 129 (2019).

54.

Rhoads, A. & Au, K. F. [PacBio Sequencing and Its Applications](https://doi.org/10.1016/j.gpb.2015.08.002). *Genomics, Proteomics & Bioinformatics* **13**, 278–289 (2015).

55.

Ip, C. L. C. *et al.* [MinION Analysis and Reference Consortium: Phase 1 data release and analysis](https://doi.org/10.12688/f1000research.7201.1). *F1000Res* **4**, 1075 (2015).

56.

Logsdon, G. A., Vollger, M. R. & Eichler, E. E. [Long-read human genome sequencing and its applications](https://doi.org/10.1038/s41576-020-0236-x). *Nat Rev Genet* **21**, 597–614 (2020).

57.

Jain, M. *et al.* [Nanopore sequencing and assembly of a human genome with ultra-long reads](https://doi.org/10.1038/nbt.4060). *Nat Biotechnol* **36**, 338–345 (2018).

59.

Payne, A., Holmes, N., Rakyan, V. & Loose, M. [BulkVis: A graphical viewer for Oxford nanopore bulk FAST5 files](https://doi.org/10.1093/bioinformatics/bty841). *Bioinformatics* **35**, 2193–2198 (2019).

60.

Murigneux, V. *et al.* [Comparison of long-read methods for sequencing and assembly of a plant genome](https://doi.org/10.1093/gigascience/giaa146). *GigaScience* **9**, giaa146 (2020).

61.

Chaisson, M. J. P. *et al.* [Resolving the complexity of the human genome using single-molecule sequencing](https://doi.org/10.1038/nature13907). *Nature* **517**, 608–611 (2015).

62.

Jain, M., Olsen, H. E., Paten, B. & Akeson, M. [The Oxford Nanopore MinION: Delivery of nanopore sequencing to the genomics community](https://doi.org/10.1186/s13059-016-1103-0). *Genome Biol* **17**, 239 (2016).

63.

Hong, M. *et al.* [RNA sequencing: New technologies and applications in cancer research](https://doi.org/10.1186/s13045-020-01005-x). *Journal of Hematology & Oncology* **13**, 166 (2020).

64.

Ozsolak, F. & Milos, P. M. [RNA sequencing: Advances, challenges and opportunities](https://doi.org/10.1038/nrg2934). *Nat Rev Genet* **12**, 87–98 (2011).

65.

Hunt, D. F., Yates, J. R., Shabanowitz, J., Winston, S. & Hauer, C. R. [Protein sequencing by tandem mass spectrometry.](https://doi.org/10.1073/pnas.83.17.6233) *Proceedings of the National Academy of Sciences* **83**, 6233–6237 (1986).

66.

Smith, B. J. *Protein Sequencing Protocols*. (Springer Science & Business Media, 2002). doi:[10.1385/1592593429](https://doi.org/10.1385/1592593429).

67.

Restrepo-Pérez, L., Joo, C. & Dekker, C. [Paving the way to single-molecule protein sequencing](https://doi.org/10.1038/s41565-018-0236-6). *Nature Nanotech* **13**, 786–796 (2018).

68.

Weirather, J. L. *et al.* [Comprehensive comparison of Pacific Biosciences and Oxford Nanopore Technologies and their applications to transcriptome analysis](https://doi.org/10.12688/f1000research.10571.2). *F1000Res* **6**, 100 (2017).

69.

Wang, Y., Zhao, Y., Bollas, A., Wang, Y. & Au, K. F. [Nanopore sequencing technology, bioinformatics and applications](https://doi.org/10.1038/s41587-021-01108-x). *Nat Biotechnol* **39**, 1348–1365 (2021).

71.

Lima, L. *et al.* [Comparative assessment of long-read error correction software applied to Nanopore RNA-sequencing data](https://doi.org/10.1093/bib/bbz058). *Briefings in Bioinformatics* **21**, 1164–1181 (2020).

73.

Zhang, H., Jain, C. & Aluru, S. [A comprehensive evaluation of long read error correction methods](https://doi.org/10.1186/s12864-020-07227-0). *BMC Genomics* **21**, 889 (2020).

74.

Amarasinghe, S. L. *et al.* [Opportunities and challenges in long-read sequencing data analysis](https://doi.org/10.1186/s13059-020-1935-5). *Genome Biology* **21**, 30 (2020).

75.

Ruan, J. & Li, H. [Fast and accurate long-read assembly with Wtdbg2](https://doi.org/10.1038/s41592-019-0669-3). *Nat Methods* **17**, 155–158 (2020).

76.

Koren, S. *et al.* [Canu: Scalable and accurate long-read assembly via adaptive k-mer weighting and repeat separation](https://doi.org/10.1101/gr.215087.116). *Genome Res.* **27**, 722–736 (2017).

77.

Tischler, G. & Myers, E. W. Non Hybrid Long Read Consensus Using Local De Bruijn Graph Assembly. 106252 (2017) doi:[10.1101/106252](https://doi.org/10.1101/106252).

78.

Warren, R. L. *et al.* [ntEdit: Scalable genome sequence polishing](https://doi.org/10.1093/bioinformatics/btz400). *Bioinformatics* **35**, 4430–4432 (2019).

79.

Hepler, N. L. *et al.* [An Improved Circular Consensus Algorithm with an Application to Detect HIV-1 Drug-Resistance Associated Mutations (DRAMs)](https://www.pacb.com/wp-content/uploads/improved-circular-consensus-algorithm-with-application-to-detection-hiv-1-drams.pdf). in *Conference on advances in genome biology and technology* 1 (2016).

80.

Simpson, J. T. *et al.* [Detecting DNA cytosine methylation using nanopore sequencing](https://doi.org/10.1038/nmeth.4184). *Nat Methods* **14**, 407–410 (2017).

81.

Vaser, R., Sović, I., Nagarajan, N. & Šikić, M. [Fast and accurate de novo genome assembly from long uncorrected reads](https://doi.org/10.1101/gr.214270.116). *Genome Res* **27**, 737–746 (2017).

82.

Hackl, T., Hedrich, R., Schultz, J. & Förster, F. [Proovread: Large-scale high-accuracy PacBio correction through iterative short read consensus](https://doi.org/10.1093/bioinformatics/btu392). *Bioinformatics* **30**, 3004–3011 (2014).

83.

Miclotte, G. *et al.* [Jabba: Hybrid error correction for long sequencing reads](https://doi.org/10.1186/s13015-016-0075-7). *Algorithms for Molecular Biology* **11**, 10 (2016).

84.

Koren, S. *et al.* [Hybrid error correction and de novo assembly of single-molecule sequencing reads](https://doi.org/10.1038/nbt.2280). *Nat Biotechnol* **30**, 693–700 (2012).

85.

Salmela, L. & Rivals, E. [LoRDEC: Accurate and efficient long read error correction](https://doi.org/10.1093/bioinformatics/btu538). *Bioinformatics* **30**, 3506–3514 (2014).

86.

Walker, B. J. *et al.* [Pilon: An Integrated Tool for Comprehensive Microbial Variant Detection and Genome Assembly Improvement](https://doi.org/10.1371/journal.pone.0112963). *Plos One* **9**, e112963 (2014).

87.

Wenger, A. M. *et al.* [Accurate circular consensus long-read sequencing improves variant detection and assembly of a human genome](https://doi.org/10.1038/s41587-019-0217-9). *Nat Biotechnol* **37**, 1155–1162 (2019).

88.

Timp, W., Comer, J. & Aksimentiev, A. [DNA Base-Calling from a Nanopore Using a Viterbi Algorithm](https://doi.org/10.1016/j.bpj.2012.04.009). *Biophysical Journal* **102**, L37–l39 (2012).

89.

Perešíni, P., Boža, V., Brejová, B. & Vinař, T. [Nanopore base calling on the edge](https://doi.org/10.1093/bioinformatics/btab528). *Bioinformatics* **37**, 4661–4667 (2021).

90.

Boža, V., Brejová, B. & Vinař, T. [DeepNano: Deep recurrent neural networks for base calling in MinION nanopore reads](https://doi.org/10.1371/journal.pone.0178751). *Plos One* **12**, e0178751 (2017).

91.

Tyler, A. D. *et al.* [Evaluation of Oxford Nanopore’s MinION Sequencing Device for Microbial Whole Genome Sequencing Applications](https://doi.org/10.1038/s41598-018-29334-5). *Sci Rep* **8**, 10931 (2018).

92.

Lin, B., Hui, J. & Mao, H. [Nanopore Technology and Its Applications in Gene Sequencing](https://doi.org/10.3390/bios11070214). *Biosensors* **11**, 214 (2021).

93.

Oxford Nanopore Tech Update: New Duplex method for Q30 nanopore single molecule reads, PromethION 2, and more. [http://nanoporetech.com/about-us/news/oxford-nanopore-tech-update-new-duplex-method-q30-nanopore-single-molecule-reads-0](http://nanoporetech.com/about-us/news/oxford-nanopore-tech-update-new-duplex-method-q30-nanopore-single-molecule-reads-0).

94.

Sanderson, N. *et al.* Comparison of R9.4.1/Kit10 and R10/Kit12 Oxford Nanopore flowcells and chemistries in bacterial genome reconstruction. 2022.04.29.490057 (2022) doi:[10.1101/2022.04.29.490057](https://doi.org/10.1101/2022.04.29.490057).

95.

Karst, S. M. *et al.* [High-accuracy long-read amplicon sequences using unique molecular identifiers with Nanopore or PacBio sequencing](https://doi.org/10.1038/s41592-020-01041-y). *Nat Methods* **18**, 165–169 (2021).

96.

Chen, Z. *et al.* [Highly accurate fluorogenic DNA sequencing with information theory–based error correction](https://doi.org/10.1038/nbt.3982). *Nat Biotechnol* **35**, 1170–1178 (2017).

97.

High Performance Long Read Assay Enables Contiguous Data up to 10Kb on Existing Illumina Platforms. [https://www.illumina.com/content/illumina-marketing/amr/en\_US/science/genomics-research/articles/infinity-high-performance-long-read-assay.html](https://www.illumina.com/content/illumina-marketing/amr/en_US/science/genomics-research/articles/infinity-high-performance-long-read-assay.html).

98.

Booeshaghi, A. S. & Pachter, L. Pseudoalignment facilitates assignment of error-prone Ultima Genomics reads. 2022.06.04.494845 (2022) doi:[10.1101/2022.06.04.494845](https://doi.org/10.1101/2022.06.04.494845).

99.

Delahaye, C. & Nicolas, J. [Sequencing DNA with nanopores: Troubles and biases](https://doi.org/10.1371/journal.pone.0257521). *Plos One* **16**, e0257521 (2021).

101.

Dohm, J. C., Peters, P., Stralis-Pavese, N. & Himmelbauer, H. [Benchmarking of long-read correction methods](https://doi.org/10.1093/nargab/lqaa037). *NAR Genomics and Bioinformatics* **2**, (2020).

102.

Foox, J. *et al.* [Performance assessment of DNA sequencing platforms in the ABRF Next-Generation Sequencing Study](https://doi.org/10.1038/s41587-021-01049-5). *Nat Biotechnol* **39**, 1129–1140 (2021).

103.

Huang, Y.-T., Liu, P.-Y. & Shih, P.-W. [Homopolish: A method for the removal of systematic errors in nanopore sequencing by homologous polishing](https://doi.org/10.1186/s13059-021-02282-6). *Genome Biology* **22**, 95 (2021).

104.

Rang, F. J., Kloosterman, W. P. & de Ridder, J. [From squiggle to basepair: Computational approaches for improving nanopore sequencing read accuracy](https://doi.org/10.1186/s13059-018-1462-9). *Genome Biology* **19**, 90 (2018).

105.

Sarkozy, P., Jobbágy, Á. & Antal, P. Calling Homopolymer Stretches from Raw Nanopore Reads by Analyzing k-mer Dwell Times. in *Embec & Nbc 2017* (eds. Eskola, H., Väisänen, O., Viik, J. & Hyttinen, J.) 241–244 (Springer, 2018). doi:[10.1007/978-981-10-5122-7\_61](https://doi.org/10.1007/978-981-10-5122-7_61).

106.

Hawkins, J. A., Jones, S. K., Finkelstein, I. J. & Press, W. H. [Indel-correcting DNA barcodes for high-throughput sequencing](https://doi.org/10.1073/pnas.1802640115). *Proceedings of the National Academy of Sciences* **115**, E6217–e6226 (2018).

107.

Srivathsan, A. *et al.* [A MinION™-based pipeline for fast and cost-effective DNA barcoding](https://doi.org/10.1111/1755-0998.12890). *Molecular Ecology Resources* **18**, 1035–1049 (2018).

108.

Wang, Y., Noor-A-Rahim, Md., Gunawan, E., Guan, Y. L. & Poh, C. L. [Construction of Bio-Constrained Code for DNA Data Storage](https://doi.org/10.1109/lcomm.2019.2912572). *IEEE Communications Letters* **23**, 963–966 (2019).

109.

R10.3: The newest nanopore for high accuracy nanopore sequencing – now available in store. [http://nanoporetech.com/about-us/news/r103-newest-nanopore-high-accuracy-nanopore-sequencing-now-available-store](http://nanoporetech.com/about-us/news/r103-newest-nanopore-high-accuracy-nanopore-sequencing-now-available-store).

110.

Zhou, L. *et al.* [Detection of DNA homopolymer with graphene nanopore](https://doi.org/10.1116/1.5116295). *Journal of Vacuum Science & Technology B* **37**, 061809 (2019).

111.

Goto, Y., Yanagi, I., Matsui, K., Yokoi, T. & Takeda, K. [Identification of four single-stranded DNA homopolymers with a solid-state nanopore in alkaline CsCl solution](https://doi.org/10.1039/c8nr04238a). *Nanoscale* **10**, 20844–20850 (2018).

112.

Nurk, S. *et al.* [HiCanu: Accurate assembly of segmental duplications, satellites, and allelic variants from high-fidelity long reads](https://doi.org/10.1101/gr.263566.120). *Genome Res.* **30**, 1291–1305 (2020).

113.

Ekim, B., Berger, B. & Chikhi, R. [Minimizer-space de Bruijn graphs: Whole-genome assembly of long reads in minutes on a personal computer](https://doi.org/10.1016/j.cels.2021.08.009). *Cell Systems* **12**, 958–968.e6 (2021).

114.

Shafin, K. *et al.* [Nanopore sequencing and the Shasta toolkit enable efficient de novo assembly of eleven human genomes](https://doi.org/10.1038/s41587-020-0503-6). *Nat Biotechnol* **38**, 1044–1053 (2020).

115.

Miller, J. R. *et al.* [Aggressive assembly of pyrosequencing reads with mates](https://doi.org/10.1093/bioinformatics/btn548). *Bioinformatics* **24**, 2818–2824 (2008).

116.

Sahlin, K. & Medvedev, P. [De Novo Clustering of Long-Read Transcriptome Data Using a Greedy, Quality Value-Based Algorithm](https://doi.org/10.1089/cmb.2019.0299). *Journal of Computational Biology* **27**, 472–484 (2020).

117.

Au, K. F., Underwood, J. G., Lee, L. & Wong, W. H. [Improving PacBio Long Read Accuracy by Short Read Alignment](https://doi.org/10.1371/journal.pone.0046679). *Plos One* **7**, e46679 (2012).

118.

Hu, R., Sun, G. & Sun, X. [LSCplus: A fast solution for improving long read accuracy by short read alignment](https://doi.org/10.1186/s12859-016-1316-y). *BMC Bioinformatics* **17**, 451 (2016).

119.

Li, H. [Minimap2: Pairwise alignment for nucleotide sequences](https://doi.org/10.1093/bioinformatics/bty191). *Bioinformatics* **34**, 3094–3100 (2018).

120.

Jain, C. *et al.* [Weighted minimizer sampling improves long read mapping](https://doi.org/10.1093/bioinformatics/btaa435). *Bioinformatics* **36**, i111–i118 (2020).

121.

Van Neste, C., Van Nieuwerburgh, F., Van Hoofstat, D. & Deforce, D. [Forensic STR analysis using massive parallel sequencing](https://doi.org/10.1016/j.fsigen.2012.03.004). *Forensic Science International: Genetics* **6**, 810–818 (2012).

122.

Short-read sequencing by binding. [https://www.pacb.com/technology/sequencing-by-binding/](https://www.pacb.com/technology/sequencing-by-binding/).

123.

Cetin, A. E. *et al.* [Plasmonic Sensor Could Enable Label-Free DNA Sequencing](https://doi.org/10.1021/acssensors.7b00957). *ACS Sens.* **3**, 561–568 (2018).

124.

Almogy, G. *et al.* Cost-efficient whole genome-sequencing using novel mostly natural sequencing-by-synthesis chemistry and open fluidics platform. 2022.05.29.493900 (2022) doi:[10.1101/2022.05.29.493900](https://doi.org/10.1101/2022.05.29.493900).

125.

Sunagawa, S. *et al.* [Tara Oceans: Towards global ocean ecosystems biology](https://doi.org/10.1038/s41579-020-0364-5). *Nat Rev Microbiol* **18**, 428–445 (2020).

126.

Lewin, H. A. *et al.* [Earth BioGenome Project: Sequencing life for the future of life](https://doi.org/10.1073/pnas.1720115115). *Proceedings of the National Academy of Sciences* **115**, 4325–4333 (2018).

127.

Lightbody, G. *et al.* [Review of applications of high-throughput sequencing in personalized medicine: Barriers and facilitators of future progress in research and clinical application](https://doi.org/10.1093/bib/bby051). *Briefings in Bioinformatics* **20**, 1795–1811 (2019).

---

[^1]: Homopolymer indels can be harmful in opposite circumstances as well. Let us consider, for example, a read that should correspond to several repetitions of a conserved motif. Homopolymer indels can artificially resolve an ambiguity by making the read unique and prefer a specific repetition of the motif or entirely misplace the read.