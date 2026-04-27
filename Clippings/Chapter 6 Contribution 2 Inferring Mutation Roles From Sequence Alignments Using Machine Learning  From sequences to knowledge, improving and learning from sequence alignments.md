---
title: "Chapter 6 Contribution 2: Inferring Mutation Roles From Sequence Alignments Using Machine Learning | From sequences to knowledge, improving and learning from sequence alignments"
source: "https://thesis.lucblassel.com/HIV-paper.html"
author:
  - "[[Luc Blassel]]"
published:
created: 2026-04-26
description: "Chapter 6 Contribution 2: Inferring Mutation Roles From Sequence Alignments Using Machine Learning | From sequences to knowledge, improving and learning from sequence alignments"
tags:
  - "clippings"
---
## Chapter 6 Contribution 2: Inferring Mutation Roles From Sequence Alignments Using Machine Learning

As we have seen in Sections [5.2.1](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#quick-presentation-of-hiv) and [5.3.3](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#consequences-of-resistance-on-global-health), the HIV pandemic is a widespread threat to public health which can have very serious consequences at the infected individual’s level and at the population scale. Despite many advances in drug development, fundamental research in new drug targets drug resistance mutations arise very quickly in response to antiretroviral therapy. This is especially important in lower income countries where the drug switching options are less numerous and give rise to multi-resistant viruses. In order to manage this global pandemic, surveying the viral infections, finding and categorizing new drug resistance mutations is very important. One such way to do this is to use HIV viral sequences, obtained from patients, and use their alignment as input for statistical and machine learning methods *(c.f. Chapter [4](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#learning-from-sequences-and-alignments) and Section [5.3.4](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#finding-drms))*. In this chapter, I will present some work done on studying drug resistance mutations in HIV sequences using a large sequence alignment and machine learning methods.

This chapter was written as an article titled: **“Using Machine Learning and Big Data to Explore the Drug Resistance Landscape in HIV”**. It was originally published in *August 2021*, in *PLoS Computational Biology* ([*doi:10.1371/journal.pcbi.1008873*](https://doi.org/10.1371/journal.pcbi.1008873)) and is presented as is, without any modification from the published version. The author list, complete with affiliations is given below:  

Luc Blassel <sup><strong>1</strong>,<strong>2</strong> *</sup>, Anna Tostevin <sup><strong>3</strong></sup>, Christian Julian Villabona-Arenas <sup><strong>4</strong>,<strong>5</strong></sup>, Martine Peeters <sup><strong>6</strong></sup>, Stéphane Hué <sup><strong>4</strong>,<strong>5</strong></sup>, Olivier Gascuel <sup><strong>1</strong>,<strong>7</strong> #</sup> On behalf of the UK HIV Drug Resistance Database <sup><span role="presentation">∧ <span role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="inline" data-latex="∧"><mo>∧</mo></math></span></span> <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline" data-latex="\wedge">\wedge</math></sup>

**1** Unité de Bioinformatique Évolutive, Institut Pasteur, Paris, France  
**2** Sorbonne Université, Collège doctoral, Paris, France  
**3** Institute for Global Health, UCL, London, UK  
**4** Department of Infectious Disease Epidemiology, London School of Hygiene and Tropical Medicine, London, UK  
**5** Centre for Mathematical Modelling of Infectious Diseases, London School of Hygiene and Tropical Medicine, London, UK  
**6** TransVIHMI (Recherches Translationnelles sur VIH et Maladies Infectieuses), Université de Montpellier, Institut de Recherche pour le Développement, INSERM, Montpellier, France  
**7** Institut de Systématique, Evolution, Biodiversité (ISYEB), UMR 7205 - Muséum National d’Histoire Naturelle, CNRS, SU, EPHE and UA, Paris, France

\# Current address: Institut de Systématique, Evolution, Biodiversité (ISYEB), UMR 7205 - Muséum National d’Histoire Naturelle, CNRS, SU, EPHE and UA, Paris, France  
\* luc.blassel@pasteur.fr (LB)  
\* olivier.gascuel@mnhn.fr (OG)

<sup><span role="presentation">∧ <span role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="inline" data-latex="∧"><mo>∧</mo></math></span></span> <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline" data-latex="\wedge">\wedge</math></sup> Membership list can be found in the acknowledgments section

## Abstract

Drug resistance mutations (DRMs) appear in HIV under treatment pressure. DRMs are commonly transmitted to naive patients. The standard approach to reveal new DRMs is to test for significant frequency differences of mutations between treated and naive patients. However, we then consider each mutation individually and cannot hope to study interactions between several mutations. Here, we aim to leverage the ever-growing quantity of high-quality sequence data and machine learning methods to study such interactions (i.e. epistasis), as well as try to find new DRMs.

We trained classifiers to discriminate between Reverse Transcriptase Inhibitor (RTI)-experienced and RTI-naive samples on a large HIV-1 reverse transcriptase (RT) sequence dataset from the UK (n≈55,000 $n≈55,000$ $n\approx 55,000$), using all observed mutations as binary representation features. To assess the robustness of our findings, our classifiers were evaluated on independent data sets, both from the UK and Africa. Important representation features for each classifier were then extracted as potential DRMs. To find novel DRMs, we repeated this process by removing either features or samples associated to known DRMs.

When keeping all known resistance signal, we detected sufficiently prevalent known DRMs, thus validating the approach. When removing features corresponding to known DRMs, our classifiers retained some prediction accuracy, and six new mutations significantly associated with resistance were identified. These six mutations have a low genetic barrier, are correlated to known DRMs, and are spatially close to either the RT active site or the regulatory binding pocket. When removing both known DRM features and sequences containing at least one known DRM, our classifiers lose all prediction accuracy. These results likely indicate that all mutations directly conferring resistance have been found, and that our newly discovered DRMs are accessory or compensatory mutations. Moreover, apart from the accessory nature of the relationships we found, we did not find any significant signal of further, more subtle epistasis combining several mutations which individually do not seem to confer any resistance.

## Author summary

Almost all drugs to treat HIV target the Reverse Transcriptase (RT) and Drug resistance mutations (DRMs) appear in HIV under treatment pressure. Resistant strains can be transmitted and limit treatment options at the population level. Classically, multiple statistical testing is used to find DRMs, by comparing virus sequences of treated and naive populations. However, with this method, each mutation is considered individually and we cannot hope to reveal any interaction (epistasis) between them. Here, we used machine learning to discover new DRMs and study potential epistasis effects. We applied this approach to a very large UK dataset comprising ≈55,000 $≈55,000$ $\approx 55,000$ RT sequences. Results robustness was checked on different UK and African datasets.

Six new mutations associated to resistance were found. All six have a low genetic barrier and show high correlations with known DRMs. Moreover, all these mutations are close to either the active site or the regulatory binding pocket of RT. Thus, they are good candidates for further wet experiments to establish their role in drug resistance. Importantly, our results indicate that epistasis seems to be limited to the classical scheme where primary DRMs confer resistance and associated mutations modulate the strength of the resistance and/or compensate for the fitness cost induced by DRMs.

## 6.1 Introduction

Drug resistance mutations (DRMs) arise in Human Immunodeficiency Virus-1 (HIV-1) due to antiretroviral treatment pressure, leading to viral rebound and treatment failure [^15]. Furthermore, drug-resistant HIV strains can be transmitted to treatment-naive individuals and further spread throughout the population over time [^8]. These transmitted resistant variants limit baseline treatment options and have clinical and public health implications worldwide. Almost all drugs to treat HIV target the reverse transcriptase (RT), encoded by the *pol* gene. Lists of DRMs are regularly compiled and updated by experts in the field, based on genotype analyses and phenotypic resistance tests or clinical outcome in patients on ART [^18]. However, with the developement of new antiretroviral drugs that target RT but also other regions of the *pol* gene like protease or integrase, and the use of anti-retrovirals in high risk populations by pre-exposure prophylaxis (PREP), it is important to further our understanding of HIV polymorphisms and notably the interactions between mutations and epistatic effects.

Among known DRMs, some mutations, such as M184V, directly confer resistance to antiretrovirals, more precisely the commonly used NRTI, 3TC (lamivudine) and FTC (emtricitabine), and are called primary or major drug resistance mutations, while some mutations like E40F have an accessory role and increases drug resistance when appearing alongside primary DRMs. Moreover, some mutations like S68G seem to have a compensatory role, but are not known to confer any resistance nor modulate resistance induced by primary DRMs. All of these mutations might have different functions in the virus, but they are all known to be associated with drug resistance phenomena. Therefore, during the rest of this article we will refer to all of these known mutations as resistance associated mutations (RAMs), rather than DRMs which is too specific, and our goal will be to search for new RAMs and study the interactions between known RAMs and the new ones.

Classically, new RAMs have been found using statistical testing and large multiple sequence alignments (MSA) of the studied protein [^10]. Tests are performed for mutations of interest on a given MSA to check if they are associated with the treatment status and outcome of the individual the viral sequences were sampled from. The test significance is corrected for multiple testing as all mutations associated to every MSA position is virtually a resistance mutation and tested. After this preliminary statistical search, the selected mutations are scrutinized to remove the effects of phylogenetic correlation (i.e. typically counting two sequences which are identical or closely related due to transmission rather than independent acquisition twice [^21]) and check that the same mutation occurred several times in different subtypes and populations being treated with the same drug. Then, these mutations can be further experimentally tested in vitro or in vivo to validate phenotypic resistance. This method has worked well, but by design it is not ideal for studying the effect of several mutations at once, since if we have to test all couples or triplets of mutations, we quickly lose statistical power when correcting for multiple testing [^11], due to the large number of tests to perform. Moreover, phylogenetic correlation is again a critical issue with such an approach.

Machine learning has been extensively used to predict resistance to antiretrovirals from sequence data. There are two main approaches to predicting resistance from sequence data. Regression, where machine learning models are trained to predict the value of a drug resistance indicator, typically IC50 $IC50$ $IC_{50}$ fold change in response to a given drug [^22] or other indicators from phenotypic resistance assays such as PhenoSense [^23]. Many methods have been used to predict a resistance level: Support Vector Machines (SVMs) [^24], k-Nearest Neighbors (KNN) and Random Forests (RFs) [^25], and more recently Artificial Neural Networks (ANNs) [^12]. Alternatively, this task has also been approached as a classification problem. Given a certain threshold on a phenotypic resistance measure, sequences are given a label of "resistant" or "susceptible" to a certain drug. Machine learning classifiers are then trained to predict that label. For this task, SVMs and decision trees have been used [^13], ensemble classifier chains [^14] and also ANNs [^29]. Most recently Steiner *et al.*[^2] have used Deep Learning Architectures to predict resistance status (i.e. classification) from sequence data. Since phenotypic assays are more complicated and costly to perform than simple genotyping, there is a limited number of sequences paired with a resistance level. This is the main limitation of these studies since machine learning methods typically benefit from a large amount of training data. This is especially true for deep neural networks which can need hundreds of thousands of training samples for certain tasks and architectures. However, despite this limitation, approaches proposed in these studies seem to have fairly good predictive accuracy. It is important to note that all of these studies aim to predict if a given sequence is resistant or not to a given drug, they do not aim to find new potential RAMs. Although Steiner *et al.*[^2] have checked that known DRM positions are captured by their models and found several positions potentially associated to resistance, it is not the main goal of their method.

It is accepted in machine learning that there is a trade-off between model accuracy and model interpretability. In these previous studies the goal was to make the most accurate predictions possible, using complex models such as SVMs and ANNs, therefore sacrificing interpretability. Here, we have a different approach, using simpler models that might be less accurate but whose predictions we can understand and interpret. We train these models to discriminate RTI-naive from RTI-experienced sequences. Without the need for phenotypic data, we are able to use much larger HIV-1 RT sequence datasets from the UK (n≈55,000 $n≈55,000$ $n\approx55,000$) ([http://www.hivrdb.org.uk/](http://www.hivrdb.org.uk/)) and Africa (n≈4,000 $n≈4,000$ $n\approx4,000$) [^10]. By using interpretable models, we can extract mutations that are important for determining if a sequence is treated or not and potentially find new mutations potentially associated to resistance. Furthermore, we aim to detect associations between mutations and their effect on antiretroviral resistance in order to study potential underlying epistasis. The African and UK datasets are very different both from genetic and treatment history standpoints, therefore training classifiers on the UK dataset and testing them on the African one, should guarantee the robustness of our findings and greatly alleviate phylogenetic correlation effects. In the following sections, we first describe the data then the methods used. Our results include the assessment of the performance of our classifiers even when trained on data devoid of any known resistance-associated signal; as well as a description of the main features (prevalence and correlation to known mutations, genetic barrier and structural analysis) of six potentially resistance associated mutations, newly discovered thanks to our approach. These results and perspectives are discussed in the concluding section.

## 6.2 Materials and methods

### 6.2.1 Data

In this study, we used all the drug resistance mutations that appeared in the Stanford HIV Drug resistance database, both for NRTI (Nucleoside Reverse Transcriptase Inhibitors; [https://hivdb.stanford.edu/dr-summary/comments/NRTI/](https://hivdb.stanford.edu/dr-summary/comments/NRTI/)) and NNRTI (Non Nucleoside RTI; [https://hivdb.stanford.edu/dr-summary/comments/NNRTI/](https://hivdb.stanford.edu/dr-summary/comments/NNRTI/)) as known RAMs. To discover new RAMs, assess their statistical significance and study potential epistatic effects, we used two datasets of HIV-1 RT sequences. A large one (n=55,539 $n=55,539$ $n=55,539$) from the UK HIV Drug Resistance Database ([http://www.hivrdb.org.uk/](http://www.hivrdb.org.uk/)) and a smaller (n=3,990 $n=3,990$ $n=3,990$) one from 10 different western, eastern and central African countries [^10]. In the UK dataset, sequences from RTI-naive individuals formed the majority class with 41,921 sequences (75%). In the African dataset, both classes were more balanced with 2,316 RTI-naive sequences (58%). In the UK dataset, RTI-naive sequences had at least one known RAM in 25% of cases, most likely due to transmissions to naive patients or undisclosed treatment history, against 48% in RTI-experienced sequences, thus making the discrimination between the RTI-experienced and RTI-naive sequences particularly difficult. In the African dataset this distribution was more contrasted, with only 14% of RTI-naive sequences having at least one known RAM, versus 83% of RTI-experienced sequences. The African dataset was also much more genetically diverse with 24 different subtypes and CRFs compared to the 2 subtypes (B and C) that we retained for this study from the UK cohort. The majority of the sequences from the African dataset were samples from Cameroon (27%), Democratic Republic of Congo (17%), Burundi (15%), Burkina Faso (13%) and Togo (11%).

It is important to note that RTI-experienced sequences in both of these datasets can be considered as resistant to treatment. Since the viral load was sufficiently high to allow for sequencing of the virus, we can consider that the ART has failed. However, in some cases this resistance might be caused by non adherence to ART, rather than by the presence of RAMs, therefore adding some noise to the relationship between treatment status and resistance.

In addition to differences in size, balance between RTI-naive and experienced classes, and the genetic difference between the UK and African datasets, there are also significant differences resulting from differing treatment strategies. In the UK and other higher income countries, the treatment is often tailored to the individual with genotype testing, which result in specific treatment as well as thorough follow-ups and high treatment adherence. In the African countries of the dataset that we used, the treatment is ZDV/ d4T (NRTI) + 3TC (NRTI) + NVP/EFV (NNRTI) in most cases [^10], and this treatment is generalized to the affected population, with poorer follow-up and adherence than in the UK. This discrepancy could lead to different mutations arising in both datasets, however since the treatment strategy is a combination of both NRTI and NNRTI drug classes, as in many countries, similar RAMs arise [^10]. Furthermore, there is potentially more uncertainty in the African dataset than in the UK. For example some individuals may have unofficially taken antiretroviral drugs, but still identify themselves as RTI-naive, or report having some form of ART while not having been treated for HIV [^30]. All of this explains the high prevalence of multiple resistance in the African data set: the median number of RAMs in sequences containing at least one RAM is 3 in the African sequences, while it is 1 in UK sequences (Table [6.1](https://thesis.lucblassel.com/HIV-paper.html#tab:tableData)). Thus, we can say that African sequences are highly resistant, with possibly different mutations and epistatic effects, compared to their UK counterparts.

<table><thead><tr><td></td><td></td><td><p>UK</p></td><td></td><td><p>Africa</p></td><td></td></tr></thead><tbody><tr><td colspan="2"><p>size</p></td><td><p>55,539</p></td><td></td><td><p>3,990</p></td><td></td></tr><tr><td><p>RTI naïve</p></td><td><p>with known RAMs</p></td><td><p>11,429</p></td><td><p>(21%)</p></td><td><p>318</p></td><td><p>(8%)</p></td></tr><tr><td></td><td><p>without known RAMs</p></td><td><p>30,492</p></td><td><p>(55%)</p></td><td><p>1,998</p></td><td><p>(50%)</p></td></tr><tr><td><p>RTI experienced</p></td><td><p>with known RAMs</p></td><td><p>6,633</p></td><td><p>(12%)</p></td><td><p>1,388</p></td><td><p>(35%)</p></td></tr><tr><td></td><td><p>without known RAMs</p></td><td><p>6,985</p></td><td><p>(13%)</p></td><td><p>286</p></td><td><p>(7%)</p></td></tr><tr><td colspan="2"><p>sequences with ≥ 2 known RAMs</p></td><td><p>8,034</p></td><td><p>(14%)</p></td><td><p>1,308</p></td><td><p>(33%)</p></td></tr><tr><td colspan="2"><p>max known RAM number</p></td><td><p>13</p></td><td></td><td><p>17</p></td><td></td></tr><tr><td colspan="2"><p>Median known RAM number</p></td><td><p>1</p></td><td></td><td><p>3</p></td><td></td></tr><tr><td colspan="2"><p>number of subtypes / CRFs</p></td><td><p>2</p></td><td></td><td><p>24</p></td><td></td></tr><tr><td><p>subtypes / CRFs</p></td><td><p>A</p></td><td><p>0</p></td><td><p>(0%)</p></td><td><p>472</p></td><td><p>(12%)</p></td></tr><tr><td></td><td><p>B</p></td><td><p>37,806</p></td><td><p>(68%)</p></td><td><p>64</p></td><td><p>(2%)</p></td></tr><tr><td></td><td><p>C</p></td><td><p>17,733</p></td><td><p>(32%)</p></td><td><p>702</p></td><td><p>(18%)</p></td></tr><tr><td></td><td><p>CRF02 AG</p></td><td><p>0</p></td><td><p>(0%)</p></td><td><p>1,477</p></td><td><p>(37%)</p></td></tr></tbody></table>

Table 6.1: **Summary of the UK and Afican datasets.**  
Percentages are computed with regards to the size of the considered dataset (e.g. 21% of the sequences of the UK dataset are RTI-naive and have at least one known RAM). The median number of RAMs was computed only on sequences that had at least one known RAM.

All these differences between the two datasets helped us to assess the generalizability of our method and the robustness of the results. That is to say, if signal extracted from the UK dataset was still relevant on such a different dataset as the African one, we could be fairly reassured in regard to the biological and epidemiological relevance of the observed signal.

Sequences in both African and UK datasets were already aligned. In order to avoid overly gappy regions of our alignment we selected only positions 41 to 235 of RT for our analysis. We used the Sierra web service ([https://hivdb.stanford.edu/page/webservice/](https://hivdb.stanford.edu/page/webservice/)) to get amino acid positions relative to the reference HXB2 HIV genome. This allowed us to determine all the amino acids present at each reference position in both datasets, among which we distinguished the “reference amino acids” for each position, corresponding to the B and C subtype reference sequences obtained from the Los Alamos sequence database ([http://www.hiv.lanl.gov/](http://www.hiv.lanl.gov/)). All the other, non-reference amino acids are named “mutations” in the following, and the set of mutations was explored to reveal new potential RAMs.

To train our supervised classification methods [^5], the sequence data needed to be encoded to numerical vectors. A common and intuitive way to do so is to create a single feature in the dataset for each position of the sequence to encode. Each amino acid is then assigned an integer value, and an amino acid sequence is represented by a succession of integers corresponding to each amino acid. There is, however, one drawback with this method: by assigning an integer value to amino acids, we transform a categorical variable into an ordinal variable. Any ordering of amino acids is hard to justify and might introduce bias. To avoid this, we represented each sequence by a binary vector using one-hot encoding. For each position in the sequence to be encoded, amino acids corresponding to mutations are mapped to a binary vector denoting its presence or absence in the sequence. For example, at site 184, amino acids M, G, I, L, T and V are present in the UK dataset. After encoding we will have 5 binary features corresponding to the M184G, M184I, M184L, M184T and M184V mutations. We did not encode the reference amino acid M, but only the mutated amino acids. With this method each mutation in the dataset (n=1,318 $n=1,318$ $n=1,318$) corresponds to a single feature. Some of these features corresponded to known RAMs (e.g., M184I and M184V) and are named (known) RAM features in the following (n=121 $n=121$ $n=121$). This encoding allows the classifiers to consider specific mutations and potentially link them to resistance.

### 6.2.2 Classifier training

In order to find new potential RAMs, we first followed the conventional multiple testing approach [^10]. We first used Fisher exact tests to identify which of these mutations were significantly associated with anti-retroviral treatment. All the resulting p-values were then corrected for multiple testing using the Bonferroni correction [^33]. Those for which the corrected p-value was ≤0.05 $≤0.05$ $≤ 0.05$ were then considered as significantly associated with treatment and potentially implicated in resistance.

This method was complemented by our parallel, machine learning based approach. In order to extract potential RAMs, we trained several classifiers to discriminate between RTI-experienced and RTI-naive sequences represented by the binary vectors described above. This classification task does not need any phenotypic resistance measure, allowing us to use much larger and more readily available datasets than other machine learning based approaches previously mentioned. Once the classifiers were trained, we extracted the most important representation features, which corresponded to potentially resistance-associated mutations (PRAM in short). To this aim we chose three interpretable supervised learning classification methods so as to be able to extract those features:

1. Multinomial naive Bayes (NB), which estimates conditional probabilities of being in the RTI-experienced class given a set of representation features [^34]; the higher (≈1.0 $≈1.0$ $\approx 1.0$) and the lower (≈0 $≈0$ $\approx0$) conditional probabilities correspond to the most important features.
2. Logistic regression (LR) with L1 regularization (LASSO) [^5] which assigns weights to each of the features, whose sign denotes the importance to one of the 2 classes, and whose absolute value denotes the weight of this importance.
3. Random Forest (RF), which has feature importance measures based on the Gini impurity in the decision trees [^6].

Interpretability was the main driver behind our classification method choice, with the conditional probabilities of NB, the weight or LR and the importance values of RF, we can easily extract which mutations are driving the discrimination of RT sequences. This is why we did not choose to use ANNs which could have led to an increase in accuracy at the cost of interpretability [^3]. Moreover, these three classification methods have the potential to detect epistatic effects. With RF, the discrimination is based on the combination of a few features (i.e. mutations), while with LR the features are weighted positively or negatively, thus making it possible to detect cumulative effects resulting from a large number of mutations, which individually have no discrimination power. Naive Bayes is a very simple approach, generally fairly accurate, and in between the two others in terms of explanatory power [^32].

In order to be able to compare all these approaches in a common framework, we devised a very simple classifier out of the results of the Fisher exact tests. This "Fisher classifier" (FC) predicts a sequence as RTI-experienced if it has at least one of the mutations significantly associated to treatment. In this way, we were able to compute metrics for all classification methods and compare their performance.

It is important to note that in all of these approaches we chose to discriminate RTI-naive from RTI-experienced sequences, regardless of the type of RTI received. One of the reasons is that we did not have detailed enough treatment history for sequences in the UK and African datasets. Moreover, even without segmenting by treatment type, the size of the training set and the power of our classification methods were both high enough to be able to detect all kinds of resistance associated mutations. We shall see (Result section) that we were able to determine the likely treatment involved by further examining the important extracted features and comparing them to known RAMs. Furthermore, since the treatment strategies are so different between the UK and African sequences, training on sequences having received different treatments should increase the robustness of our classifiers and the relevance of the mutations selected as potentially associated to resistance.

To avoid phylogenetic confounding factors (e.g. transmitted mutations within a specific country or region), and avoid finding mutations potentially specific to a given subtype, we split the training and testing sets by HIV-1 M subtype. This resulted in training a set of classifiers on all subtype B sequences of the UK dataset and testing them on subtype C sequences from the UK dataset, training another set of classifiers on the subtype C sequences of the UK dataset and testing on the subtype B sequences from the UK dataset, as well as training a final set of classifiers on the whole UK dataset, but testing it on the smaller African dataset with a completely different phylogenetic makeup and treatment context [^10]. Furthermore, in order to identify novel RAMs and study the behavior of the classifiers, we repeated this training scheme on both datasets, each time removing resistance-associated signal incrementally: first by removing all representation features corresponding to known RAMs from the dataset, and second by removing all sequences that had at least one known RAM. This resulted in each type of classifier being trained and tested 9 times, on radically different sets to ensure the interpretability and robustness of the results (see Table [6.2](https://thesis.lucblassel.com/HIV-paper.html#tab:tableTrainTest)).

<table><thead><tr><td><p>Signal removal level</p></td><td><p>Trained on</p></td><td></td><td></td><td><p>Tested on</p></td><td></td><td></td></tr></thead><tbody><tr><td><p>None</p></td><td><p>UK</p></td><td><p>subtype B</p></td><td><p>(37806)</p></td><td><p>UK</p></td><td><p>subtype C</p></td><td><p>(17733)</p></td></tr><tr><td></td><td><p>UK</p></td><td><p>subtype C</p></td><td><p>(17733)</p></td><td><p>UK</p></td><td><p>subtype B</p></td><td><p>(37806)</p></td></tr><tr><td></td><td><p>UK</p></td><td><p>subtypes B & C</p></td><td><p>(55539)</p></td><td><p>Africa</p></td><td><p>all subtypes</p></td><td><p>(3990)</p></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td><p>Known RAM features removed</p></td><td><p>UK</p></td><td><p>subtype B</p></td><td><p>(37806)</p></td><td><p>UK</p></td><td><p>subtype C</p></td><td><p>(17733)</p></td></tr><tr><td></td><td><p>UK</p></td><td><p>subtype C</p></td><td><p>(17733)</p></td><td><p>UK</p></td><td><p>subtype B</p></td><td><p>(37806)</p></td></tr><tr><td></td><td><p>UK</p></td><td><p>subtypes B & C</p></td><td><p>(55539)</p></td><td><p>Africa</p></td><td><p>all subtypes</p></td><td><p>(3990)</p></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2"><p>Known RAM features sequences with ≥1 known RAM removed</p></td><td><p>UK</p></td><td><p>subtype B</p></td><td><p>(24422)</p></td><td><p>UK</p></td><td><p>subtype C</p></td><td><p>(13055)</p></td></tr><tr><td><p>UK</p></td><td><p>subtype C</p></td><td><p>(13055)</p></td><td><p>UK</p></td><td><p>subtype B</p></td><td><p>(24422)</p></td></tr><tr><td></td><td><p>UK</p></td><td><p>subtypes B & C</p></td><td><p>(37477)</p></td><td><p>Africa</p></td><td><p>all subtypes</p></td><td><p>(2284)</p></td></tr></tbody></table>

Table 6.2: **All training and testing datasets used during this study.**  
The number of sequences in each dataset is shown in parentheses

### 6.2.3 Measuring classifier performance

To compare the performance of our classifiers we used balanced accuracy [^4], which is the average of accuracies (i.e. percentages of well-classified sequences) computed separately on each class of the test set. This score takes into account, and corrects for, the imbalance between RTI-naive and RTI-experienced samples, which would lead to a classifier always predicting a sequence as RTI-naive getting a classical accuracy score of up to 77% (i.e. the frequency of naive sequences in the UK dataset). We also computed the adjusted mutual information (AMI) between predicted and true sequence labels, which is a normalized version of MI allowing comparison of performance on differently sized test sets [^1]. Additionally, mutual information (MI) was used to compute p-values and assess the significance of the classifiers’ predictive power. The probabilistic performance of the classifiers was evaluated using an adapted Brier score [^31] more suited to binary classification, which is the mean squared difference between the actual class (coded by 1 and 0 for the RTI-experienced and RTI-naive samples respectively) and the predicted probability of being RTI-experienced. This approach refines the standard accuracy measure by rewarding methods that well approximate the true status of the sample (eg. predicting a probability of 0.9 while the true status is 1); conversly, binary methods (predicting 0 or 1, but no probabilities) will be penalized if they are often wrong. The Brier approach thus assigns better scores to methods that recognize their ignorance than to methods producing random predictions.

## 6.3 Results

### 6.3.1 Classifier performance & interpretation

As can be seen in Fig [6.1](https://thesis.lucblassel.com/HIV-paper.html#fig:figClassificationPerf) A and [6.1](https://thesis.lucblassel.com/HIV-paper.html#fig:figClassificationPerf) B, when all RAM features and sequences were kept in the training and testing sets, classifiers had good prediction accuracy, with the machine learning classifiers slightly outperforming the “Fisher” classifier. When removing RAM features from the training and testing sets, the classifiers retained a significant prediction accuracy, especially with the African data set and its multiple RAMs that are observed in a large number of sequences (but removed in this experiment). In this configuration the ML classifiers had a similar performance to the “Fisher” classifier, except for the random forest that is slightly less accurate, likely due to overfitting. Also, when removing sequences that had known RAMs, every classifier lost all prediction accuracy, and none could distinguish RTI-naive from RTI-experienced sequences. Regarding the Brier sore, we see the advantage of the machine learning classifiers over the “Fisher” classifier, which is worse than random predictions when known RAMs are removed. The ability of machine learning classifiers to quantify the resistance status should be an asset for many applications.

 $**Classifier Performance on UK and African datasets.**  
**NB**: naive Bayes, **LR**: Logistic Regression with Lasso regularization, **RF**:
Random Forest, **FC**: Fisher Classifier, **RD**: Agnostic random
probabilistic classifier (this classifier predicts, as the probability
of a sample belonging to a class, the frequency of that class in the
training data). **A)** Adjusted mutual information (higher is better)
between ground truth and predictions by classifiers trained on dataset
with all features (blue), without features corresponding to known RAMs
(orange) and without RAM features and without sequences that have at
least 1 known RAM (green). Hatching indicates the training set on which
a classifier was trained and the testing set on which the performance
was measured. The expected value for a null classifier is 0, and 1 for a
perfect classifier and a * denotes that the p-value derived from mutual
information is $\leq 0.05$. For example when trained with all features
all the classifiers have a significative MI. Conversly when removing RAM
features and RAM sequences none of the classifiers have a significative
MI and only LR trained on the entirety of the UK dataset has an AMI
$>10^{-3}$ **B)** Balanced Accuracy score, i.e. average of accuracies
per-class (higher is better) for the same classifiers as in a). The red
line at $y=0.5$ is the expected balanced accuracy for a null classifier
that only predicts the majority class as well as a random uniform (i.e.
50/50) classifier. **C)** Brier score, which is the mean squared
difference between the sample's experience to RTI and the predicted
probability of being RTI experienced (lower is better), for the same
classifiers as in **A)** and **B)**.$

Figure 6.1: **Classifier Performance on UK and African datasets.**  
**NB**: naive Bayes, **LR**: Logistic Regression with Lasso regularization, **RF**: Random Forest, **FC**: Fisher Classifier, **RD**: Agnostic random probabilistic classifier (this classifier predicts, as the probability of a sample belonging to a class, the frequency of that class in the training data). **A)** Adjusted mutual information (higher is better) between ground truth and predictions by classifiers trained on dataset with all features (blue), without features corresponding to known RAMs (orange) and without RAM features and without sequences that have at least 1 known RAM (green). Hatching indicates the training set on which a classifier was trained and the testing set on which the performance was measured. The expected value for a null classifier is 0, and 1 for a perfect classifier and a \* denotes that the p-value derived from mutual information is ≤0.05 $≤0.05$. For example when trained with all features all the classifiers have a significative MI. Conversly when removing RAM features and RAM sequences none of the classifiers have a significative MI and only LR trained on the entirety of the UK dataset has an AMI \>10−3 $>10−3$ **B)** Balanced Accuracy score, i.e. average of accuracies per-class (higher is better) for the same classifiers as in a). The red line at y=0.5 $y=0.5$ is the expected balanced accuracy for a null classifier that only predicts the majority class as well as a random uniform (i.e. 50/50) classifier. **C)** Brier score, which is the mean squared difference between the sample’s experience to RTI and the predicted probability of being RTI experienced (lower is better), for the same classifiers as in **A)** and **B)**.

The fact that classifiers retained prediction accuracy after removing known RAM corresponding features suggests that there was some residual, unknown resistance-associated signal in the data. The fact that this same power was non-existent when removing the known RAM-containing sequences from the training and testing sets, indicates that this residual signal was contained in these already mutated sequences. This suggests that the mutations that are found in the RAM removed experiment (see list below) are most likely accessory mutations that accompany known RAMs. This also suggests that all primary DRMs (i.e., that directly confer antiretroviral resistance) have been identified, which is reassuring from a public health perspective.

The performance discrepancy between the UK and African test sets can be explained by several factors. Firstly, African sequences that have known RAMs are more likely to have multiple RAMs, and thus more (known and unknown) resistance-associated features than their UK counterparts (c.f. Table [6.1](https://thesis.lucblassel.com/HIV-paper.html#tab:tableData)). This means that resistant African sequences are easier to detect even when removing known RAMs. Secondly, RTI-naive sequences in the UK test sets are more likely to have known RAMs than their African counterparts (c.f. Table [6.1](https://thesis.lucblassel.com/HIV-paper.html#tab:tableData)) and therefore more companion mutations. This means that the RTI-naive sequences in the UK test set are more likely to be misclassified as RTI-experienced than in the African test set.

### 6.3.2 Additional classification results

The fact that, when looking at classifiers trained without known RAMs, “Fisher” classifiers perform as well as the machine learning ones, leads us to believe that there is little interaction between mutations that would explain resistance better than taking each mutation separately. It is therefore likely that the kind of epistatic phenomena we were looking for, combining several mutations that do not induce any resistance when taken separately, do not come into play here. We are in a classical scheme where primary DRMs confer resistance and associated mutations reinforce the strength of the resistance and/or compensate for the fitness cost induced by primary DRMs.

It is important to remember that in the previous section we were trying (as usual, e.g. see [^10]) to find novel mutations associated with resistance by discriminating RTI-naive from RTI-experienced sequences, both with the statistical tests and the classifiers. However, this is intrinsically biased and noisy. Indeed, a RTI-naive sequence is not necessarily susceptible to RTIs as a resistant strain could have been transmitted to the individual. Conversely, an RTI-experienced sequence may not be resistant to treatment, due to poor ART adherence for example. We must therefore keep in mind that the noisy nature of the relationship between resistance and treatment status is partly responsible for the lower performance of classifiers trained on the UK sequences with reduced signal.

Moreover, as all the additional resistance signal we detected is associated to the sequences having at least one known RAM (see above), we performed another analysis trying to discriminate between the sequences having at least one known RAM and those having none. The goal was to check that the mutations we discovered by discriminating RTI-experienced from RTI-naive samples, are truly accessory and compensatory mutations. As can be seen in Fig [6.2](https://thesis.lucblassel.com/HIV-paper.html#fig:figMultiTasks) A and [6.2](https://thesis.lucblassel.com/HIV-paper.html#fig:figMultiTasks) B, the classifiers trained to discriminate sequences that have at least one known RAM from those that have none, on datasets from which all features corresponding to known RAMs were removed, perform much better than classifiers trained to discriminate RTI-experienced from RTI-naive sequences. This increase in performance is especially visible for classifiers tested on UK sequences (more difficult to classify than the African ones, see above), with an AMI often almost one order of magnitude higher for the known-RAM presence/absence classification task. This further reinforces our belief that all there is a fairly strong residual resistance-signal in sequences that contain known RAMs, due to new accessory and compensatory mutations identified by our classifiers and Fisher tests. As a side note, Logistic regression (LR) consistently outperforms other classifiers, a tendency already observed in Fig [6.1](https://thesis.lucblassel.com/HIV-paper.html#fig:figClassificationPerf).

![**Discrimination between sequences having at least one RAM, and those
having none on sequences with training features corresponding to known
RAMs removed.**  
**NB**: naive Bayes, **LR**: Logistic Regression with
Lasso regularization, **RF**: Random Forest, **FC**: Fisher Classifier.
**A)** Adjusted mutual information (higher is better) for classifiers
trained without features corresponding to known RAMs. The classifiers
are either trained to discriminate RTI-naive from RTI-experienced
sequences (blue), or sequences with at least one known RAM from
sequences that have none (orange). Hatching and braced annotations
indicate the training and testing sets resulting in a given performance
measure. **B)** Balanced accuracy, i.e. average of accuracies per-class
for the same classifiers as in **A)** (higher is better). The red line
at $y=0.5$ is the expected value for a classifier only predicting the
majority class as well as a random uniform (50/50)
classifier.](https://thesis.lucblassel.com/_main_files/figure-html/figMultiTasks-1.png)

Figure 6.2: **Discrimination between sequences having at least one RAM, and those having none on sequences with training features corresponding to known RAMs removed.**  
**NB**: naive Bayes, **LR**: Logistic Regression with Lasso regularization, **RF**: Random Forest, **FC**: Fisher Classifier. **A)** Adjusted mutual information (higher is better) for classifiers trained without features corresponding to known RAMs. The classifiers are either trained to discriminate RTI-naive from RTI-experienced sequences (blue), or sequences with at least one known RAM from sequences that have none (orange). Hatching and braced annotations indicate the training and testing sets resulting in a given performance measure. **B)** Balanced accuracy, i.e. average of accuracies per-class for the same classifiers as in **A)** (higher is better). The red line at y=0.5 $y=0.5$ $y=0.5$ is the expected value for a classifier only predicting the majority class as well as a random uniform (50/50) classifier.

