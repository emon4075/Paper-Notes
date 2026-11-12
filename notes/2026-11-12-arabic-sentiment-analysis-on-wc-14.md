---
title: "Leveraging sentiment analysis of Arabic Tweets for the 2022 FIFA World Cup insights, incorporating the gulf region"
authors: "Wadih Ishac, Vajiheh Javani, Daoud Youssef"
venue: "Managing Sport and Leisure"
year: 2024
url: "https://doi.org/10.1080/23750472.2024.2342258"
area: "nlp"
depth: skim
date_read: "2026-11-12"
---

<!--
area:      ml | nlp | security
depth:     deep | skim
date_read: YYYY-MM-DD
Save as notes/YYYY-MM-DD-short-slug.md, then run: python scripts/update_index.py
-->

## What problem

<!-- The question the paper is actually trying to answer, in my own words. -->
How did public sentiment toward the 2022 FIFA World Cup change among Arabic-speaking Twitter users in the GCC region before, during, and after the tournament? *Which resulted in a increase of positive sentiment and decrease in the negative sentiment during the tournament.*

## Prior work and its gap

<!-- What people did before, and the specific thing it couldn't do. -->
There are several works on WC related public sentiment analysis including the 2002, 2014, 2018 and 2022 WCs. Most of the studies show that the public perception was mainly in favour due to its impact on tourism and multi cultural exchange. Most the studies were limited to English. However, there was a study in Arabic on 2018 WC where emoji changed the sentiment orientations. But, there was no specific work on 2022 WC especially in Arabic, though it was hosted in a Gulf country. So, the authors tried to focus on that and analysed sentiments of Arabic speaking peoples across different periods including before, during and after the event. 

## Method in 3 sentences

<!-- No more than three. If it takes more, I haven't understood it yet. -->
The authors then extracted the lexicon samples from the tweets and for each of the samples they were compared with the Arabic Lexicon Dictionary, if the sample is positive it gave +1, if negative it gave -1. Then they calculated the sum and if the sum > 0 then Positive, if sum < 0 then Negative and if sum = 0 then Neutral.

## Data and metrics

<!-- Datasets, splits, and what is being measured. -->
Data was collected via Twitter API and Twitter Academic Research Library (R Package) from GCC regions and some preprocessing steps were employed and which resulted in a data of 43658 tweets. But the data was not disclosed publicly. The authors measured the summation of scores given by the lexicon samples and decide the output. The authors then analyzed the frequency and proportion of each sentiment category across different periods and countries.

## Headline result

<!-- The one number worth remembering, with what it's compared against. -->
Negative tweets before the event took place were 11.11% compared to 8.68% during and 7.5% after the event. Conversely, positive tweets increased from 47.83% before the event to 55.25% after the event. Overall, the findings indicate a more positive sentiment toward the World Cup after the tournament.

## What I learned that I didn't know

<!-- The part that changed my mental model, not a summary of the abstract. -->
I learned the things that I listed [here](#Terms-I-had-to-look-up)


## What I'm unsure about

<!-- Claims I can't evaluate, experiments I'd want, things that smell off. -->
As the dataset is not publicly disclosed I can't look at the dataset for further verification. However, the dataset would have helped the community to reproduce the results.

## Terms I had to look up

<!-- Vocabulary, with short definitions, so the next paper is cheaper. -->
- **GCC** - Gulf Cooperation Council, which is a political and economic alliance of six Middle Eastern countries located along the Persian Gulf (Bahrain, Kuwait, Oman, Qatar, Saudi Arabia, UAE). They share nearly similar arabic dialect.
- **WordNet** - It is a very large and computer friendly lexical database by Princeton University. Which organizes words (Nouns, Verbs, Adjectives and Adverbs) into interconnected networks based on their actual meaning. Words with the similar meanings are grouped into sets called *synsets*.[^1]
- **SentiWordNet** - It builds upon WordNet (a large lexical database where English words are grouped into sets of synonyms called synsets) by automatically assigning every synset three numerical sentiment scores. For any given synset, the sum of all three scores equals 1.0 (Pos(s) + Neg(s) + Neu(s) = 1).[^2]
- **Lexicon (Cheat-Sheet)**
	- Good words: music, dancing, delicious, laughing (+1 point each)
	- Bad words: empty, loud, cold, boring (-1 point each)
- **Lexicon-Based Features (The Clues You Count)** - You read a guest's review of the party and count how many times words from your cheat-sheet show up. Those counts become the features (evidence) you use to judge the party.


## Future Scopes

<!-- Any future directions possible from the paper -->
+ Upon obtaining the dataset, we can create an annotated subset or version through inter annotator agreement.
+ After that we can apply some baseline models and compare their performace.
+ We can apply the same methodology in Bengali data considering events like WC26, SAFF etc.
+ Study and detection of Sarcastic tweets.
+ Cross platform sentiment analysis (e.g. YouTube, Reddit)
+ Topic based sentiment analysis (e.g. Team Peformance, Tourism, Infrustructure and Stadiums, Human Rights)
+ Emoji-aware sentiment Analysis

## References

[^1]: Miller, G. A. (1995). WordNet: A lexical database for English. *Communications of the ACM, 38*(11), 39–41. https://doi.org/10.1145/219717.219748

[^2]: Baccianella, S., Esuli, A., & Sebastiani, F. (2010). SentiWordNet 3.0: An enhanced lexical resource for sentiment analysis and opinion mining. *Proceedings of the Seventh International Conference on Language Resources and Evaluation (LREC'10)*. https://aclanthology.org/L10-1531/