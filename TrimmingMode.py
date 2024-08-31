

def from_left(seq_len, itr_trim_spacing):
    chain_indexes = ""
    chain_lengths = ""
    # Never put start index of range() to 0, due to index definition bed format
    for i in range(2, min(seq_len + 1, 1023), itr_trim_spacing):
        chain_indexes += "seq1\t0\t" + str(i) + "\n" # later adapt this to handle more sequences than seq1
        chain_lengths += str(i - 0) + "\n"
    return chain_indexes, chain_lengths

def from_right(seq_len, itr_trim_spacing):
    chain_indexes = ""
    chain_lengths = ""
    for i in range(2, min(seq_len + 1, 1023),
                   itr_trim_spacing):  # Never put start index of range() to 0, due to resulting chain of 0 length in legnths file but not in subchains file
        chain_indexes += "seq1\t" + str(seq_len - i) + "\t" + str(seq_len) + "\n"
        chain_lengths += str(seq_len - (seq_len - i)) + "\n"
    return chain_indexes, chain_lengths

def from_middle(seq_len, itr_trim_spacing):
    chain_indexes = ""
    chain_lengths = ""

    # Starting point to extend within the chain can be specified in interval-based (2 index required) or position-based (1 index required)
    itr_trim_mid_mode = int(input("Enter starting point type for middle trimming (0 - interval, 1- position): "))

    intvl_bdary_l = ""
    intvl_bdary_r = ""

    if itr_trim_mid_mode == 0:
        intvl_bdary_l = int(input("Enter the interval left boundary (0 based index, inclusive): "))
        intvl_bdary_r = int(input("Enter the interval right boundary (1 based index, inclusive): "))

    elif itr_trim_mid_mode == 1:
        position_conserve = int(input("Enter the specific position; (1 based index, int): "))

        # In practice, position based starting point is same as interval based, since two boundaries are created manually by extending two residues at each side
        # Here is 1 more than right boundary due to index definition bed format
        intvl_bdary_l = position_conserve - 3
        intvl_bdary_r = position_conserve + 2

    # Trimming
    # Finding length of interval with bed format is easier just a simple subtraction
    len_intvl = intvl_bdary_r - intvl_bdary_l

    l_chunk = intvl_bdary_l
    r_chunk = seq_len - intvl_bdary_r

    half = (min(1022, seq_len) - len_intvl) // 2

    if l_chunk >= half:
        if r_chunk >= half:
            left_extension = half
            right_extension = half
        else:
            left_extension = half + (half - r_chunk)
            right_extension = r_chunk
    else:
        left_extension = l_chunk
        right_extension = half + (half - l_chunk)

    if left_extension == right_extension:
        for i in range(1, left_extension + 1, itr_trim_spacing):
            chain_indexes += "seq1\t" + str(intvl_bdary_l - i) + "\t" + str(intvl_bdary_r + i) + "\n"
            chain_lengths += str(len_intvl + 2 * i) + "\n"
    else:
        if left_extension > right_extension:
            for i in range(1, left_extension + 1, itr_trim_spacing):
                if i <= right_extension:
                    chain_indexes += "seq1\t" + str(intvl_bdary_l - i) + "\t" + str(intvl_bdary_r + i) + "\n"
                    chain_lengths += str(len_intvl + 2 * i) + "\n"
                else:
                    chain_indexes += "seq1\t" + str(intvl_bdary_l - i) + "\t" + str(intvl_bdary_r + right_extension) + "\n"
                    chain_lengths += str(len_intvl + right_extension + i) + "\n"
        else:
            for i in range(1, right_extension + 1, itr_trim_spacing):
                if i <= left_extension:
                    chain_indexes += "seq1\t" + str(intvl_bdary_l - i) + "\t" + str(intvl_bdary_r + i) + "\n"
                    chain_lengths += str(len_intvl + 2 * i) + "\n"
                else:
                    chain_indexes += "seq1\t" + str(intvl_bdary_l - left_extension) + "\t" + str(intvl_bdary_r + i) + "\n"
                    chain_lengths += str(len_intvl + left_extension + i) + "\n"
    return chain_indexes, chain_lengths