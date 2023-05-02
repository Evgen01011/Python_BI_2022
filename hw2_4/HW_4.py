#!/usr/bin/env python
# coding: utf-8

# В формулировке заданий будет использоваться понятие **worker**. Это слово обозначает какую-то единицу параллельного выполнения, в случае питона это может быть **поток** или **процесс**, выбирайте то, что лучше будет подходить к конкретной задаче
# 
# В каждом задании нужно писать подробные аннотиции типов для:
# 1. Аргументов функций и классов
# 2. Возвращаемых значений
# 3. Классовых атрибутов (если такие есть)
# 
# В каждом задании нужно писать докстроки в определённом стиле (какой вам больше нравится) для всех функций, классов и методов

# # Задание 1 (7 баллов)

# В одном из заданий по ML от вас требовалось написать кастомную реализацию Random Forest. Её проблема состоит в том, что она работает медленно, так как использует всего один поток для работы. Добавление параллельного программирования в код позволит получить существенный прирост в скорости обучения и предсказаний.
# 
# В данном задании от вас требуется добавить возможность обучать случайный лес параллельно и использовать параллелизм для предсказаний. Для этого вам понадобится:
# 1. Добавить аргумент `n_jobs` в метод `fit`. `n_jobs` показывает количество worker'ов, используемых для распараллеливания
# 2. Добавить аргумент `n_jobs` в методы `predict` и `predict_proba`
# 3. Реализовать функционал по распараллеливанию в данных методах
# 
# В результате код `random_forest.fit(X, y, n_jobs=2)` и `random_forest.predict(X, y, n_jobs=2)` должен работать в ~1.5-2 раза быстрее, чем `random_forest.fit(X, y, n_jobs=1)` и `random_forest.predict(X, y, n_jobs=1)` соответственно
# 
# Если у вас по каким-то причинам нет кода случайного леса из ДЗ по ML, то вы можете написать его заново или попросить у однокурсника. *Детали* реализации ML части оцениваться не будут, НО, если вы поломаете логику работы алгоритма во время реализации параллелизма, то за это будут сниматься баллы
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона, а также функции и классы из **sklearn** при помощи которых вы изначально писали лес

# In[228]:


from sklearn.base import BaseEstimator
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
import numpy as np

import multiprocessing
import threading
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

from typing import Type, Tuple, Any, Callable, Optional, Union, List, Dict


SEED = 111


# Теперь с использованием запараллеливания

# In[236]:


