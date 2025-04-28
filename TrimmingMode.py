

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

    # MAking sure the maximal allowed length is not supassed

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
            # Only matters the magnitude of the greater extension to loop across iteratively extending lenghts with range()
            for i in range(1, left_extension + 1, itr_trim_spacing):
                # As left extension is grater in this case it directly uses iteratively extending length from loop
                final_l = intvl_bdary_l - i
                # The difficulty here lies on the right extension as it spans less, so cant extend as long as the left one, so
                # while its possible uses the range() generated extending lenghts
                if i <= right_extension:
                    final_r = intvl_bdary_r + i
                else:
                    # else there comes the moment where it reaches its limit and now range() generated extending lengths surpass it
                    # and right extension must restrict itself
                    final_r = intvl_bdary_r + right_extension
                chain_indexes += seq_id + "\t" + str(final_l) + "\t" + str(final_r) + "\n"
        else:
            # Same considerations apply here as the immediate above ones, just now from the perspective of left extension being smaller
            for i in range(1, right_extension + 1, itr_trim_spacing):
                final_r = intvl_bdary_r + i
                if i <= left_extension:
                    final_l = intvl_bdary_l - i
                else:
                    final_l = intvl_bdary_l - left_extension
                chain_indexes += seq_id + "\t" + str(final_l) + "\t" + str(final_r) + "\n"
    return chain_indexes