### 6.3.3 Identifying new mutations from classifiers

We assessed the importance of each mutation in the learned internal model of all the classifiers, in the setting where all known RAMs have been removed from the training dataset. For the Fisher classifier, we used one minus the p-value of the exact Fisher test as the importance value, therefore the more significantly associated mutations have the higher importance value and were ranked first. For a given classification task, we ranked each mutation according to the appropriate importance value for each classifier (see above), trained on the B or C subtypes, with the highest importance value having a rank of 0. We then computed the average rank for each mutation and each classification task (RTI-naive/RTI-experienced and RAM present/RAM absent). This gave us, for each classification task, a ranking of mutations potentially associated with resistance that took into account the importance given to this new mutation by each classifier trained on this task. Mutations that were in the 10 most important mutations for both of the classification tasks were considered of interest. Based on these criteria we selected the following potentially resistance-associated mutations (w.r.t. the HXB2 reference genome): L228R, L228H, E203K, D218E, I135L and H208Y. These mutations are referred to as “new mutations” in the rest of this study.

To check the epistatic nature of these selected mutations we computed the relative risk RR(new,X) $RR(new,X)$ $RR(new, X)$ between a new mutation and a binary character X $X$ $X$. RR(new,X) $RR(new,X)$ $RR(new,X)$ was computed from the contingency table between new $new$ $new$ and X $X$ $X$ as follows:

