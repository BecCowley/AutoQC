AutoQC
======

##Introduction

Recent studies suggest that changes to global climate as have been seen at the Earth's land and ocean surface are also making their way into the deep ocean, which is the largest active storage system for heat and carbon available on the timescale of a human lifetime. Historical measurements of subsurface ocean temperature are essential to the scientific research investigating the changes in the amount of heat stored in the ocean and also to other climate research activities such as combining observations with numerical models to provide estimates of the global ocean's and Earth's climate state  in the past and predictions for the future. Unfortunately, as with all observations, these measurements contain errors and biases that must be identified to prevent a negative impact on the applications and investigations that rely on them. Various groups from around the world have developed quality control tests to perform this important task. However, this has led to duplication of effort, code that is not easily available to other researchers and the introduction of climate model differences solely due to the varying performance of these software systems whose nuances relative to one another are poorly known.

Recently, an international team of researchers has decided to work together to break down the barriers between the various groups and countries through the formation of the IQuOD (International Quality Controlled Dataset) initiative. One of the key aims is to intercompare the performance of the various automatic quality control tests that are presently being run to determine a best performing set. This work has started. However, it currently involves individuals running test datasets through their own systems and is being confounded by complications associated with the differences in the file formats and systems that are in use in the various labs and countries.

The IQuOD proposal is to set up an open quality control benchmarking system.  Work will begin by using python's `unittest` module to implement a battery of simple tests to run on some test data, and producing summary statistics and visualizations of the results.  Later goals include helping researchers either wrap their existing C, Fortran and Matlab test functions in Python for use in this test suite, or re-implementing those tests in native Python.

##Setup
AutoQC relies on [ddt](https://github.com/txels/ddt) (v0.8.0) to run over datasets:
`sudo pip install ddt`

To execute the test suite,
`python demo.py`

To execute the real quality control checks,
`python AutoQC.py`


##Notes
 - `ddt` is patched here to not append data serializations to the ends of test names.
