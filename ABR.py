''' Demo althgrothm for LiveStreaming
    Author Dan Yang
    Time 2018-10-15
    For LiveStreaming Game'''
def algorithm(time, S_time_interval, S_send_data_size, S_chunk_len, S_rebuf, S_buffer_size, S_play_time_len,S_end_delay, S_decision_flag, S_buffer_flag,S_cdn_flag, end_of_video,params):
# which part is the althgrothm part ,the buffer based 
# if the buffer is enough ,choose the high quality
# if the buffer is danger, choose the low  quality
# if there is no rebuf ,choose the low target_buffer
   RESEVOIR = 0.5
   CUSHION =  3
   bit_rate = 1
   '''if S_buffer_size[-1] < RESEVOIR:
        bit_rate = 0
   elif S_buffer_size[-1] >= RESEVOIR + CUSHION:
        bit_rate = 1'''
   target_buffer = 1
   return bit_rate, target_buffer
