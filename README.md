# ReSiPC
ReSiPC: a tool for complex searches in parallel corpora

The first version of the too (v.0.1) is described in the paper:

Antoni Oliver and Bojana Mikelenić. 2020. [ReSiPC: a Tool for Complex Searches in Parallel Corpora](https://aclanthology.org/2020.lrec-1.869/). In Proceedings of the Twelfth Language Resources and Evaluation Conference, pages 7033–7037, Marseille, France. European Language Resources Association.

The current version offers:

* A program to tag parallel corpora: paraTagger.py
* A program to perform searches in tagged parallel corpora: ReSiPC.py

Both programs are offered in two versions: terminal and GUI.

Furthermore, Windows executable versions for the GUI versions of the programs are available from:

* paraTaggerGUI.exe: [http://lpg.uoc.edu/ReSiPC/paraTaggerGUI.exe](http://lpg.uoc.edu/ReSiPC/paraTaggerGUI.exe)
* ReSiPCGUI.exe: [http://lpg.uoc.edu/ReSiPC/ReSiPCGUI.exe](http://lpg.uoc.edu/ReSiPC/ReSiPCGUI.exe)

# Requirements

Don't forget to install the requirements from the file requirements.txt

# paraTagger.py

This programs can perform tagging in a parallel corpus using [Stanza](https://stanfordnlp.github.io/stanza/). Before using this program you should make sure that a POS Tagger for Stanza is available for your language. You can check whether your language has an available model [here](https://stanfordnlp.github.io/stanza/performance.html). When running the paraTagger first time for a given language, it will automatically download the required models.

The program paraTagger.py has the option -h that shows the help of the program:

```
python3 paraTagger.py -h
usage: paraTagger.py [-h] -i PARACORPUSFILE -o TAGGEDCORPUSFILE --l1 L1 --l2 L2

ReSiPC tagger for parallel corpora.

options:
  -h, --help            show this help message and exit
  -i PARACORPUSFILE, --in PARACORPUSFILE
                        The input file containing the parallel corpus in tabbed text format.
  -o TAGGEDCORPUSFILE, --out TAGGEDCORPUSFILE
                        The output file to store the tagged corpus.
  --l1 L1               The 2 letter ISO code for language 1 (en, es, fr, ....).
  --l2 L2               The 2 letter ISO code for language 2 (en, es, fr, ....) or None if no tagger is available.
  ```

To run ReSiPC at least the source language should be tagged, as the searches will be performed on the source language. The input file should be a parallel corpus in tabbed format. For example, if we have an English-Spanish corpus (corpus-eng-spa.txt) and we want to get the tagged corpus (corpus-tagged-eng-spa.txt) we can write:

`python3 paraTagger.py -i corpus-eng-spa.txt -o corpus-tagged-eng-spa.txt --l1 en --l2 es`

The output file will be a tabbed corpus with the following structure: text_L1 tab tagged_L1 tab text_L2 tab tagged_L2. If you're not interested in tagging the target language or Stanza is not available for that language you can write:

`python3 paraTagger.py -i corpus-eng-spa.txt -o corpus-tagged-eng-spa.txt --l1 en --l2 None`

The output file will be a tabbed corpus with the following structure: text_L1 tab tagged_L1 tab text_L2 tab text_L2.

For convenience, you can use the GUI version providing a very easy-to-use graphical user interface.

# ReSiPC.py

This programs search for POS patterns in a parallel corpus tagged as described in the previous section. To run the program you have to create a file containing the patterns to search for. Each tagged token has the form:

`word_form | lemma | POSTag`

The pattern formalism allows to search for combinations of tagged tokens using regular expressions. It is very important to keep in mind that the patterns will depend on the tagset used by the POS Tagger, and these tagsets are language dependent.

For example, the pattern 

`||V.* ||SP.* ||N.*`

would select all the segments whose Spanish version contains a verb followed by a preposition followed by a noun. As we can see from the example, standard regular expressions can be used in the patterns, making this formalism very powerful.

Exact word forms or lemmata can also be specified in the patterns, as in 

`|incitar| |a| ||VMN.*`

where the pattern will select all the segments that in Spanish have the verb *incitar* (in any form, as it is specified as a lemma, to incite), followed by an *a* and followed by a verb in the infinitive form.

The formalism also allows specifying a series of undefined elements between two defined elements. The expression

`|proporcionar| *{0,5} |a|`

would select any form of the verb *proporcionar* (to provide) followed by an a allowing from 0 to 5 undefined tokens between them. This expression would detect, for example, the following cases: *..proporciono a..., ...propociono ayuda a..., ...proporcionó mucha ayuda a..., ...proporcionó una gran ayuda a. . . , ...proporcionó una ayuda muy valiosa a. . . , proporciono una ayuda realmente muy valiosa a....*

The text file may contain any number of patterns, with one pattern in each line.

The program ReSiPC.py has the option -h that shows the help:

```
python3 ReSiPC.py -h
usage: ReSiPC.py [-h] -i PARACORPUSFILE -o OUTFILE -p PATTERNSFILE [-m] [-c] [-s SOURCECOLUMN] [-t TAGGEDCOLUMN]
                 [-n NOMATCHESFILE]

ReSiPC: a tool for searching POS patterns in tagged parallel corpora.

options:
  -h, --help            show this help message and exit
  -i PARACORPUSFILE, --in PARACORPUSFILE
                        The input file containing the parallel corpus in tabbed text format.
  -o OUTFILE, --out OUTFILE
                        The output Excel file.
  -p PATTERNSFILE, --patterns PATTERNSFILE
                        The text file containing the patterns.
  -m, --marksource      Mark in bold the matches in source text (result is tokenized).
  -c, --ignorecase      Ignore case in matching regular expressions.
  -s SOURCECOLUMN, --source SOURCECOLUMN
                        The column storing the source text (0 is first). Default 0.
  -t TAGGEDCOLUMN, --tagged TAGGEDCOLUMN
                        The column storing the tagged (0 is first). Default 1
  -n NOMATCHESFILE, --nomatches NOMATCHESFILE
                        A tsv file to store the lines not matching any pattern.
```

So if we have the tagged corpus corpus-tagged-eng-spa.txt and a pattern file patterns.txt that contain the pattern, as for example:

`||VBG to|to|TO ||VB`

(note that the tags used here are the corresponding to English)

We can write:

`python3 ReSiPC.py -i corpus-tagged-eng-spa.txt -o results.xlsx -p patterns.txt`

In the Excel file results.xlsx we will get all the segments matching the pattern.

For convenience, you can also use the GUI version providing a very easy-to-use graphical user interface.




