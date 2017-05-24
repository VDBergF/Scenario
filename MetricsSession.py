# coding=utf-8
import json
import time
import datetime

path_json = "/home/berg/codigos/app/Logs/Equipe4.txt"
input_file = json.loads(open(path_json).read()) #Json
n_sharing = 3 # Number of clients

class MetricsSession():

    def __init__(self, averageBandwidthScenario, path_log):
        self.averageBandwidthScenario = long(averageBandwidthScenario)
        self.path_log = str(path_log)


    def averageBandwidth(self):
        lst_bandwidth = input_file['bandwidth']
        return sum([lst_bandwidth[i]['bandwidth'] for i, obj in enumerate(lst_bandwidth)]) / len(lst_bandwidth)

    def averageBitrate(self):
        j = input_file
        lst_chunk = j['chunk']

        sum1 = sum([(lst_chunk[i]['bitrate']/1000) * (lst_chunk[i]['duration'] / 1000) for i, obj in enumerate(lst_chunk)])
        return sum1 / (3000)

    def justice(self):
        r_obtained = self.averageBitrate()
        r_expected = self.r_expected()

        sum1 = sum([r_obtained / r_expected for i in range(0, n_sharing)]) ** 2
        sum2 = sum([(r_obtained / r_expected) ** 2 for i in range(0, n_sharing)])

        return float(sum1) / float(sum2)

    def r_expected(self):
        lst_qualities = input_file['qualities']
        averageQualities = sum([lst_qualities[i]['width'] for i, obj in enumerate(lst_qualities)]) / len(lst_qualities)
        return (averageQualities / n_sharing) * self.averageBandwidth()

    def instability(self):
        lst_chunk = input_file['chunk']

        sum1 = sum([abs(lst_chunk[i]['bitrate'] - lst_chunk[i-1]['bitrate'] * len(lst_chunk) - i) for i, obj in enumerate(lst_chunk)
                    if i-1 >= 0 and i < len(lst_chunk)-1])
        sum2 = sum([lst_chunk[i]['bitrate'] * len(lst_chunk) - i for i, obj in enumerate(lst_chunk[1:])])

        return float(sum1) / float(sum2)

    def averageInterruptions(self):
        lst_interruptions = input_file['interruption']

        sum1 = sum([lst_interruptions[i]['end']/1000 - lst_interruptions[i]['start']/1000 for i, obg in enumerate(lst_interruptions)])
        return (sum1 / len(lst_interruptions))

    def bitrate(self):
        j = input_file
        lst_chunk = j['chunk']

        arq = open('/home/berg/Arquivos/arq1.txt', "w")
        arq2 = open('/home/berg/Arquivos/arq2.txt', "w")

        for i, obj in enumerate(lst_chunk):
            arq.write(str(long(lst_chunk[i]['bitrate']) / 1000) + '\n')

        for i, obj in enumerate(lst_chunk):
            timeStamp = long(lst_chunk[i]['timeStamp'])
            a = str(self.convertEpochToTime(timeStamp)).split(':')
            a[0] = str(long(a[0])-4)
            arq2.write(a[0]+':'+a[1]+':'+a[2] + '\n')

        arq.close()
        arq2.close()

    def convertEpochToTime(self, timeStamp):
        return time.strftime('%H:%M:%S',  time.gmtime(timeStamp/1000.))


    def extraeCenario(self):
        path_file = "/home/berg/Área de Trabalho/Cenario_Experimento.txt"
        file = open(path_file, "r")
        arq1 = open('/home/berg/Arquivos/arq3.txt', "w")
        arq2 = open('/home/berg/Arquivos/arq4.txt', "w")

        for line in file:
            line = line.strip().split()
            #s = line[1] + " " + line[2]
            arq1.write(line[1] + '\n')
            arq2.write(line[2] + '\n')

        arq2.close()
        arq1.close()

m = MetricsSession(0, "")
# print'Grupo:', input_file["team"]
# print'Taxa media de bits:', m.averageBitrate(), 'bit/s'
# print'Quantidade de interrupcoes:', len(input_file['interruption'])
# print'Tempo medio de interrupcoes:', m.averageInterruptions(), 's'
# print'Instabilidade:', m.instability(), '- Entre 0-1 (1 maior instabilidade)'
m.extraeCenario()
# m.bitrate()