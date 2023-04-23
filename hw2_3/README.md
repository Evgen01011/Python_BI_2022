#### Homework 3. Internet
### Describing
The script includes 3 tasks in the area of Internet requests and API.

### Preparation
For convenient utilizing this script I advise user to create virtual environment.

First of all, you should create virtual environment in acceptable directory (*internet_venv* is a name for example).
```
python3 -m venv internet_venv
```
Also you need activate this venv
```
source internet_venv/bin/activate
```

The second step is the installation of the modules. This can be done in the following way:
```
git clone https://github.com/Evgen01011/Python_BI_2022/homework_3_Internet
pip install -r ../Python_BI_2022/hw2_3/requirements.txt
```

### Features
The script includes 3 tasks

**Tasks**

- `IMDb films`: parse IMDb site
- `Telegram bot`: creation of decoration function for Telegram bot 
- `genscan_module`: API analog for request on GENSCAN site (http://hollywood.mit.edu/GENSCAN.html)

`genscan_module` present function for creation requests on GENSCAN site

    :param sequence: input sequence
    :param sequence_file: input file containing sequence
    :param organism: options for type intron cleavage
    :param exon_cutoff: searching suboptimal options
    :param sequence_name: name of request
    :return: information about requests in GenscanOutput format
