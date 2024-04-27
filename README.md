
This code serves for converting IPA transcription to scansion, i.e. transcription of word stress over a sentence. Can be used to create datasets with poetic meters, poetic feets etc. To train AI for and poetry and the rhythm of the language.

## Example
| input        | detailed output | simplified output|
| ------------- | ------------- | ----- |
|ˈstara ˈmʲiwɔɕʨ̑ ˌɲɛ‿rʣ̑ɛˈvʲjɛ̇jɛ | Ss Ss S‿sSs | SsSsSsSs

`S` is an accented syllable and `s` is an unaccented syllable.

You can look at the output and infer that this sentence is indeed a [trochaic tetrameter](https://en.wikipedia.org/wiki/Trochaic_tetrameter)

## How to adapt it?

This has been made for Polish, but can be adopted to work with other languages as well. One caveat is that it doesn't support dyphthongs (so for example English /eɪ/ in the word *mate* would be treated as two syllables). If your language doesn't have dyphthongs, just update the list of vowels and it should work (maybe you could even just paste all IPA vowels?). Also beware for vowels that are only vowels because of combined diacritics, like English /ɫ̩/ in *bottle*. It wouldn't work because the script analyses the input character after character, without caring about combinations. One crucial thing is that your IPA transcription also has to have the information on stress, incoded with the following characters:

|  |  |  |
| ------------- | ------------- | ----- |
| ˈ	|	0x2c8	| MODIFIER LETTER VERTICAL LINE |
| ˌ	|	0x2cc |	MODIFIER LETTER LOW VERTICAL LINE |

This a standard thing in IPA. `ˈ` is used for primary stress and `ˌ` is used for secondary stress.

## How does it work?

The script takes an input string and reads it character after character, from left to right.
The reading cursor's default state is `˩`. When it finds a `ˈ` or a `ˌ`, it changes its state to `˥`. Whenever it finds a vowel, it does one of the two things depending on its state:
1. If its state is `˥`, it writes an `S` and switches back to `˩`
2. If its state is `˩`, it writes and `s`.
It also rewrites spaces ` ` and `‿` characters. And it rewrites `∅` which is what I added in preprocessing as a substitution of Polish words that are not syllabic (*w* and *z*).

## The sample dataset

The sample comes from my dataset which I created by running this script on a Wiktionary dump of the Polish language as registered in the Polish version of Wiktionary. The dataset is split into proverbs and non-proverbs. Proverbs are useful because they are sentences. I have 890 proverbs and 43301 non-proverbs. A fraction of the non-proverbs are multi-word idioms like *wsadzać nos w nie swoje sprawy* (*to stick one's nose into other people's business*).

**If you are interested in the full dataset, please don't hesitate to contact me**
