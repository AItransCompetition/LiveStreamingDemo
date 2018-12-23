import numpy
BIT_RATE_LEVELS = 2
for i in range(BIT_RATE_LEVELS):
    f = open("./frame_trace_" +str(i) + ".csv")
    lines = f.readlines()
    first_line = lines[0].split(",")
    start_time = float(first_line[0])
    f_out = open("./frame_trace_" + str(i), "w")
    for line in lines:
        line = line.replace(","," ")
        temp = line.split()
        time = ((float(temp[0]) - start_time) / 1000) - 2.0
        size = float(temp[1]) * 8
        I_flag = int(temp[2])
        FPS = int(temp[3])
        f_out.write(
                   str(time) +" " +
                   str(size) + " " +
                   str(I_flag) + " " +
                   str(FPS) +" " +"\n"
                )


