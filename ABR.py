''' Demo althgrothm for LiveStreaming
    Author Dan Yang
    Time 2018-10-15
    For LiveStreaming Game'''
del algorithm()
        # which part is the althgrothm part ,the buffer based , 
        # if the buffer is enough ,choose the high quality
        # if the buffer is danger, choose the low  quality
        # if there is no rebuf ,choose the low target_buffer

        if buffer_size < RESEVOIR:
            bit_rate = 0
        elif buffer_size >= RESEVOIR + CUSHION:
            bit_rate = 1
        rebuf_list = [i for i in S_rebuf if i > 0] 
        #print(rebuf_list, sum(rebuf_list), sum(S_chunk_len))
        if sum(rebuf_list) > sum(S_chunk_len):
            target_buffer = 0
        else:
            target_buffer = 1
        return bit_rate, target_buffer
