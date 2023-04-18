#!/usr/bin/env python
# coding: utf-8

# # Задание 1 (2 балла)

# Напишите класс `MyDict`, который будет полностью повторять поведение обычного словаря, за исключением того, что при итерации мы должны получать и ключи, и значения.
# 
# **Модули использовать нельзя**

# In[17]:


class MyDict(dict):
    
    def __iter__(self):
        for item in self.items():
            yield item

dct = MyDict({"a": 1, "b": 2, "c": 3, "d": 25})


# In[18]:


dct = MyDict({"a": 1, "b": 2, "c": 3, "d": 25})
for key, value in dct:
    print(key, value)   


# In[19]:


for key, value in dct.items():
    print(key, value)


# In[20]:


for key in dct.keys():
    print(key)


# In[21]:


dct["c"] + dct["d"]


# # Задание 2 (2 балла)

# Напишите функцию `iter_append`, которая "добавляет" новый элемент в конец итератора, возвращая итератор, который включает изначальные элементы и новый элемент. Итерироваться по итератору внутри функции нельзя, то есть вот такая штука не принимается
# ```python
# def iter_append(iterator, item):
#     lst = list(iterator) + [item]
#     return iter(lst)
# ```
# 
# **Модули использовать нельзя**

# In[32]:


def iter_append(iterator, item):
    for obj in iterator:
        yield obj
    yield item
        
    

my_iterator = iter([1, 2, 3])
new_iterator = iter_append(my_iterator, 4)

for element in new_iterator:
    print(element)


# # Задание 3 (5 баллов)

# Представим, что мы установили себе некотурую библиотеку, которая содержит в себе два класса `MyString` и `MySet`, которые являются наследниками `str` и `set`, но также несут и дополнительные методы.
# 
# Проблема заключается в том, что библиотеку писали не очень аккуратные люди, поэтому получилось так, что некоторые методы возвращают не тот тип данных, который мы ожидаем. Например, `MyString().reverse()` возвращает объект класса `str`, хотя логичнее было бы ожидать объект класса `MyString`.
# 
# Найдите и реализуйте удобный способ сделать так, чтобы подобные методы возвращали экземпляр текущего класса, а не родительского. При этом **код методов изменять нельзя**
# 
# **+3 дополнительных балла** за реализацию того, чтобы **унаследованные от `str` и `set` методы** также возвращали объект интересующего нас класса (то есть `MyString.replace(..., ...)` должен возвращать `MyString`). **Переопределять методы нельзя**
# 
# **Модули использовать нельзя**

# ##### Декораторы для функций

# In[52]:


