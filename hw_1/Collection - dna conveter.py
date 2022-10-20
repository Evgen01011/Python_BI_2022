# dna/rna convert program

# dictionary for complement, transcription reverse transcription
dict_complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C',
                   'a': 't', 't': 'a', 'c': 'g', 'g': 'c'}
dict_transcript = {'A': 'U', 'T': 'A', 'C': 'G', 'G': 'C',
                   'a': 'u', 't': 'a', 'c': 'g', 'g': 'c'}
dict_reverse_trans = {'A': 'T', 'U': 'A', 'C': 'G', 'G': 'C',
                      'a': 't', 'u': 'a', 'c': 'g', 'g': 'c'}


# function for complement, transcription and reverse transcription
def foo_common(seq, dictionary):
    output = str()
    for j in range(len(seq)):
        output += dictionary[seq[j]]
    return output


# function for reverse sequence
def foo_reverse(seq):
    return seq[::-1]


# function for reverse complement
def foo_reverse_complement(seq, dictionary):
    output = str()
    for j in range(len(seq)-1, -1, -1):
        output += dictionary[seq[j]]
    return output


# function for potential CpG-methylation
def foo_methylation(seq):
    output = seq.lower()
    return output.replace('cg', 'm5CG')


# dictionary command: function
dict_command = {"complement": foo_common, "transcribe": foo_common,
                "reverse transcription": foo_common, "reverse": foo_reverse,
                "methylation": foo_methylation, "reverse complement": foo_reverse_complement}
# dictionary command: dictionary of letters
dict_command_letter = {"complement": dict_complement, "transcribe": dict_transcript,
                       "reverse transcription": dict_reverse_trans, "reverse complement": dict_complement,
                       "reverse": 0, "methylation": 0}

# body of program
while True:
    # read input command
    command = str(input('Enter command: '))

    # check exit, else read input sequence
    if command == 'exit':
        print('Good luck')
        break
    sequence = str(input('Enter sequence: '))

    # check mistakes: T&U together and inconsistent letter
    nucleotide_list = ('a', 't', 'g', 'c', 'u')
    i = 0
    sequence_low = sequence.lower()
    while i < len(sequence):
        dna_rna_mistake = sequence_low.count('t') * sequence_low.count('u')
        if sequence_low[i] not in nucleotide_list or dna_rna_mistake != 0:
            print('Try again!')
            sequence = str(input('Enter sequence: '))
            sequence_low = sequence.lower()
            i = 0
        else:
            i += 1

    # output through dictionaries
    dict_option = dict_command_letter[command]
    if dict_option != 0:
        print(dict_command[command](sequence, dict_option))
    else:
        print(dict_command[command](sequence))
