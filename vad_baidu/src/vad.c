#include <stdio.h>
#include <common_audio/vad/include/webrtc_vad.h>
#include <stdlib.h>
#include <stdint.h>
#include "simple_vad.h"
#include "period_format.h"
#include "file_cut.h"
#include "vad.h"

void* vad_create() {
	simple_vad *vad = simple_vad_create();
	if (vad == NULL) {
		return NULL;
	}
	return (void*)vad;
}

void vad_free(void* vad) {
	simple_vad_free((simple_vad*)vad);
}

// 0 - 静音，1 - 非静音
int vad_process(void* vad, char* buf) {
	return process_vad((simple_vad*)vad, (int16_t*) strtol (buf,  NULL, 10));
	// return process_vad((simple_vad*)vad, (int16_t*)(buf))
}

// 16000 采样率 10ms，  大小 = 160 * 16bits/8 = 320字节 ,

int run(FILE *fp, simple_vad *vad, struct cut_info *cut, int *result, int *res_pos, int is_cut);

int add_period_activity(struct periods *per, int is_active, int is_last);

int cut_file(const char *filename, const char *output_filename_prefix, const char *output_dir, void *vad, int *result, int *res_pos) {
    FILE *fp = fopen(filename, "rb");
    if (fp == NULL) {
        return 3;
    }
    if (vad == NULL) {
        return 4;
    }
    FILE *fp2 = fopen(filename, "rb");
    struct cut_info *cut = cut_info_create(fp2);
    snprintf(cut->output_filename_prefix, sizeof(cut->output_filename_prefix), "%s",
             output_filename_prefix);
    snprintf(cut->output_file_dir, sizeof(cut->output_file_dir), "%s",
             output_dir);
    int res = run(fp, (simple_vad*)vad, cut, result, res_pos, 1);

    fclose(fp);
    fclose(fp2);
    cut_info_free(cut);
    // printf("PROGRAM FINISH\n");
    return res;
}

int get_activity_period(const char *filename, void *vad, int *result, int *res_pos) {
	  FILE *fp = fopen(filename, "rb");
    if (fp == NULL) {
        return 3;
    }
    if (vad == NULL) {
        return 4;
    }
    FILE *fp2 = fopen(filename, "rb");
    struct cut_info *cut = cut_info_create(fp2);
    int res = run(fp, (simple_vad*)vad, cut, result, res_pos, 0);

    fclose(fp);
    fclose(fp2);
    cut_info_free(cut);
    // printf("PROGRAM FINISH\n");
    return res;
}

int run(FILE *fp, simple_vad *vad, struct cut_info *cut, int *result, int *res_pos, int is_cut) {

    int16_t data[FRAME_SIZE];
    int res = 0;
    struct periods *per = periods_create();

    while (res == 0) {
        res = read_int16_bytes(fp, data);
        if (res <= 1) {
            int is_last = (res == 1);
            int is_active = process_vad(vad, data);
            add_period_activity(per, is_active, is_last);
            int vad_file_res = cut_add_vad_activity(cut, is_active, is_last, result, res_pos, is_cut);
            if (vad_file_res < 0) {
               // printf("file write success %s\n", cut->result_filename);
            }
        } else if (ferror(fp)) {
            // printf("read failed  ferror result  : %d\n", ferror(fp));
        }

    }
    periods_free(per);

    if (res != 1) {
        fprintf(stderr, "read file error %d\n", res);
        return res;
    }
    return 0;
}


int add_period_activity(struct periods *per, int is_active, int is_last) {
    static int old_is_active = 0;
    static int count = 0;
    int res_add = period_add_vad_activity(per, is_active, is_last);
    if (res_add != 0) {
        return res_add;
    }
    if (is_active != old_is_active) {
        // printf("%s,%d \n", old_is_active ? "A" : "I", count);
        // I,1  表示之前的1个FRAME是 INACTIVE的；
        // I,1 A,10 表示之前的1个FRAME是 INACTIVE的；第2-10个FRAME是ACTIVE的
        // periods_print(per);
        old_is_active = is_active;
    }
    count += 1;
    if (is_last) {
        // periods_print(per);
        // printf("total frames %d\n", count);
    }
}
