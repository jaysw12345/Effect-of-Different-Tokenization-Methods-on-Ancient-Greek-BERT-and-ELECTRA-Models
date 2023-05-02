import re
import time
import random
import copy

def main():
    character_overlap_threshold = 50
    success_rate = 7 / 11

    is_wordpiece = False
    is_unigram = True
    is_old = False

    if is_wordpiece:
        with open('25k_wordpiece.txt', 'r') as f:
            t = f.read()
        f.close()

    elif is_unigram:
        with open('50k_unigram.txt', 'r') as f:
            t = f.read()
        f.close()

    elif is_old:
        with open('Desi_chunked.txt', 'r') as f:
            t = f.read()
        f.close()

    t_split = t.split('\n')
    print("length of t_split")
    print(len(t_split))

    new_ls = []

    # split sentences
    for i in t_split:
        new_ls.append(i)

    # make a train and validation set of 15% and 85 % of the data    
    split_index = int(len(new_ls) * 0.15)

    random.shuffle(new_ls)
    temp_val_list = new_ls[:split_index]
    val_list = []
    train_list = new_ls[split_index:]

    train_hashes = [set() for _ in range(100)]

    count = 1

    # print("Train list length:")
    # print(len(train_list))


    # split sentences
    for unit in train_list:
        if (count % int((len(train_list) / 100 )) == 0):
            print(count)
        for i in range(len(unit) - character_overlap_threshold):
            n = count % 100
            train_hashes[n].add(unit[i:i+character_overlap_threshold])
        count += 1

    print("length of temp_val_list")
    print(len(temp_val_list))

    val_rejects = set()

    finished = False

    first_loop = True

    while not finished:
        count = 1
        print("Is Finished?")
        print(finished)
        finished = True
        val_list = []
        for unit in temp_val_list:
            if (count % int((len(temp_val_list) / 100 )) == 0):
                print(count)

            isValid = True
            for i in range(len(unit) - character_overlap_threshold):
                if first_loop:
                    for train_hash in train_hashes:
                        # if unit[i:i+character_overlap_threshold] in train_hash:
                        if unit[i:i+character_overlap_threshold] in train_hash:
                            isValid = False
                            break
                else:
                    if unit[i:i+character_overlap_threshold] in val_rejects:
                            isValid = False
                            break
            if isValid:
                val_list.append(unit)
            else:
                train_list.append(unit)
                for i in range(len(unit) - character_overlap_threshold):
                    val_rejects.add(i)
                finished = False
            count += 1
        if not finished:
            temp_val_list = copy.deepcopy(val_list)
        first_loop = False

    if is_wordpiece:
        with open('25k_val_wordpiece.txt', 'w') as h:
            for sent in val_list:
                h.write("{}\n".format(sent))

        with open('25k_train_wordpiece.txt', 'w') as h:
            for sent in train_list:
                h.write("{}\n".format(sent))

    elif is_unigram:
        with open('50k_val_unigram.txt', 'w') as h:
            for sent in val_list:
                h.write("{}\n".format(sent))

        with open('50k_train_unigram.txt', 'w') as h:
            for sent in train_list:
                h.write("{}\n".format(sent))

    elif is_old:
        with open('val_Desi.txt', 'w') as h:
            for sent in val_list:
                h.write("{}\n".format(sent))

        with open('train_Desi.txt', 'w') as h:
            for sent in train_list:
                h.write("{}\n".format(sent))

    print(len(val_list))
    print(len(train_list))

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s minutes ---" % ((time.time() - start_time) / 60))