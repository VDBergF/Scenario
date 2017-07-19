path_file = "/home/berg/PycharmProjects/Scripts/bw_fluctation_claro_sp_noite.txt"

class Data():

    def __init__(self, hour, seconds, rate):
        self.hour = str(hour)
        self.seconds = long(seconds)
        self.rate = float(rate)

    def split(self):
        return [self.hour, self.seconds, self.rate]

class Scenario():
    lst = []

    def __init__(self, file):
        self.lst = self.read(file)

    def read(self, file):
        for line in file:
            line = line.strip().split()
            self.lst.append(Data(line[0], line[1], line[2]))
           # print(line[0] + " " + line[1] + " " + line[2])

        return self.lst


file = open(path_file, "r")
scenario_lst = Scenario(file).lst

end_interval = 1800
highestSum = 0
sum = 0
highesIndex = 0

for start_interval, obj_file in enumerate(scenario_lst):
    sum = 0

    for obj in scenario_lst[start_interval:]:
        sum += obj.rate

        if (obj.seconds > end_interval):
            end_interval = obj.seconds
            break

    if sum > highestSum:
        highestSum = sum
        highesIndex = start_interval

    if end_interval > scenario_lst[-1].seconds:
        break

print(highesIndex)

sum = 0
bitrate = 0
for i, obj in enumerate(scenario_lst[7897:]):
    sum += obj.rate

    if i == 63:
        bitrate = sum / i
        break;

print (bitrate)




