## 编译方法
* `go build .`

## 使用方法
* `-config` 配置文件
* `-f` 音频文件(pcm/wav)
* 详见 run.sh

## 输出
* 将音频每 20ms 切片进行 vad 检测。0：静音，1：有输入。
* 每 50 个结果(1s)一换行。
