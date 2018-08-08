extern void* vad_create();
extern void vad_free(void* vad);
extern int vad_process(void* vad, char* buf);
extern int cut_file(const char *filename, const char *output_filename_prefix, const char *output_dir, void *vad, int *result, int *res_pos);
extern int get_activity_period(const char *filename, void *vad, int *result, int *res_pos);