| name | X present | X absent |
| --- | --- | --- |
| new present | A | B |
| new absent | C | D |

RR(new,X)=AA+C÷BB+D 
$$
RR(new,X)=AA+C÷BB+D
$$
 
$$
RR(new,X) = \frac{A}{A+C} \div \frac{B}{B+D}
$$

The RR gives us a measure for how over-represented each of our new mutations is in sequences that have the X $X$ $X$ character compared to those that don’t.

To get a general idea of this over-representation, for each new mutation we computed RR(new,treatment) $RR(new,treatment)$ $RR(new, treatment)$ comparing the prevalence of the new mutation in RTI-experienced and RTI-naive sequences. We also computed RR(new,withRAM) $RR(new,withRAM)$ $RR(new, with RAM)$ comparing the prevalence the new mutation in sequences having at least one known RAM and sequences that have none. Both of these RRs are shown in Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations) for each new mutation.

We then computed RR(new,RAM) $RR(new,RAM)$ $RR(new, RAM)$ for each known RAM present in more than 0.1% of UK sequences and the new mutations. In Fig [6.3](https://thesis.lucblassel.com/HIV-paper.html#fig:figUkRatios) we see the RRs for which the lower bound of the 95% confidence interval, computed on 1000 bootstrap samples from the UK dataset, was greater than 4.

### 6.3.4 Detailed analysis of potentially resistance-associated mutations

As can be seen in Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations), all of these new mutations except for I135L, are highly over-represented in RTI-experienced sequences and sequences that already have known RAMs, with lower bounds on the 95% RR CI always greater than 5, and often exceeding 10. When looking at the RRs computed for individual RAMs on the UK dataset (Fig [6.3](https://thesis.lucblassel.com/HIV-paper.html#fig:figUkRatios)), this impression is confirmed with very high over-representation of these new mutations potentially associated with resistance in sequences that have a given known RAM, with 95% RR lower CI bounds sometimes greater than 80 (H208Y/L210W and D218E/D67N), and most of the time greater than 10. with the noticeable exception of I135L where only 2 known RAMs give RRs with lower CI bounds greater than 4. The RRs computed on the African dataset ([C.1](https://thesis.lucblassel.com/HIV-appendix.html#fig:s1)) tell a similar story albeit with smaller RR values due to a smaller number of occurrences of both new mutations and known RAMs.

<table><thead><tr><td rowspan="2"><p>mutation</p></td><td colspan="2"><p>codon distance</p></td><td rowspan="2"><p>B62</p></td><td colspan="3"><p>UK</p></td><td rowspan="2"><p>p‑value</p></td></tr><tr><td><p>min</p></td><td><p>avg</p></td><td><p>count</p></td><td><p>RR(new,treatment)</p></td><td><p>RR(new,any RAM)</p></td></tr></thead><tbody><tr><td><p>L228R</p></td><td><p>1</p></td><td><p>1.16</p></td><td><p>-2</p></td><td><p>227 (0.4%)</p></td><td><p>18.1 [12.9;27.3]</p></td><td><p>115.7 [55.1;507.3]</p></td><td><p>2.0e‑30</p></td></tr><tr><td><p>E203K</p></td><td><p>1</p></td><td><p>1.31</p></td><td><p>1</p></td><td><p>256 (0.5%)</p></td><td><p>11.0 [8.2;15.1]</p></td><td><p>20.1 [13.7;32.1]</p></td><td><p>6.4e‑14</p></td></tr><tr><td><p>D218E</p></td><td><p>1</p></td><td><p>1</p></td><td><p>2</p></td><td><p>168 (0.3%)</p></td><td><p>13.1 [9.0;19.6]</p></td><td><p>27.0 [16.3;57.0]</p></td><td><p>2.0e‑09</p></td></tr><tr><td><p>L228H</p></td><td><p>1</p></td><td><p>1.12</p></td><td><p>-3</p></td><td><p>287 (0.5%)</p></td><td><p>6.4 [5.1;8.4]</p></td><td><p>9.2 [6.9;12.6]</p></td><td><p>2.7e‑15</p></td></tr><tr><td><p>I135L</p></td><td><p>1</p></td><td><p>1.16</p></td><td><p>2</p></td><td><p>540 (1.0%)</p></td><td><p>1.8 [1.5;2.1]</p></td><td><p>2.4 [2.0;2.8]</p></td><td><p>2.6e‑07</p></td></tr><tr><td><p>H208Y</p></td><td><p>1</p></td><td><p>1.10</p></td><td><p>2</p></td><td><p>205 (0.4%)</p></td><td><p>8.8 [6.5;12.5]</p></td><td><p>14.9 [9.9;23.6]</p></td><td><p>7.3e‑05</p></td></tr><tr><td><p>RAMs</p></td><td><p>1</p></td><td><p>1.35</p></td><td><p>0</p></td><td><p>58 (0.1%)</p></td><td><p>8.3</p></td><td><p>26.4</p></td><td><p>3.1e-2</p></td></tr><tr><td></td><td><p>[1;2]</p></td><td><p>[1;2.44]</p></td><td><p>[-2;3]</p></td><td><p>[2;1842]</p></td><td><p>[0.6;∞]</p></td><td><p>[1.4;∞]</p></td><td><p>[2.3e-58;1]</p></td></tr></tbody></table>

Table 6.3: **Analysis of new potential RAMs.**  
**Codon distance:** For each new mutation we computed the minimum number of nucleotide mutations to go from the wild amino acid codons to those of the mutated amino acid, as well as the average codon distance between both amino acids, weighted by the prevalence of each wild and mutated codon at the given position in the UK dataset. **B62:** BLOSUM62 similarity values (e.g. D218E = 2, reflecting that E and D are both negatively charged and highly similar). **Count:** We looked at the number of occurrences of each new potential RAM in the UK dataset and the corresponding prevalence in parentheses. **Relative risks:** We computed RR(new,treatment) $RR(new,treatment)$ $RR(new, treatment)$ (e.g. L228R is 18.1 times more prevalent in RTI-experienced sequences compared to RTI-naive sequences in the UK dataset). We also computed RR(new,any RAM) $RR(new,any RAM)$ $RR(new, any~RAM)$ (e.g. L228R is 115.7 times more prevalent in sequences that have at least one known RAM than in sequences that have none in the UK dataset). The 95% confidence intervals shown under each RR were computed with 1000 bootstrap samples of size n=55,000 $n=55,000$ $n=55,000$ drawn with replacement from the whole UK dataset. **p-values:** Fisher exact tests were done on the African dataset (to avoid confounding effects due to phylogenetic correlation) to see if each of these new mutations were more prevalent in RTI-experienced sequences. The same metrics were computed for all known RAMs, the median values are shown in the last two lines of this table, as well as the 5 <sup>th</sup> and 95 <sup>th</sup> percentiles which are shown underneath. RR(RAM,any RAM) $RR(RAM,any RAM)$ $RR(RAM,any~RAM)$ values were computed for any RAM except itself to avoid always having infinite ratios.

![**Relative risk of the new mutations with regards to known RAMs on the
UK dataset.**  
(i.e. the prevalence of the new mutation in sequences with
a given known RAM divided by the prevalence of the new mutation in
sequences without this RAM). RRs were only computed for mutations (new
and RAMs) that appeared in at least 0.1% (=55) sequences. 95% confidence
intervals, represented by vertical bars, were computed with 1000
bootstrap samples of UK sequences. Only RRs with a lower CI boundary
greater than 4 are shown. The shape and color of the point represents
the type of RAM as defined by Stanford's HIVDB. Blue circle: NRTI,
orange square: NNRTI, green diamond: Other. RR values are shown from
left to right, by order of decreasing values on the lower bound of the
95% CI.](https://thesis.lucblassel.com/_main_files/figure-html/figUkRatios-1.png)

Figure 6.3: **Relative risk of the new mutations with regards to known RAMs on the UK dataset.**  
(i.e. the prevalence of the new mutation in sequences with a given known RAM divided by the prevalence of the new mutation in sequences without this RAM). RRs were only computed for mutations (new and RAMs) that appeared in at least 0.1% (=55) sequences. 95% confidence intervals, represented by vertical bars, were computed with 1000 bootstrap samples of UK sequences. Only RRs with a lower CI boundary greater than 4 are shown. The shape and color of the point represents the type of RAM as defined by Stanford’s HIVDB. Blue circle: NRTI, orange square: NNRTI, green diamond: Other. RR values are shown from left to right, by order of decreasing values on the lower bound of the 95% CI.

The genetic barrier to resistance for each of these new mutations is quite low, with a minimum of 1 base change for each of them (Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations) ). We also computed the average codon distance (i.e. number of different bases), weighted by the prevalence of wild and mutated codons at the given positions in the UK (Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations) ) and Africa (Table [C.5](https://thesis.lucblassel.com/HIV-appendix.html#S1-Table)) datasets, and in each case the average codon distance was always close to 1. In other words, at the amino acid level these mutations are expected to be relatively frequent. However, their frequencies are much higher in treated/with-RAM sequences than in naive/without-RAM ones (Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations) ). Moreover, if we look at the BLOSUM62 scores (Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations) ), some of these mutations induce some substantial changes in physicochemical properties, most notably at site 228, which reinforces again the likelihood that these mutations are associated with resistance. These metrics were also computed for all known RAMs (Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations) ). For all these metrics, and the 6 new potential RAMs, values are contained between the 5 <sup>th</sup> and 95 <sup>th</sup> percentiles computed on known RAMs, except for the BLOSUM score of L228H that corresponds to a drastic physicochemical change.  
To gain more insight on these new mutations we also observed their spatial location on the 3-D HIV-1 RT structure using PyMol [^37]. HIV-1 RT is a heterodimer with two subunits translated from the same sequence with different lengths and 3-D structures. The smaller p51 subunit (440 AAs) has a mainly structural role, while the larger p66 (560 AAs) subunit has the active site at positions 110, 185 and 186. The p66 subunit also has a regulatory pocket behind the active site: the non-nucleoside inhibitor binding pocket (NNIBP) formed of several sites of the p66 subunit as well as site 138 of the p51 subunit. Nucleoside RT Inhibitors (NRTI) are nucleotide analogs and bind in the active site, blocking reverse transcription. Non-Nucleoside RT Inhibitors (NNRTI) bind in the NNIBP, changing the protein conformation and blocking reverse transcription. More details on the structure and function of HIV-1 RT can be found in [^7]. A general view of where the new mutations are situated with regards to the other important sites of HIV-1 RT is shown in Fig [6.4](https://thesis.lucblassel.com/HIV-paper.html#fig:figStructure), and is detailed below.

![**Structure of HIV-1 RT with highlighted important sites.**  
The p66 subunit is colored dark gray and the p51 subunit white. The active site
is highlighted in blue, and the NNIBP is highlighted in yellow. The
sites of new mutations are colored in
red.](https://thesis.lucblassel.com/_main_files/figure-html/figStructure-1.png)

Figure 6.4: **Structure of HIV-1 RT with highlighted important sites.**  
The p66 subunit is colored dark gray and the p51 subunit white. The active site is highlighted in blue, and the NNIBP is highlighted in yellow. The sites of new mutations are colored in red.

#### 6.3.4.1 L228R / L228H

L228R is the most important of these new mutations according to the feature importance ranking done above. This is reflected in the very high over-representation in RTI-experienced sequences and sequences with known RAMs shown in Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations). When looking at the detailed RRs shown in Fig [6.3](https://thesis.lucblassel.com/HIV-paper.html#fig:figUkRatios), we observe that L228R presents high RR values with mainly NRTI RAMs, but also with NNRTI RAMs such as Y181C and L100I, and this is even more so h for RRs computed on the African dataset ([C.1](https://thesis.lucblassel.com/HIV-appendix.html#fig:s1)). L228H is very similar in all regards to L228R, however its highest RRs are exclusively with NRTI RAMs.

Site 228 of the p66 subunit is located very close to the active site of RT, where NRTIs operate (Figs [6.4](https://thesis.lucblassel.com/HIV-paper.html#fig:figStructure) and [C.3](https://thesis.lucblassel.com/HIV-appendix.html#fig:s3)) which could explain the role that L228R and L228H seem to have in NRTI resistance. However, site 228 of the p66 subunit is also between sites 227 and 229 which are both part of the NNIBP. Furthermore, both L228H and L228R have very low BLOSUM62 score, of -3 and -2 respectively (Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations) ). Arginine (R) and Histidine (H) are both less hydrophobic that Leucine (L), and have positively charged side-chains. This important change in physicochemical properties could explain the role they both seem to have in NRTI resistance. However, while both Arginine and Histidine are larger than Leucine, Arginine is also fairly larger than Histidine, which is aromatic. This difference between both residues might explain the association L228R seems to have with NNRTI resistance that L228H does not have.

#### 6.3.4.2 E203K / H208Y

Both E203K and H208Y are highly over-represented in RTI-experienced sequences and sequences with known RAMs. They both have high RR values for NRTI RAMs. Furthermore the most highly valued RAM RRs in Fig [6.3](https://thesis.lucblassel.com/HIV-paper.html#fig:figUkRatios), are very similar for E203K and H208Y. Structurally they are close to each other on an alpha helix which is close to the active site.

Both E203K and H208Y have positive, albeit not maximal, BLOSUM62 scores, meaning they are fairly common substitutions. However, these mutations induce some change in physicochemical properties with Tyrosine (Y) being less polar than Histidine (H), and the change from Glutamic Acid (E) to Lysine (K) corresponding to a change from a negatively charged side chain to a positively charged one.

All this, combined with their structural proximity and the shared high RR values for single RAMs, suggests a similar role in NRTI resistance.

#### 6.3.4.3 I135L

In Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations) and Fig [6.3](https://thesis.lucblassel.com/HIV-paper.html#fig:figUkRatios), we observe that I135L has the lowest RR values of all the new mutations, with CI bounds lower than 2 in Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations) ’s general RRs. However, it is the most prevalent of the new mutations. If we look at the detailed RRs of Fig [6.3](https://thesis.lucblassel.com/HIV-paper.html#fig:figUkRatios), we see that I135L is significantly over-represented in sequences with NNRTI RAMs, specifically A98G and P225H. Structurally this makes sense: On the p66 subunit, site 135 is on the outside, far from both the active site and the NNIBP. However, site 135 on the p51 subunit is located very close to the NNIBP (Figs [6.3](https://thesis.lucblassel.com/HIV-paper.html#fig:figUkRatios) and [C.2](https://thesis.lucblassel.com/HIV-appendix.html#fig:s2)).

The BLOSUM62 score for this substitution is quite high (Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations)), which is expected since both residues are very similar to one another, differing only by the positioning of one methyl group. However, Leucine (L) is less hydrophobic than Isoleucine (I), despite they are still both classified as hydrophobic residues (Table [C.5](https://thesis.lucblassel.com/HIV-appendix.html#S1-Table)).

The proximity between site 135 and the pocket in which NNRTI RAMs bind, as well as the high RR values for these NNRTI RAMs leads us to believe that I135L could play a subtle accessory role in NNRTI resistance, either by enhancing the effect of some NNRTI RAMs (typically, A98G and P225H), or by compensating for loss of fitness.

#### 6.3.4.4 D218E

D218E is also highly over-represented in both RTI-experienced sequences and sequences with known RAMs. It has infinite RR values in the African dataset (Table [6.3](https://thesis.lucblassel.com/HIV-paper.html#tab:tabMutations)), because it is quite rare in this dataset, and all of its 25 occurrences are in sequences that have at least one known RAM and are RTI-experienced. In fact, from the UK dataset we can see that D218E has some of the highest RR values for individual RAMs (along with H208Y). The majority of these very high RR values occur for NRTI RAMs. Site 218 on the p66 subunit is quite close to the RT active site, which could explain the role D218E seems to have in NRTI resistance. Aspartic acid (D) and Glutamic acid (E) are very similar amino acids, both acidic with negatively charged side-chains, as reflected in their fairly high BLOSUM62 score, the main difference between both being molecular weight, with E being slightly larger than D.

## Acknowledgments

We thank Anna Zhukova, Frédéric Lemoine and Marie Morel for their help and suggestions.

We also thank the UK HIV Drug Resistance Database and the UK Collaborative HIV Cohort:

**Steering committee:** David Asboe, Anton Pozniak (Chelsea & Westminster Hospital, London); Patricia Cane (Public Health England, Porton Down); David Chadwick (South Tees Hospitals NHS Trust, Middlesbrough); Duncan Churchill (Brighton and Sussex University Hospitals NHS Trust); Simon Collins (HIV i-Base, London); Valerie Delpech (National Infection Service, Public Health England); Samuel Douthwaite (Guy’s and St. Thomas’ NHS Foundation Trust, London); David Dunn, Kholoud Porter, Anna Tostevin, Oliver Stirrup (Institute for Global Health, UCL); Christophe Fraser (University of Oxford); Anna Maria Geretti (Institute of Infection and Global Health, University of Liverpool); Rory Gunson (Gartnavel General Hospital, Glasgow); Antony Hale (Leeds Teaching Hospitals NHS Trust); Stéphane Hué (London School of Hygiene and Tropical Medicine); Michael Kidd (Public Health England, Birmingham Heartlands Hospital); Linda Lazarus (Expert Advisory Group on AIDS Secretariat, Public Health England); Andrew Leigh-Brown (University of Edinburgh); Tamyo Mbisa (National Infection Service, Public Health England); Nicola Mackie (Imperial NHS Trust, London); Chloe Orkin (Barts Health NHS Trust, London); Eleni Nastouli, Deenan Pillay, Andrew Phillips, Caroline Sabin (University College London, London); Kate Templeton (Royal Infirmary of Edinburgh); Peter Tilston (Manchester Royal Infirmary); Erik Volz (Imperial College London, London); Ian Williams (Mortimer Market Centre, London); Hongyi Zhang (Addenbrooke’s Hospital, Cambridge).

**Coordinating Center:** Institute for Global Health, UCL (David Dunn, Keith Fairbrother, Anna Tostevin, Oliver Stirrup)

**Centers contributing data:** Clinical Microbiology and Public Health Laboratory, Addenbrooke’s Hospital, Cambridge (Justine Dawkins); Guy’s and St Thomas’ NHS Foundation Trust, London (Emma Cunningham, Jane Mullen); PHE – Public Health Laboratory, Birmingham Heartlands Hospital, Birmingham (Michael Kidd); Antiviral Unit, National Infection Service, Public Health England, London (Tamyo Mbisa); Imperial College Health NHS Trust, London (Alison Cox); King’s College Hospital, London (Richard Tandy); Medical Microbiology Laboratory, Leeds Teaching Hospitals NHS Trust (Tracy Fawcett); Specialist Virology Centre, Liverpool (Elaine O’Toole); Department of Clinical Virology, Manchester Royal Infirmary, Manchester (Peter Tilston); Department of Virology, Royal Free Hospital, London (Clare Booth, Ana Garcia-Diaz); Edinburgh Specialist Virology Centre, Royal Infirmary of Edinburgh (Lynne Renwick); Department of Infection & Tropical Medicine, Royal Victoria Infirmary, Newcastle (Matthias L Schmid, Brendan Payne); South Tees Hospitals NHS Trust, Middlesbrough (David Chadwick); Department of Virology, Barts Health NHS Trust, London (Mark Hopkins); Molecular Diagnostic Unit, Imperial College, London (Simon Dustan); University College London Hospitals (Stuart Kirk); West of Scotland Specialist Virology Laboratory, Gartnavel, Glasgow (Rory Gunson, Amanda Bradley-Stewart).

## Supporting information

Supporting Information can be found in the appendix [C](https://thesis.lucblassel.com/HIV-appendix.html#HIV-appendix)

### References

[^1]: 150.

Vinh, N. X., Epps, J. & Bailey, J. [Information Theoretic Measures for Clusterings Comparison: Variants, Properties, Normalization and Correction for Chance](https://jmlr.org/papers/volume11/vinh10a/vinh10a.pdf). *Journal of Machine Learning Research* **11**, 18 (2010).

[^2]: 331.

Steiner, M. C., Gibson, K. M. & Crandall, K. A. [Drug Resistance Prediction Using Deep Learning Techniques on HIV-1 Sequence Data](https://doi.org/10.3390/v12050560). *Viruses* **12**, 560 (2020).

[^3]: 355.

Hastie, T., Tibshirani, R. & Friedman, J. *[The Elements of Statistical Learning: Data Mining, Inference, and Prediction, Second Edition](https://books.google.com/?id=tVIjmNS3Ob8C)*. (Springer Science & Business Media, 2009).

[^4]: 380.

Brodersen, K. H., Ong, C. S., Stephan, K. E. & Buhmann, J. M. The Balanced Accuracy and Its Posterior Distribution. in *2010 20th International Conference on Pattern Recognition* 3121–3124 (2010). doi:[10.1109/icpr.2010.764](https://doi.org/10.1109/icpr.2010.764).

[^5]: 386.

Tibshirani, R. [Regression Shrinkage and Selection Via the Lasso](https://doi.org/10.1111/j.2517-6161.1996.tb02080.x). *Journal of the Royal Statistical Society: Series B (Methodological)* **58**, 267–288 (1996).

[^6]: 393.

Breiman, L. [Random Forests](https://doi.org/10.1023/a:1010933404324). *Machine Learning* **45**, 5–32 (2001).

[^7]: 564.

Sarafianos, S. G. *et al.* [Structure and function of HIV-1 reverse transcriptase: Molecular mechanisms of polymerization and inhibition](https://doi.org/10.1016/j.jmb.2008.10.071). *J Mol Biol* **385**, 693–713 (2009).

[^8]: 598.

Mourad, R. *et al.* [A phylotype-based analysis highlights the role of drug-naive HIV-positive individuals in the transmission of antiretroviral resistance in the UK](https://doi.org/10.1097/qad.0000000000000768). *Aids* **29**, 1917–1925 (2015).

[^9]: 599.

Hué, S. *et al.* [Demonstration of Sustained Drug-Resistant Human Immunodeficiency Virus Type 1 Lineages Circulating among Treatment-Naïve Individuals](https://doi.org/10.1128/jvi.01556-08). *Journal of Virology* **83**, 2645–2654 (2009).

[^10]: 615.

Villabona-Arenas, C. J. *et al.* [In-depth analysis of HIV-1 drug resistance mutations in HIV-infected individuals failing first-line regimens in West and Central Africa](https://doi.org/10.1097/qad.0000000000001233). *Aids* **30**, 2577 (2016).

[^11]: 624.

Sham, P. C. & Purcell, S. M. [Statistical power and significance testing in large-scale genetic studies](https://doi.org/10.1038/nrg3706). *Nature Reviews Genetics* **15**, 335–346 (2014).

[^12]: 638.

Sheik Amamuddy, O., Bishop, N. T. & Tastan Bishop, Ö. [Improving fold resistance prediction of HIV-1 against protease and reverse transcriptase inhibitors using artificial neural networks](https://doi.org/10.1186/s12859-017-1782-x). *BMC Bioinformatics* **18**, 369 (2017).

[^13]: 639.

Beerenwinkel, N. *et al.* [Geno2pheno: Interpreting genotypic HIV drug resistance tests](https://doi.org/10.1109/5254.972080). *IEEE Intelligent Systems* **16**, 35–41 (2001).

[^14]: 642.

Heider, D., Senge, R., Cheng, W. & Hüllermeier, E. [Multilabel classification for exploiting cross-resistance information in HIV-1 drug resistance prediction](https://doi.org/10.1093/bioinformatics/btt331). *Bioinformatics* **29**, 1946–1952 (2013).

[^15]: 

[^16]: 644.

Verhofstede, C. *et al.* [Detection of drug resistance mutations as a predictor of subsequent virological failure in patients with HIV-1 viral rebounds of less than 1,000 RNA copies/ml](https://doi.org/10.1002/jmv.20950). *Journal of Medical Virology* **79**, 1254–1260 (2007).

[^17]: 645.

Zhukova, A., Cutino-Moguel, T., Gascuel, O. & Pillay, D. [The Role of Phylogenetics as a Tool to Predict the Spread of Resistance](https://doi.org/10.1093/infdis/jix411). *J Infect Dis* **216**, S820–s823 (2017).

[^18]: 646.

Bennett, D. E. *et al.* [Drug Resistance Mutations for Surveillance of Transmitted HIV-1 Drug-Resistance: 2009 Update](https://doi.org/10.1371/journal.pone.0004724). *Plos One* **4**, e4724 (2009).

[^19]: 648.

Wensing, A. M. *et al.* [2017 Update of the Drug Resistance Mutations in HIV-1., 2017 Update of the Drug Resistance Mutations in HIV-1](https://www.ncbi.nlm.nih.gov/pubmed/28208121). *Top Antivir Med* **24, 24**, 132, 132–133 (2016).

[^20]: 649.

Dudoit, S. & Laan, M. J. van der. *Multiple Testing Procedures with Applications to Genomics*. (Springer Science & Business Media, 2007). doi:[10.1007/978-0-387-49317-6](https://doi.org/10.1007/978-0-387-49317-6).

[^21]: 650.

Maddison, W. P. & FitzJohn, R. G. [The Unsolved Challenge to Phylogenetic Correlation Tests for Categorical Characters](https://doi.org/10.1093/sysbio/syu070). *Syst Biol* **64**, 127–136 (2015).

[^22]: 651.

Lengauer, T. & Sing, T. [Bioinformatics-assisted anti-HIV therapy](https://doi.org/10.1038/nrmicro1477). *Nat Rev Microbiol* **4**, 790–797 (2006).

[^23]: 652.

Zhang, J., Rhee, S.-Y., Taylor, J. & Shafer, R. W. [Comparison of the Precision and Sensitivity of the Antivirogram and PhenoSense HIV Drug Susceptibility Assays](https://doi.org/10.1097/01.qai.0000147526.64863.53). *JAIDS Journal of Acquired Immune Deficiency Syndromes* **38**, 439–444 (2005).

[^24]: 653.

Beerenwinkel, N. *et al.* [Geno2pheno: Estimating phenotypic drug resistance from HIV-1 genotypes](https://doi.org/10.1093/nar/gkg575). *Nucleic Acids Research* **31**, 3850–3855 (2003).

[^25]: 654.

Shen, C., Yu, X., Harrison, R. W. & Weber, I. T. [Automated prediction of HIV drug resistance from genotype data](https://doi.org/10.1186/s12859-016-1114-6). *BMC Bioinformatics* **17**, 278 (2016).

[^26]: 655.

Yu, X., Weber, I. T. & Harrison, R. W. [Prediction of HIV drug resistance from genotype with encoded three-dimensional protein structure](https://doi.org/10.1186/1471-2164-15-s5-s1). *BMC Genomics* **15**, S1 (2014).

[^27]: 656.

Araya, S. T. & Hazelhurst, S. [Support vector machine prediction of HIV-1 drug resistance using the viral nucleotide patterns](https://doi.org/10.1080/00359190909519238). *Transactions of the Royal Society of South Africa* **64**, 62–72 (2009).

[^28]: 657.

Riemenschneider, M., Senge, R., Neumann, U., Hüllermeier, E. & Heider, D. [Exploiting HIV-1 protease and reverse transcriptase cross-resistance information for improved drug resistance prediction by means of multi-label classification](https://doi.org/10.1186/s13040-016-0089-1). *BioData Min* **9**, 10 (2016).

[^29]: 658.

Dr̆aghici, S. & Potter, R. B. [Predicting HIV drug resistance with neural networks](https://doi.org/10.1093/bioinformatics/19.1.98). *Bioinformatics* **19**, 98–107 (2003).

[^30]: 659.

Mooney, A. C. *et al.* [Beyond Social Desirability Bias: Investigating Inconsistencies in Self-Reported HIV Testing and Treatment Behaviors Among HIV-Positive Adults in North West Province, South Africa](https://doi.org/10.1007/s10461-018-2155-9). *AIDS Behav* **22**, 2368–2379 (2018).

[^31]: 660.

Brier, G. W. [Verification of Forecasts Expressed in Terms of Probability](https://doi.org/10.1175/1520-0493\(1950\)078%3C0001:vofeit%3E2.0.co;2). *Mon. Wea. Rev.* **78**, 1–3 (1950).

[^32]: 661.

Gascuel, O. *et al.* [Twelve Numerical, Symbolic and Hybrid Supervised Classification Methods](https://doi.org/10.1142/s0218001498000336). *Int. J. Patt. Recogn. Artif. Intell.* **12**, 517–571 (1998).

[^33]: 662.

Goeman, J. J. & Solari, A. [Multiple hypothesis testing in genomics](https://doi.org/10.1002/sim.6082). *Statistics in Medicine* **33**, 1946–1978 (2014).

[^34]: 663.

Rennie, J. D., Shih, L., Teevan, J. & Karger, D. R. [Tackling the Poor Assumptions of Naive Bayes Text Classifiers](https://www.aaai.org/Papers/ICML/2003/ICML03-081.pdf). in *Proceedings of the 20th international conference on machine learning (ICML-03)* 616–623 (2003).

[^35]: 664.

Alvarez Melis, D. & Jaakkola, T. [Towards Robust Interpretability with Self-Explaining Neural Networks](http://papers.nips.cc/paper/8003-towards-robust-interpretability-with-self-explaining-neural-networks.pdf). in *Advances in Neural Information Processing Systems 31* (eds. Bengio, S. et al.) 7775–7784 (Curran Associates, Inc., 2018).

[^36]: 665.

Zhang, Q., Wu, Y. N. & Zhu, S.-C. Interpretable Convolutional Neural Networks. in *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition* 8827–8836 (2018). doi:[10.1109/CVPR.2018.00920](https://doi.org/10.1109/CVPR.2018.00920).

[^37]: 666.

Schrödinger, LLC. The PyMOL molecular graphics system, version 1.8. (2015).

[^38]: 667.

Rhee, S.-Y., Liu, T. F., Holmes, S. P. & Shafer, R. W. [HIV-1 Subtype B Protease and Reverse Transcriptase Amino Acid Covariation](https://doi.org/10.1371/journal.pcbi.0030087). *PLOS Computational Biology* **3**, e87 (2007).

[^39]: 668.

De Luca, A. *et al.* [Improved Interpretation of Genotypic Changes in the HIV-1 Reverse Transcriptase Coding Region That Determine the Virological Response to Didanosine](https://doi.org/10.1086/522231). *J Infect Dis* **196**, 1645–1653 (2007).

[^40]: 669.

Marcelin, A.-G. *et al.* Impact of HIV-1 reverse transcriptase polymorphism at codons 211 and 228 on virological response to didanosine. *Antiviral Therapy* 8 (2006) doi:[10.1177/135965350601100609](https://doi.org/10.1177/135965350601100609).

[^41]: 670.

Brown, A. J. L. *et al.* [Reduced Susceptibility of Human Immunodeficiency Virus Type 1 (HIV-1) from Patients with Primary HIV Infection to Nonnucleoside Reverse Transcriptase Inhibitors Is Associated with Variation at Novel Amino Acid Sites](https://doi.org/10.1128/jvi.74.22.10269-10273.2000). *J Virol* **74**, 10269–10273 (2000).

[^42]: 671.

Clark, S. A., Shulman, N. S., Bosch, R. J. & Mellors, J. W. [Reverse transcriptase mutations 118I, 208Y, and 215Y cause HIV-1 hypersusceptibility to non-nucleoside reverse transcriptase inhibitors](https://doi.org/10.1097/01.aids.0000222069.14878.44). *Aids* **20**, 981–984 (2006).

[^43]: 672.

Nebbia, G., Sabin, C. A., Dunn, D. T. & Geretti, A. M. [Emergence of the H208Y mutation in the reverse transcriptase (RT) of HIV-1 in association with nucleoside RT inhibitor therapy](https://doi.org/10.1093/jac/dkm067). *J Antimicrob Chemother* **59**, 1013–1016 (2007).

[^44]: 673.

Saracino, A. *et al.* [Impact of unreported HIV-1 reverse transcriptase mutations on phenotypic resistance to nucleoside and non-nucleoside inhibitors](https://doi.org/10.1002/jmv.20500). *Journal of Medical Virology* **78**, 9–17 (2006).

[^45]: 674.

Wu, T. T., Chen, Y. F., Hastie, T., Sobel, E. & Lange, K. [Genome-wide association analysis by lasso penalized logistic regression](https://doi.org/10.1093/bioinformatics/btp041). *Bioinformatics* **25**, 714–721 (2009).