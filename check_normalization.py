def main():
    with open('normalization.TSV', 'r') as f:
        t = f.read()
    f.close()
    lines = t.splitlines()

    duplicates = {}
    for line in lines:
        key = line.split('\t')[0]
        value = line[-1] # get the last character of the line
        if key in duplicates and duplicates[key] != value:
            print(key)
        else:
            duplicates[key] = value
    
    with open('normalization.TSV', 'r') as f:
        t = f.read()
    f.close()
    lines = t.splitlines()

    for line in lines:
        hex_chars, rest_of_line = line.split('\t')
        char_list = hex_chars.split()
        unicode_str = ''.join([chr(int(c, 16)) for c in char_list])
        last_char = rest_of_line.strip()[-1]
        print(f"{unicode_str}\t{last_char}")

if __name__ == '__main__':
    main()