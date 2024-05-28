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

# ReSiPC


