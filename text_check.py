import time

def find_overlap(file1, file2):
    with open(file1, 'r') as f1:
        text1 = f1.read()
    with open(file2, 'r') as f2:
        text2 = f2.read()

    print(len(text1))

    for i in range(len(text1)-49):
        if (i % int((len(text1) / 100 )) == 0):
            print(i)
        for j in range(len(text2)-49):
            if text1[i:i+25] == text2[j:j+50]:
                print(text1[i:i+50])
                print(text2[j:j+50])
                return True
    return False

def main():
    if find_overlap('super_mini_val_wordpiece.txt', 'super_mini_train_wordpiece.txt'):
        print('There is an overlap of at least 25 sequential characters between the two files')
    else:
        print('There is no overlap of at least 25 sequential characters between the two files')

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s minutes ---" % ((time.time() - start_time) / 60))