import LiveStreamingEnv.env as env
#import env
import LiveStreamingEnv.load_trace as load_trace
TEST_LOG_FOLDER = './test_results/'
#TRAIN_TRACES = './cooked_traces/'
TRAIN_TRACES = './train_sim_traces/'
video_size_file = './video_size_'
DEBUG = False
LogFile_Path = "./log/" 

all_cooked_time, all_cooked_bw, all_cooked_rtt,_ = load_trace.load_trace(TRAIN_TRACES)
agent_id = 2
net_env = env.Environment(all_cooked_time=all_cooked_time,
                              all_cooked_bw=all_cooked_bw,
                              all_cooked_rtt=all_cooked_rtt,
                              random_seed=agent_id,
                              logfile_path=LogFile_Path,
                              VIDEO_SIZE_FILE=video_size_file,
                              Debug = True)
i = 0
S_time_interval = []
S_send_data_size = []
S_chunk_len = []
S_rebuf = []
S_buffer_size = []
S_end_delay = []
S_chunk_size = []
S_rtt = []
BIT_RATE      = [500,800]
TARGET_BUFFER = [2,3]
RESEVOIR = 0.5
CUSHION  = 3

while True:
    # input 
    if i > 50000:
        break
    bit_rate = 0
    target_buffer = 2
    #time_interval, send_data_size, chunk_len, rebuf, buffer_size, rtt, end_delay, decision_flag, buffer_flag, end_of_video =   net_env.get_video_frame(bit_rate,TARGET_BUFFER[target_buffer])
    time_interval, send_data_size, chunk_len, rebuf, buffer_size, rtt, end_delay, decision_flag, buffer_flag, end_of_video =   net_env.get_video_frame(bit_rate,target_buffer)
    i += 1
    if decision_flag and DEBUG:
        print("interval",S_time_interval)
        print("send_data",S_send_data_size)
        print("chunk len",S_chunk_len)
        print("buffer",S_buffer_size)
        print("rebuf",S_rebuf)
        print("delay",S_end_delay)
        print("rtt",S_rtt)
        print("\n-------------------------------------------------------------------------------------\n")
        
        '''if buffer_size < RESEVOIR:
            bit_rate = 0
        elif buffer_size >= RESEVOIR + CUSHION:
            bit_rate = 1
        rebuf_list = [i for i in S_rebuf if i > 0] 
        print(rebuf_list, sum(rebuf_list), sum(S_chunk_len))
        if sum(rebuf_list) > sum(S_chunk_len):
            target_buffer = 0
        else:
            target_buffer = 0'''

        S_time_interval = []
        S_send_data_size = []
        S_chunk_len = []
        S_rebuf = []
        S_buffer_size = [] 
        S_end_delay = []
        S_rtt = []
        S_chunk_size = []
    S_time_interval.append(time_interval)
    S_send_data_size.append(send_data_size)
    S_chunk_len.append(chunk_len)
    S_buffer_size.append(buffer_size)
    S_rebuf.append(rebuf)
    S_end_delay.append(end_delay)
    S_rtt.append(rtt)
  
    
    # output
