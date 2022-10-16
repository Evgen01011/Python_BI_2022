# global filtering function
def main(input_fastq, output_file_prefix, gc_bounds=(20, 80),
         length_bounds=(0, 2 ** 32), quality_threshold=0, save_filtered=False):

    # dictionary for positive and negative selection of reads
    dict_selection = {0: [], 1: []}

    # create additional variable; it's allow to not read entire file
    i = 0
    sep_line = []

    # filtering function according to GC-content of sequence
    def gc_count(sequence, gc_broad=gc_bounds):
        if type(gc_broad) != tuple:                          # in case one variable
            gc_broad = (0, gc_broad)
        min_gc, max_gc = gc_broad
        gc_percent = (sequence.count('G')+sequence.count('C'))*100/len(sequence)
        if min_gc <= gc_percent <= max_gc:
            return 1
        else:
            return 0

    # filtering function according to length of sequence
    def length_threshold(sequence, length_broads=length_bounds):
        if type(length_broads) != tuple:                             # in case one variable
            length_broads = (0, length_broads)
        min_length, max_length = length_broads
        if min_length <= len(sequence) <= max_length:
            return 1
        else:
            return 0

    # filtering function according to quality of reading
    def quality_estimation(askii_quality, quality_threshold1=quality_threshold):
        mean_quality = sum([ord(symbol)-33 for symbol in askii_quality])/len(askii_quality)  # convert askii into number
        if mean_quality >= quality_threshold1:
            return 1
        else:
            return 0

    # read file dividing it by 4 lines
    with open(input_fastq, 'r') as file:
        for line in file:
            if i < 4:
                i += 1
            else:
                dict_selection[gc_count(sep_line[1]) * length_threshold(sep_line[1])
                               * quality_estimation(sep_line[3])] += sep_line           # location in dictionary
                i = 1
                sep_line.clear()
            sep_line.append(line)
    # output
    if save_filtered == 0:
        with open(''.join((output_file_prefix, '_passed.fastq')), 'w') as out_passed:
            for value in dict_selection[1]:
                out_passed.write("%s" % value)
    else:
        with open(''.join((output_file_prefix, '_passed.fastq')), 'w') as out_passed, \
             open(''.join((output_file_prefix, '_filtered.fastq')), 'w') as out_filtered:
            for value in dict_selection[1]:
                out_passed.write("%s" % value)
            for value in dict_selection[0]:
                out_filtered.write("%s" % value)
