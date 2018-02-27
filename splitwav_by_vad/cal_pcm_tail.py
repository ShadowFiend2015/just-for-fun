# 计算 wav 最后 1s(可调) 的平均分贝，以判断用 vad 的切割效果(有没有尾巴)。
import argparse
import math
import numpy

def cal_average_db(pcmfile, tail_frame):
    pcmdata = numpy.memmap(pcmfile, dtype='h', mode='r')
    pcmdata = pcmdata[-int(tail_frame * 16):]
    sum_db = 0
    data_range = pow(2, 15)
    dbs = []
    avg_dbs = []
    for data in pcmdata:
        temp_db = 20 * math.log10(abs(float(data)) / data_range) if data != 0 else -90
        dbs.append(temp_db)
        sum_db += temp_db
    for i in range(0, len(dbs), int(len(dbs)/10)):
        avg_dbs.append(int(sum(dbs[i:i+int(len(dbs)/10)])/(len(dbs)/10)))
    return avg_dbs, int(sum_db / len(pcmdata))


def new_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, nargs='+', help="name of pcm")
    parser.add_argument("-t", "--tail", type=int, default=1000, help="tail length of pcm(ms), default = 1000ms")
    return parser.parse_args()

if __name__ == '__main__':
    args = new_args()
    total_avg_db = 0
    file_num = 0
    for file in args.file:
        if file[-4:] != ".pcm":
            continue
        file_num += 1
        avg_dbs, avg_db = cal_average_db(file, args.tail)
        total_avg_db += avg_db
        print avg_db, avg_dbs
    total_avg_db /= file_num
    print(int(total_avg_db))

