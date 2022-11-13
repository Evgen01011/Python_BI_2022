# Homework 5. COVID-19 analysis

## Describing
Script realises some data analysis of first stage of COVID-19 pandemic

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
The EDA contains next step:  

### First
The first graph (Covid_Heatmap.png) demonstrates amount of new cases of disease in different country. According these data, we can observe different dynamics of spreading.
I have assumption that annotation of new cases in first period associates with development of test system rather than real spreading. 

So I try to investigate amount of new test a day in the nearest country with different dynamics and similar level of development- USA and Canada.

### Second
The second graph (New_test_violinplot.png) demonstrate that these countries actually have dramatically gap in amount of test a day. 
In this case, it may serve as a proof of my hypothesis, but I need check correlation between new cases and new tests a day.

### Third
The third graph (Dependances.png) shows that dependencies between these values aren't constant (only in range of one fifth of maximum) so my assumtion is needed to additional check. 
