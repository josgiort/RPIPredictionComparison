

def from_left(seq_id, seq_len, itr_trim_spacing):
    chain_indexes = ""
    # Never put start index of range() to 0, due to index definition bed format
    for i in range(itr_trim_spacing, min(seq_len + 1, 1023), itr_trim_spacing):
        chain_indexes += seq_id + "\t0\t" + str(i) + "\n"
    return chain_indexes

def from_right(seq_id, seq_len, itr_trim_spacing):
    chain_indexes = ""
    for i in range(itr_trim_spacing, min(seq_len + 1, 1023), itr_trim_spacing):  # Never put start index of range() to 0, due to resulting chain of 0 length in lengths file but not in subchains file
        chain_indexes += seq_id + "\t" + str(seq_len - i) + "\t" + str(seq_len) + "\n"
    return chain_indexes

def from_middle(seq_id, seq_len, itr_trim_spacing, intvl_bdary_l, intvl_bdary_r):
    chain_indexes = ""

    # Creation of subtrings of successive lengths
    # Finding length of interval with bed format is easier: just a simple subtraction
    len_intvl = intvl_bdary_r - intvl_bdary_l

    l_chunk = intvl_bdary_l
    r_chunk = seq_len - intvl_bdary_r

    half = (min(1022, seq_len) - len_intvl) // 2

    if l_chunk >= half:
        if r_chunk >= half:
            left_extension = half
            right_extension = half
        else:
            left_extension = half
            right_extension = r_chunk
    else:
        if r_chunk >= half:
            left_extension = l_chunk
            right_extension = half
        else:
            left_extension = l_chunk
            right_extension = r_chunk

    if left_extension == right_extension:
        for i in range(1, left_extension + 1, itr_trim_spacing):
            final_l= intvl_bdary_l - i
            final_r= intvl_bdary_r + i
            chain_indexes += seq_id + "\t" + str(final_l) + "\t" + str(final_r) + "\n"
    else:
        if left_extension > right_extension:
            for i in range(1, left_extension + 1, itr_trim_spacing):
                final_l = intvl_bdary_l - i
                if i <= right_extension:
                    final_r = intvl_bdary_r + i
                else:
                    final_r = intvl_bdary_r + right_extension
                chain_indexes += seq_id + "\t" + str(final_l) + "\t" + str(final_r) + "\n"
        else:
            for i in range(1, right_extension + 1, itr_trim_spacing):
                final_r = intvl_bdary_r + i
                if i <= left_extension:
                    final_l = intvl_bdary_l - i
                else:
                    final_l = intvl_bdary_l - left_extension
                chain_indexes += seq_id + "\t" + str(final_l) + "\t" + str(final_r) + "\n"
    return chain_indexes