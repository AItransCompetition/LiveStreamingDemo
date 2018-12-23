file = open("./2018-12-16.txt")
lines = file.readlines()
output = {}
temp = ""
cnt = 0
for line in lines:
    line=line.strip('\n')
    if line.startswith("FPS"): 
        fps_split = line.split("=")
        #print(fps_split)
        fps_temp = fps_split[1]
        for i in range(1,cnt+1):
            output[temp][-i] += " "+fps_temp
        cnt = 0
    elif line.startswith("ID:dokidoki/mlinkm/"):
        Channel_ID_1200 = line[19:] 
        if output.has_key(Channel_ID_1200):
            temp = Channel_ID_1200 + "_high" 
        else:
            output[Channel_ID_1200 + "_high"] = []
            temp = Channel_ID_1200 + "_high"
        cnt = 0
    elif line.startswith("ID:EXT-ENC-0/dokidoki/mlinkm/"):
        Channel_ID_500 = line[29:]
        if output.has_key(Channel_ID_500):
            temp = Channel_ID_500 + "_low" 
        else:
            output[Channel_ID_500 + "_low"] = []
            temp = Channel_ID_500 + "_low"
        cnt = 0
    else:
        output[temp].append(line) 
        cnt += 1
for key,value in output.items():
    f_file = open("./12-16/" + str(key) + ".csv","w")
    for idx in range(len(value)):
        data = value[idx].replace(" ",",")
        data += "\n"
        f_file.write(data)
#print(output)
        #print(Channel_ID_500)
