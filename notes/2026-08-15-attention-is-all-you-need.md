---
title: "Attention Is All You Need"
authors: "Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin"
venue: "NeurIPS"
year: 2017
url: "https://arxiv.org/abs/1706.03762"
area: nlp
depth: deep
date_read: 2026-08-15
---

## What problem

Sequence transduction models were built on recurrence, which forces computation
to proceed one position at a time: step *t* can't start until step *t-1* finishes.
That serialization caps training throughput on long sequences and makes long-range
dependencies expensive to learn. The paper asks whether the recurrence is load-bearing
at all, or whether attention — until then a component bolted onto an RNN — can carry
the whole model.

## Prior work and its gap

Encoder-decoder RNNs with attention (Bahdanau, Luong) were the strong baselines:
attention fixed the fixed-length-bottleneck problem, but the sequential backbone
remained, so nothing could be parallelized across positions within an example.
Convolutional alternatives (ByteNet, ConvS2S) did parallelize, but the number of
operations needed to relate two positions grows with the distance between them —
linearly for ConvS2S, logarithmically for ByteNet — so learning distant dependencies
stays harder the further apart they are. The gap: an architecture where relating any
two positions is a constant number of operations *and* the whole layer is parallel.

## Method in 3 sentences

Drop recurrence and convolution entirely; build the encoder and decoder as stacks of
6 identical layers, each a multi-head self-attention sublayer followed by a
position-wise feed-forward network, with residual connections and layer normalization
around both. Attention is scaled dot-product, `softmax(QKᵀ/√d_k)V`, computed in 8
parallel heads of dimension 64 so different heads can attend to different relations,
concatenated back to `d_model = 512`. Because the model has no notion of order, inject
sinusoidal positional encodings into the input embeddings, and mask the decoder's
self-attention so position *i* can only attend to positions ≤ *i*.

## Data and metrics

WMT 2014 English→German (~4.5M sentence pairs, 37k shared byte-pair-encoding
vocabulary) and WMT 2014 English→French (36M pairs, 32k word-piece vocabulary),
scored by BLEU on newstest2014, with training cost reported in FLOPs alongside it.
A secondary experiment on English constituency parsing (WSJ Penn Treebank, ~40k
sentences, plus a semi-supervised setting) tests whether the architecture generalizes
past translation. Ablations vary head count, key dimension, model size, dropout, and
swap learned positional embeddings for sinusoidal ones.

## Headline result

28.4 BLEU on EN→DE — over 2 BLEU past the previous best, including ensembles — and
41.8 BLEU on EN→FR, a new single-model state of the art, trained in 3.5 days on eight
P100 GPUs at a fraction of the training cost of the models it beat. The base model
already reached 27.3 EN→DE in 12 hours. The parsing experiment gets 91.3 F1 on WSJ
Section 23 with no task-specific tuning.

## What I learned that I didn't know

The `1/√d_k` scaling isn't cosmetic. For large `d_k` the dot products grow with
variance proportional to `d_k`, pushing softmax into regions where its gradient is
vanishingly small — the scaling is what keeps the thing trainable at width, and it's
the reason additive attention had been competitive at small dimensions in the first place.

I also hadn't registered that the *headline* argument is a complexity-table argument,
not an accuracy argument. Self-attention relates any two positions in O(1) sequential
operations versus O(n) for recurrence, at O(n²·d) work per layer versus O(n·d²). For
the sentence lengths in these datasets n < d, so self-attention is cheaper *and*
shorter-path. That inequality is the load-bearing assumption, and it flips for long
documents — which retroactively explains the entire efficient-attention literature.

Smaller thing: the decoder's masking is the only thing making generation autoregressive.
The architecture itself is order-agnostic; causality is a mask, not a structure.

## What I'm unsure about

Whether the reported gains come from the architecture or from the training recipe that
travels with it — warmup-then-inverse-sqrt learning rate, label smoothing at 0.1,
checkpoint averaging. The ablations vary the architecture, not the recipe, so I can't
separate them from this paper alone.

I also can't tell how much the multi-head story is real mechanism versus post-hoc reading
of the attention visualizations in the appendix. "Different heads learn different
relations" is asserted from a handful of hand-picked heads; the ablation only shows
that too few or too many heads is worse.

## Terms I had to look up

- **Byte-pair encoding (BPE)** — subword vocabulary built by iteratively merging the
  most frequent adjacent symbol pair; keeps rare words representable without an
  unbounded vocabulary.
- **Label smoothing** — replacing the one-hot target with `1-ε` on the true class and
  `ε` spread over the rest; hurts perplexity, helps BLEU and accuracy by discouraging
  overconfidence.
- **Position-wise feed-forward network** — the same two-layer MLP applied independently
  at every position; equivalently two convolutions of kernel size 1.
- **Constituency parsing / F1 on WSJ 23** — recovering the phrase-structure tree of a
  sentence; Section 23 of the Penn Treebank is the standard held-out test set.
