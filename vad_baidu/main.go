package main

import (
	"fmt"
)

func main() {
	v := NewVad()
	/*
		res, err := v.Split("pcm/16k_1.pcm", "test", "output")
		if err != nil {
			fmt.Println("split err:", err)
			return
		}
	*/
	res, err := v.Period("pcm/vad_5min.wav")
	if err != nil {
		fmt.Println("period err:", err)
		return
	}

	for i := 0; i < len(res); i += 2 {
		fmt.Println(res[i], "-", res[i+1])
	}
	return
}
