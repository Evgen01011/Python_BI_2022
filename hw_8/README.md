## Homework 8. UNIX command

### Describing
Script realises some programs imitating UNIX utilities. 

### Preparation
WSL Wsman Shell commandLine version 0.2.1 (installed Ubuntu 20.04.4 LTS) was utilized for running command.

For convenient utilizing this script I advise user to create virtual environment.

First of all, you should create virtual environment in acceptable directory (*unix* is a name for example).
```
python3 -m venv unix_venv
```
Also you need activate this venv
```
source unix_venv/bin/activate
```
The second step is the installation of modules. You may do it such way.

Copy requiremets.txt from this repository (branch homework_8)
```
git clone https://github.com/Evgen01011/Python_BI_2022/homework_8
pip install -r ../Python_BI_2022/hw_8/requirements.txt
```

For execution you chould change the access permissions of every utilities
```
chmod +x utilite.py
```

After that if you use WSL and utilise Vim, you should enter the following command:
```
:set fileformat=unix
```

Execution of every command happens next way:
```
./utilite.py
```


### Features
The script contain next programs:  
- `wc.py` - wc analog. It is used to find out number of lines, word count and byte in the files specified in the file arguments.
    ```
    ./wc.py [OPTION]... [FILE]...
    ```
> Flags: 
> -l: count line
> -w: count words
> -c: count bytes

- `ls.py` - ls analog. It is used to list the names of all the objects that are present in directories.
    ```
    ./ls.py [OPTION]... [DIRECTORY]...
    ```
> Flag: 
> -a: show hidden objects

- `sort.py` - sort analog. It is used to sort a file, arranging the records in a particular order.
    ```
    ./sort.py [FILE]...
    ```
 
 - `rm.py` - rm analog. It is used to remove objects such as files and directories.
    ```
    ./rm.py [OPTION]... [FILE / DIRECTORY]...
    ```
> Flag: 
> -r: remove directories and contained files

 - `mkdir.py` - mkdir analog. It is used to create new directories.
    ```
    ./mkdir.py [OPTION]... [DIRECTORY]...
    ```
> Flag: 
> -p: create directory and parent directories


 - `cat.py` - cat analog. It is used to read files.
    ```
    ./cat.py [FILE]...
    ```

 - `cp.py` - cp analog. It is used to copy objects.
    ```
    ./cp.py [OPTION]... [ORIGINAL OBJECT1] [NEW OBJECT2]
    ```
> Flag: 
> -r: copy directory


