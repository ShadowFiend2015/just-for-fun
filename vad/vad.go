package main

//package main

/*
#cgo CFLAGS: -I./include
#cgo LDFLAGS: -lspeexdsp -L./libs -lvad
#include "vad.h"
#include <stdlib.h>
*/
import "C"
import (
	"flag"
	"fmt"
	"github.com/BurntSushi/toml"
	"io"
	"log"
	"os"
	"strings"
	"time"
	"unsafe"
)

var (
	wavFile = flag.String("f", "", "wav/pcm file")
)

func VadInit(frameSize int, sampleRate int, vadProbStart int, vadProbContinue int) unsafe.Pointer {
	return C.vad_create(C.int(frameSize), C.int(sampleRate), C.int(vadProbStart), C.int(vadProbContinue))
}

func VadDestroy(state unsafe.Pointer) {
	C.vad_destroy(state)
}

func VadMonitor(state unsafe.Pointer, data []byte) int {
	buf := (*C.char)(unsafe.Pointer(&data[0]))
	//defer C.free(unsafe.Pointer(buf))
	is_input := int(C.vad_monitor(state, buf))
	return is_input
}

type Options struct {
	FrameSize       int `toml:'frame_size'`
	SampleRate      int `toml:'sample_rate'`
	VadProbStart    int `toml:'vad_prob_start'`
	VadProbContinue int `toml:'vad_prob_continue'`
	WavPath         string
	Delay           int `toml:'delay'`
}

func NewOptions() *Options {
	return &Options{
		FrameSize:       20,
		SampleRate:      16000,
		VadProbStart:    99,
		VadProbContinue: 99,
	}
}

func vadFlagSet() *flag.FlagSet {
	flagSet := flag.NewFlagSet("vad", flag.ExitOnError)
	flagSet.String("f", "", "wav/pcm file")
	flagSet.String("config", "", "config file path")
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
	return opts
}

func main() {
	opts := readConfig()
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
	var result []int
	for {
		n, err := f.Read(b)
		if err != nil {
			if err == io.EOF {
				log.Printf("read all data done")
				break
			}
			log.Printf("read wav err: %s", err.Error())
			break
		}

		if len(b) != n {
			log.Printf("read all data done")
			break
		}
		flag := VadMonitor(state, b)
		result = append(result, flag)
		time.Sleep(time.Duration(opts.Delay))
	}
	for idx, flag := range result {
		if idx%50 == 0 {
			fmt.Println()
			fmt.Printf("%03d - %03d: ", idx/50, idx/50+1)
		}
		fmt.Printf("%d ", flag)
	}
	fmt.Println()
}
