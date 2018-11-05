# INFO
* LiveStreamingDemo
* For LiveStreaming Game SDK demo
* python 2 or python 3
* python demo.py

# net Env
* Init the  env:
```python
         net_env = env.Environment(all_cooked_time=all_cooked_time,       # physical time
                                  all_cooked_bw=all_cooked_bw,            # throughput
                                  all_cooked_rtt=all_cooked_rtt,          # rtt
                                 random_seed=random_seed,                 # random_seed
                                  logfile_path=LogFile_Path,              # log setting
                                  VIDEO_SIZE_FILE=video_size_file,        # video trace
                                  Debug = DEBUG)                          # Debug setting
```
* Loop:
    cnt control you train setps:
```python    
    if steps > 50000:
          break;
```
* every step you can get the info from env:
```python
        time, time_interval, send_data_size, chunk_len, rebuf, buffer_size, rtt, play_time_len,end_delay, decision_flag, buffer_flag,cdn_flag, end_of_video = net_env.get_video_frame(bit_rate,TARGET_BUFFER[target_buffer])
```
* calculate the score
    *    



#Trace Data setting 
* you will have two types trace, one is network trace, another is video trace

                   12 TRAIN_TRACES = './train_sim_traces/'   #train trace path setting,
                   13 video_size_file = './video_size_'      #video trace path setting,

* Video trace: Video trace has N files.```(N means the num of bitrate actions)```   
* Video trace Formate   
   
        |   Time(s)  | frame_data_size(b) |  is_I_flag |
        |------------|--------------------|------------|
        | 22.1131    | 321312             |   1        |  
        
* Network trace Formate:   
   
        |Time(s)  | throughput(kpbs) | rtt(ms)|
        |---------|------------------|--------|
        |20.5     | 1.312            |   56   |
    
#Log Setting
* log is used to debug the code. you can set you log file path:

                   14 LogFile_Path = "./log/"                #log file trace path setting, 
        
   * if you are debugging your code, you can let the DEBUG = True.
   * if you are training your model, consider the I/O, advise you let the DEBUG = False
   
* Log formate:
```
     real_time        :   physical time
     cdn_rebuf        :   cdn_rebuf time
     client_rebuf     :   client_rebuf time
     download_duration:   download time
     frame_size       :   download frame data size
     play_time_len    :   play the video time len in this download_duration
     download_id      :   download frame seq
     cnd_new_frame    :   the seq of the cdn newest frame
     client_buffer    :   the clinet buffer
     play_time        :   play time
     play_id          :   play frame seq
     latency          :   end to end latency
```
* 
```  
real_time 3.0476    cdn_rebuf0.0412	client_rebuf 0.000	download_duration 0.0000	frame_size 21569.0000	play_time_len 0.0412	download_id 76	cdn_newest_frame 76	client_buffer 2.9588	play_time 0.0412	play_id 1.0000	latency 2.9588	000
```
* <font color=#46A3ff size=2> which 000 type means the cdn can't get the frame  , you can see the cdn_rebuf = 0.0412, the download_id = cdn_newest_frame </font>

* 
```
real_time 0.8897	cdn_rebuf0.0278	client_rebuf 0.006	download_duration 0.0059	frame_size 14587.0000	play_time len 0.0000	download_id 23	cdn_newest_frame 22	client_buffer 0.9200	play_time 0.0000	play_id 0.0000	latency 0.9200	111
```

* <font color=#46A3ff size=2> which 111 type means the buffering status , you can see the play_time_len = 0 </font>

* 
```
real_time 4.8653	cdn_rebuf0.0000	client_rebuf 0.000	download_duration 0.0628	frame_size 36672.0000	play_time_len 0.0628	download_id 118	cdn_newest_frame 122	client_buffer 2.7584	play_time 1.9216	play_id 48.0000	latency 2.9184	222
```
* <font color=#46A3ff size=2> which 222 type means the normal type status, you can see the play_time_len = download_duration</font>

* 
```
skip events: skip_download_frame, play_frame, new_download_frame, ADD_frame428 357 528 100
```
* <font color=#46A3ff size=2> which means that it happens the skip events, the player not download the next frame , but to download the next ADD_FRAME frame. to let the latency small.</font>
```
ADD_Frame100
```
* <font color=#46A3ff size=2> which means the player skip </font>


About livestreaming player sim please click the http://www.aitrans.online


