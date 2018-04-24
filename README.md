gpseqc v2.0.1.dev
===

A Python3 package that provides tools to estimate the 3D spatial nuclear centrality of genomic regions and compare different centrality rankings.

* Read the (public) [documentation](https://ggirelli.github.io/gpseqc/) for more details.
* Read the (private) [documentation](https://github.com/ggirelli/gpseqc/wiki) for more details.  
*Once the repo goes public, private docs will be merged with public ones.*

Installation
---

To **install**, run the following:

```
git clone http://github.com/ggirelli/gpseqc
cd gpseqc
sudo -H pip3 install .
```

To **uninstall** run the following from within the repository folder:

```
sudo -H pip3 uninstall gpseqc
```

To **update**, first uninstall, and then run the following from within the repository folder.

```
git pull
sudo -H pip3 install .
```

Usage
---

#### Estimate centrality

The `gpseqc_estimate` script allows to estimate regional nuclear centrality based on a multi-condition GPSeq experiment. Run `gpseqc_estimate -h` for more details.

#### Compare centrality ranks

<s>The `gpseqc_compare` script allows to compare different regional centrality ranks. Run `gpseqc_estimate -h` for more details.</s>

**NOTE: the `gpseqc_compare` script is not available yet. Please, use the old `gpseqc_compare_legacy` script instead (more info with `-h`).**

Contributing
---

We welcome any contributions to `GPSeqC`. Please, refer to the [contribution guidelines](https://ggirelli.github.io/gpseqc/contributing) if this is your first time contributing! Also, check out our [code of conduct](https://ggirelli.github.io/gpseqc/code_of_conduct).

License
---

```
MIT License
Copyright (c) 2017-18 Gabriele Girelli
```