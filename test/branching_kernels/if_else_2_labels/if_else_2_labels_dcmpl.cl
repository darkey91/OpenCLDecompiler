__kernel __attribute__((reqd_work_group_size(8, 8, 1)))
void if_else_2_labels(int x, __global int *data, int y)
{
    uint *var3;
    uint var6;
    if (1 == get_global_id(0)) {
        var3 = &data[(get_global_id(0) * 4) / 4];
        var6 = (get_global_id(1) * x) - y;
    }
    else {
        var3 = &data[(get_global_id(0) * 4) / 4];
        var6 = y * x;
    }
    *var3 = var6;
    data[(get_global_id(1) * 4) / 4] = x;
}
