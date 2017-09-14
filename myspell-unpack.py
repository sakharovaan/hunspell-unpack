import sys, getopt

USAGE_STR = """usage: myspell-unpack.py -i <dict_prefix> -o <output_file>
      
For example:

python3 en_us words.txt
(This means that en_us.aff and en_us.dic both are in the same directory where script is and words.txt will be generated there)
"""


def parse_cmd(argv):
    inputfile = ''
    outputfile = ''

    if len(argv) < 2:
        print(USAGE_STR)
        sys.exit(2)
    else:
        argv = argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["i=", "o="])
    except getopt.GetoptError:
        print(USAGE_STR)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(USAGE_STR)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    return inputfile, outputfile


if __name__ == "__main__":
    prefix, output_file = parse_cmd(sys.argv)
    afffix_dict = {}
    
    with open('%s.aff' % prefix) as f:
        for line in f.readlines():
            aff_type, aff_data = line.split(' ', 1)
            if aff_type in afffix_dict:
                afffix_dict[aff_type].append(aff_data.strip())
            else:
                afffix_dict[aff_type] = [aff_data.strip()]

    suffix_dict = {}
    for suffix in afffix_dict['SFX']:
        suff_key, *data = suffix.split()
        if len(data) > 2: # don't need suffix class and number of causes
            if suff_key in suffix_dict:
                suffix_dict[suff_key][data[0]] = {'suffix': data[1], 'replace': data[2]}
            else:
                suffix_dict[suff_key] = {data[0]: {'suffix': data[1], 'replace': data[2]}}

    out_f = open(output_file, mode='w')

    with open('%s.dic' % prefix) as f:
        f.readline() # pass header
        for line in f.readlines():
            word, *word_suff = line.split('/')
            word = word.strip()

            if len(word_suff) > 0:
                word_suff = word_suff[0].split(',')

            out_f.write(word + '\n')
            for suffix in word_suff:
                suffix = suffix.strip()

                if suffix in suffix_dict:
                    for k, v in suffix_dict[suffix].items():
                        if k == '0' or word.endswith(k):
                            if v['replace'] == '.':
                                out_f.write(word + v['suffix'])
                            else:
                                out_f.write(v['suffix'].join(word.rsplit(v['replace'], 1)))

                        out_f.write('\n')



                else:
                    print('Suffix no %s not found in affix file ' % suffix)

    out_f.flush()
    out_f.close()