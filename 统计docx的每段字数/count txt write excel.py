# 统计txt里每段的字数，标点数，标点之间的字数(不算书名号)。结果写入excel(xlsx)。

import re, xlsxwriter, chardet

filename = 'test.txt'
result_file = 'result.xlsx'

def read_txt(filename):
    fencoding = chardet.detect(open(filename, 'rb').read())['encoding']
    print(fencoding)
    try:
        txtfile = open(filename, 'r', encoding=fencoding)
    except IOError as e:
        print(e)
        return None
    result = []
    lines = txtfile.readlines()
    for idx, par in enumerate(lines):
        par_result = []
        par_result.append(idx + 1)
        par = par[:-2]
        words = re.split('，|。|？|！', par)
        # print(words)
        par_result.append(len(words) - 1)
        word_len = 0
        for word in words:
            word = word.replace('《', '')
            word = word.replace('》', '')
            if len(word) == 0:
                continue
            par_result.append(len(word))
            word_len += len(word)
        par_result.insert(1, word_len)
        result.append(par_result)
    result.sort(key=lambda x: x[1])
    return result

def write_xlsx(xlsx_name, txt_result):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(xlsx_name)
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Initialize the sheet
    worksheet.write(row, col, '行号')
    worksheet.write(row, col + 1, '行字数')
    worksheet.write(row, col + 2, '行标点数')
    worksheet.write(row, col + 3, '标点间字数')

    row += 1

    # Iterate over the data and write it out row by row.
    for line in txt_result:
        for num in line:
            worksheet.write(row, col, num)
            col += 1
        row += 1
        col = 0

    # Write a total using a formula.
    # worksheet.write(row, 0, 'Total')
    # worksheet.write(row, 1, '=SUM(B1:B4)')

    workbook.close()


if __name__ == "__main__":
    txt_result = read_txt(filename)
    write_xlsx(result_file, txt_result)
    print('Well Done!')

