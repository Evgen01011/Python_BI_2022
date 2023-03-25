#!/usr/bin/env python
# coding: utf-8

# # Задание 1 (5 баллов)

# Напишите классы **Chat**, **Message** и **User**. Они должны соответствовать следующим требованиям:
# 
# **Chat**:
# + Должен иметь атрибут `chat_history`, где будут храниться все сообщения (`Message`) в обратном хронологическом порядке (сначала новые, затем старые)
# + Должен иметь метод `show_last_message`, выводящий на экран информацию о последнем сообщении
# + Должен иметь метод `get_history_from_time_period`, который принимает два опциональных аргумента (даты с которой и по какую мы ищем сообщения и выдаём их). Метод также должен возвращать объект типа `Chat`
# + Должен иметь метод `show_chat`, выводящий на экран все сообщения (каждое сообщение в таком же виде как и `show_last_message`, но с разделителем между ними)
# + Должен иметь метод `recieve`, который будет принимать сообщение и добавлять его в чат
# 
# **Message**:
# + Должен иметь три обязательных атрибута
#     + `text` - текст сообщения
#     + `datetime` - дата и время сообщения (встроенный модуль datetime вам в помощь). Важно! Это должна быть не дата создания сообщения, а дата его попадания в чат! 
#     + `user` - информация о пользователе, который оставил сообщение (какой тип данных использовать здесь, разберётесь сами)
# + Должен иметь метод `show`, который печатает или возвращает информацию о сообщении с необходимой информацией (дата, время, юзер, текст)
# + Должен иметь метод `send`, который будет отправлять сообщение в чат
# 
# **User**:
# + Класс с информацией о юзере, наполнение для этого класса придумайте сами
# 
# Напишите несколько примеров использования кода, которое показывает взаимодействие между объектами.
# 
# В тексте задания намерено не указано, какие аргументы должны принимать методы, пускай вам в этом поможет здравый смысл)
# 
# В этом задании не стоит флексить всякими продвинутыми штуками, для этого есть последующие
# 
# В этом задании можно использовать только модуль `datetime`

# In[1]:


from datetime import datetime
from random import choice   # for User


# In[2]:


class User:
    def __init__(self, name='I'):
        self.name = name 

    def online_offline(self):
        return choice(['online', 'offline'])


# In[3]:


class Message:
   def __init__(self, text, user, datetime = 'Draft'):   #maybe as draft or as planning message 
       self.text = text
       self.time = datetime
       if isinstance(user, User):                        #i think its better then convert into User
           self.user = user.name
       else:
           self.user = User('Incognito').name
   
   def show(self):
       print(f' Message text: {self.text} \n Time: {self.time} \n Sender: {self.user} \n')
   
   def send(self, chat):
       if not isinstance(self.time, datetime):
           self.time = datetime.now()
           
       chat.chat_history.insert(0, self)


# In[4]:


class Chat:
    def __init__(self, chat_history = []):
        self.chat_history = chat_history
        
    def show_last_message(self):
        type(Message)(self.chat_history[0]).show(self.chat_history[0])
    
    def get_history_from_time_period(self, start = datetime.now, stop = datetime.min):
        if start == datetime.now:                            #in order to dont activate during exampler creation
            start = start()
        try: 
            isinstance(start and stop, datetime) == True
        except:
            raise BaseException('Class inconsistancy: use datetime') 
        
        history_period = []

        for choise in self.chat_history:
            
            if start > choise.time > stop:
                history_period.append(choise)
                            
        if history_period:
            return(Chat(history_period))
        else:
            print('Chat history in this period is empty')
            return None
    
    def show_chat(self):
        for messages in self.chat_history:
            messages.show()
            
    def receive(self, mail):
        type(Message)(mail).send(mail, self) 


# Создаем юзеров и проверяем в сети ли они

# In[5]:


i = User('Zhenya')


# In[6]:


i.name


# In[7]:


i.online_offline()


# In[8]:


my_friend1 = User('Sasha')


# In[9]:


my_friend2 = User('Stepa')


# In[10]:


my_friend3 = User('Yulya')


# Создадим черновик первого сообщения

# In[11]:


first_message = Message('Hello', i)


# In[12]:


first_message.text


# In[13]:


first_message.time


# И запланируем отправку второго (тут немного странно, но это хорошо сработало для проверки истории)

