__kernel void mask_kernel(int n, __global float *x, float mask_num, __global float *mask, float scale)
{
    uint var0;
    uint var1;
    if (n > ((((get_global_offset(1) + (get_global_size(1) * get_global_id(2))) + (get_global_id(1) - get_global_offset(1))) * get_global_size(0)) + get_global_id(0))) {
        var0 = mask[(((((get_global_offset(1) + (get_global_size(1) * get_global_id(2))) + (get_global_id(1) - get_global_offset(1))) * get_global_size(0)) + get_global_id(0)) * 4) / 4];
        if (mask_num == var0) {
            var1 = x[(((((get_global_offset(1) + (get_global_size(1) * get_global_id(2))) + (get_global_id(1) - get_global_offset(1))) * get_global_size(0)) + get_global_id(0)) * 4) / 4];
            x[(((((get_global_offset(1) + (get_global_size(1) * get_global_id(2))) + (get_global_id(1) - get_global_offset(1))) * get_global_size(0)) + get_global_id(0)) * 4) / 4] = scale * var1;
        }
    }
}
