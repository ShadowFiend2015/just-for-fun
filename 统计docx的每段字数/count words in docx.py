# 统计word(.docx)里每段的字数，标点数，标点之间的字数。(不算书名号)

import docx, re

filename = 'testfile.docx'
doc = docx.Document(filename)

def func(doc):
    result = []
    for idx, par in enumerate(doc.paragraphs):
        par_result = []
        par_result.append(idx + 1)
        words = re.split('，|。|？|！', par.text)
        par_result.append(len(words) - 1)
        word_len = 0
        for word in words:
            if len(word) == 0:
                continue
            word = word.replace('《', '')
            word = word.replace('》', '')
            par_result.append(len(word))
            word_len += len(word)
        par_result.insert(1, word_len)
        result.append(par_result)
    result.sort(key=lambda x: x[1])
    return result

result = func(doc)
for r in result:
    print(r)