class RandomForestClassifierCustom(BaseEstimator):
    """
    The class is a custom analog of RandomForestClassifier from sklearn

    Attributes:
        n_estimators: the number of trees in forest
        max_depth: depth of decision trees
        max_features: number of features that is taken into account in tree
        random_state: control of random
        
    Methods:
        fit(): fit training data
        predict_proba(): predict probability of test data
        predict(): predict classes of test data
    """

    def __init__(self, n_estimators: int = 10, max_depth: int = None,
                 max_features: int = None, random_state: int = SEED) -> None:
        """
        Initializer of the class object
        :param self: the class object
        :param n_estimators: the number of trees in forest
        :param max_depth: depth of decision trees
        :param max_features: number of features that is taken into account in tree
        :param random_state: control of random
        :return: None
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.random_state = random_state

        self.trees = []
        self.feat_ids_by_tree = []

    def fit(self, X: np.ndarray, y: np.ndarray, n_jobs: int) -> None:
        """
        Fit training data
        :param self: the class object
        :param X: the train features and their value
        :param y: the train target
        :param n_jobs: the number of thread
        :return: None
        """
        self.classes_ = sorted(np.unique(y))

        def one_tree_function(self, X: np.ndarray, y: np.ndarray) -> DecisionTreeClassifier:
            """
            Construction of one decision tree of forests
            :param self: the class object
            :param X: the test features and their value
            :param y: the test target
            :return: one tree of forests
            """
            self.seed_fit = np.random.seed(self.random_state)
            feature_amount = np.random.choice(X.shape[1], self.max_features, replace=False)
            self.feat_ids_by_tree.append(feature_amount)
            bootstrep_X = np.random.choice(X.shape[0], X.shape[0], replace=True)
            random_X = X[bootstrep_X]
            new_X = random_X[:, feature_amount]
            new_y = y[bootstrep_X]

            tree = DecisionTreeClassifier(max_depth=self.max_depth,
                                          max_features=self.max_features,
                                          random_state=self.seed_fit)

            tree.fit(new_X, new_y)
            return tree

        # introduce parallel programming
        with ThreadPoolExecutor(n_jobs) as pool:
            self.trees = pool.map(one_tree_function, [self] * self.n_estimators,
                                  [X] * self.n_estimators,
                                  [y] * self.n_estimators)
        return self

    def predict_proba(self, X: np.ndarray, n_jobs: int) -> np.ndarray:
        """
        Function of probability calculation of test data
        :param self: the class object
        :param X: the test features and their value
        :param n_jobs: the number of thread
        :return: the probability of an object belonging to the target class
        """
        # introduce parallel programming
        with ThreadPoolExecutor(n_jobs) as pool:
            proba = pool.map(lambda x, X, i: x.predict_proba(X[:, self.feat_ids_by_tree[i]]), list(self.trees),
                             [X] * self.n_estimators,
                             list(range(self.n_estimators)))

        result = np.mean(list(proba), axis=0)
        return result

    def predict(self, X: np.ndarray, n_jobs: int) -> np.ndarray:
        """
        Function of prediction of test data object belonging
        :param self:
        :param X:
        :param n_jobs:
        :return:
        """
        probas = self.predict_proba(X, n_jobs)
        predictions = np.argmax(probas, axis=1)
        return predictions


# In[222]:


random_forest = RandomForestClassifierCustom(max_depth=30, n_estimators=10, max_features=2, random_state=42)


# In[225]:


get_ipython().run_cell_magic('time', '', 'a = random_forest.fit(X, y, n_jobs=1)')


# In[301]:


get_ipython().run_cell_magic('time', '', '\npreds_1 = random_forest.predict(X, n_jobs=1)')


# In[302]:


random_forest = RandomForestClassifierCustom(max_depth=30, n_estimators=10, max_features=2, random_state=42)


# In[303]:


get_ipython().run_cell_magic('time', '', '\n_ = random_forest.fit(X, y, n_jobs=2)')


# In[304]:


get_ipython().run_cell_magic('time', '', '\npreds_2 = random_forest.predict(X, n_jobs=2)')


# In[305]:


(preds_1 == preds_2).all()  # Количество worker'ов не должно влиять на предсказания


# In[306]:


len(preds_1) - (preds_1 == preds_2).sum()


# Ускорить, действительно, получилось

# #### Какие есть недостатки у вашей реализации параллельного Random Forest (если они есть)? Как это можно исправить? Опишите словами, можно без кода (+1 дополнительный балл)

# Первое, у меня не совсем сошлись предсказания. С т.з. внедрения параллельности, это не должно влиять (насколько я могу судить), и вероятно ошибки связаны с тем, что в ходе программы несколько раз подбрасывается хоть и детерменированный, но рандом
# 
# Второе, я выигрываю в человеческом времени, но, как и ожидалось, забиваю CPU. Наверно, в лучшем варианте, надо залезать внутрь класса дерева и запускать мультипроцессинг фитирования, чтобы действительно распараллелить процессы

# # Задание 2 (9 баллов)

# Напишите декоратор `memory_limit`, который позволит ограничивать использование памяти декорируемой функцией.
# 
# Декоратор должен принимать следующие аргументы:
# 1. `soft_limit` - "мягкий" лимит использования памяти. При превышении функцией этого лимита должен будет отображён **warning**
# 2. `hard_limit` - "жёсткий" лимит использования памяти. При превышении функцией этого лимита должно будет брошено исключение, а функция должна немедленно завершить свою работу
# 3. `poll_interval` - интервал времени (в секундах) между проверками использования памяти
# 
# Требования:
# 1. Потребление функцией памяти должно отслеживаться **во время выполнения функции**, а не после её завершения
# 2. **warning** при превышении `soft_limit` должен отображаться один раз, даже если функция переходила через этот лимит несколько раз
# 3. Если задать `soft_limit` или `hard_limit` как `None`, то соответствующий лимит должен быть отключён
# 4. Лимиты должны передаваться и отображаться в формате `<number>X`, где `X` - символ, обозначающий порядок единицы измерения памяти ("B", "K", "M", "G", "T", ...)
# 5. В тексте warning'ов и исключений должен быть указан текщий объём используемой памяти и величина превышенного лимита
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона, можно писать вспомогательные функции и/или классы
# 
# В коде ниже для вас предопределены некоторые полезные функции, вы можете ими пользоваться, а можете не пользоваться

# In[27]:


import os
import sys
import psutil
import time
import warnings
import threading


# In[230]:


def get_memory_usage() -> int:    # Показывает текущее потребление памяти процессом
    """
    Shows the current memory consumption of the process
    """
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def bytes_to_human_readable(n_bytes: int) -> str:
    """
    Convert bytes to readable object
    :param n_bytes: the number of bytes
    :return: human adaptable number of bytes
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for idx, s in enumerate(symbols):
        prefix[s] = 1 << (idx + 1) * 10
    for s in reversed(symbols):
        if n_bytes >= prefix[s]:
            value = float(n_bytes) / prefix[s]
            return f"{value:.2f}{s}"
    return f"{n_bytes}B"

