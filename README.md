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

### chatmania.csv

A CSV file containing sentences originating from chatmania. 
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
target_sentence = split_sentences[1]
```

The columns of the file are as follows:

- `comment_id`: the id of the facebook comment
- `status_id`: the id of the status this comment was posted on
- `parent_id`: the id of a parent post for this post, if it exists. `-1` if there is no parent.
- `sentence_number`: the consecutive sentence number when the comment is tokenized with the `sent_tokenize` method of NLTK, starting at 0.
- `md5_hash`: the md5-hash of the sentence to verify a correct download
- `sentence_id`: the unique id of the sentence

#### Fetching Facebook comments

A sample script to fetch the facebook sentences is provided in `get_fb_comments.py` .

Note that the following fields need to be set at the top of the file:

- `app_id`: the Facebook application id
- `app_secret: the Facebook application secret
- `file_id`: the path to the source file (facebook.csv)
- `result_file`: the path to the result file


Alternatively, you can also set `access_token` in the file directly to an access token.

The script was written for python 3.6

The script can be executed as:

```bash
$ python get_fb_comments.py
Scraping facebook.csv Comments: 2018-02-05 14:45:45.636237
[...]
Done!
56945 Comments Processed in 648221.15
```

Facebook apps can be created according to [this guide](https://developers.facebook.com/docs/apps/register).

This script is based on [Facebook Page Post Scraper](https://github.com/minimaxir/facebook-page-post-scraper)

### noah.csv

A CSV file mapping NOAH corpus Sentences to SB-CH sentiment annotations.

The columns of the file are as follows:

- `document_id`: the name of the source xml file of the sentence the NOAH corpus
- `article_id`: the id of the &lt;article&gt; tag of the sentence
- `s_id`: the id of the &lt;s&gt; tag of the sentence
- `md5_hash`: the md5 hash of the sentence
- `sentence_id`: the SB-CH sentence id 


### sms4science.csv

A CSV file mapping sms4science corpus Sentences to SB-CH sentiment annotations.

The columns of the file are as follows:

- `sms_id`: the the sms4science sms id
- `sentence_number`: the number of the sentence when the SMS is split with sent_tokenize()
- `md5_hash`: the md5 hash of the sentence
- `sentence_id`: the SB-CH sentence id 

### sentiment.csv

A CSV-File containing the sentiment annotations for a subset of the sentences.

The columns are as follows:

- `sentence_id`: the unique id of the sentence
- `un`: the number of times this sentence was annotated with the `UN` label (Gibberish/Not Swiss-German)
- `unsure`: the number of times this sentence was annotated with the `UNSURE`label (Mixed/ambiguous sentiment)
- `neut`: the number of times this sentence was annotated with the `NEUTRAL`label (Neither positive nor negative sentiment)
- `neg`: the number of times this sentence was annotated with the `NEGATIVE`label (Negative sentiment)
- `pos`: the number of times this sentence was annotated with the `POSITIVE`label (Positive sentiment)

## Licence

See [our homepage](https://www.spinningbytes.com/resources/swissgermansentiment) for Licence information

## Remarks

This corpus is provided as is. It was cleaned up as best effort, but due to the low-resourced nature of Swiss German, automated
cleanup of the corpus is difficult and there are still roughly 30% non-Swiss German sentences in the corpus.
The annotations were done by 5 different annotators.

## Acknowledgements

The sentiment annotated text contained elements from the following two corpora. They are referenced by ID – in order to obtain the full text, please directly access the original corpora.

- Stark, Elisabeth; Ueberwasser, Simone; Ruef, Beni (2009-2015). Swiss SMS Corpus. University of Zurich. [www.sms4science.ch](www.sms4science.ch)
- Nora Hollenstein and Noëmi Aepli. "Compilation of a Swiss German Dialect Corpus and its Application to PoS Tagging." COLING 2014 (2014): 85 [http://kitt.cl.uzh.ch/kitt/noah/corpus](http://kitt.cl.uzh.ch/kitt/noah/corpus)

We thank the creators of the SMS4Science and NOAH corpora for their work.

## Contact

[SpinningBytes AG](https://www.spinningbytes.com/resources/swissgermansentiment) can be contacted at info@spinningbytes.com
