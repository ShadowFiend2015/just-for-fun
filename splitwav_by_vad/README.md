## 编译方法
* `go build .`

## 使用方法
* 先用`go build .`编译生成 splitwav
### 默认标准单次切割音频
* `sh split.sh`
### 以10为步长，vad_prob_start 和 vad_prob_continue 分别从9--99 共 10\*10=100 次切割音频。
* `sh batch_split.sh`
### 查看单个文件结尾平均分贝数
* `python cal_pcm_tail.py -t <int(ms)> -f <name1.pcm> <name2.pcm>...` -t 默认为 1000ms
### 批量查看文件结尾平均分贝数
* `sh batch_statis.sh` 

## 输出
### 切割
* 放到 `<音频名>-<vad_prob_start>_<vad_prob_continue>` 文件夹下，音频名为：1.pcm, 2.pcm……，有序
### 统计
* 单个：输出 tail 长度平均，tail长度等长 10 份的平均，同文件夹下所有切割结果音频的 tail 长度平均
* 批量：输出到第个文件夹下的 statis.log里，终端输出按不同 start, continue 切割后的总平均排序后的结果。