def bytes_to_machine(n_bytes: str) -> int:
    """
    Convert human readable object into computer bytes 
    :param n_bytes: the number of bytes
    :return: computer number of bytes
    """    
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for idx, s in enumerate(symbols):
        prefix[s] = 1 << (idx + 1) * 10
    prefix['B'] = 1
    return prefix[n_bytes[-1]] * float(n_bytes[:-1])


def memory_limit(soft_limit: str = None, hard_limit: str = None, poll_interval: int = 1) -> Callable:
    """
    Restriction of memory consumption
    :param soft_limit: lower limit for warning
    :param hard_limit: upper limit for exception
    :param poll_interval: delay of control
    :return: decorating function
    """
    def wrapper(func: Callable) -> Callable:
        def inner_func(*args, **kwargs) -> Callable:
            current_memory = get_memory_usage()   
            
            # check None of hard_limit
            try:
                strict_control = bytes_to_machine(hard_limit)
            except TypeError:
                strict_control = False
            
            # check None of soft_limit
            try:
                soft_control = bytes_to_machine(soft_limit)
            except TypeError:
                soft_control = False
            
            # run function in another thread 
            tread_for_function = threading.Thread(target = func, args=(*args,), kwargs={**kwargs,})
            tread_for_function.start()
            
            while True:    
                if strict_control and (current_memory > strict_control):   # check  hard_limit
                    tread_for_function.join()                              # output of thread to the main area its interruption
                    warnings.filterwarnings('default')                     # switch on warnings for other function
                    raise Exception(f'Exception, hard limit({bytes_to_human_readable(strict_control)}) is exceed - {bytes_to_human_readable(current_memory)}')
                if soft_control and (current_memory > soft_control):       # check soft_limit
                    warnings.warn(f'Warning, soft limit({bytes_to_human_readable(soft_control)}) is exceed - {bytes_to_human_readable(current_memory)}')
                    warnings.filterwarnings('ignore')                      # switch off warnings
                    
                time.sleep(poll_interval)
                current_memory = get_memory_usage()
                
        return inner_func
    return wrapper


# In[25]:


@memory_limit(soft_limit='150M', hard_limit="0.5G", poll_interval=0.1)
def memory_increment():
    """
    Функция для тестирования
    
    В течение нескольких секунд достигает использования памяти 1.89G
    Потребление памяти и скорость накопления можно варьировать, изменяя код
    """
    lst = []
    for i in range(500000000000):
        if i % 500000 != 0:
#            time.sleep(0.1)
            lst.append(i)
    return lst
memory_increment()


# Ячейка завершает выполнение после Исключения, но такое ощущение, что при запуске начинает добегать другой поток и до этого момента выскакивает MemoryError (не совсем понимаю откуда, потому что аттрибут is_alive выдает False. Видимо, пока тестировал, я их очень много запустил, потому что выдает разный номер потока)

# # Задание 3 (11 баллов)