# In[14]:


second_message = Message('Hi, Im from future', my_friend2, datetime(2023, 5, 18, 23, 59))


# In[15]:


second_message.user


# In[16]:


second_message.show()


# Создание чата с сообщениями и проверка его функционала

# In[17]:


group = Chat()


# In[18]:


second_message.send(group)


# In[19]:


group.chat_history


# In[20]:


group.receive(first_message)


# In[21]:


group.chat_history


# In[22]:


group.show_chat()


# In[23]:


group.show_last_message()


# In[24]:


group.get_history_from_time_period().show_chat()


# In[25]:


group.get_history_from_time_period(datetime(2023, 5, 19, 23, 59), datetime(2023, 5, 8, 23, 59)).show_chat()


# # Задание 2 (3 балла)

# В питоне как-то слишком типично и неинтересно происходят вызовы функций. Напишите класс `Args`, который будет хранить в себе аргументы, а функции можно будет вызывать при помощи следующего синтаксиса.
# 
# Использовать любые модули **нельзя**, да и вряд-ли это как-то поможет)

# In[26]:


class Args:
    def __init__(self, *args, **kwargs):
        self.alt_args = args
        self.alt_kwargs = kwargs
        
    def __repr__(self):
        return f'Object contains: args = {self.alt_args}, kwargs = {self.alt_kwargs}'  
        
    def __rlshift__(self, other):
        return other(*self.alt_args, **self.alt_kwargs)


# In[27]:


sum << Args([1, 2])


# In[28]:


(lambda a, b, c: a**2 + b + c) << Args(1, 2, c=50)


# # Задание 3 (5 баллов)

# Сделайте класс наследник `float`. Он должен вести себя как `float`, но также должен обладать некоторыми особенностями:
# + При получении атрибутов формата `<действие>_<число>` мы получаем результат такого действия над нашим числом
# + Создавать данные атрибуты в явном виде, очевидно, не стоит
# 
# Подсказка: если в процессе гуглёжки, вы выйдете на такую тему как **"Дескрипторы", то это НЕ то, что вам сейчас нужно**
# 
# Примеры использования ниже

# In[29]:


def change_operation(self, method):
        try:
            action, number = str(method).split('_')
            if action in self._operations.keys():
                return type(self)(self._operations[action](float(number)))
            else:
                return NotImplemented
        except:
            return NotImplemented
            
    

class StrangeFloat(float):
    
    def __init__(self, operations):
        self._operations = {'add' : self.__add__, 'subtract' : self.__sub__, 
                           'multiply' : self.__mul__, 'divide' : self.__truediv__,
                           'pow' : self.__pow__, 'floor_divide' : self.__floordiv__
                            }
        super().__init__()

                                  
    def __getattr__(self, item):
        return change_operation(self, item)
    


# In[30]:


number = StrangeFloat(6)


# In[31]:


number.add_1


# In[32]:


number.subtract_20


# In[33]:


number.multiply_5


# In[34]:


number.divide_25


# In[35]:


number.add_1.add_2.multiply_6.divide_8.subtract_9


# In[36]:


getattr(number, "add_-2.5")   # Используем getattr, так как не можем написать number.add_-2.5 - это SyntaxError


# In[37]:


number + 6   # Стандартные для float операции работают также


# In[38]:


number.as_integer_ratio()   # Стандартные для float операции работают также  (это встроенный метод float, писать его НЕ НАДО)


# # Задание 4 (3 балла)

# В данном задании мы немного отдохнём и повеселимся. От вас требуется заменить в данном коде максимально возможное количество синтаксических конструкций на вызовы dunder методов, dunder атрибутов и dunder переменных.
# 
# Маленькая заметка: полностью всё заменить невозможно. Например, `function()` можно записать как `function.__call__()`, но при этом мы всё ещё не избавляемся от скобочек, так что можно делать так до бесконечности `function.__call__.__call__.__call__.__call__.....__call__()` и при всём при этом мы ещё не избавляемся от `.` для доступа к атрибутам. В общем, замените всё, что получится, не закапываясь в повторы, как в приведённом примере. Чем больше разных методов вы найдёте и используете, тем лучше и тем выше будет балл
# 
# Код по итогу дожен работать и печатать число **4420.0**, как в примере. Структуру кода менять нельзя, просто изменяем конструкции на синонимичные
# 
# И ещё маленькая подсказка. Заменить здесь можно всё кроме:
# + Конструкции `for ... in ...`:
# + Синтаксиса создания лямбда функции
# + Оператора присваивания `=`
# + Конструкции `if-else`

