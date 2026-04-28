---
title: "Chapter 7 Learning Alignments, an Interesting Perspective | From sequences to knowledge, improving and learning from sequence alignments"
source: "https://thesis.lucblassel.com/learning-alignments-an-interesting-perspective.html"
author:
  - "[[Luc Blassel]]"
published:
created: 2026-04-26
description: "Chapter 7 Learning Alignments, an Interesting Perspective | From sequences to knowledge, improving and learning from sequence alignments"
tags: []
---
## Chapter 7 Learning Alignments, an Interesting Perspective

Recently, machine learning methods have been increasingly applied to the process of alignment. Using this framework to “learn” an optimal sequence alignment algorithm might lead to better performance with less design biases.

## 7.1 Deep learning and sequences

As many of these techniques are based on deep learning, which I did not introduce in Chapter [4](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#learning-from-sequences-and-alignments), I will first present deep learning very shortly. I will then introduce the concept of learned sequence embeddings which could become very useful for machine sequence alignment.

### 7.1.1 Intro to deep learning

Deep learning is the process of learning using neural networks. Neural networks all started in 1958 when Rosenblatt proposed the *perceptron* [^6]. This learning algorithm was loosely inspired by biological neurons, which led to the name: *neural networks.* The perceptron takes as input n $n$ $n$ values, these are used in a weighted sum that is then fed through an *activation function.* The output of this function is the output of the perceptron. Originally, to replicate biological neurons, the activation function was a step function where, the perceptron has an output only if the weighted sum crosses a given threshold. This structure is often represented through a computational graph as in Figure [7.1](https://thesis.lucblassel.com/learning-alignments-an-interesting-perspective.html#fig:perceptron). By tuning the weights of the inputs, the perceptron can be used to solve linear separation problems.

 $**Computational graph of a perceptron.**  
Here, $n$ inputs $\{x_1,\ldots,x_n\}$ are passed into the perceptron where they are summed, weighted by $w_1,\ldots,w_n$. This sum is then fed through the perceptron's activation function $f$ (here a binary step function) which gives the output $y$ of the perceptron. Often the sum is implicitely considered part of the activation function, and will be represented as a single node in computational graphs.$

Figure 7.1: **Computational graph of a perceptron.**  
Here, n $n$ inputs {x1,…,xn} ${x1,…,xn}$ are passed into the perceptron where they are summed, weighted by w1,…,wn $w1,…,wn$. This sum is then fed through the perceptron’s activation function f $f$ (here a binary step function) which gives the output y $y$ of the perceptron. Often the sum is implicitely considered part of the activation function, and will be represented as a single node in computational graphs.

The perceptron could only be used on simple linear separation problems, but it was discovered that by linking several perceptrons together, mimicking a biological brain, more complex problems could also be solved. These structure, called *multilayer perceptrons* (MLP), are organized in layers where the outputs of perceptrons on a layer are used as inputs by perceptrons is the next layer (c.f. Figure [7.2](https://thesis.lucblassel.com/learning-alignments-an-interesting-perspective.html#fig:mlp)). The perceptrons, when in this form, are often called *neurons*, and the MLP a *neural network* (NN). These neural networks are organized in layers, with an input and output layer on either end, and hidden layers in the middle. With the large number of weights to tune, these models were very difficult to train and therefore not very practically useful.

 $**Computational graph of a multilayer perceptron.**  
This MLP, also called feedforward neural network, has $n$ inputs $\{x_1, \ldots, x_n\}$ represented as the input layer, 2 hidden layers of 3 neurons each and an output layer of 2 neurons (e.g. suitable for binary classification). It is fully connected meaning that each node of a given layer is used as input for every neuron of the following layer. Each edge in this graph corresponds to a weight which are the tunable parameters during the training process.$

Figure 7.2: **Computational graph of a multilayer perceptron.**  
This MLP, also called feedforward neural network, has n $n$ inputs {x1,…,xn} ${x1,…,xn}$ represented as the input layer, 2 hidden layers of 3 neurons each and an output layer of 2 neurons (e.g. suitable for binary classification). It is fully connected meaning that each node of a given layer is used as input for every neuron of the following layer. Each edge in this graph corresponds to a weight which are the tunable parameters during the training process.

There was a great resurgence of these models in the nineties due to the invention of *backpropagation* [^7]. By replacing the step functions of neurons with continuous, differentiable activation functions like sigmoids or hyperbolic tangents, a gradient of the output could be computed w.r.t each weight. This made gradient descent procedures possible for automatically learning the optimal weights from data as (c.f. Section [4.1.1](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#supervised-learning-from-biological-sequences)). With this method, neural networks could be efficiently trained on complex classification and regression problems [^8]. It was also proven that with hidden layers, neural networks are universal function approximators [^9], suitable for all types of tasks. One notable caveat for neural networks is, due to the large amount of weights to tune, that they require large amounts of training data, which also explains their low usage before the internet and accompanying data explosion.

In the following years, NNs saw an large increase in usage, with more complex architectures like convolutional neural networks (CNN) achieving state of the art results in computer vision tasks [^11]. By representing an input variable as a linear combination of its neighbors, some form of contextual information can be passed to the NN and improve performance. CNNs can also have good results in non computer-vision tasks like: drug resistance prediction [^3], protein subcellular localization [^4], or epidemiological model parameter estimation [^13].

More recently, as computational power and the amount of training data grew, larger and deeper (i.e. more hidden layers) architectures were able to be trained and achieved state of the art performance in many fields: image recognition with deep CNNs like `Alexnet` [^14] or `Resnet` [^15], translation with Recurrent NNs [^16] and Transformers [^17] (more on that in Section [7.1.2](https://thesis.lucblassel.com/learning-alignments-an-interesting-perspective.html#learned-sequence-embeddings)) or protein structure prediction with `Alphafold2` [^1].

### 7.1.2 Learned sequence embeddings

An area that in which deep learning has recently proved particularly useful, is the creation of relevant learned embeddings. These embeddings, similarly to the encodings discussed in Section [4.3](https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html#pre-processing-the-alignment-for-machine-learning), transform a sequence of categorical tokens in a numerical vector which can then be used in machine learning tasks. By learning these embeddings, the hope is that the resulting vector will retain the most important information in the sequence and some contextual information.

#### 7.1.2.1 xxx-2vec

Learned embeddings were mainly developed in the field of natural language processing (NLP), where machine learning algorithms use text, in languages such as English or French, as input. In this contexts, simple encodings like OHE are not very practical because of the very high dimensionality of a language. For example, the Merriam-Webster English dictionary contains 470,000 words [^18] so to encode a single word with OHE would result in a 470,000-dimensional sparse vector. Encoding a whole text or even a single sentence is wildly unpractical. Therefore, as a field, NLP needed to come up with ways of efficiently representing words in lower-dimensional vectors than naive encoding methods, while retaining semantic meaning.

One of the early methods for creating such embeddings is called `word2vec` [^19], proposed by researchers at Google, that learns a word-embedding on a particular text corpus. This method is designed to make embeddings that contain semantically relevant information. An example given in the article is that the vector corresponding to vec(Madrid)−vec(Spain)+vec(France) $vec(Madrid)−vec(Spain)+vec(France)$ $vec(Madrid) - vec(Spain) + vec(France)$ should be very similar to the vector vec(Paris) $vec(Paris)$ $vec(Paris)$, and that similar words should result in similar vectors.

The way this method works is by considering a word within its context, *i.e.* a window of length k $k$ $k$ centered around the word. In a corpus of words (*i.e.* our training data), each word is encoded as a One Hot Vector, which is possible since the corpus contains only a subset of the words in the English language. A neural network is then trained on one of two tasks [^21]:

- Continuous bag of words: where the word is predicted given the context of the word as input
- Skip-gram: where the context is predicted given the encoded word vector

After having sufficiently trained the neural network on the corpus on one of these tasks, one of the hidden layers of the network can be extracted and used as a vector representation of the input word, this results in an embedding method that is specific to a given corpus and the embedded vectors can be used in downstream learning tasks.

`word2vec` was very successful and widely used in the field of NLP, it is perhaps no surprise that the ideas behind it were adapted and reused in the field of bioinformatics. `dna2vec` [^22] uses similar ideas and was used to embed k $k$ $k$ -mers, and predict methylation sites on DNA sequences [^23]. Similar embedding methods like `seq2vec` [^24] as well as `bioVec` (including the protein specific `protVec`) [^25] were also developed to embed whole biological sequences. They were successfully used in biological sequence classification problems [^26].

#### 7.1.2.2 The attention revolution

While `word2vec` was widely used for many NLP tasks where word embeddings were needed, a lot of interesting developments on word embeddings were made in the field of automated machine translation. In this application, the desired embedding characteristics are slightly different. While semantic relevance is useful, in machine translation the embedding method needs to be able to capture dependencies, e.g. within a sentence where the link between the subject and the verb must be captured even though they are not necessarily next to each other. This was initially done by using recurrent neural networks, called RNNs or LSTMs, but they were hard to train and had trouble properly capturing long-range dependencies [^27].

One of the most successful methods developed for this task is the transformer [^17], also created by Google researchers. The main mechanisms of the transformer is the *self-attention* mechanisms: each input token, usually encoded as a One-Hot vector, is represented as a weighted sum of all the other tokens in a sequence *(here a token is a word and the sequence is a sentence)*. The weights of this sum are trained along with the rest of this network. By stacking several of these self-attention blocks, transformers can learn to represent and leverage long-range dependencies. These transformers are made of an encoder module that learns the token embedding, and a decoder module that makes predictions when fed embedded tokens sequentially. This mechanism, attention, and the transformer in general have had very successful applications in machine translation, while being easier to train than recurrent networks [^28].

This architecture was used to create very large pre-trained language models, that is to say models that perform word embedding. These models like `BERT` [^29] or `GPT-3` [^30] are huge, with millions or even billions of learned weights, and have been trained on huge quantities of data in order to produce word embeddings useful in a wide range of contexts. `BERT` was trained using Masked Language Modelling (MLM), where some percentage of the tokens *(words)* in an input sequence *(sentence)* are replaced by a special `[MASK]` token, and the model is trained to predict the whole sentence, effectively guessing what words are missing based on the context of the whole sequence. This process allows the model to learn relevant dependencies between tokens in the training data.

As was the case with `word2vec`, these methods have been adapted to bioinformatics tasks with state of the art results, proving the versatility of the transformer model. Several *protein language models* similar to `BERT` were trained on various training sets of protein data like `ProGen` [^31], `ProGen2` [^32] and `ProtBERT` [^5]. These large protein language models have been studied and interesting properties have been observed [^33]. Some specific characteristics of proteins can be inferred from these models without specifying them in the training step. For example, protein language models seem to learn some information about the protein structure and attention maps can be used to infer residue contact maps [^34]. Similarly these models capture some information about protein function [^36], mutational effects [^37], evolutionary characteristics [^38] and can even be used to generate new protein with desired properties [^31]. Some large language models have also been trained on DNA sequences like `DNABert` [^39] and also seem to capture some information without explicit specification during training, like variant effects [^40].

While, these protein language models have shown very useful for embedding single sequences, some developments have been made to embed multiple sequence alignments as learning inputs. In some cases this is done by including information on the alignment in the tokens and then using a regular language model to embed them [^41]. In the case of the MSA transformer [^42], the attention mechanism was extended to include a weighted sum between aligned sequences effectively taking the alignment into account when embedding sequences. An attention-like mechanism was also used to train a protein structure prediction model directly on MSAs [^43]. Similarly, by pre-training language models on profiles derived from MSAs, some information about the alignment can be included in the resulting embeddings [^44]. Finally aligned sequences can be used as inputs in a regular transformer as was done `DeepConsensus` [^45], a transformer-based polisher to decrease the error rate PacBio HiFi reads even further. Finally the *EvoFormer* model included in `AlphaFold2` [^1], which embeds MSAs to predict protein structure, is partly responsible for the leap in performance between the two generations of the `AlphaFold` model, and the current protein structure prediction revolution [^46].

It is important to note that while these transformer models are very powerful and useful in practice, their complexity and size makes them very hard to study and understand what they actually learn. There is work to peek inside this “black box”, notably by interpreting the learned attention maps [^47] and decipher biologically relevant information contained within.

## 7.2 Learning sequence alignment

With the success of deep learning methods in learning informative and effective embeddings from sequences, it is maybe natural to try and see if similar methods can learn how to align sequences to each other.

### 7.2.1 Predicting a substitution matrix

One approach is to learn a *position-specific scoring matrix* (PSSM), which assigns an alignment cost not between two amino-acids but between two specific residues of the sequences (i.e. an amino acid/position pair). Therefore, when aligning a sequence of length m $m$ $m$ and another of length n $n$ $n$, we can use a standard alignment method such as NW or SW with an m×n $m×n$ $m\times n$ PSSM.

One approach, used in the `SAdLSA` model [^48] used CNNs to refine an input PSSM. The model is trained on experimentally validated structural alignments. A starting PSSM is created from both sequences with `PSI-BLAST` [^2], and fed through a deep CNN, which outputs a refined PSSM. This learned matrix is used with a SW algorithm to locally align the two sequences. This alignment is then compared to the structural alignment to compute a loss and train the model.

Some methods rely on protein language model embeddings coupled with differentiable alignment algorithms to learn a PSSM in an end-to-end fashion. `DeepBLAST` is one such model [^49]. It was trained on 1.5 million structural alignments obtained from the PDB database [^50]. The sequences are embedded using a pre-trained LSTM-based protein language model. These embeddings are fed through LSTM networks to predict a match scoring and gap scoring PSSMs. These matrices are then used in a differentiable variant of the NW algorithm, that can be used to backpropagate the alignment error through the network and learn relevant parameters. RNNs and LSTMs were also used to predict PSSMs by Guo *et al.* albeit with the goal of protein structure prediction rather than alignment [^51].

The `DEDAL` model [^52] implements similar ideas. It predicts matching, gap-open and gap-extend PSSMs from a pair of sequences, that can be used in a classical alignment method, in this case a SW algorithm. In this model, a transformer-based embedding network is used to embed each residue of both sequences. Then each possible pair of embedded residues from both sequences is used to predict specific gap-open, gap-extend and match scores used to build the PSSMs. The `DEDAL` model is trained on three tasks at once:

1. Masked language modelling (c.f. Section [7.1.2.2](https://thesis.lucblassel.com/learning-alignments-an-interesting-perspective.html#the-attention-revolution)) to train the transformer-based embedding model on 30 million sequences from the UniRef50 database [^53].
2. A homology detection task where the whole model is trained to predict if a pair of sequences are evolutionarily related or not. This was done on pairs of sequences extracted from the 1.2 million sequences of the Pfam-A seed database [^54].
3. An alignment task, where the whole model is trained to align two sequences using the authors’ differentiable variant of the SW algorithm to backpropagate the alignment error through the network and tune the parameters. This training task was also done using aligned sequence pairs from the Pfam-A seed database.

Trained on the three tasks at once, the `DEDAL` model predicts PSSMs leading to good alignments overall. However, where it really shines and outperforms other methods is on alignments of remote homologs. Classical alignment algorithms can struggle when the similarity between two sequences dips below a certain threshold, `DEDAL` is able to pick up on this remote homology and produce a sensible and accurate alignment.

The learned alignment module [^55] also uses a differentiable variant of the SW algorithm to learn a scoring matrix. Sequences are encoded as OHE vectors and fed embedded with simple convolutions, to predict a “context-specific” scoring matrix. This module is used to build MSAs where, similarly to the center star alignment, all *target* sequences are aligned to a single *query* sequence. This model was validated by including it in the `Alphafold2` model and seeing the improvement in performance for certain protein structure prediction tasks.

### 7.2.2 Predicting an alignment

Predicting a PSSM is one way of learning to align. However, an alignment algorithm still needs to be used in order to obtain aligned sequences. It might be possible to directly output an alignment between input sequences. As stated above, transformers have been particularly useful in automated translation, and one could construe the alignment problem as translating from an unaligned sequence “language” to an aligned sequence “language”. This is exactly the idea behind `BetaAlign`, a recently developed transformer model used for pairwise and multiple sequence alignment [^56]. For example, the two sequences `AAG` and `ACGG` can be represented as a single “sentence”: `AAG|ACGG` with the `|` special token denoting a separation between sequences. Aligned sequences output by the transformer can then be represented as a succession of aligned pairs: `AAAC-GGG` corresponding to the following alignment:

**`AA-G`**  
**`ACGG`**

The authors trained this model on millions of simulated alignments, of two to ten sequences, generated with different underlying evolutionary models, in the same fashion that regular transformers are trained for machine translation. The authors trained models for protein and DNA sequence alignment on these simulated datasets, containing sequences around 40 residues long. According to some measures, `BetaAlign` outperforms widely used multiple sequence aligners such as `MUSCLE`, `CLUSTALW` or `T-Coffee`, especially on nucleotide sequence alignment. This model was also trained to deal with longer sequences, generating MSAs of 5 sequences between 500 and 1000 residues long. In this setting `BetaAlign` performs on par with most widely used aligners.

While `BetaAlign` is an interesting step in the direction of learned alignment methods, and a good proof of concept, it seems to be efficient only on a low number of short sequences. This is mostly due to the attention mechanism at the heart of transformers.

### 7.2.3 The attention limitation

While the transformer architecture has revolutionized the field of machine translation, and proved to be useful in sequence-related bioinformatics tasks, the attention mechanism at its heart presents some problems. The main problem is that by including a weighted sum of all input tokens in the embedding of a specific token, the time and space complexity of the attention mechanism is quadratic in sequence length. This is particularly problematic in biological tasks where DNA and protein sequences can be much longer than a typical sentence, in any spoken language. This limitation is mentioned in the articles for both the `DEDAL` and `BetaAlign` models described above.

This problem is not inherent to biology and many different approaches to counter it have been proposed in other fields where transformer usage is prevalent. The *Linformer* [^57] and *Nyströmformer* [^58] architectures both present different approximations of the attention mechanism that scale linearly w.r.t. sequence length both in time and memory. Others yet have tried to make the attention process produce sparse matrices, reducing the memory requirements [^59]. Others have tried adjusting the attention span, i.e. the number of tokens taken into account in the attention mechanism, with an adaptive attention span [^61] or long-short range attention [^62]. Finally, with some change the operations in the attention mechanism, the *Reformer* model reduces the memory requirements to a linear complexity by replacing a dot product operation [^63].

Some improvements to the attention mechanism have also been tried in a biological context. Choromanski *et al.* propose the *Performer* model that uses a fast attention mechanism [^64], based on orthogonal random features and trained on an protein MLM task. With this approach, the attention mechanism scales linearly with the sequence length rather than quadratically. Another team used factored attention in their model trained on protein structure prediction [^65]. They show that with this mechanism, fewer parameters need to be tuned, lowering the memory and time requirements, while retaining structurally relevant information.

### 7.2.4 Predicting read-mappings

In the read-mapping setting, the methods described above are of limited use. This is due to some intrinsic characteristics of read-mapping: mainly the size discrepancy between reads and the reference sequence, as well as the length of the reference sequence. Some work has been done however on including machine learning methods into the read-mapping process.

One first approach is to learn data structures, called *learned indices*, used to store potential seeds in the seed and extend framework. These learned indices are trained to replicate the output of a particular data structure. This approach was first proposed in 2018 [^66], although it was not implemented then. The `BWA-MEME` [^67] read-mapper uses a learned index that predicts positions in a suffix array. This approach is also the one used by the `Sapling` algorithm [^68]. Learned indices have also been used to predict a position in an FM-index [^69]. These learned indices lower the memory cost and execution time costs by eliminating the need to build the whole data structure and only storing a reduced amount of information. Furthermore it is well adapted to read-mapping since it only needs to be trained once on a specific reference sequence that can be used anytime reads need to be mapped to this reference.

Another approach where machine learning has proven useful is in learning a seed selection scheme. `DeepMinimizer` [^70] is one such method, where neural networks are trained to select appropriate minimizers from a DNA sequence. This approach results in minimizers (c.f. Section [2.2.2.1.2](https://thesis.lucblassel.com/aligning-sequence-data.html#other-algorithms)) with optimal density, that is to say they are spread out evenly over the whole sequence lowering the memory and time costs of building a seed index. Similarly, although not a direct application of read mapping, deep learning has been used to predict candidate alignment sites in mRNA-miRNA pairs, a similar task to seed selection [^71].

Finally, the pre-processing function framework of MSRs presented in Chapter [3](https://thesis.lucblassel.com/HPC-paper.html#HPC-paper) could also be extended with machine learning methods. Learning connections in the graphs representing MSRs could allow the exploration of the large function spaces of higher-order MSRs. Alternatively some sequence-to-sequence models like transformers could also be used to learn a pre-processing function. To learn an appropriate pre-processing function in an end-to-end fashion, a differentiable read-mapping algorithm is needed. Differentiable versions of the NW and SW could be used in read-mappers, but differentiable seeding and seed-selection processes are also needed.

## 7.3 Conclusion

Deep learning is a powerful framework for sequence-based tasks. The recent transformer architecture has shown an unprecedented ability to capture within-sequence dependencies and learn relevant information. This ability has made them dominant in the NLP field, particularly machine translation. Transformers and large language models have shown some power in biological sequence processing and sequence alignment. However, the attention mechanism that makes these models so successful has limitations, especially w.r.t. input sequence length. Some approaches and approximations, have been proposed to lower the time and memory complexity of the attention mechanism, but these improvements have yet to be implemented in a sequence alignment task. In the special case of read-mapping, even with improved attention mechanisms, the size discrepancy between reference and reads, as well as the often very large scale of the reference sequence, make transformer based embedding approaches impractical. Learned data structures and seeding schemes might be one of the approaches to improve read alignment.

### References

[^1]: 137.

Jumper, J. *et al.* [Highly accurate protein structure prediction with AlphaFold](https://doi.org/10.1038/s41586-021-03819-2). *Nature* **596**, 583–589 (2021).

[^2]: 200.

Altschul, S. F. *et al.* [Gapped BLAST and PSI-BLAST: A new generation of protein database search programs](https://doi.org/10.1093/nar/25.17.3389). *Nucleic Acids Research* **25**, 3389–3402 (1997).

[^3]: 331.

Steiner, M. C., Gibson, K. M. & Crandall, K. A. [Drug Resistance Prediction Using Deep Learning Techniques on HIV-1 Sequence Data](https://doi.org/10.3390/v12050560). *Viruses* **12**, 560 (2020).

[^4]: 352.

Wei, L., Ding, Y., Su, R., Tang, J. & Zou, Q. [Prediction of human protein subcellular localization using deep learning](https://doi.org/10.1016/j.jpdc.2017.08.009). *Journal of Parallel and Distributed Computing* **117**, 212–217 (2018).

[^5]: 373.

Elnaggar, A. *et al.* [ProtTrans: Towards Cracking the Language of Life’s Code Through Self-Supervised Deep Learning and High Performance Computing](https://doi.org/10.48550/arXiv.2007.06225). *IEEE Transactions on Pattern Analysis and Machine Intelligence* vol. Pp 1–1 (2021).

[^6]: 675.

Rosenblatt, F. [The perceptron: A probabilistic model for information storage and organization in the brain](https://doi.org/10.1037/h0042519). *Psychological Review* **65**, 386–408 (1958).

[^7]: 676.

Rumelhart, D. E., Hinton, G. E. & Williams, R. J. [Learning representations by back-propagating errors](https://doi.org/10.1038/323533a0). *Nature* **323**, 533–536 (1986).

[^8]: 677.

Murtagh, F. [Multilayer perceptrons for classification and regression](https://doi.org/10.1016/0925-2312\(91\)90023-5). *Neurocomputing* **2**, 183–197 (1991).

[^9]: 678.

Cybenko, G. [Approximation by superpositions of a sigmoidal function](https://doi.org/10.1007/bf02551274). *Math. Control Signal Systems* **2**, 303–314 (1989).

[^10]: 680.

Hornik, K. [Approximation capabilities of multilayer feedforward networks](https://doi.org/10.1016/0893-6080\(91\)90009-t). *Neural Networks* **4**, 251–257 (1991).

[^11]: 681.

LeCun, Y. *et al.* [Backpropagation Applied to Handwritten Zip Code Recognition](https://doi.org/10.1162/neco.1989.1.4.541). *Neural Computation* **1**, 541–551 (1989).

[^12]: 682.

Lecun, Y., Bottou, L., Bengio, Y. & Haffner, P. [Gradient-based learning applied to document recognition](https://doi.org/10.1109/5.726791). *Proceedings of the IEEE* **86**, 2278–2324 (1998).

[^13]: 

[^14]: 684.

Krizhevsky, A., Sutskever, I. & Hinton, G. E. [ImageNet classification with deep convolutional neural networks](https://doi.org/10.1145/3065386). *Commun. ACM* **60**, 84–90 (2017).

[^15]: 685.

He, K., Zhang, X., Ren, S. & Sun, J. [Deep Residual Learning for Image Recognition](https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html). in *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)* 770–778 (2016).

[^16]: 686.

Bahdanau, D., Cho, K. & Bengio, Y. Neural Machine Translation by Jointly Learning to Align and Translate. (2016) doi:[10.48550/arXiv.1409.0473](https://doi.org/10.48550/arXiv.1409.0473).

[^17]: 687.

Vaswani, A. *et al.* [Attention is All you Need](https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html). in *Advances in Neural Information Processing Systems* vol. 30 (Curran Associates, Inc., 2017).

[^18]: 688.

How many words are there in English? | Merriam-Webster. [https://www.merriam-webster.com/help/faq-how-many-english-words](https://www.merriam-webster.com/help/faq-how-many-english-words).

[^19]: 689.

Mikolov, T., Chen, K., Corrado, G. & Dean, J. Efficient Estimation of Word Representations in Vector Space. (2013) doi:[10.48550/arXiv.1301.3781](https://doi.org/10.48550/arXiv.1301.3781).

[^20]: 690.

Mikolov, T., Sutskever, I., Chen, K., Corrado, G. S. & Dean, J. [Distributed Representations of Words and Phrases and their Compositionality](https://proceedings.neurips.cc/paper/2013/hash/9aa42b31882ec039965f3c4923ce901b-Abstract.html). in *Advances in Neural Information Processing Systems* vol. 26 (Curran Associates, Inc., 2013).

[^21]: 691.

Goldberg, Y. & Levy, O. Word2vec Explained: Deriving Mikolov et al.’s negative-sampling word-embedding method. (2014) doi:[10.48550/arXiv.1402.3722](https://doi.org/10.48550/arXiv.1402.3722).

[^22]: 692.

Ng, P. Dna2vec: Consistent vector representations of variable-length k-mers. (2017) doi:[10.48550/arXiv.1701.06279](https://doi.org/10.48550/arXiv.1701.06279).

[^23]: 693.

Liang, Y. *et al.* [Hyb4mC: A hybrid DNA2vec-based model for DNA N4-methylcytosine sites prediction](https://doi.org/10.1186/s12859-022-04789-6). *BMC Bioinformatics* **23**, 258 (2022).

[^24]: 694.

Kimothi, D., Soni, A., Biyani, P. & Hogan, J. M. Distributed Representations for Biological Sequence Analysis. (2016) doi:[10.48550/arXiv.1608.05949](https://doi.org/10.48550/arXiv.1608.05949).

[^25]: 695.

Asgari, E. & Mofrad, M. R. K. [Continuous Distributed Representation of Biological Sequences for Deep Proteomics and Genomics](https://doi.org/10.1371/journal.pone.0141287). *PLoS One* **10**, e0141287 (2015).

[^26]: 696.

Kimothi, D., Shukla, A., Biyani, P., Anand, S. & Hogan, J. M. Metric learning on biological sequence embeddings. in *2017 IEEE 18th International Workshop on Signal Processing Advances in Wireless Communications (SPAWC)* 1–5 (2017). doi:[10.1109/spawc.2017.8227769](https://doi.org/10.1109/spawc.2017.8227769).

[^27]: 697.

Song, B. *et al.* [Pretraining model for biological sequence data.](https://doi.org/10.1093/bfgp/elab025) *Briefings in Functional Genomics* **20**, 181–195 (2021).

[^28]: 698.

Wang, H., Wu, H., He, Z., Huang, L. & Ward Church, K. Progress in Machine Translation. *Engineering* (2021) doi:[10.1016/j.eng.2021.03.023](https://doi.org/10.1016/j.eng.2021.03.023).

[^29]: 699.

Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *Naacl* (2019) doi:[10.48550/arXiv.1810.04805](https://doi.org/10.48550/arXiv.1810.04805).

[^30]: 700.

Brown, T. *et al.* [Language Models are Few-Shot Learners](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html). in *Advances in Neural Information Processing Systems* vol. 33 1877–1901 (Curran Associates, Inc., 2020).

[^31]: 701.

Madani, A. *et al.* ProGen: Language Modeling for Protein Generation. *bioRxiv* (2020) doi:[10.1101/2020.03.07.982272](https://doi.org/10.1101/2020.03.07.982272).

[^32]: 702.

Erik Nijkamp, Jeffrey A. Ruffolo, Eli N. Weinstein, Nikhil Naik & Ali Madani. ProGen2: Exploring the Boundaries of Protein Language Models. *ArXiv* (2022) doi:[10.48550/arxiv.2206.13517](https://doi.org/10.48550/arxiv.2206.13517).

[^33]: 703.

Bepler, T. & Berger, B. [Learning the protein language: Evolution, structure, and function.](https://doi.org/10.1016/j.cels.2021.05.017) *Cell Systems* **12**, 654–669.e3 (2021).

[^34]: 704.

Rao, R., Meier, J., Sercu, T., Ovchinnikov, S. & Rives, A. Transformer protein language models are unsupervised structure learners. 2020.12.15.422761 (2020) doi:[10.1101/2020.12.15.422761](https://doi.org/10.1101/2020.12.15.422761).

[^35]: 706.

Bhattacharya, N. *et al.* Single Layers of Attention Suffice to Predict Protein Contacts. 2020.12.21.423882 (2020) doi:[10.1101/2020.12.21.423882](https://doi.org/10.1101/2020.12.21.423882).

[^36]: 707.

Hu, M. *et al.* Exploring evolution-based & -free protein language models as protein function predictors. (2022) doi:[10.48550/arXiv.2206.06583](https://doi.org/10.48550/arXiv.2206.06583).

[^37]: 708.

Meier, J. *et al.* [Language models enable zero-shot prediction of the effects of mutations on protein function](https://doi.org/10.1101/2021.07.09.450648). *bioRxiv* **34**, 29287–29303 (2021).

[^38]: 709.

Hie, B., Kevin K Yang & Kim, S. K. [Evolutionary velocity with protein language models predicts evolutionary dynamics of diverse proteins](https://doi.org/10.1016/j.cels.2022.01.003). *Cell Systems* **13**, 274–285.e6 (2022).

[^39]: 710.

Ji, Y., Zhou, Z., Liu, H. & Davuluri, R. V. [DNABERT: Pre-trained Bidirectional Encoder Representations from Transformers model for DNA-language in genome](https://doi.org/10.1093/bioinformatics/btab083). *Bioinformatics* **37**, 2112–2120 (2021).

[^40]: 711.

Benegas, G., Batra, S. S. & Song, Y. S. DNA language models are powerful zero-shot predictors of non-coding variant effects. 2022.08.22.504706 (2022) doi:[10.1101/2022.08.22.504706](https://doi.org/10.1101/2022.08.22.504706).

[^41]: 712.

Cai, T. *et al.* Genome-wide Prediction of Small Molecule Binding to Remote Orphan Proteins Using Distilled Sequence Alignment Embedding. 2020.08.04.236729 (2020) doi:[10.1101/2020.08.04.236729](https://doi.org/10.1101/2020.08.04.236729).

[^42]: 713.

Rao, R. *et al.* MSA Transformer. *bioRxiv* (2021) doi:[10.1101/2021.02.12.430858](https://doi.org/10.1101/2021.02.12.430858).

[^43]: 714.

Sercu, T. *et al.* Neural Potts Model. 2021.04.08.439084 (2021) doi:[10.1101/2021.04.08.439084](https://doi.org/10.1101/2021.04.08.439084).

[^44]: 

[^45]: 716.

Baid, G. *et al.* DeepConsensus improves the accuracy of sequences with a gap-aware sequence transformer. *Nat Biotechnol* 1–7 (2022) doi:[10.1038/s41587-022-01435-7](https://doi.org/10.1038/s41587-022-01435-7).

[^46]: 717.

Ourmazd, A., Moffat, K. & Lattman, E. E. [Structural biology is solved — now what?](https://doi.org/10.1038/s41592-021-01357-3) *Nat Methods* **19**, 24–26 (2022).

[^47]: 718.

Vig, J. *et al.* BERTology Meets Biology: Interpreting Attention in Protein Language Models. (2021) doi:[10.48550/arXiv.2006.15222](https://doi.org/10.48550/arXiv.2006.15222).

[^48]: 719.

Gao, M. & Skolnick, J. [A novel sequence alignment algorithm based on deep learning of the protein folding code](https://doi.org/10.1093/bioinformatics/btaa810). *Bioinformatics* **37**, 490–496 (2021).

[^49]: 720.

Morton, J. T. *et al.* Protein Structural Alignments From Sequence. 2020.11.03.365932 (2020) doi:[10.1101/2020.11.03.365932](https://doi.org/10.1101/2020.11.03.365932).

[^50]: 721.

Berman, H., Henrick, K., Nakamura, H. & Markley, J. L. [The worldwide Protein Data Bank (wwPDB): Ensuring a single, uniform archive of PDB data](https://doi.org/10.1093/nar/gkl971). *Nucleic Acids Research* **35**, D301–d303 (2007).

[^51]: 722.

Guo, Y., Wu, J., Ma, H., Wang, S. & Huang, J. [Comprehensive Study on Enhancing Low-Quality Position-Specific Scoring Matrix with Deep Learning for Accurate Protein Structure Property Prediction: Using Bagging Multiple Sequence Alignment Learning](https://doi.org/10.1089/cmb.2020.0416). *Journal of Computational Biology* **28**, 346–361 (2021).

[^52]: 723.

Llinares-López, F., Berthet, Q., Blondel, M., Teboul, O. & Vert, J.-P. Deep embedding and alignment of protein sequences. 2021.11.15.468653 (2022) doi:[10.1101/2021.11.15.468653](https://doi.org/10.1101/2021.11.15.468653).

[^53]: 724.

Suzek, B. E. *et al.* [UniRef clusters: A comprehensive and scalable alternative for improving sequence similarity searches](https://doi.org/10.1093/bioinformatics/btu739). *Bioinformatics* **31**, 926–932 (2015).

[^54]: 725.

Mistry, J. *et al.* [Pfam: The protein families database in 2021](https://doi.org/10.1093/nar/gkaa913). *Nucleic Acids Research* **49**, D412–d419 (2021).

[^55]: 726.

Petti, S. *et al.* End-to-end learning of multiple sequence alignments with differentiable Smith-Waterman. 2021.10.23.465204 (2022) doi:[10.1101/2021.10.23.465204](https://doi.org/10.1101/2021.10.23.465204).

[^56]: 727.

Dotan, E. *et al.* Harnessing machine translation methods for sequence alignment. 2022.07.22.501063 (2022) doi:[10.1101/2022.07.22.501063](https://doi.org/10.1101/2022.07.22.501063).

[^57]: 728.

Wang, S., Li, B. Z., Khabsa, M., Fang, H. & Ma, H. Linformer: Self-Attention with Linear Complexity. (2020) doi:[10.48550/arXiv.2006.04768](https://doi.org/10.48550/arXiv.2006.04768).

[^58]: 729.

Xiong, Y. *et al.* [Nyströmformer: A Nyström-based Algorithm for Approximating Self-Attention](https://doi.org/10.1609/aaai.v35i16.17664). *Proceedings of the AAAI Conference on Artificial Intelligence* **35**, 14138–14148 (2021).

[^59]: 730.

Child, R., Gray, S., Radford, A. & Sutskever, I. Generating Long Sequences with Sparse Transformers. (2019) doi:[10.48550/arXiv.1904.10509](https://doi.org/10.48550/arXiv.1904.10509).

[^60]: 731.

Correia, G. M., Niculae, V. & Martins, A. F. T. Adaptively Sparse Transformers. in *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)* 2174–2184 (Association for Computational Linguistics, 2019). doi:[10.18653/v1/D19-1223](https://doi.org/10.18653/v1/D19-1223).

[^61]: 732.

Sukhbaatar, S., Grave, E., Bojanowski, P. & Joulin, A. Adaptive Attention Span in Transformers. (2019) doi:[10.48550/arXiv.1905.07799](https://doi.org/10.48550/arXiv.1905.07799).

[^62]: 733.

Wu, Z., Liu, Z., Lin, J., Lin, Y. & Han, S. Lite Transformer with Long-Short Range Attention. (2020) doi:[10.48550/arXiv.2004.11886](https://doi.org/10.48550/arXiv.2004.11886).

[^63]: 734.

Kitaev, N., Kaiser, Ł. & Levskaya, A. Reformer: The Efficient Transformer. (2020) doi:[10.48550/arXiv.2001.04451](https://doi.org/10.48550/arXiv.2001.04451).

[^64]: 735.

Choromanski, K. *et al.* Masked Language Modeling for Proteins via Linearly Scalable Long-Context Transformers. (2020) doi:[10.48550/arXiv.2006.03555](https://doi.org/10.48550/arXiv.2006.03555).

[^65]: 736.

Bhattacharya, N. *et al.* Interpreting Potts and Transformer Protein Models Through the Lens of Simplified Attention. in *Biocomputing 2022* 34–45 (World Scientific, 2021). doi:[10.1142/9789811250477\_0004](https://doi.org/10.1142/9789811250477_0004).

[^66]: 737.

Kraska, T., Beutel, A., Chi, E. H., Dean, J. & Polyzotis, N. The Case for Learned Index Structures. in *Proceedings of the 2018 International Conference on Management of Data* 489–504 (Association for Computing Machinery, 2018). doi:[10.1145/3183713.3196909](https://doi.org/10.1145/3183713.3196909).

[^67]: 738.

Jung, Y. & Han, D. [BWA-MEME: BWA-MEM emulated with a machine learning approach](https://doi.org/10.1093/bioinformatics/btac137). *Bioinformatics* **38**, 2404–2413 (2022).

[^68]: 739.

Kirsche, M., Das, A. & Schatz, M. C. [Sapling: Accelerating suffix array queries with learned data models](https://doi.org/10.1093/bioinformatics/btaa911). *Bioinformatics* **37**, 744–749 (2021).

[^69]: 740.

Ho, D. *et al.* LISA: Learned Indexes for Sequence Analysis. 2020.12.22.423964 (2021) doi:[10.1101/2020.12.22.423964](https://doi.org/10.1101/2020.12.22.423964).

[^70]: 741.

Hoang, M., Zheng, H. & Kingsford, C. Differentiable Learning of Sequence-Specific Minimizer Schemes with DeepMinimizer. *Journal of Computational Biology* (2022) doi:[10.1089/cmb.2022.0275](https://doi.org/10.1089/cmb.2022.0275).

[^71]: 742.

Min, S., Lee, B. & Yoon, S. [TargetNet: Functional microRNA target prediction with deep neural networks](https://doi.org/10.1093/bioinformatics/btab733). *Bioinformatics* **38**, 671–677 (2022).