# Напишите функцию `parallel_map`. Это должна быть **универсальная** функция для распараллеливания, которая эффективно работает в любых условиях.
# 
# Функция должна принимать следующие аргументы:
# 1. `target_func` - целевая функция (обязательный аргумент)
# 2. `args_container` - контейнер с позиционными аргументами для `target_func` (по-умолчанию `None` - позиционные аргументы не передаются)
# 3. `kwargs_container` - контейнер с именованными аргументами для `target_func` (по-умолчанию `None` - именованные аргументы не передаются)
# 4. `n_jobs` - количество workers, которые будут использованы для выполнения (по-умолчанию `None` - количество логических ядер CPU в системе)
# 
# Функция должна работать аналогично `***PoolExecutor.map`, применяя функцию к переданному набору аргументов, но с некоторыми дополнениями и улучшениями
#     
# Поскольку мы пишем **универсальную** функцию, то нам нужно будет выполнить ряд требований, чтобы она могла логично и эффективно работать в большинстве ситуаций
# 
# 1. `target_func` может принимать аргументы любого вида в любом количестве
# 2. Любые типы данных в `args_container`, кроме `tuple`, передаются в `target_func` как единственный позиционный аргумент. `tuple` распаковываются в несколько аргументов
# 3. Количество элементов в `args_container` должно совпадать с количеством элементов в `kwargs_container` и наоборот, также значение одного из них или обоих может быть равно `None`, в иных случаях должна кидаться ошибка (оба аргумента переданы, но размеры не совпадают)
# 
# 4. Функция должна выполнять определённое количество параллельных вызовов `target_func`, это количество зависит от числа переданных аргументов и значения `n_jobs`. Сценарии могут быть следующие
#     + `args_container=None`, `kwargs_container=None`, `n_jobs=None`. В таком случае функция `target_func` выполнится параллельно столько раз, сколько на вашем устройстве логических ядер CPU
#     + `args_container=None`, `kwargs_container=None`, `n_jobs=5`. В таком случае функция `target_func` выполнится параллельно **5** раз
#     + `args_container=[1, 2, 3]`, `kwargs_container=None`, `n_jobs=5`. В таком случае функция `target_func` выполнится параллельно **3** раза, несмотря на то, что `n_jobs=5` (так как есть всего 3 набора аргументов для которых нам нужно получить результат, а лишние worker'ы создавать не имеет смысла)
#     + `args_container=None`, `kwargs_container=[{"s": 1}, {"s": 2}, {"s": 3}]`, `n_jobs=5`. Данный случай аналогичен предыдущему, но здесь мы используем именованные аргументы
#     + `args_container=[1, 2, 3]`, `kwargs_container=[{"s": 1}, {"s": 2}, {"s": 3}]`, `n_jobs=5`. Данный случай аналогичен предыдущему, но здесь мы используем и позиционные, и именованные аргументы
#     + `args_container=[1, 2, 3, 4]`, `kwargs_container=None`, `n_jobs=2`. В таком случае в каждый момент времени параллельно будет выполняться **не более 2** функций `target_func`, так как нам нужно выполнить её 4 раза, но у нас есть только 2 worker'а.
#     + В подобных случаях (из примера выше) должно оптимизироваться время выполнения. Если эти 4 вызова выполняются за 5, 1, 2 и 1 секунды, то параллельное выполнение с `n_jobs=2` должно занять **5 секунд** (не 7 и тем более не 10)
# 
# 5. `parallel_map` возвращает результаты выполнения `target_func` **в том же порядке**, в котором были переданы соответствующие аргументы
# 6. Работает с функциями, созданными внутри других функций
# 
# Для базового решения от вас не ожидается **сверххорошая** оптимизация по времени и памяти для всех возможных случаев. Однако за хорошо оптимизированную логику работы можно получить до **+3 дополнительных баллов**
# 
# Вы можете сделать класс вместо функции, если вам удобнее
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона
# 
# Ниже приведены тестовые примеры по каждому из требований

# In[30]:


import multiprocessing
import threading
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor


# In[232]:


