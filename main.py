# text files obtained from: https://www.gutenberg.org/ebooks/11

import string
import re


def process_file(fname, enc):
    # open file for reading 'r'
    with open(fname, 'r', encoding=enc) as file:
        dat = file.read()  # read file
        dat = perform_re(dat)  # group the chapter headings together as one word: 'chapteriii'
    return dat.split()  # return read data, get rid of all white space


def write_results(fname, data, enc):
    # open a file for writing 'w'
    with open(fname, 'w', encoding=enc) as file:
        file.write(data)


def words_to_dict(all_words, dictionary):
    for w in all_words:  # for each word
        w = clean_word(w)  # send word for cleaning (get rid of punctuation and make everything lowercase)
        if w in dictionary:  # if word was counted before
            dictionary[w] += 1  # increment count
        else:
            dictionary[w] = 1  # begin count for new word


# get rid of punctuation and make everything lowercase
def clean_word(word):
    for p in string.punctuation:
        word = word.replace(p, "")  # delete punctuation  TODO: this doesn't get rid of quotations i.e. "word or word"
    return word.lower()


# uses regular expressions to clean up chapter headings
def perform_re(text):
    text = re.sub(r'(CHAPTER) ([IVXLC]+.)', '\\1\\2', text)
    return text


# ask user to choose a text to analyze
def get_user_input():
    while True:
        num_range = range(1, 6, 1)
        choice = input("\nChoose a text you want to compare: (1-5) ")
        if int(choice) in num_range:
            return int(choice)
        else:
            print("Invalid entry, try again.")


# takes a file, returns a list
def word_list(file):
    words = process_file(file, 'utf-8')
    return words


# takes a list, returns a dictionary with each unique word as the key and the count of that word as the value
def unique_words_dict(words):
    unique_words_counts = {}  # empty dictionary for unique words count
    words_to_dict(words, unique_words_counts)  # run through all words to get each word and count them
    return unique_words_counts


# takes a dictionary, returns a list of words that appear only once
def get_first_five(dictionary):
    # make a new list for the words that appear only one time in the text
    unique = []
    for key in dictionary.keys():
        if dictionary[key] == 1:
            unique.append(key)
    return unique[:5]


# return first five words in a list of words
def first_five(words):
    return words[:5]


# calculate the type to token ratio
def calc_TTR(unique_words, words):
    ttr = float(unique_words / words)
    return round(ttr, 3)


# find a word and its count in the text
def find_word(word, words):
    if word in words:
        count = words.count(word)
    else:
        count = 0
    return count


# calculate whether word count difference is less than 3000
def TTR_validity(difference):
    if difference <= 3000:
        return "These TTR values are between comparable texts."
    else:
        return "TTR is not a reliable comparison of lexical complexity for the chosen texts."


def main():
    # put the txt documents in a list with a parallel number list for display to user
    numbers = ['1 ', '2 ', '3 ', '4 ', '5 ']
    texts = ["alice.txt", "dorian-gray.txt", "frankenstein.txt", "mystics-of-islam.txt",
             "oxford-lectures-on-poetry.txt"]
    for number, text in zip(numbers, texts):
        print(number, text)

    # ask user which two texts to compare
    while True:
        try:
            choice1 = get_user_input()
            choice2 = get_user_input()
            break
        except ValueError:
            print("Invalid entry, try again.")

    # give the user statistics like total words, unique words, ttr
    text1 = texts[choice1 - 1]  # the file name to read in and process
    txt1_words = process_file(text1, 'utf-8')  # read in file with splits and regex cleanup to return a list
    txt1_unique = unique_words_dict(txt1_words)  # make the dictionary of unique words from the list of total words
    five = get_first_five(txt1_unique)  # a list of the first 5 unique words
    ttr1 = calc_TTR(len(txt1_unique), len(txt1_words))
    total_words1 = len(txt1_words)

    print('\nIn {0} there are {1:,} total words and {2:,} unique words.\nHere are the first five unique words {3}\n'
          '{0} has a TTR of {4}'.format(text1, total_words1, len(txt1_unique), five, ttr1))

    text2 = texts[choice2 - 1]  # the file name to read in and process
    txt2_words = process_file(text2, 'utf-8')  # read in file with splits and cleanup to return a list of all words
    txt2_unique = unique_words_dict(txt2_words)  # make the dictionary of unique words from the list of total words
    five = get_first_five(txt2_unique)  # a list of the first 5 unique words
    ttr2 = calc_TTR(len(txt2_unique), len(txt2_words))
    total_words2 = len(txt2_words)

    print('\nIn {0} there are {1:,} total words and {2:,} unique words.\nHere are the first five unique words {3}\n'
          '{0} has a TTR of {4}'.format(text2, total_words2, len(txt2_unique), five, ttr2))

    # ask user for another text to compare their choice to
    choice3 = get_user_input()

    text3 = texts[choice3 - 1]  # the file name to read in and process
    txt3_words = process_file(text3, 'utf-8')  # read in file with splits and cleanup to return a list of all words
    txt3_unique = unique_words_dict(txt3_words)  # make the dictionary of unique words from the list of total words
    five = get_first_five(txt3_unique)  # a list of the first 5 unique words
    ttr3 = calc_TTR(len(txt3_unique), len(txt3_words))
    total_words3 = len(txt3_words)

    print('\nIn {0} there are {1:,} total words and {2:,} unique words.\nHere are the first five unique words {3}\n'
          '{0} has a TTR of {4}'.format(text3, total_words3, len(txt3_unique), five, ttr3))

    # TODO: compare the ttr for each of the 3 texts chosen
    # if the total number of words of each text differs by 3000 words or less, tell user "TTR is between comparable
    # texts." Otherwise, tell them "TTR is not a reliable comparison for chosen texts."

    # put text names and word counts in a dictionary
    totals = {text3: total_words3, text2: total_words2, text1: total_words1}

    # sort dictionary values from least to greatest word count
    # reference: https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
    totals = sorted(totals.items(), key=lambda kv: (kv[1], kv[0]))

    # notes:
    # greatest word count = totals[2][1]
    # middle word count = totals[1][1]
    # smallest word count = totals[0][1]

    # get differences between word counts of all 3 texts
    diff1 = totals[2][1] - totals[1][1]
    print("\n{0} has {1:,} words, which is {2:,} more words than {3}".format(totals[2][0], totals[2][1], diff1,
                                                                             totals[1][0]))
    print(TTR_validity(diff1))

    diff2 = totals[2][1] - totals[0][1]
    print("\n{0} has {1:,} words, which is {2:,} more words than {3}".format(totals[2][0], totals[2][1], diff2,
                                                                             totals[0][0]))
    print(TTR_validity(diff2))

    diff3 = totals[1][1] - totals[0][1]
    print("\n{0} has {1:,} words, which is {2:,} more words than {3}".format(totals[1][0], totals[1][1], diff3,
                                                                             totals[0][0]))
    print(TTR_validity(diff3))

    # let the user search for a word in each of the first 2 texts they chose and display the results
    user_word = input("\nEnter a word to search in the texts: ")
    count1 = find_word(user_word, txt1_words)
    count2 = find_word(user_word, txt2_words)
    count3 = find_word(user_word, txt3_words)
    print(
        "'{0}' appears {1:,} time(s) in {2}, {3:,} time(s) in {4}, and {5:,} time(s) in {6}.".format(user_word, count1,
                                                                                                     text1,
                                                                                                     count2, text2,
                                                                                                     count3,
                                                                                                     text3))


if __name__ == "__main__":
    main()
