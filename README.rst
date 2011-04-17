=====
Sulci
=====

Sulci is a French text mining tool, initially designed for the analysis of
the corpus and thesaurus of `Libération <http://www.liberation.fr/>`_, a 
french newspaper.

This code is "work in progress"; it's not used (nor usable) in production yet.

Therefore, here is a demo page with the freezed 0.1 alpha version:
 
 http://alpha.sulci.dotcloud.com

Sulci provides 4 algorithms, designed to be run in sequence: each algorithm
needs the data provided by the previous one :

#. Part of Speech tagging
#. Lemmatization
#. Collocation and key entities extraction
#. Semantical tagging

Each algorithm must be *trained* to be operational. Therefore, a trained set of 
data is provided (see fixtures/). This is the result of a training with the
Libération corpus.

Therefore, if you want a textmining most accurate to your own texts, you must
should train it.

What does "training" mean?

#. You first need to prepare a corpus, for each of the algorithm. A corpus is a 
   set of texts with the final output you want : for example, the corpus for the 
   PosTagger is some texts where each word is pos tagged, with a verified value.
#. You then have to launch the training with the command line.
#. Each algorithm has it's own trainer. This trainer will take the input texts, 
   remove the verified output, and begin to find the best rules to determine the
   right ouput. The trainer will analyze its mistakes, and change its processing
   rules/weights/triggers/... in order to avoid making those mistakes again in 
   the future. The trainer will loop over the corpus untill it concider that no 
   more rules could be infered.

.. note::
   You can also use the algorithm to help you create the corpus : give a text to
   the algorithm, and correct the output.

.. warning: each algorithm needs the previous algorithm to work, so remember
   to train the algorithms in the order they are called.

.. note::
   The trained datas provided with the Sulci alpha version has been made with a
   corpus of :
   #. 15500 POS tagged words
   #. 2000 words in lexicon (lexicon must be smaller than POS corpus)
   #. FIXME: 2000 lemmatized words
   #. 28000 semantical tagged words
   #. 17000 descriptors in thesaurus

Before running the first algorithm, the text is split into tokens
(words, symbols, punctuation marks, etc.), using simple regular expressions.


Part-of-speech tagging
----------------------

The PosTagger finds out the "POS tag", or "lexical class", or "lexical 
category" of each word. 
The algorithm used is similar to the `Brill POS-tagging algorithm
<http://en.wikipedia.org/wiki/Brill_tagger>`_.

Some possible classes are:

* VCJ:sg (Verbe ConJugé singulier),
* PAR:pl (PARticipe pluriel),
* PREP (PREPosition),
* etc.

To see more available classes, see in base.py the methods named is_<something> or
run the following command (it provides the tag stats in corpus)::

 python manage.py sulci_cli -g

The format used is a plain text file; tokens are separated by spaces;
each token is annotated with its POS tag, separated with a slash. Example::

  Mon/DTN:sg cher/ADJ:sg Fred/SBP:sg ,/, Je/PRV:sg quitte/VCJ:sg 
  Paris/SBP:sg demain/ADV matin/SBC:sg ./. 

This format combines "input" and "output": the input is the token, the output
is the POS tag.

Check "corpus/*.crp" to see more examples of "valid output".


Lemmatization
-------------

The Lemmatizer tries to find the *Lemma* of each word. The lemma of a word
is almost similar to its stem. A few examples:

* "mangerons" lemma is "manger" (infinitive form of the verb)
* "bonnes" lemma is "bon" (masculine singular form of the adjective)
* "filles" lemma is "fille" (singular form of the noun)

The format used is similar to the one of the PosTagger, but each token
is annotated by both its POS tag and its lemma. Example::

  «/« Ce/PRV:sg/ce n'/ADV/ne est/ECJ:sg/être pas/ADV à/PREP moi/PRO:sg 
  de/PREP partir/VNCFF ./. Je/PRV:sg/je me/PRV:sg battrai/VCJ:sg/battre 
  jusqu'/PREP/jusque au/DTC:sg bout/SBC:sg ./. »/» 

If a word and its lemma are identical, the lemma is omitted. Note that
this is case-sensitive (as you can see on the first word of the above
excerpt).

Check "corpus/*.lem.lxc.crp" to see more examples of "valid output".

Semantical tagging
------------------

The SemanticalTagger tries to find "collocations" -- i.e., sequence of tokens
that have a higher chance of appearing together -- and key entities -- i.e. words
the may help to find the significance of the text : proper nouns, for example, or
ones with many occurrences in the text, etc.
A few examples:

* Président de la République
* voiture électrique
* Barack Obama

The SemanticalTagger will actually use two different algorithms:

* a purely statistical algorithm, scoring n-grams according to their
  relatives frequences in the corpus.
* an heuristics-based algorithm, scoring n-grams (sequences of words) with
  hand-crafted rules;

The statistical algorithm uses `Pointwise mutual information 
<http://en.wikipedia.org/wiki/Pointwise_mutual_information>`_.

The first one is mainly used do determine weither or not a séquence of words is 
a collocation ; the second one, to determine weither or not a word or a collocation
is representative of the text.


Semantical training
-------------------

*  each text of the semantical corpus is processed by the previous algorithm, to
find the key entities (triggers)
* each of the triggers found are linked with a weight to the descriptors to the
text processed
* finally, the more a trigger was linked to a descriptors, the more this trigger
will trigger the descriptors in the tagging process.


After the training phase...
---------------------------

Once all algorithms have been trained to a satisfactory level, they are 
ready to analyze new texts without your guidance (i.e., you won't have
to pre-tag those texts, indeed).

Steps 1 to 4 are run in sequence, and trigger to descriptors relations are used
to extract the must pertinent descriptors.


Installation
------------

You have to unzip the SQL fixtures (52Mo) and load them in DB.
After that, "python setup.py install" or put the sulci folder in your 
PYTHONPATH::

 $ export PYTHONPATH=$PYTHONPATH:`pwd`

Add "sulci" to your INSTALLED_APPS.

If you plan to train you own Sulci or to use the command line,
you have to add these settings (with you own values, of course)::

 SULCI_CLI_CONTENT_MANAGER_METHOD_NAME = 'objects'
 SULCI_CLI_CONTENT_APP_NAME = 'libe'
 SULCI_CLI_CONTENT_MODEL_NAME = 'article'
 SULCI_CLI_KEYWORDS_PROPERTY = 'keywords'
 SULCI_CLI_CONTENT_PROPERTY = "content"

Sample usage::

  >> from sulci.textmining import SemanticalTagger
  >> my_text = u"Voici mon magnifique texte en français qui parle de Charlie Chaplin en Europe."
  >> S = SemanticalTagger(my_text)
  >> S.descriptors()
  ((Charlie Chaplin, 87.8984),
  (Europe, 78.4387))

Generic roadmap for the beta version
------------------------------------

* More categorized texts for the POS tagger corpus (15000 words now, I'd like to
have almost 30000)

* Find a way to build unittests for every algorithm

* Refine the key entities extraction

* Make a documentation (Sphinx)

* Find a way to remove useless relations in triggertodescriptors

* Clean thesaurus

* Be able to train the algorithm for one new descriptor

* Generic python optimisation

* Generic algorithm optimisation

Feel free to contribute any help!

How can I help?
---------------

* You're a python killer: there is many optimisations to do in the actual code

* You're a language expert: all the algorithm can be optimized

* You know well french language: you can add texts in the POS corpus, or make a 
proof read of the actual texts (in corpus/*.crp)

* You're an enthousiast: you can play with the demo, with the debug, and make
tickets for the bug seen ; you can help for making the doc, etc.