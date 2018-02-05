# SB-CH Corpus
----------------

## Introduction

The SpinningBytes Swiss German Corpus (SB-CH) is a corpus of Swiss German sentences along with Sentiment Annotations for those sentences.

It contains 165'916 sentences (of which ~70% are in Swiss German), of which 2799 are annotated with sentiment.

The sentiment annotations are done in 5 categories:

- UN: Sentences that don't make sense, are gibberish or aren't Swiss German
- UNSURE: Sentences with mixed or ambiguous sentiment
- NEUTRAL: Sentences which are neither positive nor negative
- NEGATIVE: Sentences with negative sentiment
- POSITIVE: sentences with positive sentiment


## Files

### non_facebook.csv

A CSV file containing sentences that didn't originate from Facebook and can be shared as is. 
The file consists of the following columns:

- `sentence_id`: the unique id of the sentence (int)
- `sentence_text`: the text of the sentence, in quotes (")


### facebook.csv

A CSV-File containing information about sentences in facebook posts. Since the content of Facebook posts cannot be shared freely,
this file contains information for recreating the sentences in the corpus.
To this end, the file contains the unique ID of each Facebook post, along with a sentence number. The sentence number (starting at 0) describes
which sentence the entry is for, when the comment is split with the `sent_tokenize` method in the `nltk.tokenize` namespace of
NLTK (Version 3.2.2).

Concretely, for a facebook comment body `facebook_comment` and a `sentence_number` of `1`, this would mean:

```python
from nltk.tokenize import sent_tokenize

comment_text = "this is the text of a facebook comment. You need to fetch this from facebook"
split_sentences = sent_tokenize(comment_text, language='german')
target_sentence = split_sentences[1] #"You need to fetch this from facebook"
```

The columns of the file are as follows:

- `comment_id`: the id of the facebook comment
- `status_id`: the id of the status this comment was posted on
- `parent_id`: the id of a parent post for this post, if it exists. `-1` if there is no parent.
- `sentence_number`: the consecutive sentence number when the comment is tokenized with the `sent_tokenize` method of NLTK, starting at 0.
- `sentence_id`: the unique id of the sentence

### sentiment.csv

A CSV-File containing the sentiment annotations for a subset of the sentences.

The columns are as follows:

- `sentence_id`: the unique id of the sentence
- `un`: the number of times this sentence was annotated with the `UN` label (Gibberish/Not Swiss-German)
- `unsure`: the number of times this sentence was annotated with the `UNSURE`label (Mixed/ambiguous sentiment)
- `neut`: the number of times this sentence was annotated with the `NEUTRAL`label (Neither positive nor negative sentiment)
- `neg`: the number of times this sentence was annotated with the `NEGATIVE`label (Negative sentiment)
- `pos`: the number of times this sentence was annotated with the `POSITIVE`label (Positive sentiment)


## Remarks

This corpus is provided as is. It was cleanup up as best effort, but due to the low-resourced nature of Swiss German, automated
cleanup of the corpus is difficult and there are still roughly 30% non-Swiss German sentences in the corpus.
The annotations were done by 5 different annotators.

## Contact

SpinningBytes AG can be contacted at info@spinningbytes.com