def parallel_map(target_func: Callable,
                 args_container: Union[Tuple, List] = None,
                 kwargs_container: Dict = None,
                 n_jobs: int = None) -> Any:
    """
    Function for parallelizing other functions
    :param target_func: target function
    :param args_container: position arguments of fuction
    :param kwargs_container: key arguments of function
    :param n_jobs: the number of threads
    :return: result of target function execution
    """
    
    # determine n_jobs in case n_jobs=None
    if n_jobs == None:
        n_jobs = os.cpu_count()
    
    # introduce flag for tracing status of args and kwargs
    flag = 0
    
    # arg_module is needed for real_n_jobs: in case None it transforms to kwargs_container and then i observe what contains kwargs 
    if args_container == None:
        arg_module = kwargs_container  
    else:
        arg_module = args_container
        # for succesfull executing all args convert into tuple
        for element, arg in enumerate(args_container):
            args_container[element] = arg if isinstance(arg, tuple) else (arg,) 
        flag += 1
     
    # kwarg_module is also needed for real_n_jobs: in case None it and arg_module transforms into amount greater than number of threads
    if kwargs_container == None:
        arg_module, kwarg_module = [1] * (n_jobs + 1), [1] * (n_jobs + 1)
    else:
        kwarg_module = kwargs_container
        flag += 2
    
    # check equal length
    if len(arg_module) != len(kwarg_module):
        raise Exception(f'The length of containers does not equal: {len(arg_module)} and {len(kwarg_module)}')
    else:
        real_n_jobs = min(len(arg_module), n_jobs)        # determine real threads
    
    # start parallel programming for every possible way
    with ThreadPoolExecutor(real_n_jobs) as pool:
        future_list, result = [], []
        
        if flag == 3:
            container_mix = list(zip(args_container, kwargs_container))
            for combination in container_mix:
                future = pool.submit(target_func, *combination[0], **combination[1])
                future_list.append(future)
            for execute in future_list:
                result.append(execute.result())
                
        if flag == 2:
            for k_arg in kwargs_container:
                future = pool.submit(target_func, **k_arg)
                future_list.append(future)
            for execute in future_list:
                result.append(execute.result())
        
        if flag == 1:
            for arg in args_container:
                future = pool.submit(target_func, *arg)
                future_list.append(future)
            for execute in future_list:
                result.append(execute.result())
            
        if flag == 0:
            for _ in range(real_n_jobs):
                future = pool.submit(target_func)
                future_list.append(future)
            for execute in future_list:
                result.append(execute.result())
    
    return result


# In[233]:


import time


# Это только один пример тестовой функции, ваша parallel_map должна уметь эффективно работать с ЛЮБЫМИ функциями
# Поэтому обязательно протестируйте код на чём-нибудбь ещё
def test_func(x=1, s=2, a=1, b=1, c=1):
    time.sleep(s)
    return a*x**2 + b*x + c


# In[234]:


get_ipython().run_cell_magic('time', '', '\n# Пример 2.1.0 \n# Работа в одном потоке\n# Отдельные значения в args_container передаются в качестве позиционных аргументов\nparallel_map(test_func, args_container=[1, 2.0, 3j-1, 4], n_jobs=1)   # Здесь происходят параллельные вызовы: test_func(1) test_func(2.0) test_func(3j-1) test_func(4)')


# In[235]:


get_ipython().run_cell_magic('time', '', '\n# Пример 2.1.1\n# Запускаю в 8 потоках\n# Отдельные значения в args_container передаются в качестве позиционных аргументов\nparallel_map(test_func, args_container=[1, 2.0, 3j-1, 4], n_jobs=8)   # Здесь происходят параллельные вызовы: test_func(1) test_func(2.0) test_func(3j-1) test_func(4)')


# In[203]:


get_ipython().run_cell_magic('time', '', '\n# Пример 2.2\n# Элементы типа tuple в args_container распаковываются в качестве позиционных аргументов\nparallel_map(test_func, [(1, 1), (2.0, 2), (3j-1, 3), 4])    # Здесь происходят параллельные вызовы: test_func(1, 1) test_func(2.0, 2) test_func(3j-1, 3) test_func(4)')


# In[206]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.1\n# Возможна одновременная передача args_container и kwargs_container, но количества элементов в них должны быть равны\nparallel_map(test_func,\n             args_container=[1, 2, 3, 4],\n             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}, {"s": 3}])\n\n# Здесь происходят параллельные вызовы: test_func(1, s=3) test_func(2, s=3) test_func(3, s=3) test_func(4, s=3)')


