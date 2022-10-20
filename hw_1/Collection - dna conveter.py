# dna/rna convert program

# dictionary for complement, transcription reverse transcription
DICT_COMPLEMENT = {'A': ('T', 'U'), 'T': ('A', 'A'),
                   'C': ('G', 'G'), 'G': ('C', 'C'),
                   'a': ('t', 'u'), 't': ('a', 'a'),
                   'c': ('g', 'g'), 'g': ('c', 'c'),
                   'u': ('a', 'a'), 'U': ('A', 'A')}
DICT_TRANSCRIPT = {'A': 'U', 'T': 'A', 'C': 'G', 'G': 'C',
                   'a': 'u', 't': 'a', 'c': 'g', 'g': 'c'}
DICT_REVERSE_TRANS = {'A': 'T', 'U': 'A', 'C': 'G', 'G': 'C',
                      'a': 't', 'u': 'a', 'c': 'g', 'g': 'c'}


# function for complement, transcription and reverse transcription
def fun_complement(seq, dictionary, dna_rna):
    output = []
    for nucl in seq:
        output += dictionary[nucl][dna_rna]
        output = ''.join(output)
    return output


# function for reverse sequence
def fun_reverse(seq):
    return seq[::-1]


# function for reverse complement
def fun_reverse_complement(seq, dictionary):
    output = foo_reverse(foo_complement(seq, dictionary))
    return output


# function for potential CpG-methylation
def fun_methylation(seq):
    output = seq.lower()
    return output.replace('cg', 'm5CG')


# dictionary command: function
dict_command = {"complement": fun_complement, "transcribe": fun_complement,
                "reverse transcription": fun_complement, "reverse": fun_reverse,
                "methylation": fun_methylation, "reverse complement": fun_reverse_complement}
# dictionary command: dictionary of letters
dict_command_letter = {"complement": DICT_COMPLEMENT, "transcribe": DICT_TRANSCRIPT,
                       "reverse transcription": DICT_REVERSE_TRANS, "reverse complement": DICT_COMPLEMENT,
                       "reverse": 0, "methylation": 0}

# body of program
while True:
    # read input command
    command = input('Enter command: ')
    mistake_command = command in ("complement", "transcribe", "reverse transcription",
                                  "reverse complement", "reverse", "methylation")

    # check exit, else read input sequence
    if command == 'exit':
        print('Good luck')
        break
    elif mistake_command == 0:
        print('Unrecognized command')
        continue
    sequence = input('Enter sequence: ')

    # check mistakes: T&U together and inconsistent letter
    nucleotide_list = ('a', 't', 'g', 'c', 'u', 'A', 'T', 'G', 'C', 'U')

    for i in sequence:
        dna_rna_mistake = {'u', 't'} <= set(sequence.lower())
        if i not in nucleotide_list or dna_rna_mistake == 1:
            print('Try again!')
            sequence = input('Enter sequence: ')

    # output through dictionaries
    dict_option = dict_command_letter[command]
    if dict_option == 0:
        print(dict_command[command](sequence))
    elif dict_option == DICT_COMPLEMENT:
        rna_check = {'u'} <= set(sequence.lower())
        print(dict_command[command](sequence, dict_option, rna_check))
    else:
        print(dict_command[command](sequence, dict_option))
