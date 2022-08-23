



if __name__ == '__main__':
    lines = [line.strip("\r\n ").split(' ')[0] for line in open('refined_origin.txt')]
    for line in set(lines):
        print(line)