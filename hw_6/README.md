# Homework 6. regex

## Describing
Script realises some regular expression search tool

## Preparation
For convenient utilizing this script I advise user to create virtual environment.

First of all, you should create virtual environment in acceptable directory (*pandas_venv* is a name for example).
```
python3 -m venv regex_venv
```
Also you need activate this venv
```
source regex_venv/bin/activate
```
The second step is the installation of the necessary module. This can be done in the following way:
Through copy requiremets.txt from this repository (branch homework_6)
```
git clone https://github.com/Evgen01011/Python_BI_2022/tree/homework_6
pip install -r ../Python_BI_2022/hw_6/requirements.txt
```

## Features
The script contain next separate stages:  
### First task
Parsing of the `references file` (access by link https://raw.githubusercontent.com/Serfentum/bf_course/master/15.re/references) using regular expressions and write all ftp links from there to the `ftps file`:
The result presents in Files/only_ftp.txt

### Second task
Extraction of all the numbers from the story 2430 A.D. (presents in File directory)

### Third task
Extraction of all the words that have the letter a in them from the story 2430 A.D.

### Fourth task
Extraction of all exclamatory sentences from the story 2430 A.D.

### Fifth task
The search of unique words and creation a histogram of the distribution of the their lengths from the story 2430 A.D.
Graph containes:
- X axis - word length 
- Y axis - their fractions


The graph presents in File directory

### Sixth task
Creation of translator function from Russian and English to "brick language" (a -> aka)

- `def brick_language_russian` - the function accepts Russian string and convert them to brick string
    ```
    def brick_language_russian(string)
    ```
- `def brick_language` - the function accepts English string and convert them to brick string
    ```
   def brick_language(string)
    ```
> Examples:
> квантификаторы -> квакантикификикакатокорыкы
> example -> ekexakampleke

### Seventh task
The function for extracting sentences with a given number of words from the text

- `find_n_words_sentences` - the function accepts string and the desired number of contained words convert. Function seaches and outputs suitable.
    ```
    def find_n_words_sentences(text, words_amount)
    ```



