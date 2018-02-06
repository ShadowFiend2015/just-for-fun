#include <stdio.h>  
#include <stdlib.h>  
#include <unistd.h>  
#include <stdint.h>  
#include <assert.h>  
#include "include/speex/speex_preprocess.h"  
#include "include/vad.h"
#define SAMPLE_RATE (16000)  
#define FRAME_SIZE (20) //ms  
#define SAMPLES_PER_FRAME (SAMPLE_RATE/1000 * FRAME_SIZE)//每毫秒16个样点  
#define FRAME_BYTES (SAMPLES_PER_FRAME * 2)//每个样点2字节（单通道）  

void* vad_create(int frame_size, int sample_rate, int vadProbStart, int vadProbContinue) {
	SpeexPreprocessState *state = speex_preprocess_state_init(frame_size, sample_rate);  
	int denoise = 0;  
    speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_DENOISE, &denoise); //关闭降噪  
    //speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_NOISE_SUPPRESS, &noiseSuppress); //设置噪声的dB  
    //speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_AGC, &agc);//增益  
    //speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_AGC_LEVEL,&agcLevel);//设置增益的dB  
  
    //int vad = 1, vadProbStart = 80, vadProbContinue = 65;  
    int vad = 1; 
    speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_VAD, &vad); //静音检测  
    speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_PROB_START , &vadProbStart); //Set probability required for the VAD to go from silence to voice  
    speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_PROB_CONTINUE, &vadProbContinue); //Set probability required for the VAD to stay in the voice state (integer percent)  
	return (void*)state;
}
void vad_destroy(void *state) {
    speex_preprocess_state_destroy((SpeexPreprocessState*)state);  
}
int vad_monitor(void *state, char *buf) {
    int is_input = 0;
		is_input = speex_preprocess_run((SpeexPreprocessState*)state, (spx_int16_t*)(buf));  
	return is_input;
}

