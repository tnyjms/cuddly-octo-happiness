import sys
from elftools.elf.elffile import ELFFile


def process_file(filename):
    print('Processing file:', filename)
    with open(filename, 'rb') as f:
        elffile = ELFFile(f)
        code_section = '.text'
        for section in elffile.iter_sections():
            print (section.name)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        process_file(sys.argv[1])