def class_changes(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return type(self)(func(self, *args, **kwargs))
    return wrapper


# In[53]:


class MyString(str):
    @class_changes
    def reverse(self):
        return self[::-1]
    
    @class_changes
    def make_uppercase(self):
        return "".join([chr(ord(char) - 32) if 97 <= ord(char) <= 122 else char for char in self])
    
    @class_changes
    def make_lowercase(self):
        return "".join([chr(ord(char) + 32) if 65 <= ord(char) <= 90 else char for char in self])
    
    @class_changes
    def capitalize_words(self):
        return " ".join([word.capitalize() for word in self.split()])
    
    
class MySet(set):
    
    def is_empty(self):
        return len(self) == 0
    
    def has_duplicates(self):
        return len(self) != len(set(self))
    
    @class_changes
    def union_with(self, other):
        return self.union(other)
    
    @class_changes
    def intersection_with(self, other):
        return self.intersection(other)
    
    @class_changes
    def difference_with(self, other):
        return self.difference(other)


# In[54]:


string_example = MyString("Aa Bb Cc")
set_example_1 = MySet({1, 2, 3, 4})
set_example_2 = MySet({3, 4, 5, 6, 6})


print(type(string_example.reverse()))
print(type(string_example.make_uppercase()))
print(type(string_example.make_lowercase()))
print(type(string_example.capitalize_words()))
print()
print(type(set_example_1.is_empty()))
print(type(set_example_2.has_duplicates()))
print(type(set_example_1.union_with(set_example_2)))
print(type(set_example_1.difference_with(set_example_2)))


# ##### Декораторы для классов

# In[55]:


def transform(cls):
    for attribute in dir(cls):
        attr = getattr(cls, attribute)
        if callable(attr) and attribute[0:2] != '__':
            setattr(cls, attribute, class_changes_mod(attr))
    return cls

def class_changes_mod(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if isinstance(result, (set, str)):
            result = type(self)(result)
        return result
    return wrapper


# In[56]:


@transform
class MyString(str):
    def reverse(self):
        return self[::-1]
    
    def make_uppercase(self):
        return "".join([chr(ord(char) - 32) if 97 <= ord(char) <= 122 else char for char in self])
    
    def make_lowercase(self):
        return "".join([chr(ord(char) + 32) if 65 <= ord(char) <= 90 else char for char in self])
    
    def capitalize_words(self):
        return " ".join([word.capitalize() for word in self.split()])
    
@transform
class MySet(set):
    def is_empty(self):
        return len(self) == 0
    
    def has_duplicates(self):
        return len(self) != len(set(self))
    
    def union_with(self, other):
        return self.union(other)
    
    def intersection_with(self, other):
        return self.intersection(other)
    
    def difference_with(self, other):
        return self.difference(other)
    
string_example = MyString("Aa Bb Cc")
set_example_1 = MySet({1, 2, 3, 4})
set_example_2 = MySet({3, 4, 5, 6, 6})


print(type(string_example.reverse()))
print(type(string_example.make_uppercase()))
print(type(string_example.make_lowercase()))
print(type(string_example.capitalize_words()))
print()
print(type(set_example_1.is_empty()))
print(type(set_example_2.has_duplicates()))
print(type(set_example_1.union_with(set_example_2)))
print(type(set_example_1.difference_with(set_example_2)))
print('Parent function')
print(type(set_example_1.union(set_example_2)))


# # Задание 4 (5 баллов)

# Напишите декоратор `switch_privacy`:
# 1. Делает все публичные **методы** класса приватными
# 2. Делает все приватные методы класса публичными
# 3. Dunder методы и защищённые методы остаются без изменений
# 4. Должен работать тестовый код ниже, в теле класса писать код нельзя
# 
# **Модули использовать нельзя**

# In[89]:


def switch_privacy(cls):
    for attr in dir(cls):
        if attr[0] != '_':
            value = getattr(cls, attr)
            setattr(cls, f'_{cls.__name__}__{attr}', value)
            delattr(cls, attr)
        elif cls.__name__ in attr:
            value = getattr(cls, attr)
            setattr(cls, attr.replace(f'_{cls.__name__}__', ''), value)
            delattr(cls, attr)
    return cls
    


# In[90]:



@switch_privacy        
class ExampleClass:
    # Но не здесь
    def public_method(self):
        return 1
    
    def _protected_method(self):
        return 2
    
    def __private_method(self):
        return 3
    
    def __dunder_method__(self):
        pass


# In[94]:


test_object._ExampleClass__public_method()   # Публичный метод стал приватным


# In[95]:


test_object.private_method()   # Приватный метод стал публичным


# In[96]:


test_object._protected_method()   # Защищённый метод остался защищённым


# In[97]:


test_object.__dunder_method__()   # Дандер метод не изменился


# In[98]:


hasattr(test_object, "public_method"), hasattr(test_object, "private")   # Изначальные варианты изменённых методов не сохраняются


# # Задание 5 (7 баллов)

# Напишите [контекстный менеджер](https://docs.python.org/3/library/stdtypes.html#context-manager-types) `OpenFasta`
# 
# Контекстные менеджеры это специальные объекты, которые могут работать с конструкцией `with ... as ...:`. В них нет ничего сложного, для их реализации как обычно нужно только определить только пару dunder методов. Изучите этот вопрос самостоятельно
# 
# 1. Объект должен работать как обычные файлы в питоне (наследоваться не надо, здесь лучше будет использовать **композицию**), но:
#     + При итерации по объекту мы должны будем получать не строку из файла, а специальный объект `FastaRecord`. Он будет хранить в себе информацию о последовательности. Важно, **не строки, а именно последовательности**, в fasta файлах последовательность часто разбивают на много строк
#     + Нужно написать методы `read_record` и `read_records`, которые по смыслу соответствуют `readline()` и `readlines()` в обычных файлах, но они должны выдавать не строки, а объект(ы) `FastaRecord`
# 2. Конструктор должен принимать один аргумент - **путь к файлу**
# 3. Класс должен эффективно распоряжаться памятью, с расчётом на работу с очень большими файлами
#     
# Объект `FastaRecord`. Это должен быть **датакласс** (см. про примеры декораторов в соответствующей лекции) с тремя полями:
# + `seq` - последовательность
# + `id_` - ID последовательности (это то, что в фаста файле в строке, которая начинается с `>` до первого пробела. Например, >**GTD326487.1** Species anonymous 24 chromosome) 
# + `description` - то, что осталось после ID (Например, >GTD326487.1 **Species anonymous 24 chromosome**)
# 
# 
# Напишите демонстрацию работы кода с использованием всех написанных методов, обязательно добавьте файл с тестовыми данными в репозиторий (не обязательно большой)
# 
# **Можно использовать модули из стандартной библиотеки**

# In[645]:


import os
from dataclasses import dataclass


@dataclass
class FastaRecord:
    id : str
    description : str
    seq : str

class OpenFasta():
    
    leading_line = None     #keep line determining start of new sequence
    
    def __init__(self, path):
        self.file_path = path
        
    def __enter__(self):
        self.opened_file = open(self.file_path)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.opened_file.close()
                
    def __iter__(self):
        return self

    def read_record(self):
        
        #processing the first line of the sequence (but not the first line of the file), creating future key attributes ща FastaRecord
        if self.leading_line is not None and self.leading_line.startswith('>'):     
            current_id = self.leading_line.split(' ')[0]
            current_desc = ' '.join(self.leading_line.split(' ')[1:])
            current_seq = str()
        
        for record in self.opened_file:
            reading_process = record.strip()
            if reading_process.startswith('>'):                 #processing the first line of the sequence 
                try:                                            #allow to process even in start of file
                    previous_id, previous_desc, previous_seq = current_id, current_desc, current_seq
                    self.leading_line = reading_process
                    return FastaRecord(id=previous_id, description=previous_desc, seq=previous_seq)
                except:
                    pass
                
                current_id = reading_process.split(' ')[0]
                current_desc = ' '.join(reading_process.split(' ')[1:])
                current_seq = str()
                
            else:               
                current_seq += reading_process                  #for all part of sequence
                
        else:
            return FastaRecord(id=current_id, description=current_desc, seq=current_seq)
            self.marker = False
            print(current_id, current_desc, current_seq)
    
    #not the optimal code for reading the entire file (good options fell with errors)
    def read_records(self):
        result = self.read_record()
        fasta_data = [result]
        while result.seq != '':
            result = self.read_record()
            fasta_data.append(result)
        return fasta_data[:-1]


# ##### Читаем всю fasta

# In[646]:


with OpenFasta(os.path.join("fasta_file", "seqdump.fasta")) as fasta:
    print(fasta.read_records())


# ##### Читаем отдельные последовательности

# In[647]:


with OpenFasta(os.path.join("fasta_file", "seqdump.fasta")) as fasta:
    print(fasta.read_record())
    print(fasta.read_record())
    print(fasta.read_record())


# ##### Другой файл, где нет описаний к сиквенсам

# In[648]:


with OpenFasta(os.path.join("fasta_file", "sequences.fasta")) as fasta:
    print(fasta.read_record())


# > Из минусов класса будет продолжать выводить FastaRecord при вызове read_record даже если записей уже нет

# # Задание 6 (7 баллов)

# 1. Напишите код, который позволит получать все возможные (неуникальные) генотипы при скрещивании двух организмов. Это может быть функция или класс, что вам кажется более удобным.
# 
# Например, все возможные исходы скрещивания "Aabb" и "Aabb" (неуникальные) это
# 
# ```
# AAbb
# AAbb
# AAbb
# AAbb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# aabb
# aabb
# aabb
# aabb
# ```
# 
# 2. Напишите функцию, которая вычисляет вероятность появления определённого генотипа (его ожидаемую долю в потомстве).
# Например,
# 
# ```python
# get_offspting_genotype_probability(parent1="Aabb", parent2="Aabb", target_genotype="Аabb")   # 0.5
# 
# ```
# 
# 3. Напишите код, который выводит все уникальные генотипы при скрещивании `'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн'` и `'АаббВвГгДДЕеЖжЗзИиЙйКкЛлМмНН'`, которые содержат в себе следующую комбинацию аллелей `'АаБбВвГгДдЕеЖжЗзИиЙйКкЛл'`
# 4. Напишите код, который расчитывает вероятность появления генотипа `'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн'` при скрещивании `АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн` и `АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн`
# 
# Важные замечания:
# 1. Порядок следования аллелей в случае гетерозигот всегда должен быть следующим: сначала большая буква, затем маленькая (вариант `AaBb` допустим, но `aAbB` быть не должно)
# 2. Подзадачи 3 и 4 могут потребовать много вычислительного времени (до 15+ минут в зависимости от железа), поэтому убедитесь, что вы хорошо протестировали написанный вами код на малых данных перед выполнением этих задач. Если ваш код работает **дольше 20 мин**, то скорее всего ваше решение не оптимально, попытайтесь что-нибудь оптимизировать. Если оптимальное решение совсем не получается, то попробуйте из входных данных во всех заданиях убрать последний ген (это должно уменьшить время выполнения примерно в 4 раза), но **за такое решение будет снято 2 балла**
# 3. Несмотря на то, что подзадания 2, 3 и 4 возможно решить математически, не прибегая к непосредственному получению всех возможных генотипов, от вас требуется именно brute-force вариант алгоритма
# 
# **Можно использовать модули из стандартной библиотеки питона**, но **за выполнение задания без использования модулей придусмотрено +3 дополнительных балла**

# In[643]:


# Ваш код здесь (1 и 2 подзадание)
import itertools

#function combine combination and part of probability function via parametr auxilary
def hybridisation(genotype_1, genotype_2, auxilary = False):
    genotype = []
    for window in range(0, len(genotype_1), 2):
        options = []
        for i in itertools.product(genotype_1[window: window + 2], genotype_2[window: window + 2]):
            options.append(sorted(list(i)))
        genotype.append(options)
    
    result_list = []
    for gene in itertools.product(*genotype):
        result = ''.join(map(lambda x: ''.join(x),  gene))
        result_list.append(result)
        if not auxilary:
            print(result)
            
    if auxilary:
        return result_list
        
        

hybridisation("AaBbCC", "AabbCc")


# In[644]:


def get_offspting_genotype_probability(parent1, parent2, target_genotype):
    all_result = hybridisation(parent1, parent2, auxilary=True)
    return all_result.count(target_genotype) / len(all_result)

get_offspting_genotype_probability("Aabb", "Aabb", "Aabb")


# ###### Вроде перебор всех вариантов, но, как мне теперь кажется, не совсем брут-форс. Но чистый брутфорс ноут совсе не вывозил

# In[94]:


get_ipython().run_cell_magic('time', '', "# Ваш код здесь (3 подзадание)\nimport numpy as np\n\ndef complex_hybridisation(genotype_1, genotype_2, target_genotype):\n    assembly_genotype = []\n    \n    #collect all options of hybridisation of separated genes \n    for window in range(0, len(genotype_1), 2):\n        options = []\n        for i in itertools.product(genotype_1[window: window + 2], genotype_2[window: window + 2]):\n            options.append(sorted(list(i)))\n        assembly_genotype.append(options)\n\n    #divide target by gene\n    divide_target = []\n    for window in range(0, len(target_genotype), 2):   \n        divide_target.append([target_genotype[window], target_genotype[window+1]])\n\n    genotype_copy = assembly_genotype.copy()\n    result = []\n    str_reference_genotype = str()\n    \n    #check target genes, delete them from collection and combine free part\n    for number, list_of_allel in enumerate(genotype_copy):\n        try:\n            str_reference_genotype += ''.join(divide_target[number])\n            assembly_genotype.remove(list_of_allel)\n        except IndexError:\n            for gene in itertools.product(*assembly_genotype):\n                variant = ''.join(map(lambda x: ''.join(x),  gene))\n                result.append(variant)\n            \n    output = list(map(lambda x: str_reference_genotype + x, np.unique(result)))\n    print(*output, sep='\\n')\n        \n        \n\ncomplex_hybridisation('АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн', 'АаббВвГгДДЕеЖжЗзИиЙйКкЛлМмНН', 'АаБбВвГгДдЕеЖжЗзИиЙйКкЛл')")


# In[100]:


# Ваш код здесь (4 подзадание)

def calculate_special_hybridisation(genotype_1, genotype_2, target_genotype):
    assembly_genotype = []
    for window in range(0, len(genotype_1), 2):
        options = []
        for i in itertools.product(genotype_1[window: window + 2], genotype_2[window: window + 2]):
            options.append(sorted(list(i)))
        assembly_genotype.append(options)

    divide_target = []
    for window in range(0, len(target_genotype), 2):   
        divide_target.append([target_genotype[window], target_genotype[window+1]])

    probability = 1
    for number, list_of_allel in enumerate(assembly_genotype):
        probability *= list_of_allel.count(divide_target[number]) / len(list_of_allel)
        
    return probability

calculate_special_hybridisation('АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн','АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн', 'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн')

