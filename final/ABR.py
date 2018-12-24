class Algorithm:
     def __init__(self):
     # fill your init vars
         self.buffer_size = 0
         
     # Intial 
     def Initial(self):
         self.buffer_size = 0

     #Define your al
     def run(self, S_time_interval, S_send_data_size, S_frame_time_len, S_frame_type, S_buffer_size, S_end_delay, rebuf_time, cdn_has_frame,cdn_flag, buffer_flag):
         bit_rate = 1
         target_buffer = 1.5
         return bit_rate, target_buffer


