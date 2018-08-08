package main

/*
#cgo CFLAGS: -I./include
#cgo LDFLAGS: -L./libs -lvad
#include "vad.h"
#include <stdlib.h>
*/
import "C"
import (
	"fmt"
	"unsafe"
)

type Vad struct {
	State unsafe.Pointer
}

func NewVad() *Vad {
	v := new(Vad)
	v.State = C.vad_create()
	return v
}

func (v *Vad) Free() {
	C.vad_free(v.State)
}

func (v *Vad) Process(data []byte) int {
	buf := (*C.char)(unsafe.Pointer(&data[0]))
	// defer C.free(unsafe.Pointer(buf))
	return int(C.vad_process(v.State, buf))
}

func (v *Vad) Split(input, outputPrefix, outputDir string) ([]int32, error) {
	cInput := C.CString(input)
	defer C.free(unsafe.Pointer(cInput))
	cOutputPrefix := C.CString(outputPrefix)
	defer C.free(unsafe.Pointer(cOutputPrefix))
	cOutputDir := C.CString(outputDir)
	defer C.free(unsafe.Pointer(cOutputDir))

	results := make([]int32, 500)
	resSize := 0
	tmp := C.int(resSize)
	res := C.cut_file(cInput, cOutputPrefix, cOutputDir, v.State, (*C.int)(&results[0]), (*C.int)(&tmp))
	if res != 0 {
		return results, fmt.Errorf("vad error code: %d", res)
	}
	resSize = int(tmp)
	return results[:resSize], nil
}

func (v *Vad) Period(input string) ([]int32, error) {
	cInput := C.CString(input)
	defer C.free(unsafe.Pointer(cInput))

	results := make([]int32, 500)
	resSize := 0
	tmp := C.int(resSize)
	res := C.get_activity_period(cInput, v.State, (*C.int)(&results[0]), (*C.int)(&tmp))
	if res != 0 {
		return results, fmt.Errorf("vad error code: %d", res)
	}
	resSize = int(tmp)
	left := 1
	right := 1
	for ; right < resSize; right += 2 {
		if right == resSize-1 {
			results[left] = results[right]
			break
		}
		if results[right+1]-results[right] < 20 {
			continue
		}
		results[left] = results[right]
		results[left+1] = results[right+1]
		left += 2
	}
	return results[:left+1], nil
}