# In[207]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.2\n# args_container может быть None, а kwargs_container задан явно\nparallel_map(test_func,\n             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}, {"s": 3}])')


# In[208]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.3\n# kwargs_container может быть None, а args_container задан явно\nparallel_map(test_func,\n             args_container=[1, 2, 3, 4])')


# In[209]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.4\n# И kwargs_container, и args_container могут быть не заданы\nparallel_map(test_func)')


# In[210]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.5\n# При несовпадении количеств позиционных и именованных аргументов кидается ошибка\nparallel_map(test_func,\n             args_container=[1, 2, 3, 4],\n             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}])')


# In[211]:


get_ipython().run_cell_magic('time', '', '\n# Пример 4.1\n# Если функция не имеет обязательных аргументов и аргумент n_jobs не был передан, то она выполняется параллельно столько раз, сколько ваш CPU имеет логических ядер\n# В моём случае это 24, у вас может быть больше или меньше\nparallel_map(test_func)')


# In[212]:


get_ipython().run_cell_magic('time', '', '\n# Пример 4.2\n# Если функция не имеет обязательных аргументов и передан только аргумент n_jobs, то она выполняется параллельно n_jobs раз\nparallel_map(test_func, n_jobs=2)')


# In[213]:


get_ipython().run_cell_magic('time', '', "\n# Пример 4.3\n# Если аргументов для target_func указано МЕНЬШЕ, чем n_jobs, то используется такое же количество worker'ов, сколько было передано аргументов\nparallel_map(test_func,\n             args_container=[1, 2, 3],\n             n_jobs=5)   # Здесь используется 3 worker'a")


# In[214]:


get_ipython().run_cell_magic('time', '', '\n# Пример 4.4\n# Аналогичный предыдущему случай, но с именованными аргументами\nparallel_map(test_func,\n             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}],\n             n_jobs=5)   # Здесь используется 3 worker\'a')


# In[215]:


get_ipython().run_cell_magic('time', '', '\n# Пример 4.5\n# Комбинация примеров 4.3 и 4.4 (переданы и позиционные и именованные аргументы)\nparallel_map(test_func,\n             args_container=[1, 2, 3],\n             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}],\n             n_jobs=5)   # Здесь используется 3 worker\'a')


# In[216]:


get_ipython().run_cell_magic('time', '', "\n# Пример 4.6\n# Если аргументов для target_func указано БОЛЬШЕ, чем n_jobs, то используется n_jobs worker'ов\nparallel_map(test_func,\n             args_container=[1, 2, 3, 4],\n             kwargs_container=None,\n             n_jobs=2)   # Здесь используется 2 worker'a")


# In[217]:


get_ipython().run_cell_magic('time', '', '\n# Пример 4.7\n# Время выполнения оптимизируется, данный код должен отрабатывать за 5 секунд\nparallel_map(test_func,\n             kwargs_container=[{"s": 5}, {"s": 1}, {"s": 2}, {"s": 1}],\n             n_jobs=2)')


# In[218]:


def test_func2(string, sleep_time=1):
    time.sleep(sleep_time)
    return string

# Пример 5
# Результаты возвращаются в том же порядке, в котором были переданы соответствующие аргументы вне зависимости от того, когда завершился worker
arguments = ["first", "second", "third", "fourth", "fifth"]
parallel_map(test_func2,
             args_container=arguments,
             kwargs_container=[{"sleep_time": 5}, {"sleep_time": 4}, {"sleep_time": 3}, {"sleep_time": 2}, {"sleep_time": 1}])


# In[219]:


get_ipython().run_cell_magic('time', '', '\n\ndef test_func3():\n    def inner_test_func(sleep_time):\n        time.sleep(sleep_time)\n    return parallel_map(inner_test_func, args_container=[1, 2, 3])\n\n# Пример 6\n# Работает с функциями, созданными внутри других функций\ntest_func3()')


# #### P.S. Pома и Катя, огромное вам спасибо за отличный фидбек, за быструю проверку и в целом за курс. 
# 
# #### Роме еще отдельное спасибо за потрясающие лекции и ноутбуки, они супер! И сам курс мне показался самым лучшим и полезным за этот год в ИБ - только Дане не говорите, мне ему еще домашки по МL сдавать :) Спасибо большое!  
