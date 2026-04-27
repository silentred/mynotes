---
title: "Chapter 4 Learning From Sequences and Alignments | From sequences to knowledge, improving and learning from sequence alignments"
source: "https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html"
author:
  - "[[Luc Blassel]]"
published:
created: 2026-04-26
description: "Chapter 4 Learning From Sequences and Alignments | From sequences to knowledge, improving and learning from sequence alignments"
tags:
  - "clippings"
---
## Chapter 4 Learning From Sequences and Alignments

Sequences and sequence alignments are very rich sources of information. As was stated in Chapters [2](https://thesis.lucblassel.com/aligning-sequence-data.html#aligning-sequence-data) and [3](https://thesis.lucblassel.com/HPC-paper.html#HPC-paper), many downstream analyses rely on sequence alignments.

In whole genome assembly, where sequencing reads are combined together to deduce the genome sequence, pairwise sequence alignment is used, both in reference-based [^3] and *de novo* [^5] assembly. It has also been used to deduce protein function [^7]. Pairwise alignment, has been used for sequence clustering [^1] as well as detecting genetic [^8] and structural variants [^9]. Multiple sequence alignments are also very widely used, mainly in phylogenetic analyses where the evolutionary history of a set of sequences are studied and represented as trees [^11], but they have also been used extensively in protein structure prediction [^13].

More recently, as computational power and datasets have grown, more and more machine learning methods are being used on sequence alignments in order to gain biological insight. In this chapter, we will explore how this can be done, as an introduction to Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper) where we present an application: predicting HIV drug resistance mutations.

## 4.1 What to learn?

One of the first questions one might ask themselves when wishing to use machine learning with sequence data is “what can I learn?”. A simplistic answer to this question would be “a lot of things” as the following section will strive to show. To choose what we learn we must first choose a learning paradigm.

### 4.1.1 Supervised learning from biological sequences

Supervised learning is one of the main machine learning paradigms, where we have data that consists of a collection of input and output pairs (e.g. a DNA sequence and an associated species). By feeding these pairs to our algorithm of choice, it will learn to predict the output based on the input alone. This is a very powerful way of learning something interesting. We can consider the link between inputs and outputs as extra knowledge that the dataset creator or curator can infuse in the learning algorithm. Within the supervised learning paradigm there are two possible tasks: *regression* and *classification*.

#### 4.1.1.1 Regression tasks

For regression tasks, the outputs of our input-output pairs are encoded by a continuous numerical value. Regression models will therefore output continuous real values. Fortunately, many interesting continuous values can be computed from aligned sequences, and in many cases, machine learning models can be trained to predict these variables.

Regression methods have been used to predict drug response in cancer patients [^14] and resistance levels to drugs in HIV [^15]. These methods are also extensively used in protein structure prediction where they are trained to predict residue angles or values in protein contact maps from aligned sequences [^16], or directly from an MSA [^2]. Regression algorithms have been used to predict protein fitness *in silico* [^18] to speed up protein engineering, and make some processes like drug development faster and cheaper. They have also been used in many other tasks such as predicting gene expression levels [^20] or predicting multiple sequence alignment scores [^21].

