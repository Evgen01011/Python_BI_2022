#### Homework 2. Functions and files
Script realises filtering function `main`, task of which filters FASTQ file.

**Features**
Function `main` allows to sort FASTQ file accourding to  
- GC-content of reads - the `gc_bounds` argument
- reads length - the `length_bounds` argument
- reading quality - the `quality_threshold` argument

**Describing**
```sh
main(input_fastq, output_file_prefix, gc_bounds=(20, 80),
     length_bounds=(0, 2 ** 32), quality_threshold=0, save_filtered=False)
```
Argumets:
1. `input_fastq` - the directory of input FASTQ file
(ex.: '/users/jones/bioinf/test.fastq')
2. `output_file_prefix` - the prefix for output FASTQ file(s) 
(ex.: '/users/jones/bioinf/gfp')
3. `gc_bounds` - the range of GC-content for sorting. If read GC-content is in specified range, it will collect. Also user can notice only high threshold. Bonders include.
(by default gc_bounds=(20, 80))
4. `length_bounds` - the range of length for sorting. If read length is in specified range, it will collect. Also user can notice only high threshold. Bonders include.
(by default length_bounds=(0, 2 ** 32))
5. `quality_threshold` - the low thresholdrange of quality for sorting. If read reaches or exceeds this value, it will collect. Bonder includes.
(by default quality_threshold=0)
6. `save_filtered` - the cursur of saving unsatisfactory passed reads. 
By default save_filtered=False - passed reads don't save. If save_filtered=True - passed reads will be saved

**Result**
As a result user gets output FASTQ file(s). 
Argument `output_file_prefix` serve as the cursor of output files transmitted by the user. 
- successful passed reads save as 
*output_file_prefix__passed.fastq*
(for previous example:/users/jones/bioinf/gfp__passed.fastq) 
- unsatisfactory passed reads save as 
*output_file_prefix__filtered.fastq*
(for previous example:/users/jones/bioinf/gfp__filtered.fastq) 

> However filtered reads will be saved only if 
> argument `save_filtered`=True (by default = False)

