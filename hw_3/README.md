#### Homework 3. Moduls ane virtual environment
WSL Wsman Shell commandLine version 0.2.1 (installed Ubuntu 20.04.4 LTS) was utilized for running [ultraviolence.py](https://github.com/krglkvrmn/Virtual_environment_research/blob/master/ultraviolence.py) 

**Preparation**

Script uses pre-release version of Python3.11, so previously you need install it. Instruction for installing you can find [there](https://bytexd.com/how-to-install-python-on-ubuntu/)

Please note that conda hasn't contained Python3.11 yet, so for creation Virtual environment (further venv) should use virtualenv. To install virtualenv via pip:
```
pip install virtualenv
```
Also you need recognise directory of Python3.11:
```
which python3.11
```
In my case it's:
```
/usr/bin/python3.11
```
**Creation Virtual environment**

A. Determine directory of future venv
B. Create venv
```
virtualenv --python="/path/to/python3.11" name_venv
```
For example:
```
virtualenv --python="/usr/bin/python3.11" venv
```
C. Activate venv
```
source venv/bin/activate
```
Due to improve installation you may install python3.11-dev and upgrade pip inside venv
```
$ sudo apt install -y python3.11-dev
$ pip install --upgrade pip
```
N.B. To check Python version is python3.11:
```
python --version
```
**Install packages**

You should install next packages inside venv:
```
$ pip install google
$ pip install google-cloud
$ pip install google-cloud-vision
$ pip install Biopython
$ pip install aiohttp  
$ pip install pandas==1.4.4
$ pip install opencv-python
$ pip install lxml
```
Or you may use *requirements.txt* in relevant directory:
```
pip install -r requirements.txt
```
And check attendance these packages in *site-packages* (you see another moduls - it's important for executing function these one):
```
ls /path/to/venv/lib/python3.11/site-packages
ls ~/Bioinf/Practise_Python/hw3/venv/lib/python3.11/site-packages (mine)
```
If you need you may again save dependencies (suddenly):
```
pip freeze > requirements.txt
```
**Run ultraviolence**

Inside venv run ultraviolence.py
```
python /path/to/script/ultraviolence.py
```
Finally, you can deactivate venv and write to Mikhail that he doesn't do it anymore
