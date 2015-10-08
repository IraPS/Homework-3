__author__ = 'IrinaPavlova'

import re
from lxml import etree


punctuation = set('!"#$%&()*+,-./:;<=>?@[\]^_`{|}~—–\'«»0123456789')


def prepare_file(file):
    prepare = open(file, 'r', encoding='utf-8')
    res = prepare.read()
    res = re.sub('<mediawiki .*>', '<mediawiki>', res)
    prepare.close()
    prepare = open(file, 'w', encoding='utf-8')
    prepare.write(res)
    prepare.close()


def parse(file):
    prepare_file(file)
    tree = etree.parse(file)
    return tree


def get_page(file):
    page = parse(file).xpath('.//page')
    return page


def get_title(file):
    for e in get_page(file):
        title = e.xpath('.//title')
        for el in title:
            title = el.text
            yield title


def get_text(file):
    for ele in get_page(file):
        text = ele.xpath('.//revision//text')
        for elem in text:
            text = elem.text
            if text is not None:
                yield text


def get_len_text(file):
    for eleme in get_text(file):
        eleme = eleme.split()
        if eleme is not None:
            yield len(eleme)
        else:
            yield 0


def count_links(file):
    m = re.compile('\[\[[^:]*?\]\]')
    for elemen in get_text(file):
        if elemen is not None:
            elemen = len(m.findall(elemen))
            yield elemen
        else:
            yield 0


def c(file):
    for h in get_text(file):
        d = {}
        h = ''.join(z for z in h if z not in punctuation)
        h = h.lower()
        h = h.split()
        for word in h:
            if word not in d:
                n = 1
                d[word] = n
            else:
                d[word] += 1
        yield d


def a(file):
    alld = []
    for element in c(file):
        alld.append(element)
    return alld


def combine_values(file):
    allv = []
    for q, w, e in zip(get_title(file), get_len_text(file), count_links(file)):
        allv.append((q, w, e))
    return allv


def freq_dict(file):
    fd = {}
    for d in a(file):
        for key, value in d.items():
            if fd.get(key) is None:
                fd[key] = d[key]
            else:
                fd[key] += d[key]
    return [(k, v) for v, k in sorted([(v, k) for k, v in fd.items()], reverse=True)]


def write_info(file):
    with open('Articles_info.csv', 'w', encoding='utf-8') as out:
        out.write('Title;' + 'Length;'+'Count of links;\n')
        for row in combine_values(file):
            for column in row:
                out.write('%s;' % column)
            out.write('\n')
    out.close()


def write_freq(file):
    with open('Frequency_dictionary.csv', 'w', encoding='utf-8') as out:
        out.write('Word;' + 'Frequency;\n')
        for u in freq_dict(file):
            out.write(u[0] + ';' + str(u[1]) + ';\n')
    out.close()


dump = 'dump.xml'
write_info(dump)
write_freq(dump)

