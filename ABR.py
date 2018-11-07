''' Demo althgrothm for LiveStreaming
    Author Dan Yang
    Time 2018-10-15
    For LiveStreaming Game'''
def algorithm(time, time_interval, send_data_size, chunk_len, rebuf, buffer_size, rtt, play_time_len,end_delay, decision_flag, buffer_flag,cdn_flag, end_of_video):
# which part is the althgrothm part ,the buffer based 
# if the buffer is enough ,choose the high quality
# if the buffer is danger, choose the low  quality
# if there is no rebuf ,choose the low target_buffer
   RESEVOIR = 0.5
   CUSHION =  3
   bit_rate = 1
   if buffer_size < RESEVOIR:
        bit_rate = 0
   elif buffer_size >= RESEVOIR + CUSHION:
        bit_rate = 1
   target_buffer = 1
   return bit_rate, target_buffer
