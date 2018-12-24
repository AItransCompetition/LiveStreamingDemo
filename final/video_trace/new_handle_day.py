# !/usr/bin/evn python3
# -*- coding:UTF-8 -*-
import urllib.request
import os


# 文件下载
def file_download(url, file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    def Schedule(a,b,c):
        per = 100.0 * a * b / c
        if per > 100 :
            per = 100
        print('%.2f%%' % per)
    urllib.request.urlretrieve(url, file_path, Schedule)


# 文件读取
def file_read(file_path):
    file = open(file_path)
    lines = file.readlines()
    output = {}
    temp = ""
    # FPS的数目
    cnt = 0
    for line in lines:
        line=line.strip('\n')
        # 帧率的添加
        if line.startswith("FPS"):
            fps_split = line.split("=")
            fps_temp = fps_split[1]
            for i in range(1,cnt+1):
                output[temp][-i] += " "+fps_temp
            cnt = 0
        # 高码率文件的创建
        elif line.startswith("ID:dokidoki/mlinkm/"):
            Channel_ID_1200 = line[19:]
            if Channel_ID_1200 in output:
                temp = Channel_ID_1200 + "_high"
            else:
                output[Channel_ID_1200 + "_high"] = []
                temp = Channel_ID_1200 + "_high"
            cnt = 0
        # 低码率文件的创建
        elif line.startswith("ID:EXT-ENC-0/dokidoki/mlinkm/"):
            Channel_ID_500 = line[29:]
            if Channel_ID_500 in output:
                temp = Channel_ID_500 + "_low"
            else:
                output[Channel_ID_500 + "_low"] = []
                temp = Channel_ID_500 + "_low"
            cnt = 0
        # 帧内容添加
        else:
            output[temp].append(line)
            cnt += 1
    return output


# 将只有high没有low的文件删除,或只有low没有high的文件删除
def file_match(output):
    file_mach = {}
    file_len = {}
    for key, value in output.items():
        if key[10:] == "_high":
            new_key = key[:10] + "_low"
            if new_key in output:
                file_mach[key] = value
                if key[:10] in file_len:
                    file_len[key[:10]] += len(value)
                else:
                    file_len[key[:10]] = len(value)
        if key[10:] == "_low":
            new_key = key[:10] + "_high"
            if new_key in output:
                file_mach[key] = value
                if key[:10] in file_len:
                    file_len[key[:10]] += len(value)
                else:
                    file_len[key[:10]] = len(value)
    return file_mach, file_len


# 按文件大小,排序,获取文件大小较大的文件
def file_sorted(file_mach, file_len):
    file_len_max = sorted(file_len.items(), key=lambda item: item[1], reverse=True)
    result = []
    file_high = file_len_max[0][0] + "_high"
    file_low = file_len_max[0][0] + "_low"
    result.append(file_mach[file_low])
    result.append(file_mach[file_high])
    return result


# 文件时间对齐
def file_align(result):
    result_align = []
    start_time_1 = float(result[0][0].split()[0])
    start_time_2 = float(result[1][0].split()[0])
    if start_time_1 < start_time_2:
        for i in range(len(result[0])):
            start_time_1 = float(result[0][i].split()[0])
            if start_time_1 >= start_time_2:
                result_align.append(result[0][i:])
                result_align.append(result[1])
                break
    else:
        for i in range(len(result[1])):
            start_time_2 = float(result[1][i].split()[0])
            if start_time_1 <= start_time_2:
                result_align.append(result[0])
                result_align.append(result[1][i:])
                break
    return result_align


# 文件保存
def file_save(dir_path, file_mach):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for key,value in file_mach.items():
        f_file = open(dir_path + str(key) + ".csv", "w")
        for idx in range(len(value)):
            data = value[idx].replace(" ",",")
            data += "\n"
            f_file.write(data)


# 文件输出
def file_print(result_path, result_align):
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    for i in range(len(result_align)):
        first_line = result_align[i][0].split()
        start_time = float(first_line[0])
        f_out = open(result_path + "./frame_trace_" + str(i), "w")
        for line in result_align[i]:
            temp = line.split()
            time = ((float(temp[0]) - start_time) / 1000) - 2.0
            time = "%.3f" % time
            size = float(temp[1]) * 8
            I_flag = int(temp[2])
            FPS = 25
            if len(temp) > 3:
                FPS = int(temp[3])
            f_out.write(
                str(time) + " " +
                str(size) + " " +
                str(I_flag) + " " +
                str(FPS) + " " + "\n"
            )


def main():
    file_path = "./12-12/2018-12-12.txt"
    dir_path = "./12-12/"
    result_path = "./12-12/video_trace/"
    url = "http://164.52.0.183:8000/file/findTrace/2018-12-12.txt"
    # file_download(url, file_path)
    output = file_read(file_path)
    file_mach, file_len = file_match(output)
    file_save(dir_path, file_mach)
    result = file_sorted(file_mach, file_len)
    result_align = file_align(result)
    file_print(result_path, result_align)


main()