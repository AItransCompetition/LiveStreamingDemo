''' Demo SDK for LiveStreaming
    Author Dan Yang
    Time 2018-12-15
    For LiveStreaming final Game'''
# import the env from pip
#import LiveStreamingEnv.fixed_final_env as env
import LiveStreamingEnv.final_fixed_env as env
import LiveStreamingEnv.load_trace as load_trace
#import matplotlib.pyplot as plt
import time
import numpy as np
import ABR
def test(user_id):
    # path setting
    TRAIN_TRACES = './network_trace/'   #train trace path setting,
    #video_size_file = './video_trace/AsianCup_China_Uzbekistan/frame_trace_'      #video trace path setting,
    video_size_file = './video_trace/frame_trace_'      #video trace path setting,
    LogFile_Path = "./log/"                #log file trace path setting,
    # Debug Mode: if True, You can see the debug info in the logfile
    #             if False, no log ,but the training speed is high
    DEBUG = False
    DRAW = False
    # load the trace
    all_cooked_time, all_cooked_bw, all_file_names = load_trace.load_trace(TRAIN_TRACES)
    #random_seed 
    random_seed = 2
    video_count = 0
    #FPS = 25
    frame_time_len = 0.04
    reward_all_sum = 0
    #init the environment
    #setting one:
    #     1,all_cooked_time : timestamp
    #     2,all_cooked_bw   : throughput
    #     3,all_cooked_rtt  : rtt
    #     4,agent_id        : random_seed
    #     5,logfile_path    : logfile_path
    #     6,VIDEO_SIZE_FILE : Video Size File Path
    #     7,Debug Setting   : Debug
    net_env = env.Environment(all_cooked_time=all_cooked_time,
    			  all_cooked_bw=all_cooked_bw,
    			  random_seed=random_seed,
    			  logfile_path=LogFile_Path,
    			  VIDEO_SIZE_FILE=video_size_file,
    			  Debug = DEBUG)
    BIT_RATE      = [500.0,1200.0] # kpbs
    TARGET_BUFFER = [2.0,3.0]   # seconds
    # ABR setting
    RESEVOIR = 0.5
    CUSHION  = 2
    
    cnt = 0
    # defalut setting
    last_bit_rate = 0
    bit_rate = 0
    target_buffer = 1.5
    # QOE setting
    reward_frame = 0
    reward_all = 0
    SMOOTH_PENALTY= 0.02 
    REBUF_PENALTY = 1.5 
    LANTENCY_PENALTY = 0.005 
    
    call_cnt = 0
    call_time = 0
    switch_num = 0
    
    S_time_interval = []
    S_send_data_size = []
    S_frame_type = []
    S_frame_time_len = []
    S_buffer_size = []
    S_end_delay = []
    cdn_has_frame = []
    rebuf_time = 0
    buffer_flag = 0
    cdn_flag=0
    
    abr = ABR.Algorithm()
    abr.Initial()
    
    while True:
        reward_frame = 0
        # input the train steps
        #if cnt > 1200:
            #plt.ioff()
        #    break
        #actions bit_rate  target_buffer
        # every steps to call the environment
        # time           : physical time 
        # time_interval  : time duration in this step
        # send_data_size : download frame data size in this step
        # chunk_len      : frame time len
        # rebuf          : rebuf time in this step          
        # buffer_size    : current client buffer_size in this step          
        # rtt            : current buffer  in this step          
        # play_time_len  : played time len  in this step          
        # end_delay      : end to end latency which means the (upload end timestamp - play end timestamp)
        # decision_flag  : Only in decision_flag is True ,you can choose the new actions, other time can't Becasuse the Gop is consist by the I frame and P frame. Only in I frame you can skip your frame
        # buffer_flag    : If the True which means the video is rebuffing , client buffer is rebuffing, no play the video
        # cdn_flag       : If the True cdn has no frame to get 
        # end_of_video   : If the True ,which means the video is over.
        time, time_interval, send_data_size, frame_time_len, rebuf, buffer_size, end_delay, cdn_newest_id, downlaod_id, cdn_has_frame, decision_flag, buffer_flag,switch,cdn_flag, end_of_video = net_env.get_video_frame(bit_rate,target_buffer)
        cnt += 1
        call_time += time_interval
        switch_num += switch

        S_time_interval.append(time_interval)
        S_buffer_size.append(buffer_size)
        S_send_data_size.append(send_data_size)
        S_frame_time_len.append(frame_time_len)
        S_end_delay.append(end_delay)
        if decision_flag:
            S_frame_type.append(1)
        else:
            S_frame_type.append(0)
        rebuf_time += rebuf

        if not cdn_flag:
            reward_frame = frame_time_len * float(BIT_RATE[bit_rate]) / 1000  - REBUF_PENALTY * rebuf - LANTENCY_PENALTY * end_delay
        else:
            reward_frame = -(REBUF_PENALTY * rebuf)
        if call_time > 0.5 and not end_of_video:
            reward_frame += -(switch_num) * SMOOTH_PENALTY * (1200 - 500) / 1000
            
            bit_rate , target_buffer = abr.run(S_time_interval, S_send_data_size,S_frame_time_len,S_frame_type,S_buffer_size,S_end_delay,\
                                      rebuf_time, cdn_has_frame, cdn_flag, buffer_flag)

            call_time = 0
            switch_num = 0
            call_cnt += 1

            S_time_interval= []
            S_send_data_size = []
            S_frame_type = []
            S_frame_time_len = []
            S_buffer_size = []
            S_end_delay = []
            rebuf_time = 0

        # --`----------------------------------------- End  ------------------------------------------- 

        reward_all += reward_frame
        if end_of_video:
            # Narrow the range of results
            print("video count", video_count, reward_all)
            reward_all_sum += reward_all / 100
            video_count += 1
            if video_count >= len(all_file_names):
                break
            cnt = 0
            reward_all = 0
            last_bit_rate = 0
            bit_rate = 0
            target_buffer = 1.5

            S_time_interval = []
            S_send_data_size = []
            S_frame_type = []
            S_frame_time_len = []
            S_buffer_size = []
            S_end_delay = []
            cdn_has_frame = []
            rebuf_time = 0
            buffer_flag = 0
            cdn_flag=0

            call_cnt = 0
            call_time = 0
            switch_num = 0
    return reward_all_sum
a = test("aaa")
print(a)