# In[39]:


import numpy as np


matrix = []
for idx in range(0, 100, 10):
    matrix += [list(range(idx, idx + 10))]
    
selected_columns_indices = list(filter(lambda x: x in range(1, 5, 2), range(len(matrix))))
selected_columns = map(lambda x: [x[col] for col in selected_columns_indices], matrix)

arr = np.array(list(selected_columns))

mask = arr[:, 1] % 3 == 0
new_arr = arr[mask]

product = new_arr @ new_arr.T

if (product[0] < 1000).all() and (product[2] > 1000).any():
    print(product.mean())


# In[40]:


import numpy as np


matrix = []
for idx in range(0, 100, 10):
    matrix.__iadd__([list.__call__(range(idx, idx.__add__(10)))])
    
selected_columns_indices = list.__call__(filter.__call__(lambda x: x in range(1, 5, 2), range(matrix.__len__())))
selected_columns = map(lambda x: list.__call__(x.__getitem__(col) for col in selected_columns_indices), matrix)

arr = np.array(list.__call__(selected_columns))

mask = arr[:, 1].__mod__(3).__eq__(0)
new_arr = arr.__getitem__(mask)

product = new_arr.__matmul__(new_arr.T)

if (all.__call__(product.__getitem__(0).__le__(1000))).__and__(any.__call__(product.__getitem__(2).__gt__(1000))):
    print.__call__(product.mean().__str__())


# # Задание 5 (10 баллов)

# Напишите абстрактный класс `BiologicalSequence`, который задаёт следующий интерфейс:
# + Работа с функцией `len`
# + Возможность получать элементы по индексу и делать срезы последовательности (аналогично строкам)
# + Вывод на печать в удобном виде и возможность конвертации в строку
# + Возможность проверить алфавит последовательности на корректность
# 
# Напишите класс `NucleicAcidSequence`:
# + Данный класс реализует интерфейс `BiologicalSequence`
# + Данный класс имеет новый метод `complement`, возвращающий комплементарную последовательность
# + Данный класс имеет новый метод `gc_content`, возвращающий GC-состав (без разницы, в процентах или в долях)
# 
# Напишите классы наследники `NucleicAcidSequence`: `DNASequence` и `RNASequence`
# + `DNASequence` должен иметь метод `transcribe`, возвращающий транскрибированную РНК-последовательность
# + Данные классы не должны иметь <ins>публичных методов</ins> `complement` и метода для проверки алфавита, так как они уже должны быть реализованы в `NucleicAcidSequence`.
# 
# Напишите класс `AminoAcidSequence`:
# + Данный класс реализует интерфейс `BiologicalSequence`
# + Добавьте этому классу один любой метод, подходящий по смыслу к аминокислотной последовательности. Например, метод для нахождения изоэлектрической точки, молекулярного веса и т.д.
# 
# Комментарий по поводу метода `NucleicAcidSequence.complement`, так как я хочу, чтобы вы сделали его опредедённым образом:
# 
# При вызове `dna.complement()` или условного `dna.check_alphabet()` должны будут вызываться соответствующие методы из `NucleicAcidSequence`. При этом, данный метод должен обладать свойством полиморфизма, иначе говоря, внутри `complement` не надо делать условия а-ля `if seuqence_type == "DNA": return self.complement_dna()`, это крайне не гибко. Данный метод должен опираться на какой-то общий интерфейс между ДНК и РНК. Создание экземпляров `NucleicAcidSequence` не подразумевается, поэтому код `NucleicAcidSequence("ATGC").complement()` не обязан работать, а в идеале должен кидать исключение `NotImplementedError` при вызове от экземпляра `NucleicAcidSequence`
# 
# Вся сложность задания в том, чтобы правильно организовать код. Если у вас есть повторяющийся код в сестринских классах или родительском и дочернем, значит вы что-то делаете не так.
# 
# 
# Маленькое замечание: По-хорошему, между классом `BiologicalSequence` и классами `NucleicAcidSequence` и `AminoAcidSequence`, ещё должен быть класс-прослойка, частично реализующий интерфейс `BiologicalSequence`, но его писать не обязательно, так как задание и так довольно большое (правда из-за этого у вас неминуемо возникнет повторяющийся код в классах `NucleicAcidSequence` и `AminoAcidSequence`)

