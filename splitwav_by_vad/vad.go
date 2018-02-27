package main

//package main

/*
#cgo CFLAGS: -I./include
#cgo LDFLAGS: -lspeexdsp -L./libs -lvad
#include "vad.h"
#include <stdlib.h>
*/
import "C"
import "unsafe"

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
