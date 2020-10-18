class colors :
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    cyan = '\u001b[36;1m'
    red = '\u001b[31;1m'

def create_table(headers, datas):
    n_headers = len(headers)
    lengths = []
    for i in range(n_headers):
        length = len(headers[i])
        for data in datas[i]:
            if length < len(data):
                length = len(data)
        lengths.append(length)
    for i in range(n_headers):
        print('+',end='')
        print('-'*(lengths[i] + 2), end='')
        if i + 1 == n_headers:
            print('+')
    for i in range(n_headers):
        print('|', headers[i], ' '*(lengths[i] - len(headers[i])), end='')
        if i + 1 == n_headers:
            print('|')
    for i in range(n_headers):
        print('+',end='')
        print('-'*(lengths[i] + 2), end='')
        if i + 1 == n_headers:
            print('+')
    lines = len(datas[i])
    for i in range(lines):
        for j in range(n_headers):
            print('|', datas[j][i],' '*(lengths[j] - len(datas[j][i])), end='')
        print('|')
    for i in range(n_headers):
        print('+',end='')
        print('-'*(lengths[i] + 2), end='')
        if i + 1 == n_headers:
            print('+')

if __name__ == "__main__" :
    create_table(['ab', 'bcdvdvdfvdc', 'cd'],[['ab', 'bcdvdvdfvdc', 'cd'],['ab', 'bcdvdvdfvdc', 'cd'], ['ab', 'bcdvdvdfvdc', 'cd']])