# In[41]:


from abc import ABC, abstractmethod

class BiologicalSequence(ABC):
    
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self, slc):
        pass
    
    @abstractmethod
    def __str__(self):
        pass
    
    @abstractmethod
    def check_alphabet(self):
        pass
    
    
class SequenceIncorrectionError(Warning):  
    
    def __str__(cls):
        return 'Your sequence does not match with alphabet. See standart alphabet of class using attribute .alphabet'


# In[42]:


class ClassicalPolymer(BiologicalSequence):
    
    def __init__(self, sequence):
        self.sequence = sequence
        self.standard_alphabet = {'DNA' : {'t', 'g', 'c', 'a'},
                                  'RNA' : {'u', 'g', 'c', 'a'},
                                  'Protein' : {'a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n','p', 'q', 'r', 's', 't', 'v', 'w', 'y'}}
    
    def __len__(self):
        return len(self.sequence)

    def __getitem__(self, slc):
        return type(self)(self.sequence[slc])
    
    def __str__(self):
        return str(self.sequence)
    
    def __repr__(self):
        return 'Sequence: ' + str(self.sequence)
    
    def check_alphabet(self):
        if isinstance(self, DNASequence):
            self.alphabet = self.standard_alphabet['DNA']
        elif isinstance(self, RNASequence):
            self.alphabet = self.standard_alphabet['RNA']
        elif isinstance(self, AminoAcidSequence):
            self.alphabet = self.standard_alphabet['Protein']
        else:
            raise BaseException('Nonstandard input')   # in case of carbohydrates in future
            
        if set(self.sequence.lower()) <= self.alphabet:
            return True
        else:
            raise SequenceIncorrectionError


# In[43]:


class NucleicAcidSequence(ClassicalPolymer):
    
    def complement(self):
        if isinstance(self, DNASequence) or isinstance(self, RNASequence): 
            table = str.maketrans('aAgGcCtTuU', 'tTcCgGaAaA')
            return type(self)(self.sequence.translate(table))
        else:
            raise NotImplementedError('Only for DNA and RNA subclasses') 
    
    def gc_content(self):
        return self.sequence.lower().count('g' and 'c') / len(self)
    
class AminoAcidSequence(ClassicalPolymer):
    
    def charge(self):
        return self.sequence.lower().count('e' and 'd') * -1 + self.sequence.lower().count('k' and 'r')
        
    def lazy_mass(self):
        print('Use, if you are really lazy or you very like my classes')
        return len(self.sequence) * 110
              


# In[44]:


class DNASequence(NucleicAcidSequence):
    
    # transcribe according to coding chain
    def transcribe(self):     
        table = str.maketrans('aAgGcCtT', 'uUcCgGaA')
        return type(self)(self.sequence.translate(table))
    
class RNASequence(NucleicAcidSequence):
    pass


# Пример DNASequence: длина, слайсы, вывод repr

# In[45]:


dna = DNASequence('ACGTATT')


# In[46]:


part_dna = dna[0:4]


# In[47]:


part_dna


# In[48]:


len(dna)


# Особые свойства DNASequence: complement, gc_content, transcribe (в том числе строчные)

# In[49]:


dna.complement()


# In[50]:


small_dna = DNASequence('ACGTATT'.lower())


# In[51]:


small_dna.complement()


# In[52]:


dna.gc_content()


# In[53]:


dna.transcribe()


# Свойства RNASequence, вывод на печать и вывод алфавита

# In[54]:


rna = RNASequence('ACGUACU')


# In[55]:


print(rna)


# In[56]:


rna.check_alphabet()


# In[57]:


rna.alphabet


# In[58]:


rna.gc_content()


# AminoAcidSequence и ошибка при некорректном алфавите

# In[59]:


nonprotein = AminoAcidSequence('UUUU')


# In[60]:


nonprotein.check_alphabet()


# In[61]:


protein = AminoAcidSequence('CYIGNCPLG')


# In[62]:


protein.check_alphabet()


# In[63]:


protein.charge()


# In[64]:


protein.lazy_mass()


# In[65]:


nucl_acid = NucleicAcidSequence('ACGT')


# In[66]:


nucl_acid.complement()

