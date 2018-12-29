# 数据集
* 决赛视频数据集文档：
  * 视频数据集获得
        获取方法：wget http://164.52.0.183:8000/file/findTrace/2018-12-06.txt”（其中的2018-12-06为所需日期）
  * 视频数据集解释：
      * ID:dokidoki/mlinkm/4515447156：代表高码率1200 时各个帧的情况
      * ID:EXT-ENC-0/dokidoki/mlinkm/9715447060: 代表低码率500时各个帧的情况
      * 其中4515447156、9715447060都为流ID，高码率与低码率一一对应需要流ID相同
      * Video trace format   
   
        |  timestamp    | frame_data_size(B) |  I/P       |
        |---------------|--------------------|------------|
        | 1544715697964 | 14599              |   1        |  
        
      * 由于数据集量巨大，组委会不再每日提供数据，而是将清洗脚本与原数据提供给大家，大家自行使用.
  * 视频数据清洗：
      * 将每日trace文件下载，同时下载处理脚本handle_day.py 与decrase2.py 脚本下载地址：https://github.com/NGnetLab/LiveStreamingDemo/tree/master/final/video_trace/
      * 清洗脚本 handle_day.py 放置在同一目录下，并在该目录下创建一个文件夹（以时间命名，如“12-06”）
      * 修改handle_day.py文件第1行的文件名为要处理的trace文件名，第35行的路径为上一步创建文件夹的路径
      * 运行脚本 python handle_day.py
      * 打开创建的文件夹，挑选一对流ID相同的的文件（如：“7515448308_high.csv”和“7515448308_low.csv”）挑选规则为：挑选文件大小较大的文件，即视频长度相对较长的文件。
      * 适当修改所选出来的一对文件的开头，适当删除几行，使得第一行的时间戳尽量接近。
      * 然后下载decrease2.py脚本，对数据做最后的最终处理。即可得到相应的以-2开头的相对偏移的可以被仿真器利用的数据源
* 决赛网络数据集文档：
  * 网络数据集
    网络数据集请保持0.5s的采样周期。组委会也已经为大家提供了相应的生成脚本，下载地址https://github.com/NGnetLab/LiveStreamingDemo/tree/master/final/network_trace
  * 网络数据集注意事项：
    请确保网络数据集的时间戳长度小于视频数据集的时间戳长度。网络数据集时间戳长度代表了用户观看的时长。
    所以根据网络数据集和视频数据集的问题，希望大家自行裁剪长度。推荐长度，视频数据集25分钟（即timestamp相对偏移量为1500s）观看长度24分钟（即timestamp为1460s）
  * 关于网络数据集脚本:
```python
         python make_network  1 0.5 0.5 1440
```
 * 具体参数含义请看代码
# online 接口
```python
         # 每 500ms 调用一次
         if call_time > 0.5 and not end_of_video:
            reward_frame += -(switch_num) * SMOOTH_PENALTY * (1200 - 500) / 1000

            bit_rate , target_buffer = abr.run(S_time_interval,  # 过去500ms的每个周期时长
                                              S_send_data_size,\ # 过去500ms的每个周期下载数据量
                                              S_frame_time_len,\ # 过去500ms的每个周期下载帧的视频时长
                                              S_frame_type,\     # 过去500ms的每个周期下载帧的帧类型 （0为P帧，1为I帧）
                                              S_real_quality,\   # 过去500ms的每个周期下载帧的码率类型（500k, 1200k）
                                              S_buffer_size,\    # 过去500ms的每个周期客户端buffer长度
                                              S_end_delay,\      # 过去500ms的每个周期端到端时延
                                              rebuf_time,\       # 过去500ms的总卡顿时间
                                              cdn_has_frame,\    # 此刻的cdn 帧积累的累积值
                                              cdn_flag,\         # 此刻的cdn是否存在的卡顿，cdn flag 实际为cdn rebuf flag
                                              buffer_flag)       # 此刻客户端是否处于缓冲

            call_time = 0
            switch_num = 0
            call_cnt += 1

            S_time_interval= []
            S_send_data_size = []
            S_frame_type = []
            S_frame_time_len = []
            S_buffer_size = []
            S_end_delay = []
            S_real_quality = []
            rebuf_time = 0
```
