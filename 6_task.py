import numpy as np
import re


def char_delete(text):
    reg = re.compile(r'[^a-zа-я ]')
    result = reg.sub('', text)

    return result


class file_read():
    def __init__(self, read_from_file, filepathes_or_text=''):
        if read_from_file and filepathes_or_text:
            if isinstance(filepathes_or_text, str):
                files = [filepathes_or_text]
            else:
                files = list(filepathes_or_text)
            try:
                files = map(lambda x: open(x, 'r', errors='ignore').read().lower(), files)
                texts = ''
                for text in files:
                    texts += text + '\n'
            except UnicodeDecodeError:
                print('Decode error. Exiting...')
                sys.exit(1)
            self.text = np.array(char_delete(texts).split())
        elif not read_from_file and filepathes_or_text:
            self.text = np.array(char_delete(filepathes_or_text.lower()).split())
        else:
            print('Creating empty file read class.')
            self.text = filepathes_or_text


class n_gramm(file_read):
    def __init__(self, read_from_file, filepath_or_text='', auto_choose=True, prefix_number=1):
        super().__init__(read_from_file, filepath_or_text)
        self.auto_choose = auto_choose
        self.gram_dict = {}

    def gram_form(self, text, prefix_number):
        if self.auto_choose:
            chosen = np.random.choice(np.arange(len(text)))
            prefix = [text[chosen + index] for index in range(prefix_number)]
            prefix_dt = tuple(text[index] for index in range(chosen, chosen + prefix_number))
        else:
            prefix = input('Input prefix/prefixes: ').lower().split()
            prefix_dt = tuple(prefix)
            prefix_number = len(prefix)
        match_indexes = np.where(text == prefix[0])[0]
        match_indexes = self.find_match_indexes(text, prefix_number, match_indexes, prefix)
        word = np.array([text[pos + prefix_number] for pos in match_indexes[0] if pos + prefix_number < len(text)])
        unique = np.unique(word)
        self.gram_dict = {prefix_dt: [(unique[i], len(np.where(unique[i] == word)[0]) / len(word))
                                      for i in range(len(unique))]}

    def find_match_indexes(self, text, prefix_number, match_indexes, prefix):
        truth_matches = []
        for match_index in match_indexes:
            if match_index + prefix_number < len(text):
                for index in range(1, prefix_number):
                    if text[match_index + index] != prefix[index]:
                        break
                else:
                    truth_matches.append(match_index)
        return np.array([truth_matches])

    def __repr__(self):
        return str(self.gram_dict)


if __name__ == '__main__':
    import sys, os

    input_dir, prefix = '', 0
    if len(sys.argv) > 1:
        try:
            os.listdir(sys.argv[1])
        except FileNotFoundError:
            prefix = sys.argv[1]
        else:
            input_dir = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            os.listdir(sys.argv[2])
        except FileNotFoundError:
            prefix = sys.argv[2]
        else:
            input_dir = sys.argv[2]

    read_from_file = True if input_dir else False
    if read_from_file:
        texts = os.listdir(input_dir)
        texts = [texts[index] for index in range(len(texts)) if texts[index].endswith('.txt')]
    else:
        texts = input('Input your text:\n')

    while True:
        mode = input('Which mode do you want to use? Auto choose or manual write of prefix: a/m?\n')
        if mode and mode.lower()[0] == 'm':
            mode = False
            break
        else:
            mode = True
            break

    if not prefix:
        while True:
            try:
                prefix = int(input('Input prefix words count:\t'))
            except ValueError:
                pass
            else:
                break

    n_gramm_object = n_gramm(read_from_file, texts, mode, int(prefix))
    print('\nWork with parameters: read from file - ' + str(read_from_file) + ', auto choose - ' +
          str(n_gramm_object.auto_choose) + ', prefix words - ' + str(prefix) + '\n')
    while True:
        n_gramm_object.gram_form(n_gramm_object.text, prefix_number=int(prefix))
        print(n_gramm_object, sep='\n\n')
        args = input('Continue: Enter; Exit: n\n')
        if args and args.lower()[0] == 'n':
            break
