package main

import (
	"bufio"
	"flag"
	"fmt"
	"github.com/BurntSushi/toml"
	"io"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

type Options struct {
	FrameSize       int `toml:"frame_size"`
	SampleRate      int `toml:"sample_rate"`
	VadProbStart    int `toml:"vad_prob_start"`
	VadProbContinue int `toml:"vad_prob_continue"`
	MuteLength      int `toml:"mute_length"`
	PCMLength       int `toml:"pcm_length"`
	WavPath         string
	Delay           int `toml:"delay"`
}

func NewOptions() *Options {
	return &Options{
		FrameSize:       20,
		SampleRate:      16000,
		VadProbStart:    99,
		VadProbContinue: 99,
		MuteLength:      400,
		PCMLength:       5000,
		Delay:           10,
	}
}

func vadFlagSet() *flag.FlagSet {
	flagSet := flag.NewFlagSet("vad", flag.ExitOnError)
	flagSet.String("f", "", "wav/pcm file")
	flagSet.String("config", "", "config file path")
	flagSet.Int("vps", 0, "VadProbStart, 1~99")
	flagSet.Int("vpc", 0, "VadProbContinue, 1~99")
	return flagSet
}

func readConfig() *Options {
	opts := NewOptions()

	flagSet := vadFlagSet()
	flagSet.Parse(os.Args[1:])

	configFile := flagSet.Lookup("config").Value.String()
	if configFile != "" {
		_, err := toml.DecodeFile(configFile, &opts)
		if err != nil {
			log.Fatalf("ERROR: failed to load config file %s - %s", configFile, err.Error())
		}
	}
	wavPath := flagSet.Lookup("f").Value.String()
	if wavPath == "" {
		log.Fatalf("ERROR: wav/pcm file path can't be none")
	}
	opts.WavPath = wavPath
	vps, _ := strconv.Atoi(flagSet.Lookup("vps").Value.String())
	if vps != 0 {
		opts.VadProbStart = vps
	}
	vpc, _ := strconv.Atoi(flagSet.Lookup("vpc").Value.String())
	if vps != 0 {
		opts.VadProbContinue = vpc
	}
	return opts
}

func splitWav() {
	opts := readConfig()
	log.Printf("MuteLength: %d\n", opts.MuteLength)
	state := VadInit(opts.FrameSize, opts.SampleRate, opts.VadProbStart, opts.VadProbContinue)
	defer VadDestroy(state)
	f, err := os.Open(opts.WavPath)
	if err != nil {
		log.Fatalf("ERROR: read wav/pcm file failed - %s", err.Error())
		return
	}
	defer f.Close()

	if strings.HasSuffix(opts.WavPath, ".wav") {
		f.Seek(46, 0)
	}

	b := make([]byte, opts.FrameSize*opts.SampleRate/1000*2)
	n, err := f.Read(b)
	if err != nil {
		if err == io.EOF {
			log.Fatalf("read all data done, %s", n)
		}
		log.Fatalf("read wav err: %s", err.Error())
	}
	os.Mkdir(opts.WavPath[:len(opts.WavPath)-4]+"-"+strconv.Itoa(opts.VadProbStart)+"_"+strconv.Itoa(opts.VadProbContinue), 0777)

	cur := 0
	end := false
	for i := 1; ; i++ {
		b := make([]byte, opts.FrameSize*opts.SampleRate/1000*2)
		// outpath := opts.WavPath[:len(opts.WavPath)-4] + "-" + strconv.Itoa(i) + ".pcm"
		outpath := fmt.Sprintf("%s/%s.pcm", opts.WavPath[:len(opts.WavPath)-4]+"-"+strconv.Itoa(opts.VadProbStart)+"_"+strconv.Itoa(opts.VadProbContinue), strconv.Itoa(i))
		var pcm []byte
		countVAD := 0
		for j := 1; ; j++ {
			cur++
			n, err := f.Read(b)
			pcm = append(pcm, b...)
			if err != nil {
				end = true
				if err == io.EOF {
					log.Printf("read all data done")
					break
				}
				log.Printf("read wav err: %s", err.Error())
				break
			}

			if len(b) != n {
				end = true
				log.Printf("read all data done")
				break
			}
			flag := VadMonitor(state, b)
			log.Printf("cur: %03d	countVAD: %02d	flag: %d\n", cur/50, countVAD, flag)
			if flag == 0 {
				countVAD += 1
				continue
			} else {
				if countVAD*opts.FrameSize > opts.MuteLength && j*opts.FrameSize > opts.PCMLength {
					log.Printf("here!!!")
					break
				} else {
					countVAD = 0
				}
			}
		}
		writePCM(outpath, pcm)
		if end == true {
			break
		}
		time.Sleep(time.Duration(opts.Delay) * time.Millisecond)
	}
}

func writePCM(path string, pcm []byte) error {
	file, err := os.Create(path)
	if err != nil {
		log.Printf("writePCM: error in write PCM - %s", err.Error())
		return err
	}
	defer file.Close()

	w := bufio.NewWriter(file)
	if _, err := w.Write(pcm); err != nil {
		return err
	}
	return w.Flush()
}

func main() {
	splitWav()
}
