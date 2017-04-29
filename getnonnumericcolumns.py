file = "/home/binderchri/kddcup1999/kddcup.data.corrected"
delim = ","

# http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float-in-python
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


invalidColumns = list()
countOfColumns = 0

with open(file) as f:
    for line in f.readlines():
        splitted = line.split(delim)
        if len(splitted) > countOfColumns:
            countOfColumns = len(splitted)

        for idx, val in enumerate(splitted):
            if not is_number(val) and not idx in invalidColumns:
                invalidColumns.append(idx)

print("total columns: ", countOfColumns)
print("non-numeric columns, zero-based:", invalidColumns)

validColumns = [i for i in range(countOfColumns) if i not in invalidColumns]
print("numeric columns, zero-based:", validColumns)

# https://unix.stackexchange.com/questions/222121/how-to-remove-a-column-or-multiple-columns-from-file-using-shell-command
cutcommand = "cut -f{} -d\"{}\" {}".format(",".join([str(i+1) for i in validColumns]),
                                       delim,
                                       file)
print(cutcommand)

# results:
# non-numeric columns, zero-based: [1, 2, 3, 41]

#total columns:  42
#non-numeric columns, zero-based: [1, 2, 3, 41]
#numeric columns, zero-based: [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
#cut -f1,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41 -d"," /tmp/ass2/test.txt
