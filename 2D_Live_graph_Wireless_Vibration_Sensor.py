import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial    

seru = serial.Serial('COM6', 115200)

# Create figure for plotting
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Initialize globally
xs = []
ys = []
y2 = []
y3 = []


# Animate Function
def animate(i, xs, ys,y2,y3):
    # Read max value
    rmsX,rmsY,rmsZ = vib_sense();
    print(rmsX);
    print(rmsY);
    
    #rounding off the figure upto 2 decimal format
    rms = round(rmsX, 2)
    rms1 = round(rmsY, 2)
    rms2 = round(rmsZ, 2)
    
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(rms)
    y2.append(rms1)
    y3.append(rms2)

    # Limit x and y lists to 50 items
    xs = xs[-50:]
    ys = ys[-50:]
    y2 = y2[-50:]
    y3 = y3[-50:]
    

    # Draw x and y lists
    ax1.clear()
    ax1.plot(xs, ys, label='RMS X', marker='o')
    ax1.plot(xs, y2, label='RMS Y',marker='o')
    ax1.plot(xs, y3, label='RMS Z',marker='o')
    
    # Format plot
    plt.xticks(rotation=60, ha='right')
    plt.subplots_adjust(bottom=0.30)

    plt.title('RMS Values for Vibration')
    plt.ylabel('axis in mg')
    plt.xlabel('Time')  
    plt.legend(loc='upper right')

# vibration Sensor Data 
def vib_sense():
    while True:
        s = seru.read(54)
        if(s[0] == 126):
            if(s[15] == 127):
                if(s[22]== 8):
                    rms_x = (((s[24]*65536)+(s[25]*256)+s[26])& 0xffff)/100
                    rms_y = (((s[27]*65536)+(s[28]*256)+s[29])& 0xffff)/100
                    rms_z = (((s[30]*65536)+(s[31]*256)+s[32])& 0xffff)/100
                    max_x = (((s[33]* 65536)+(s[34]*256)+s[35])& 0xffff)/100
                    max_y = (((s[36]*65536)+(s[37]*256)+s[38])& 0xffff)/100
                    max_z = (((s[39]*65536)+(s[40]*256)+s[41])& 0xffff)/100
                    min_x = (((s[42]*65536)+(s[43]*256)+s[44])& 0xffff)/100
                    min_y = (((s[45]*65536)+(s[46]*256)+s[47])& 0xffff)/100
                    min_z = (((s[48]*65536)+(s[49]*256)+s[50])& 0xffff)/100
                    ctemp = (((s[51]*256)+s[52])& 0xffff)
                    battery = ((s[18]*256)+s[19])
                    voltage = 0.00322*battery
                    rmsValueX = 0;
                    rmsValueY = 0;
                    
                    return rms_x,rms_y,rms_z



ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, y2, y3), interval=500)
plt.show()