In many cases these methods use an encoded representation of the sequences (c.f. Section [4.3](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#pre-processing-the-alignment-for-machine-learning)) as input, but some represent the inputs as values computed from alignments. For example, protein structure can be predicted from contact maps [^22] derived from MSAs, and gene expression levels can be predicted from lists of mutations that are obtained through alignment to a reference sequence [^20]. This last approach is also used in Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper) to predict drug resistance in HIV.

#### 4.1.1.2 Classification tasks

For classification tasks, the outputs of our input-output pairs are categorical in nature and often represented as discrete integer values. Originally, most classification methods were designed for binary classification with only two possible outputs: a “positive” and a “negative” class. This is a simpler problem to solve than multiclass classification problems where more than two outputs are possible. Most methods that can handle binary classification have been adapted to multiclass classification.

In biology, categorizing and classifying is often at the root of several research problems. As such, machine learning classifiers have obvious applications and have been widely used with sequence data as inputs. Classifiers have been used to predict if a particular virus [^23] (also Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper)), or bacteria [^25] is resistant to antiviral or antimicrobial drugs respectively. Some classifier models have also been used to predict characteristics at positions in a sequence, like methylation site prediction [^27] or splicing site detection [^28]. This type of approach has also been applied for sequence labeling tasks, where each token of a sequence *(amino acids, codons, …)*, is assigned a label using classifiers. This has been applied to protein secondary structure prediction [^29] where each residue is assigned a label (α $α$ $\alpha$ -helix or β $β$ $\beta$ -sheet), or gene prediction where stretches of the sequence are classified as part of a gene or not [^30]. Base calling for Nanopore sequencing data (mentioned in [1.2.3](https://thesis.lucblassel.com/what-is-sequence-data.html#long-read-sequencing)), is also a sequence labeling task, although the sequence is made up of voltages and the assigned labels are nucleotides. Finally, classifiers have also been used to predict more general characteristics of a given sequence, like the cellular localization [^32] and putative function [^33] of proteins, or the cellular localization of gene expression data [^34].

I have presented here, only a fraction of what is possible to learn from sequences in the supervised learning paradigm. I hope you will agree with me that there is no shortage of problems in computational biology that are suited to this sort of approach. By using machine learning, instead of more formal statistical approaches, there is a lower amount of upfront assumptions and the algorithm is tasked with figuring out what features of the data are important or not for the task at hand.

### 4.1.2 Unsupervised learning from biological sequences

The second main machine learning paradigm is called, by contrast to supervised learning, unsupervised learning. In this paradigm we do not have input-output pairs but only inputs. The goal of unsupervised machine learning methods is to extract some structure or patterns from the given input without additional guidance.

One of the main tasks in the unsupervised learning paradigm is clustering, wherein similar inputs are grouped together, methods like k $k$ $k$ -means or hierarchical clustering [^35] often use some type of distance metric between inputs to define clusters of similar inputs. Clustering can be used for classification tasks, indeed if some characteristics of sequences in a given cluster are known then we can make the assumptions that sequences in the same cluster will be similar and share these characteristics. This has been used to group proteins in families [^36]. Clustering methods can also be used to remove duplicate or near-duplicate sequences in datasets [^37]. Phylogenetic trees can be considered as a specific type of clustering methods, and they have been used to group biological sequences [^38].

One of the main obstacles to clustering biological sequences is the need for computing distances between sequences. As stated in Chapter [2](https://thesis.lucblassel.com/aligning-sequence-data.html#aligning-sequence-data), obtaining a biologically relevant distance metric between two sequences, such as the edit-distance, is no easy task. Additionally, in many cases, all pairwise distances are needed for clustering, meaning at least a quadratic time and space complexity for a naive clustering algorithm. Two approaches can be used to resolve this problem: devise methods that do not need all pairwise distances [^39], or find a way to speed up distance computation. Some methods have been developed to devise distance metrics that are biologically relevant and less expensive to compute than the edit-distance: like the hashing based MASH [^40] or dashing [^41], or the neural network based NeuroSEED [^42].

Unsupervised learning can also be used without clustering. For example, unsupervised methods based on maximum likelihood approaches have been used to predict mutational effects in protein sequence [^43] as well as predict recombination hotspots in human genomic sequences [^44].

In many cases, unsupervised learning can be done as a preliminary dimensionality reduction step to a supervised learning task. Indeed biological data is often high-dimensional, and it is often useful to lower the amount of dimensions to speed up computations. Some unsupervised methods can reduce the number of dimensions while retaining most of the information. One such method, Principal Component Analysis (PCA), is widely used. PCA has been applied to distance matrices to compute phylogenetic trees [^45], and work has been done to apply PCA directly to MSAs without needing to go through a distance matrix [^46]. PCA is also widely used in clustering applications [^47].

### 4.1.3 Others paradigms

More recently, other learning paradigms have gained popularity in machine learning circles. Within the *semi-supervised* paradigm, a small amount of labelled data (*i.e.* input-output pairs) is included in a large un-labelled dataset, and methods can leverage both. This approach has been used to predict drug to protein interactions [^49] and predict the secondary structure of specific transmembrane proteins [^50].

In the *self-supervised* paradigm, models are first trained on a proxy task that hopefully makes use of important information in the data. Through this pre-training step, self-supervised models extract important information from the data and create internal features and models that can then be leveraged in a supervised or unsupervised fine-tuning task. This paradigm has exploded lately within the field of natural language processing and machine translation with the rise of transformers, but has also been widely used to create protein language models like ProtBert [^51] and extract information from disordered protein regions [^52]. We will look at self-supervised learning in a little more detail in Chapter [7](https://thesis.lucblassel.com/learning-alignments-an-interesting-perspective.html#learning-alignments-an-interesting-perspective).

Finally, the end-to-end learning paradigm designates the process of chaining several machine learning tasks together and optimizing the algorithms simultaneously using the error from the loss of the last task of the group. This has been successfully used to predict protein-protein interaction surfaces in three dimensions [^53] as well as predict micro-RNA targets sequences [^54]. This paradigm can also be used in a task-based fashion, where a differentiable loss function is crafted on a traditionally non-machine learning task and used to train preceding models. This has been explored for sequence alignment and is further detailed in Chapter [7](https://thesis.lucblassel.com/learning-alignments-an-interesting-perspective.html#learning-alignments-an-interesting-perspective)

## 4.2 How to learn?

Machine learning regroups a multitude of techniques and methods to extract knowledge and make data-driven predictions. In this section, we will quickly go over some of the main supervised-learning methods, and go into more detail for techniques used in Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper): logistic regression, naive Bayes and random forests.

### 4.2.1 General setting

Supervised machine learning is an optimization process. A given algorithm, which I will refer to as a *model*, has an associated loss function that can be evaluated on a dataset. This loss represents how well the model is predicting outputs from inputs on known input-output pairs. Through an iterative process, this loss is optimized *(in our case minimized)* over all pairs forming a dataset. Often, in the literature, loss and cost are used interchangeably [^55]. I will favor loss in the following sections.

There is no shortage of loss functions [^56], some of them are specifically crafted for a given model while some are widely used in regression tasks like the Root Mean Square Error (RMSE). Others like the cross-entropy loss are used in classification tasks.

After training a machine learning model on a dataset, it is often important to compute a performance measure to get an idea of how well this model is performing. We could do this on the same data on which the model was trained, this would however be wrong. Indeed, it gives an unfair advantage to the model since it predicts outputs from examples it has already seen. Furthermore, it gives us no insight into the generalizability of the model since it could just learn the dataset by heart, getting a perfect score on it while being completely useless on new unseen data. This situation is known as *overfitting* [^35], shown in Figure [4.1](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#fig:overfitting). Since being able to predict outcomes on unseen data is the main goal of a machine learning model, we need another way of measuring model performance. The way machine learning practitioners can measure the performance of their model in a more unbiased manner is by separating the dataset into two parts before even starting to train the model: one part (usually the majority of the data) is used as the *training set*, and the other as the *testing set*. Logically, the training set is used to train the model while the testing set is used to evaluate the performance of the model after training.

![**Overfitting behaviour in loss functions.**  
The two curves show how the loss calculated on the training set (blue) and the testing set (red) evolve as training time increases. At first both decrease showing that the model learns informative and generalizable features. At some point, training loss keeps decreasing and testing loss increases, meaning that the model is learning over-specific features on the training set and is no longer generalizable: it is overfitting.](https://thesis.lucblassel.com/figures/Encode-seqs/Overfitting.png)

Figure 4.1: **Overfitting behaviour in loss functions.**  
The two curves show how the loss calculated on the training set (blue) and the testing set (red) evolve as training time increases. At first both decrease showing that the model learns informative and generalizable features. At some point, training loss keeps decreasing and testing loss increases, meaning that the model is learning over-specific features on the training set and is no longer generalizable: it is overfitting.

As there is a multitude of loss functions, there are many performance metrics to assess how the model is doing on the testing data, especially for classification tasks [^57]. For regression, RMSE is also widely used as a performance metric, along with the Mean Absolute Error (MAE). For classification, accuracy is the most widely used performance metric. Accuracy is the ratio of the number of correctly classified examples divided by the total number of examples. Accuracy has also been adapted to specific settings like unbalanced data where the different possible output classes are not represented equally [^58]. The testing set must stay completely separate from the training set and decisions about model settings or input features used must be made without help of the testing data. If these stringent conditions are not respected this can lead to *data leakage* and artificially increase performance of the model on the testing data, giving us a biased view of the model’s performance and generalizability [^59]. This leaking of testing data into the training process is a common pitfall of machine learning [^60]. To remedy to this problem, a separate dataset is often reserved and used as a *validation set,* in order to provide some estimation of model performance without using the testing set.

In many cases, machine learning models have a number of parameters that guide model behavior. These parameters are chosen before training and are different from the internal parameters of the model that are optimized during training. As such, they are often called *hyper-parameters*. These could, for example, be the number of levels in a decision tree, a learning rate, or a stopping threshold. The value of these hyper-parameters is often very influential on model performance. However, setting hyper-parameter values based on the model’s test set performance would lead to data leakage as stated earlier, and using a separate validation set can lead to small training sets. To still be able to tune hyper-parameters for optimal performance, and keep a large training set, k $k$ $k$ *\-fold cross-validation* is used [^35]. In this setting, shown in Figure [4.2](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#fig:crossValidation), the testing set is set aside before model training and reserved for the final model performance evaluation. The training set is then further subdivided into k $k$ $k$ equally-sized subsets, called folds. Each of the k $k$ $k$ folds is then used to create a what is called a *validation split*: the fold acting as a within-split testing set and the rest of the general training set is used as the within-split training set. This results in k $k$ $k$ pairs of disjoint training and testing sets, and each example of the general training data is used exactly once in a within-split testing set. An idea of the model performance can be obtained by measuring performance on the within-split testing sets and averaging the measures. This cross-validation performance can be used to inform hyper-parameter value choice without using the reserved testing set and avoiding data leakage.

![**Example of data splits into training, testing and validation sets with 6-fold cross-validation.**  
In this setting, the whole data set is first split into a training and testing set. The testing set is kept separate to assess final model performance. The training set is split into 6 folds resulting in 6 splits. In each split of the training set, the correspoding fold is used as the within-split test set (green), and the rest of the training set is used as the within-split training set (blue). You can get an idea of the model performance by averaging measures on within-split testing sets and adjusting hyper-parameters accordingly, without using the global, reserved testing set. Adapted from <https://scikit-learn.org/stable/modules/cross_validation.html>](https://thesis.lucblassel.com/figures/Encode-seqs/Cross-validation.png)

Figure 4.2: **Example of data splits into training, testing and validation sets with 6-fold cross-validation.**  
In this setting, the whole data set is first split into a training and testing set. The testing set is kept separate to assess final model performance. The training set is split into 6 folds resulting in 6 splits. In each split of the training set, the correspoding fold is used as the within-split test set (green), and the rest of the training set is used as the within-split training set (blue). You can get an idea of the model performance by averaging measures on within-split testing sets and adjusting hyper-parameters accordingly, without using the global, reserved testing set. Adapted from [https://scikit-learn.org/stable/modules/cross\_validation.html](https://scikit-learn.org/stable/modules/cross_validation.html)

This is the general setting in which a lot of the supervised learning approaches in computational biology reside, *e.g.* cross-validation was used to tune hyper-parameters for the models in Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper).

### 4.2.2 Tests and statistical learning

Some of the simplest models possible are derived from statistics and based on probabilities. One such way to classify data is with a statistical test, like Fisher’s exact test [^61] or a χ2 $χ2$ $\chi^2$ test [^62], depending on the number of training examples. If one of the input variables is significantly related to the output then one can make a crude prediction on the output based solely on the value of one input variable. By testing several features and predicting the output from a set of significantly related input variables (e.g. through a vote), then prediction accuracy can be improved. This approach is used as a baseline in the study presented in Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper). It is, however, not very sophisticated and does not have the best predictive power.

A model that fits more squarely in the process of supervised learning described above is linear regression. This regression model assumes that the output value results from a linear combination of the input features and an intercept value. The coefficients of this linear combination and the intercept are the parameters that the models optimizes during the learning process. Often, the loss function used to fit this model is the RMSE mentioned above. The gradient of the RMSE w.r.t. all the coefficients of the model is easily derived and can be used for optimization. Since this model is very simple there is an exact analytical solution to find the minimum gradient value [^35]. However, in some cases a gradient descent approach can be beneficial to train this model. This model has also been adapted to binary classification, by considering that the output value results from a linear combination of input models, passed through a logistic function. The resulting model is called logistic regression, and is one of the classifiers used in Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper). Equations [(4.1)](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#eq:linReg) and [(4.2)](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#eq:logReg) show the mathematical model of linear and logistic regression respectively. In these equations, ^y(i) $y^(i)$ $\hat{y}^{(i)}$ represents the predicted output of the i <sup>th</sup> example and x(i)j $xj(i)$ $x_j^{(i)}$ the j <sup>th</sup> variable of the i <sup>th</sup> example input. θ0 $θ0$ $\theta_0$ is the intercept and θj $θj$ $\theta_j$ the coefficient corresponding to the j <sup>th</sup> input variable.

^y(i)=θ0+k∑j=1θj⋅x(i)j(4.1) 
$$
(4.1)y^(i)=θ0+∑j=1kθj⋅xj(i)
$$
 
$$
\begin{equation}
  \hat{y}^{(i)} = \theta_0 + \sum_{j=1}^k \theta_j \cdot x_j^{(i)}
  \tag{4.1}
\end{equation}
$$
 ^y(i)=11+e−(θ0+∑kj=1θj⋅x(i)j)(4.2) 
$$
(4.2)y^(i)=11+e−(θ0+∑j=1kθj⋅xj(i))
$$
 
$$
\begin{equation}
  \hat{y}^{(i)} = \frac{1}{
    1 + e^{
      -(\theta_0 + \sum_{j=1}^k \theta_j \cdot x_j^{(i)})
    }
  }
  \tag{4.2}
\end{equation}
$$

The model in Equation [(4.1)](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#eq:linReg) outputs a continuous value used in regression, and the model in Equation [(4.2)](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#eq:logReg) outputs a continuous value bounded between 0 and 1, that we can consider a probability of being in one of the classes. With this probability it is easy to classify a given example in one of the two classes. It is easy to extend the logistic regression model to multiclass classification, by training several models and predicting the class with the maximal probability.

These linear models are simple, but can achieve good performance. They can, however, be prone to overfitting. This often translates into very large values for the θ $θ$ $\theta$ coefficients. In order to counter this, regularized versions of linear and logistic regression were introduced by adding the weights to the loss function in some way. By adding the coefficient values to the loss they are kept small through the optimization process, reducing the risk of overfitting. The two main regularization strategies are the ridge [^63] and Lasso [^64] penalties.

The final supervised model I will present in this section is the Naive Bayes classifier. As its name indicates, it is based on Bayes’ theorem of conditional probabilities. By making a strong assumption, that all variables of the input examples are mutually independent, we can derive the probability of the i <sup>th</sup> input example belonging to class Cα $Cα$ $C_{\alpha}$ as:

p(Cα|x(i)1,…,x(i)k)=Z⋅p(Cα)k∏j=1p(x(i)j|Cα) 
$$
p(Cα|x1(i),…,xk(i))=Z⋅p(Cα)∏j=1kp(xj(i)|Cα)
$$
 
$$
\begin{equation}
p(C_{\alpha} | x^{(i)}_1, \ldots, x^{(i)}_k) = Z \cdot p(C_{\alpha}) \prod_{j=1}^k p(x^{(i)}_j | C_{\alpha})
\end{equation}
$$

With Z $Z$ $Z$ a constant that can be computed from the training data. Therefore it is very easy to use this to build a classifier by computing the probabilities of an example belonging to a class for all possible classes in the training data and assign the one with the maximal probability. In practice this is a very flexible model, since any probability distribution can be used for each feature and class. The parameters of these distributions can be learned with a maximum likelihood approach for example. This model builds upon the naive assumption (hence the name) that all input variables are mutually independent. This assumption is very often violated, especially in biological sequence data where independence is not at all guaranteed by the evolutionary process. This model is, however, quite robust to this, and stays performant despite the violations of this assumption [^65].

## 4.3 Pre-processing the alignment for machine learning

By now you will surely have noticed that all the models I presented above (with the exception of RFs) need to be trained on a collection of numerical variables, *i.e.* numerical vectors. Biological sequences, however, are not vectors of numbers. We therefore need to transform our sequences of letters into numerical sequences that we can feed to the machine learning model in this digestible form. Most supervised machine learning algorithms expect a matrix as input, where the rows are individual training examples and the columns numerical variables. A vector where each entry corresponds to an expected output value is used during training. In this section, I will present a few encoding methods, that transform a multiple sequence alignment in a matrix. Most of the encoding methods are not defined on an alignment, but on sequences alone. However, to represent these sequences they often need to have the same length, and for models to learn anything meaningful the values in features should encode the same information across sequences. Therefore, prior to the encoding methods described below the sequences often need to be aligned to each other so that a specific position in a sequence is homologous to that position in all other training sequences.

### 4.3.1 General purpose encodings

The letters making up biological sequences are a form of categorical data. This type of variable is not specific to biology and as such, there exists many encoding schemes [^76] to transform categorical variables into numerical vectors.

The most basic, and conceptually simple way to do so is to use the labeling scheme, often called ordinal encoding. Each level of the categorical variable is assigned an integer label. For example, when dealing with DNA sequences, we could have A=1, C=2, G=3 and T=4. This scheme outputs vectors that have the same size as the input sequence and going from the sequence to the encoded vector (and *vice versa*) is very easy. This encoding scheme has been used to predict resistance levels of HIV to antiviral drugs from sequencing data [^15]. There is, however, a major disadvantage with using this method. As its name indicates, ordinal encoding implies that there is an order to the categorical variable levels (*e.g.* T>A) which, by definition, does not exist [^77]. Another option is to use what I will refer to as binary labeling, where the categorical levels are first assigned an integer label which is then converted to a binary vector. If we use the ordinal DNA encoding from above and convert it to binary vectors we would get: A= \[0,0\] $[0,0]$ $[0,0]$, C= \[0,1\] $[0,1]$ $[0,1]$, G= \[1,0\] $[1,0]$ $[1,0]$ and T= \[1,1\] $[1,1]$ $[1,1]$. This type of representation is frequently used to represent gapless sequences, like k $k$ $k$ -mers, in a compressed form [^79] (a character now only needs 2 bits instead of a full byte). For amino acids, since there are more characters, this encoding yields vectors of 5 bits [^81]. Fundamentally, this encoding scheme has the same problem as the ordinal encoding, creating an order that does not exist, although with the order being split into separate values it can mitigate this effect a little bit.

One of the most widely used categorical encoding schemes, One-Hot encoding (OHE) (sometimes called orthonormal encoding [^82]), does not have this ordering issue. The way OHE works is by creating a sparse binary vector of length d $d$ $d$ to represent a variable with d $d$ $d$ levels *(for DNA* d=4 $d=4$ $d=4$). If the i <sup>th</sup> level of the categorical variable is to be encoded, then the i <sup>th</sup> position in the vector is set to 1 and the rest set to 0. For example, if we consider that A is the first level of our variable then OHE would yield the following vector: \[1,0,0,0\] $[1,0,0,0]$ $[1,0,0,0]$. This encoding scheme has been used from the 1980’s [^83] to now [^84], and is the scheme used in Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper). The performance of OHE can be on par with ordinal encoding [^85], but it is easily interpretable, which is often very important in biology since there is a one to one correspondence between a categorical value and a numerical feature. The main problem with OHE is that it tends to increase the number of features quite a lot, since the encoded vector representation of a length n $n$ $n$ sequence is of length n×d $n×d$ $n\times d$. An example comparing Ordinal, Binary and One-Hot encodings can be seen in Figure [4.4](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#fig:generalEncoding).

![**Example of 3 general categorical encoding schemes.**  
Two sequences, `ATCG` and `TAAT` are shown encoded in three different encoding schemes: ordinal, binary and one-hot encoding. In the ordinal encoding, each character is assigned an integer value, here A=0, C=1, G=3 and T=4. In the binary encoding, these integer values are encoded with 2 bits. In the one-hot encoding scheme, a character corresponds to a sparse vector indicating which level of the variable is present: here A=[1,0,0,0]. Ordinal encoding preserves the dimension of the sequence while binary and one-hot encoding result in vectors with a bigger dimension than the original sequence. 
](https://thesis.lucblassel.com/figures/Encode-seqs/General-purpose.png)

Figure 4.4: **Example of 3 general categorical encoding schemes.**  
Two sequences, `ATCG` and `TAAT` are shown encoded in three different encoding schemes: ordinal, binary and one-hot encoding. In the ordinal encoding, each character is assigned an integer value, here A=0, C=1, G=3 and T=4. In the binary encoding, these integer values are encoded with 2 bits. In the one-hot encoding scheme, a character corresponds to a sparse vector indicating which level of the variable is present: here A=\[1,0,0,0\]. Ordinal encoding preserves the dimension of the sequence while binary and one-hot encoding result in vectors with a bigger dimension than the original sequence.

These three general purpose encodings are but some of many [^76], and since categorical variables are often used in machine learning applications, these encodings are often available in widely used software libraries [^86].

### 4.3.2 Biological sequence-specific encodings

While the general-purpose encoding schemes presented above work well enough in practice, some specific encoding methods were developed to include some biological information in the sequence encodings that hopefully machine learning models will be able to leverage during training. These encodings have mostly been developed for encoding protein sequences, using physicochemical properties of amino acids [^81].

AAIndex [^87] is a public database containing amino acid indices, *i.e.* sets of 20 numerical values (one for each AA) measuring some physicochemical property. There is a wide range of these indices, from hydrophobicity to flexibility or residue volume measures. By selecting an informative subset of 9 of these measures [^88], an amino acid can be represented by a length 9 numerical vector. In some cases, amino acids can be represented by all the 566 properties of AAIndex, and through PCA the dimension of the resulting numerical vectors can be reduced [^89]. This biological sequence specific encoding has been implemented in a software library for biological sequence encoding [^90].

Another biological sequence-specific encoding is based on the Amino Acid classification Venn diagram defined by Taylor in 1986 [^91], which groups amino acids into eight different groups based on physicochemical properties: aliphatic, aromatic, hydrophobic, polar, charged, positive, small and tiny. With this classification, a single amino acid can be represented by a vector of length 8, each element representing a group, set to one when the amino acid belongs to the group and to zero when it does not. This encoding method was used as early as 1987 to predict secondary structures of proteins [^92]. Later on, another five groups were proposed and used to encode each amino acid with longer vectors [^93].

A third encoding method, named BLOMAP [^94], encodes sequences based on values from the BLOSUM62 substitution matrix presented in Section [2.1.3](https://thesis.lucblassel.com/aligning-sequence-data.html#scoring-and-substitution-models). BLOMAP is defined by using a non-linear projection algorithm to generate vectors of length five, that capture the similarity measures contained in BLOSUM62. This encoding has been used to successfully predict cleavage sites of the HIV-1 protease [^82] *(c.f. Section* [5.3.2.2](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#protease)). Other encodings such as OETMAP [^95] have been derived from BLOMAP.

These three encodings are far from being the only ones specific to biological sequence. Many other encoding schemes were developed to learn from this type of sequence data. Some schemes do not encode positional data, and as such, can be applied to unaligned sequences. The simplest of these would be to represent a sequence by its amino acid, or k $k$ $k$ -mer frequencies. The latter is often referred to as n $n$ $n$ -gram encoding [^96] and widely used, although with very short k $k$ $k$ -mers since the dimension of the encoding grows exponentially with k $k$ $k$. With 20 amino acids, this encoding results in vectors that have a length of 20k $20k$ $20^k$. Other encoding schemes use codon information to encode amino acids. One such scheme was proposed in [^81], where an amino acid is represented by a directed graph where vertices are nucleotides and edges represent paths needed to represent codons that code for that amino acid. This graph can then be converted to a 16-dimensional vector by flattening the corresponding adjacency matrix and used as an encoding method.

During the work that led to Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper), several encoding methods were tested: Ordinal, Binary, OHE, AAIndex and Group encodings. The same two training sets of sequences were encoded using each of these methods, and 10 RF models were trained on each of the encoded datasets, om a binary classification task. Accuracy, precision and recall metrics were used to evaluate the performance of the RF on each encoded dataset. According to these metrics, the RF model had the best performance on the datasets encoded with OHE. OHE, also has the advantage of being more easily interpretable. As such, it was chosen for the work presented in Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper).

Other encodings have been used to convert a biological sequence into a single real value. An encoding method based on chaos game theory [^97] allows for a bijective mapping between the DNA sequence set and the real numbers set. This encoding is not specific to alignments and can be used to do alignment-free comparisons, as such it has been used often in bioinformatics applications [^98]. Recently, this encoding scheme has been used to classify SARS-CoV2 sequences [^99], predict anti-microbial resistance from sequence data [^25] and for phylogenetic analysis [^100].

In recent years algorithmic developments, computing power increase and the massive amounts of available data have made deep learning methods useful, possible to train and very popular. This has given rise to new sequence encoding methods, that are learned on the training data. These are often referred to as embeddings rather than encodings. Since these learned embeddings are not used in Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper), for the sake of thematic coherence I will not be mentioning them here. I will, however, go over these embedding methods shortly in Chapter [7](https://thesis.lucblassel.com/learning-alignments-an-interesting-perspective.html#learning-alignments-an-interesting-perspective).

## 4.4 Conclusion

Alignments, and the sequences within them, are rich sources of information, that have long been exploited widely for many different types of analyses. With the rise of machine learning in the last years, it is logical that machine learning models have been applied more and more frequently to biological sequence data. Machine Learning is a wide field with many different methods and paradigms. Even simple methods like linear regression or naive Bayes can be very useful, and more complex models like random forests have been able to make very good predictions on biological data. The model is not the only variable to take into account when looking to apply machine learning methods on sequence data. Different encoding methods will yield different vector representations, with different characteristics and applications. Special care must therefore be given to the choice of biological sequence encoding scheme, prior to starting a machine learning analysis.

### References

[^1]: 116.

Sahlin, K. & Medvedev, P. [De Novo Clustering of Long-Read Transcriptome Data Using a Greedy, Quality Value-Based Algorithm](https://doi.org/10.1089/cmb.2019.0299). *Journal of Computational Biology* **27**, 472–484 (2020).

[^2]: 137.

Jumper, J. *et al.* [Highly accurate protein structure prediction with AlphaFold](https://doi.org/10.1038/s41586-021-03819-2). *Nature* **596**, 583–589 (2021).

[^3]: 319.

Martin, J. A. & Wang, Z. [Next-generation transcriptome assembly](https://doi.org/10.1038/nrg3068). *Nat Rev Genet* **12**, 671–682 (2011).

[^4]: 320.

Kyriakidou, M., Tai, H. H., Anglin, N. L., Ellis, D. & Strömvik, M. V. [Current Strategies of Polyploid Plant Genome Sequence Assembly](https://doi.org/10.3389/fpls.2018.01660). *Frontiers in Plant Science* **9**, (2018).

[^5]: 321.

Paszkiewicz, K. & Studholme, D. J. [De novo assembly of short sequence reads](https://doi.org/10.1093/bib/bbq020). *Briefings in Bioinformatics* **11**, 457–472 (2010).

[^6]: 322.

Sohn, J. & Nam, J.-W. [The present and future of de novo whole-genome assembly](https://doi.org/10.1093/bib/bbw096). *Briefings in Bioinformatics* **19**, 23–40 (2018).

[^7]: 323.

Sleator, R. D. & Walsh, P. [An overview of in silico protein function prediction](https://doi.org/10.1007/s00203-010-0549-9). *Arch Microbiol* **192**, 151–155 (2010).

[^8]: 324.

Koboldt, D. C. [Best practices for variant calling in clinical sequencing](https://doi.org/10.1186/s13073-020-00791-w). *Genome Medicine* **12**, 91 (2020).

[^9]: 325.

Alkan, C., Coe, B. P. & Eichler, E. E. [Genome structural variation discovery and genotyping](https://doi.org/10.1038/nrg2958). *Nat Rev Genet* **12**, 363–376 (2011).

[^10]: 326.

Ho, S. S., Urban, A. E. & Mills, R. E. [Structural variation in the sequencing era](https://doi.org/10.1038/s41576-019-0180-9). *Nat Rev Genet* **21**, 171–189 (2020).

[^11]: 327.

Morrison, D. A. [Phylogenetic tree-building](https://doi.org/10.1016/0020-7519\(96\)00044-6). *International Journal for Parasitology* **26**, 589–617 (1996).

[^12]: 328.

Kapli, P., Yang, Z. & Telford, M. J. [Phylogenetic tree building in the genomic age](https://doi.org/10.1038/s41576-020-0233-0). *Nat Rev Genet* **21**, 428–444 (2020).

[^13]: 329.

Kuhlman, B. & Bradley, P. [Advances in protein structure prediction and design](https://doi.org/10.1038/s41580-019-0163-x). *Nat Rev Mol Cell Biol* **20**, 681–697 (2019).

[^14]: 330.

Ammad-ud-din, M., Khan, S. A., Wennerberg, K. & Aittokallio, T. [Systematic identification of feature combinations for predicting drug response with Bayesian multi-view multi-task linear regression](https://doi.org/10.1093/bioinformatics/btx266). *Bioinformatics* **33**, i359–i368 (2017).

[^15]: 331.

Steiner, M. C., Gibson, K. M. & Crandall, K. A. [Drug Resistance Prediction Using Deep Learning Techniques on HIV-1 Sequence Data](https://doi.org/10.3390/v12050560). *Viruses* **12**, 560 (2020).

[^16]: 332.

Noé, F., De Fabritiis, G. & Clementi, C. [Machine learning for protein folding and dynamics](https://doi.org/10.1016/j.sbi.2019.12.005). *Current Opinion in Structural Biology* **60**, 77–84 (2020).

[^17]: 336.

AlQuraishi, M. [Machine learning in protein structure prediction](https://doi.org/10.1016/j.cbpa.2021.04.005). *Current Opinion in Chemical Biology* **65**, 1–8 (2021).

[^18]: 337.

Wittmann, B. J., Johnston, K. E., Wu, Z. & Arnold, F. H. [Advances in machine learning for directed evolution](https://doi.org/10.1016/j.sbi.2021.01.008). *Current Opinion in Structural Biology* **69**, 11–18 (2021).

[^19]: 339.

Li, G., Dong, Y. & Reetz, M. T. [Can Machine Learning Revolutionize Directed Evolution of Selective Enzymes?](https://doi.org/10.1002/adsc.201900149) *Advanced Synthesis & Catalysis* **361**, 2377–2386 (2019).

[^20]: 340.

Xie, R., Wen, J., Quitadamo, A., Cheng, J. & Shi, X. [A deep auto-encoder model for gene expression prediction](https://doi.org/10.1186/s12864-017-4226-0). *BMC Genomics* **18**, 845 (2017).

[^21]: 341.

Ortuño, F. M. *et al.* [Comparing different machine learning and mathematical regression models to evaluate multiple sequence alignments](https://doi.org/10.1016/j.neucom.2015.01.080). *Neurocomputing* **164**, 123–136 (2015).

[^22]: 342.

Wang, S., Sun, S., Li, Z., Zhang, R. & Xu, J. [Accurate De Novo Prediction of Protein Contact Map by Ultra-Deep Learning Model](https://doi.org/10.1371/journal.pcbi.1005324). *PLOS Computational Biology* **13**, e1005324 (2017).

[^23]: 343.

Haga, H. *et al.* [A machine learning-based treatment prediction model using whole genome variants of hepatitis C virus](https://doi.org/10.1371/journal.pone.0242028). *Plos One* **15**, e0242028 (2020).

[^24]: 344.

Zazzi, M. *et al.* [Predicting Response to Antiretroviral Treatment by Machine Learning: The EuResist Project](https://doi.org/10.1159/000332008). *Int* **55**, 123–127 (2012).

[^25]: 345.

Ren, Y. *et al.* [Prediction of antimicrobial resistance based on whole-genome sequencing and machine learning](https://doi.org/10.1093/bioinformatics/btab681). *Bioinformatics* **38**, 325–334 (2022).

[^26]: 346.

Kim, J. I. *et al.* [Machine Learning for Antimicrobial Resistance Prediction: Current Practice, Limitations, and Clinical Perspective](https://doi.org/10.1128/cmr.00179-21). *Clinical Microbiology Reviews* **0**, e00179–21 (2022).

[^27]: 347.

Wang, Y. *et al.* [Predicting DNA Methylation State of CpG Dinucleotide Using Genome Topological Features and Deep Networks](https://doi.org/10.1038/srep19598). *Sci Rep* **6**, 19598 (2016).

[^28]: 348.

Rätsch, G., Sonnenburg, S. & Schäfer, C. [Learning Interpretable SVMs for Biological Sequence Classification](https://doi.org/10.1186/1471-2105-7-s1-s9). *BMC Bioinformatics* **7**, S9 (2006).

[^29]: 349.

Jones, D. T. [Protein secondary structure prediction based on position-specific scoring matrices](https://doi.org/10.1006/jmbi.1999.3091). *J. Mol. Biol.* **292**, 195–202 (1999).

[^30]: 350.

Alioto, T. Gene Prediction. in (ed. Anisimova, M.) 175–201 (Humana Press, 2012). doi:[10.1007/978-1-61779-582-4\_6](https://doi.org/10.1007/978-1-61779-582-4_6).

[^31]: 351.

Fang, Z. *et al.* [PlasGUN: Gene prediction in plasmid metagenomic short reads using deep learning](https://doi.org/10.1093/bioinformatics/btaa103). *Bioinformatics* **36**, 3239–3241 (2020).

[^32]: 352.

Wei, L., Ding, Y., Su, R., Tang, J. & Zou, Q. [Prediction of human protein subcellular localization using deep learning](https://doi.org/10.1016/j.jpdc.2017.08.009). *Journal of Parallel and Distributed Computing* **117**, 212–217 (2018).

[^33]: 353.

Wang, H., Yan, L., Huang, H. & Ding, C. [From Protein Sequence to Protein Function via Multi-Label Linear Discriminant Analysis](https://doi.org/10.1109/tcbb.2016.2591529). *IEEE/ACM Transactions on Computational Biology and Bioinformatics* **14**, 503–513 (2017).

[^34]: 354.

Kelley, D. R., Snoek, J. & Rinn, J. L. [Basset: Learning the regulatory code of the accessible genome with deep convolutional neural networks](https://doi.org/10.1101/gr.200535.115). *Genome Res* **26**, 990–999 (2016).

[^35]: 355.

Hastie, T., Tibshirani, R. & Friedman, J. *[The Elements of Statistical Learning: Data Mining, Inference, and Prediction, Second Edition](https://books.google.com/?id=tVIjmNS3Ob8C)*. (Springer Science & Business Media, 2009).

[^36]: 356.

Kriventseva, E. V., Biswas, M. & Apweiler, R. [Clustering and analysis of protein families](https://doi.org/10.1016/s0959-440x\(00\)00211-6). *Current Opinion in Structural Biology* **11**, 334–339 (2001).

[^37]: 357.

Fu, L., Niu, B., Zhu, Z., Wu, S. & Li, W. [CD-HIT: Accelerated for clustering the next-generation sequencing data](https://doi.org/10.1093/bioinformatics/bts565). *Bioinformatics* **28**, 3150–3152 (2012).

[^38]: 358.

Balaban, M., Moshiri, N., Mai, U., Jia, X. & Mirarab, S. [TreeCluster: Clustering biological sequences using phylogenetic trees](https://doi.org/10.1371/journal.pone.0221068). *Plos One* **14**, e0221068 (2019).

[^39]: 359.

Zorita, E., Cuscó, P. & Filion, G. J. [Starcode: Sequence clustering based on all-pairs search](https://doi.org/10.1093/bioinformatics/btv053). *Bioinformatics* **31**, 1913–1919 (2015).

[^40]: 360.

Ondov, B. D. *et al.* [Mash: Fast genome and metagenome distance estimation using MinHash](https://doi.org/10.1186/s13059-016-0997-x). *Genome Biology* **17**, 132 (2016).

[^41]: 361.

Baker, D. N. & Langmead, B. [Dashing: Fast and accurate genomic distances with HyperLogLog](https://doi.org/10.1186/s13059-019-1875-0). *Genome Biology* **20**, 265 (2019).

[^42]: 362.

Corso, G. *et al.* [Neural Distance Embeddings for Biological Sequences](https://proceedings.neurips.cc/paper/2021/hash/9a1de01f893e0d2551ecbb7ce4dc963e-Abstract.html). in *Advances in Neural Information Processing Systems* vol. 34 18539–18551 (Curran Associates, Inc., 2021).

[^43]: 363.

Hopf, T. A. *et al.* [Mutation effects predicted from sequence co-variation](https://doi.org/10.1038/nbt.3769). *Nat Biotechnol* **35**, 128–135 (2017).

[^44]: 364.

Castro, B. M., Lemes, R. B., Cesar, J., Hünemeier, T. & Leonardi, F. [A model selection approach for multiple sequence segmentation and dimensionality reduction](https://doi.org/10.1016/j.jmva.2018.05.006). *Journal of Multivariate Analysis* **167**, 319–330 (2018).

[^45]: 365.

Haschka, T., Ponger, L., Escudé, C. & Mozziconacci, J. [MNHN-Tree-Tools: A toolbox for tree inference using multi-scale clustering of a set of sequences](https://doi.org/10.1093/bioinformatics/btab430). *Bioinformatics* **37**, 3947–3949 (2021).

[^46]: 366.

Konishi, T. *et al.* [Principal Component Analysis applied directly to Sequence Matrix](https://doi.org/10.1038/s41598-019-55253-0). *Sci Rep* **9**, 19297 (2019).

[^47]: 367.

Ben-Hur, A. & Guyon, I. Detecting Stable Clusters Using Principal Component Analysis. in *Functional Genomics: Methods and Protocols* (eds. Brownstein, M. J. & Khodursky, A. B.) 159–182 (Humana Press, 2003). doi:[10.1385/1-59259-364-x:159](https://doi.org/10.1385/1-59259-364-x:159).

[^48]: 370.

Clamp, M., Cuff, J., Searle, S. M. & Barton, G. J. [The Jalview Java alignment editor](https://doi.org/10.1093/bioinformatics/btg430). *Bioinformatics* **20**, 426–427 (2004).

[^49]: 

[^50]: 372.

Tamposis, I. A., Tsirigos, K. D., Theodoropoulou, M. C., Kontou, P. I. & Bagos, P. G. [Semi-supervised learning of Hidden Markov Models for biological sequence analysis](https://doi.org/10.1093/bioinformatics/bty910). *Bioinformatics* **35**, 2208–2215 (2019).

[^51]: 373.

Elnaggar, A. *et al.* [ProtTrans: Towards Cracking the Language of Life’s Code Through Self-Supervised Deep Learning and High Performance Computing](https://doi.org/10.48550/arXiv.2007.06225). *IEEE Transactions on Pattern Analysis and Machine Intelligence* vol. Pp 1–1 (2021).

[^52]: 374.

Lu, A. X. *et al.* [Discovering molecular features of intrinsically disordered regions by using evolution for contrastive learning](https://doi.org/10.1371/journal.pcbi.1010238). *PLOS Computational Biology* **18**, e1010238 (2022).

[^53]: 375.

Townshend, R., Bedi, R., Suriana, P. & Dror, R. [End-to-End Learning on 3D Protein Structure for Interface Prediction](https://proceedings.neurips.cc/paper/2019/hash/6c7de1f27f7de61a6daddfffbe05c058-Abstract.html). in *Advances in Neural Information Processing Systems* vol. 32 (Curran Associates, Inc., 2019).

[^54]: 376.

Lee, B., Baek, J., Park, S. & Yoon, S. deepTarget: End-to-end Learning Framework for microRNA Target Prediction using Deep Recurrent Neural Networks. in *Proceedings of the 7th ACM International Conference on Bioinformatics, Computational Biology, and Health Informatics* 434–442 (Association for Computing Machinery, 2016). doi:[10.1145/2975167.2975212](https://doi.org/10.1145/2975167.2975212).

[^55]: 

[^56]: 378.

Wang, Q., Ma, Y., Zhao, K. & Tian, Y. [A Comprehensive Survey of Loss Functions in Machine Learning](https://doi.org/10.1007/s40745-020-00253-5). *Ann. Data. Sci.* **9**, 187–212 (2022).

[^57]: 379.

Jiao, Y. & Du, P. [Performance measures in evaluating machine learning based bioinformatics predictors for classifications](https://doi.org/10.1007/s40484-016-0081-2). *Quant Biol* **4**, 320–330 (2016).

[^58]: 380.

Brodersen, K. H., Ong, C. S., Stephan, K. E. & Buhmann, J. M. The Balanced Accuracy and Its Posterior Distribution. in *2010 20th International Conference on Pattern Recognition* 3121–3124 (2010). doi:[10.1109/icpr.2010.764](https://doi.org/10.1109/icpr.2010.764).

[^59]: 381.

Kaufman, S., Rosset, S. & Perlich, C. Leakage in data mining: Formulation, detection, and avoidance. in *Proceedings of the 17th ACM SIGKDD international conference on Knowledge discovery and data mining* 556–563 (Association for Computing Machinery, 2011). doi:[10.1145/2020408.2020496](https://doi.org/10.1145/2020408.2020496).

[^60]: 382.

Whalen, S., Schreiber, J., Noble, W. S. & Pollard, K. S. [Navigating the pitfalls of applying machine learning in genomics](https://doi.org/10.1038/s41576-021-00434-9). *Nat Rev Genet* **23**, 169–181 (2022).

[^61]: 383.

Fisher, R. A. [On the Interpretation of Χ2 from Contingency Tables, and the Calculation of P](https://doi.org/10.2307/2340521). *Journal of the Royal Statistical Society* **85**, 87–94 (1922).

[^62]: 384.

Pearson, K. [X. On the criterion that a given system of deviations from the probable in the case of a correlated system of variables is such that it can be reasonably supposed to have arisen from random sampling](https://doi.org/10.1080/14786440009463897). *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science* **50**, 157–175 (1900).

[^63]: 385.

Hoerl, A. E. & Kennard, R. W. [Ridge Regression: Biased Estimation for Nonorthogonal Problems](https://doi.org/10.1080/00401706.1970.10488634). *Technometrics* **12**, 55–67 (1970).

[^64]: 386.

Tibshirani, R. [Regression Shrinkage and Selection Via the Lasso](https://doi.org/10.1111/j.2517-6161.1996.tb02080.x). *Journal of the Royal Statistical Society: Series B (Methodological)* **58**, 267–288 (1996).

[^65]: 387.

Zhang, H. [The Optimality of Naive Bayes](https://www.aaai.org/Papers/FLAIRS/2004/Flairs04-097.pdf). in *Proceedings of the the 17th international FLAIRS conference (FLAIRS2004)* 6 (2004).

[^66]: 388.

Rish, I. [An empirical study of the naive Bayes classifier](https://www.cc.gatech.edu/home/isbell/classes/reading/papers/Rish.pdf). in *IJCAI 2001 workshop on empirical methods in artificial intelligence* vol. 3 6 (2001).

[^67]: 389.

Vapnik, V. *Estimation of Dependences Based on Empirical Data: Springer Series in Statistics (Springer Series in Statistics)*. (Springer-Verlag, 1982).

[^68]: 390.

Boser, B. E., Guyon, I. M. & Vapnik, V. N. A training algorithm for optimal margin classifiers. in *Proceedings of the fifth annual workshop on Computational learning theory* 144–152 (Association for Computing Machinery, 1992). doi:[10.1145/130385.130401](https://doi.org/10.1145/130385.130401).

[^69]: 391.

Cortes, C. & Vapnik, V. [Support-vector networks](https://doi.org/10.1007/bf00994018). *Mach Learn* **20**, 273–297 (1995).

[^70]: 392.

Drucker, H., Burges, C. J. C., Kaufman, L., Smola, A. & Vapnik, V. [Support Vector Regression Machines](https://proceedings.neurips.cc/paper/1996/hash/d38901788c533e8286cb6400b40b386d-Abstract.html). in *Advances in Neural Information Processing Systems* vol. 9 (MIT Press, 1996).

[^71]: 393.

Breiman, L. [Random Forests](https://doi.org/10.1023/a:1010933404324). *Machine Learning* **45**, 5–32 (2001).

[^72]: 394.

Breiman, L., Friedman, J. H., Olshen, R. A. & Stone, C. J. *Classification and regression trees*. (1983). doi:[10.1201/9781315139470](https://doi.org/10.1201/9781315139470).

[^73]: 395.

Kingsford, C. & Salzberg, S. L. [What are decision trees?](https://doi.org/10.1038/nbt0908-1011) *Nat Biotechnol* **26**, 1011–1013 (2008).

[^74]: 396.

Caruana, R. & Niculescu-Mizil, A. An empirical comparison of supervised learning algorithms. in *Proceedings of the 23rd international conference on Machine learning* 161–168 (Association for Computing Machinery, 2006). doi:[10.1145/1143844.1143865](https://doi.org/10.1145/1143844.1143865).

[^75]: 397.

Yang, P., Hwa Yang, Y., B. Zhou, B. & Y. Zomaya, A. [A Review of Ensemble Methods in Bioinformatics](https://doi.org/10.2174/157489310794072508). *Current Bioinformatics* **5**, 296–308 (2010).

[^76]: 398.

Potdar, K., S., T. & D., C. [A Comparative Study of Categorical Variable Encoding Techniques for Neural Network Classifiers](https://doi.org/10.5120/ijca2017915495). *Ijca* **175**, 7–9 (2017).

[^77]: 399.

Hassani Saadi, H., Sameni, R. & Zollanvari, A. [Interpretive time-frequency analysis of genomic sequences](https://doi.org/10.1186/s12859-017-1524-0). *BMC Bioinformatics* **18**, 154 (2017).

[^78]: 401.

Kunanbayev, K., Temirbek, I. & Zollanvari, A. Complex Encoding. in *2021 International Joint Conference on Neural Networks (IJCNN)* 1–6 (2021). doi:[10.1109/ijcnn52387.2021.9534094](https://doi.org/10.1109/ijcnn52387.2021.9534094).

[^79]: 402.

Dufresne, Y. *et al.* The K-mer File Format: A standardized and compact disk representation of sets of k-mers. *Bioinformatics* btac528 (2022) doi:[10.1093/bioinformatics/btac528](https://doi.org/10.1093/bioinformatics/btac528).

[^80]: 403.

Wright, E. S. [Using DECIPHER v2.0 to Analyze Big Biological Sequence Data in R](https://doi.org/10.32614/rj-2016-025). *The R Journal* **8**, 352–359 (2016).

[^81]: 404.

Zamani, M. & Kremer, S. C. Amino acid encoding schemes for machine learning methods. in *2011 IEEE International Conference on Bioinformatics and Biomedicine Workshops (BIBMW)* 327–333 (2011). doi:[10.1109/bibmw.2011.6112394](https://doi.org/10.1109/bibmw.2011.6112394).

[^82]: 405.

Singh, D., Singh, P. & Sisodia, D. S. [Evolutionary based optimal ensemble classifiers for HIV-1 protease cleavage sites prediction](https://doi.org/10.1016/j.eswa.2018.05.003). *Expert Systems with Applications* **109**, 86–99 (2018).

[^83]: 406.

Qian, N. & Sejnowski, T. J. [Predicting the secondary structure of globular proteins using neural network models](https://doi.org/10.1016/0022-2836\(88\)90564-5). *Journal of Molecular Biology* **202**, 865–884 (1988).

[^84]: 407.

Budach, S. & Marsico, A. [Pysster: Classification of biological sequences by learning sequence and structure motifs with convolutional neural networks](https://doi.org/10.1093/bioinformatics/bty222). *Bioinformatics* **34**, 3035–3037 (2018).

[^85]: 408.

Choong, A. C. H. & Lee, N. K. Evaluation of convolutionary neural networks modeling of DNA sequences using ordinal versus one-hot encoding method. in *2017 International Conference on Computer and Drone Applications (IConDA)* 60–65 (2017). doi:[10.1109/iconda.2017.8270400](https://doi.org/10.1109/iconda.2017.8270400).

[^86]: 409.

McGinnis, W. *et al.* Scikit-Learn-Contrib/Categorical-Encoding: Release For Zenodo. (2018) doi:[10.5281/zenodo.1157110](https://doi.org/10.5281/zenodo.1157110).

[^87]: 410.

Kawashima, S. *et al.* [AAindex: amino acid index database, progress report 2008](https://doi.org/10.1093/nar/gkm998). *Nucleic Acids Res* **36**, D202–d205 (2008).

[^88]: 411.

Li, Z.-C., Zhou, X.-B., Dai, Z. & Zou, X.-Y. [Prediction of protein structural classes by Chou’s pseudo amino acid composition: Approached using continuous wavelet transform and principal component analysis](https://doi.org/10.1007/s00726-008-0170-2). *Amino Acids* **37**, 415 (2008).

[^89]: 412.

Nanni, L. & Lumini, A. [A new encoding technique for peptide classification](https://doi.org/10.1016/j.eswa.2010.09.005). *Expert Systems with Applications* **38**, 3185–3191 (2011).

[^90]: 413.

Chen, Z. *et al.* [iFeature: A Python package and web server for features extraction and selection from protein and peptide sequences](https://doi.org/10.1093/bioinformatics/bty140). *Bioinformatics* **34**, 2499–2502 (2018).

[^91]: 414.

Taylor, W. R. [The classification of amino acid conservation](https://doi.org/10.1016/s0022-5193\(86\)80075-3). *Journal of Theoretical Biology* **119**, 205–218 (1986).

[^92]: 415.

Zvelebil, M. J., Barton, G. J., Taylor, W. R. & Sternberg, M. J. E. [Prediction of protein secondary structure and active sites using the alignment of homologous sequences](https://doi.org/10.1016/0022-2836\(87\)90501-8). *Journal of Molecular Biology* **195**, 957–961 (1987).

[^93]: 416.

Kremer, S. & Lac, H. [Method, system and computer program product for levinthal process induction from known structure using machine learning](https://patents.google.com/patent/US20090024375A1/en). (2009).

[^94]: 417.

Maetschke, S., Towsey, M. & Bodén, M. [Blomap: An encoding of amino acids which improves signal peptide cleavage site prediction](https://doi.org/10.1142/9781860947322_0014). in *Proceedings of the 3rd Asia-Pacific Bioinformatics Conference* vols Volume 1 141–150 (Published By Imperial College Press And Distributed By World Scientific Publishing Co., 2005).

[^95]: 418.

Gök, M. & Özcerit, A. T. [A new feature encoding scheme for HIV-1 protease cleavage site prediction](https://doi.org/10.1007/s00521-012-0967-5). *Neural Comput & Applic* **22**, 1757–1761 (2013).

[^96]: 419.

Saha, S. & Bhattacharya, T. A Novel Approach to Find the Saturation Point of n-Gram Encoding Method for Protein Sequence Classification Involving Data Mining. in *International Conference on Innovative Computing and Communications* (eds. Bhattacharyya, S., Hassanien, A. E., Gupta, D., Khanna, A. & Pan, I.) 101–108 (Springer, 2019). doi:[10.1007/978-981-13-2354-6\_12](https://doi.org/10.1007/978-981-13-2354-6_12).

[^97]: 420.

Jeffrey, H. J. [Chaos game representation of gene structure](https://doi.org/10.1093/nar/18.8.2163). *Nucleic Acids Research* **18**, 2163–2170 (1990).

[^98]: 421.

Löchel, H. F. & Heider, D. [Chaos game representation and its applications in bioinformatics](https://doi.org/10.1016/j.csbj.2021.11.008). *Computational and Structural Biotechnology Journal* **19**, 6263–6271 (2021).

[^99]: 422.

Cartes, J. A., Anand, S., Ciccolella, S., Bonizzoni, P. & Vedova, G. D. Accurate and Fast Clade Assignment via Deep Learning and Frequency Chaos Game Representation. 2022.06.13.495912 (2022) doi:[10.1101/2022.06.13.495912](https://doi.org/10.1101/2022.06.13.495912).

[^100]: 423.

Ni, H., Mu, H. & Qi, D. [Applying frequency chaos game representation with perceptual image hashing to gene sequence phylogenetic analyses](https://doi.org/10.1016/j.jmgm.2021.107942). *Journal of Molecular Graphics and Modelling* **107**, 107942 (2021).