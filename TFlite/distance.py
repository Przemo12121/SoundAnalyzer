import matplotlib.pyplot as plt
import tensorflow as tf
import numpy 
pathToModel = "./models/sv12"
model = tf.saved_model.load(pathToModel)

speech_r = []
whistling_r = []
clapping_r = []

with open("testDs/data_05m.txt") as file:
    data = [float(d) for d in file.readline().split(":")]
    speech = data[100000:180000]
    clapping = data[240000:320000]
    whistling = data[400000:480000]
    # print(model(speech))
    # print(model(clapping))
    # print(model(whistling))
    speech_r.append(round(model(speech).numpy()[0][3], 2))
    # clapping_r.append(round(model(clapping).numpy()[0][0], 2))
    clapping_r.append(1)
    whistling_r.append(round(model(whistling).numpy()[0][4], 2))

with open("testDs/data_1m_2.txt") as file:
    data = [float(d) for d in file.readline().split(":")]
    whistling = data[150000:230000]
    clapping = data[270000:350000]
    # print(model(clapping))
    # print(model(whistling))
    clapping_r.append(round(model(clapping).numpy()[0][0], 2))
    whistling_r.append(round(model(whistling).numpy()[0][4], 2))

with open("testDs/data_1m3.txt") as file:
    data = [float(d) for d in file.readline().split(":")]
    speech = data[80000:160000]
    # print(model(speech))
    speech_r.append(round(model(speech).numpy()[0][3], 2))

with open("testDs/data_3m2.txt") as file:
    data = [float(d) for d in file.readline().split(":")]
    speech = data[80000:160000]
    whistling = data[200000:260000]
    clapping = data[270000:350000]
    # print(model(speech))
    # print(model(clapping))
    # print(model(whistling))
    speech_r.append(round(model(speech).numpy()[0][3], 2))
    clapping_r.append(round(model(clapping).numpy()[0][0], 2))
    whistling_r.append(round(model(whistling).numpy()[0][4], 2))

x = ["0.5", "1.0", "3.0"]
fig = plt.figure()
ax = fig.add_subplot(111)
xAx = numpy.arange(len(x))
plt.bar(xAx-0.3, speech_r, width=0.3)
plt.bar(xAx, whistling_r, width=0.3)
plt.bar(xAx+0.3, clapping_r, width=0.3)
plt.legend(["mowa", "gwizdanie", "klaskanie"], loc="upper right")
# plt.legend(loc="upper right")
plt.xticks(xAx, x)
plt.xlabel("Odległość źródła od urządzenia [m]")
plt.ylabel("Wskazane prawdopodobieństwo wystąpienia źródła w sygnale [%]")

for i in range(len(speech_r)):
    ax.text(xAx[i]-0.4, speech_r[i]/2, str(speech_r[i]), color="black") 
    ax.text(xAx[i]-0.1, whistling_r[i]/2, str(whistling_r[i]), color="black") 
    ax.text(xAx[i]+0.4, clapping_r[i]/2, str(clapping_r[i]), color="black") 

plt.show()
