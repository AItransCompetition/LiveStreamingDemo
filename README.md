Table of Contents
=================

   * [INFO]()
   * [What you need to do ?]()
   * [Code structure]()
   * [Trace Data setting]()
   * [Draw settings]()
   * [Log Setting]()
   
# INFO
* LiveStreamingDemo
* For LiveStreaming Game SDK demo
* Languages: python 2 or python 3
* Document description:
     * demo.py         --- ```An SDK to call the SIM, and you will fill your algorithm in it. ```
     * video_size_0    --- ```video trace (low_bitrate)```
     * video_size_1    --- ```video trace (high_bitrate)```
     * train_sim_trace --- ```network trace for trainning```
     * test_sim_trace  --- ```network trace for you test```
     * ABR.py          --- ```you need to copy your algorithm in demo file to this file and upload it in the website to get your score.```
     * online.py       --- ``the same as the file in the server to call you ABR.py, which helps you to debug your uploads.```
# What you need to do ?
* you should  upload your algorithm in this area
```python
        # -------------------------------------------Your Althgrithom -------------------------------------------
        # which part is the algorithm part ,the buffer based ,
        # if the buffer is enough, choose the high quality
        # if the buffer is in danger, choose the low  quality
        # if there is no rebuf , choose the low target_buffer
  
        if buffer_size < RESEVOIR:
            bit_rate = 0
        elif buffer_size >= RESEVOIR + CUSHION:
            bit_rate = 1
        rebuf_list = [i for i in S_rebuf if i > 0]
  
        if sum(rebuf_list) > sum(S_chunk_len):
            target_buffer = 0
        else:
            target_buffer = 1
  
        # ------------------------------------------- End  -------------------------------------------
```

# Code structure
* Init the  env sim :
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
    The cnt control you train steps:
```python    
    if cnt > 50000:
          break;
```
* every step you can get the observations from env:
```python
        time, time_interval, send_data_size, chunk_len, rebuf, buffer_size, rtt, play_time_len,end_delay, decision_flag, buffer_flag,cdn_flag, end_of_video = net_env.get_video_frame(bit_rate,TARGET_BUFFER[target_buffer])
```
* calculate the score
    ```python
       if decision_flag :
           # reward formate = play_time * BIT_RATE - 4.3 * rebuf - 1.2 * end_delay
           reward =  sum(S_play_time) *  BIT_RATE[bit_rate] - 0.8 *  sum(S_rebuf) -  0.2 * (end_delay - 3)  -       abs(BIT_RATE[bit_rate] - BIT_RATE[last_bit_rate])
           reward_all += reward
    ```



# Trace Data setting 
* you will have two types of the trace, one is network trace, another is video trace

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

# Draw settings
* if you want to Debug the code, the Draw = True, the image will let you know all kinds of indicators
* ![Image text](https://github.com/NGnetLab/LiveStreamingDemo/blob/master/figure_1.png)

```python
           if DRAW:
               ax = fig.add_subplot(311)
               plt.ylabel("BIT_RATE")
               plt.ylim(300,1000)
               plt.plot(id_list,bit_rate_record,'-r')
  
               ax = fig.add_subplot(312)
               plt.ylabel("Buffer_size")
               plt.ylim(0,7)
               plt.plot(id_list,buffer_record,'-b')
  
               ax = fig.add_subplot(313)
               plt.ylabel("throughput")
               plt.ylim(0,2500)
               plt.plot(id_list,throughput_record,'-g')
  
               plt.draw()
               plt.pause(0.01)
```

# Log Setting
* the log is used to debug the code. you can set you log file path:

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
* which 000 type means the cdn can't get the frame  , you can see the cdn_rebuf = 0.0412, the download_id = cdn_newest_frame 
* 
```
real_time 0.8897	cdn_rebuf0.0278	client_rebuf 0.006	download_duration 0.0059	frame_size 14587.0000	play_time len 0.0000	download_id 23	cdn_newest_frame 22	client_buffer 0.9200	play_time 0.0000	play_id 0.0000	latency 0.9200	111
```

* which 111 type means the buffering status , you can see the play_time_len = 0 

* 
```
real_time 4.8653	cdn_rebuf0.0000	client_rebuf 0.000	download_duration 0.0628	frame_size 36672.0000	play_time_len 0.0628	download_id 118	cdn_newest_frame 122	client_buffer 2.7584	play_time 1.9216	play_id 48.0000	latency 2.9184	222
```
* which 222 type means the normal status, you can see the play_time_len = download_duration

* 
```
skip events: skip_download_frame, play_frame, new_download_frame, ADD_frame428 357 528 100
```
*  which means that it happens the skip events, the player not download the next frame, but to download the next ADD_FRAME frame. to let the latency small.
```
ADD_Frame100
```
*  which means the player skip 


About livestreaming player sim please click the http://www.aitrans.online


