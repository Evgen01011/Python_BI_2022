# Homework 5. pandas

## Describing
Script realises some  data analysis in biological area

## Preparation
For convenient utilizing this script I advise user to create virtual environment.

First of all, you should create virtual environment in acceptable directory (*pandas_venv* is a name for example).
```
python3 -m venv pandas_venv
```
Also you need activate this venv
```
source numpy_venv/bin/activate
```
The second step is the installation of the necessary module. This can be done in the following way:
Through copy requiremets.txt from this repository (branch homework_5)
```
git clone https://github.com/Evgen01011/Python_BI_2022/tree/homework_4
pip install -r ../Python_BI_2022/hw_5/requiremets.txt
```

## Features
The script contain next separate stages:  
### First task
First step present 2 functions:
- `read_gff` - the function accepts .gff file and convert them to pandas.DataFrame
    ```
    read_gff(input_gff)
    ```
- `read_bed6` - the function accepts .bed file and convert them to pandas.DataFrame
    ```
    read_bed6(input_bed)
    ```

After that *attribute* column contained rRNA type in rrna_annotation.gff (you can find it in Files directory) turn into convenient format - 16S, 23S, 5S

The analysis of representations of every rRNA type per chronmosomes shows in plot (rRNA_barplot.png)

The analysis of the rRNA amount collected during the assembly process was carried out at the next step. In general, this is an analogue of bedtools intersect.
 The table contains the original records of the rna completely included in the assembly (not a fragment), as well as a record of the content in which this RNA got (Table1.csv)
 
### Second task
The data of differential gene expression was visualised via volcano plot (Volcano_plot.png) 

On the X-axis: Logarithmic Fold Change

On the Y axis: negative decimal logarithm p-value (adjusted for multiple comparison)

Data from diffexpr_data.tsv.gz

The arrows show the 2 most significantly increased and decreased gene expression

### Third task

The data of cancer incidence spreading on different organs the last year was visualised via pie chart (Pie_plot.png) 

The diagram demonctates percent of particular cancer type

Data from Worldwide Cancer Dataset.csv (from Kaggle)




