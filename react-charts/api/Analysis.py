import math
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import savgol_filter

class Analysis:
    def __init__(self, data):
        self.stats = {}
        self.data = data
        #self.GetAnalytics()


    def calculDiv(self, a, b):
        try:
            return a/b
        except ZeroDivisionError:
            return 0.0
    

    def GetDiffInTime(self, time):
        timesDiff = []  
        for i in range(1, len(time)):
            timesDiff.append(time[i] - time[i-1]) # change for timestamp /1000
        #returns time spent in seconds
        return timesDiff

    
    def GetTimes(self):
        times = []
        for i in range(len(self.data)):
            times.append(self.data[i]['Time'])
        return times

    
    def GenerateTime(self):
        k = 2.0
        time = [0.0]
        for i in range(len(self.data)+1):
            time.append(i)
            k += 1
        return time


    def CalculDistance(self, x1, y1, x2, y2):
        R = 6373.0
        lat1 = math.radians(x1)
        lon1 = math.radians(y1)
        lat2 = math.radians(x2)
        lon2 = math.radians(y2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R*c
        #distance = math.sqrt(d**2 + ((h2-h1)/1000)**2)
        #returns distance in km
        return d 


    def CalculDistanceElev(self, x1, y1, x2, y2, h1, h2):
        R = 6373.0
        lat1 = math.radians(x1)
        lon1 = math.radians(y1)
        lat2 = math.radians(x2)
        lon2 = math.radians(y2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R*c
        distance = math.sqrt(d**2 + ((h2-h1)/1000)**2)
        #returns distance in km
        return distance
    

    def GetDistances(self):
        distances = []
        for i in range(1, len(self.data)):
            dist = self.CalculDistance(self.data[i]['Latitude'], self.data[i]['Longitude'], self.data[i-1]['Latitude'], self.data[i-1]['Longitude'])*1000
            if dist < 0.5:
                distances.append(0.0)
            else:
                distances.append(dist)
        #returns distances in m
        return distances
    
    
    def GetSpeed(self, distance, timeDiff):
        speed = [0.0]
        for i in range(len(distance)):
            #print(distance[i])
            speed.append(self.calculDiv(distance[i], timeDiff[i]))
        #returns speed in m/s
        return speed


    def PlotSpeed(self, speed, time):
        x = np.array(time[:800])
        speed_klm = [i *3600/1000 for i in speed]
        y = np.array(speed_klm[:800])

        sortId = np.argsort(x)
        x = x[sortId]
        y = y[sortId]

        w = savgol_filter(y, 51, 4)
        peaks, _ = find_peaks(w)
        plt.plot(x, w)
        plt.plot(peaks, w[peaks], "x")
        
        #peaks, _ = find_peaks(y, 130.0)
        #print(type(peaks))
        plt.plot(x, y)
        plt.plot(peaks, y[peaks], "x")
        plt.show()
        return 0

        
    def PlotAccel(self, accel, time, speed):
        speed_klm = [i *3600/1000 for i in speed]
        x = np.array(time)
        y = np.array(accel)
        w = np.array(speed_klm)

        fig, axs = plt.subplots(2)
        fig.suptitle('Vertically stacked subplots')
        
        axs[0].plot(x ,y)
        axs[1].plot(x, w)
        
        plt.show()
        return 0


    def GetAcceleration(self, speed, time):
        accelerations = [0.0]
        for i in range(1, len(speed)):
            accelerations.append(self.calculDiv((speed[i] - speed[i-1]), (time[i] - time[i-1])))
        #returns accel in m/s/s
        return accelerations


    def GetAccelerationNumber(self ,acc, vel, time):
        i = 0
        nbA = 0
        accels = []
        index = []
        while i < len(acc):
            if acc[i] == 0.0:
                i += 1
            elif acc[i] > 0.0:
                j = i
                while j < len(acc):
                    if acc[j] > 0.0:
                        if acc[j-1]==0:
                            accels.append(acc[j-1])
                            index.append(j-1)
                        accels.append(acc[j])
                        index.append(j)
                        j += 1
                    else:
                        break
                if (max(accels) >= 2.0):
                    peak = accels.index(max(accels))
                    new_vel = [(vel[i]) for i in index[:peak+2]]
                    lst = []
                    if(len(new_vel) > 1):
                        for i in range(1, len(new_vel)):
                            lst.append(new_vel[i]- new_vel[i-1])
                        if max(lst) > 2.2:  #same result for 2.3
                            nbA += 1
                    elif (len(new_vel) == 1):
                        if(new_vel[0]) > 2.2:
                            nbA += 1
                    else:
                        pass
                accels.clear()
                index.clear()
                i = j
            else:
                i += 1
        return nbA


    def GetDecelerationNumber(self, acc, vel, time):
        i = 0
        nbD = 0
        decels = []
        index = []
        while i < len(acc):
            if acc[i] == 0.0:
                i += 1
            elif acc[i] < 0.0:
                k = i
                while k < len(acc):
                    if acc[k] < 0.0:
                        if acc[k-1] == 0:
                            decels.append(acc[k-1])
                            index.append(k-1)
                        decels.append(acc[k])
                        index.append(k)
                        k += 1
                    else:
                        break
                if (min(decels) <= -1.8):
                    peak = decels.index(min(decels))
                    new_vel = [(vel[i])/3.6 for i in index[:peak+2]]
                    lst = []
                    if(len(new_vel) > 1):
                        for i in range(1, len(new_vel)):
                            lst.append(abs(new_vel[i]- new_vel[i-1]))
                        if max(lst) > 2.0: 
                            nbD += 1
                    elif (len(new_vel) == 1):
                        if(new_vel[0]) > 2.0:
                            nbD +=1
                    else:
                        pass
                decels.clear()
                index.clear()
                i = k
            else:
                i += 1
        return nbD


    def GetAdhNumber(self, heading, time):
        pass


    def GetStopRunTimes(self, speed, time):
        stopTime = speed.count(0.0)
        runTime = time[len(time)-1] - stopTime
        return [runTime, stopTime]


    def CountVehiculeStops(self, speed):
        nbr = 0
        i = 0
        while i<len(speed)-2:
            if speed[i] == 0.0 and speed[i+1] == 0.0 and speed[i+2] == 0.0:
                nbr += 1
                j = i + 3
                while j < len(speed):
                    if speed[j] == 0:
                        j += 1
                    else:   
                        i = j + 1
                        break
                i += 1
            else: 
                i += 1
        return nbr


    def GetIndexes(self, ind):
        indexs = []
        for i in range(len(ind)):
            if ind[i] == 0.0:
                indexs.append(i)
        return indexs
    

    def DistanceLength(self, dist, ind):
        for i in range(len(ind)-1):
            if sum(dist[ind[i]:ind[i+1]]) < 100.0:
                return False
        return True

    
    def CheckDistanceBetweenZeros(self, distances):
        indexs = self.GetIndexes(distances)
        return self.DistanceLength(distances, indexs)


    def GetDistanceTraffic(self, speed, distance):
        t = 0.0
        t1 = 0.0
        i = 0
        while i < len(speed):
            if speed[i] < 10.0:
                j = i
                while j < len(speed):
                    if t1 + distance[j] < 100.0 and speed[j]< 10.0:
                        t1 += distance[j]
                        j += 1 
                        i = j
                    else:
                        break
                t += t1
                t1 = 0.0
            else:
                i += 1
        return t


    def GetDistanceTrafficUrb(self, speed, distance):
        h = 0.0
        i = 0
        sub_dist = []
        while i < len(speed):
            if speed[i] < 30.0:
                k = i
                while k < len(speed):
                    if speed[k] < 30.0:
                        sub_dist.append(distance[k])
                        k += 1
                        i = k
                    else: 
                        i += 1
                        break
                if sub_dist.count(0.0) > 1:
                    if self.CheckDistanceBetweenZeros(sub_dist):
                        h += sum(sub_dist)
                        sub_dist = []
            else:
                i += 1
        return h


    def GetContext(self, speed, distance):
        T = 0.0
        H = 0.0
        C = 0.0
        S = 0.0
        E = 0.0
        speed_klm = [ i * 3600/1000 for i in speed]
        for i in range(len(speed_klm)):
            if speed_klm[i] > 96.0:
                E += distance[i]
            elif 65.0 < speed_klm[i] < 96.0:
                S += distance[i]
            elif 30.0 < speed_klm[i] < 65.0:
                C += distance[i]
            else:
                continue
        T = self.GetDistanceTraffic(speed_klm, distance)
        H = self.GetDistanceTrafficUrb(speed_klm, distance)
        return (T, H, C, S, E)


    def GetDisplacementNubmer(self, speed):
        nb = 0
        i = 0
        while i < len(speed)-1:
            if speed[i] < speed[i+1]:
                j = i+1
                first_inc = i
                while j < len(speed)-1:
                    if speed[j+1]>speed[j]:
                        j += 1
                    else:
                        i = j
                        break
                if speed[i]*3600/1000 - speed[first_inc]*3600/1000 > 5.0:
                    l = i+1
                    first_dec = i+1
                    if l >= len(speed): # => to prevent index out of range error
                        break
                    while l < len(speed)-1:
                        if speed[l] > speed[l+1]:
                            l += 1
                        else:
                            i = l
                            break
                    if speed[first_dec]*3600/1000 - speed[l]*3600/1000 > 5.0:
                        nb += 1
            else:
                i += 1 #better to update i to j
        return nb


    def GetTripLength(self):
        if self.data[len(self.data)-1]['Distance'] > 1900:
            return True
        return False


    def GetTotalTime(self, time):
        return str(datetime.timedelta(seconds=time[len(time)-1] - time[0]))


    def GetTotalDistance(self, distance):
        return round(sum(distance)/1000, 3)


    def GetAverageSpeed(self, speed):
        return round((sum(speed)/len(speed))*3600/1000, 1)


    def GetVehiStopRunTime(self, speed, time):
        stop_run_time =  self.GetStopRunTimes(speed, time)
        return (str(datetime.timedelta(seconds=stop_run_time[1])) , str(datetime.timedelta(seconds=stop_run_time[0])))
    
    
    def GetContextInfo(self):
        pass


    def GetSafetyInfo(self):
        pass

    
    '''def GetSafety(self):
        res  = {}
        time = self.GetTimes()
        timeDiff = self.GetDiffInTime()
        distance = distance = self.GetDistances()
        speed = self.GetSpeed(distance, timeDiff)
        accelerations = self.GetAcceleration(speed, time)

        res['Acceleration Count'] = self.GetAccelerationNumber(accelerations, speed, time)
        res['Deceleration Count'] = self.GetDecelerationNumber(accelerations, speed, time)
        res['Vehicule Stops '] = self.CountVehiculeStops(speed)
        res['Displacement number'] = self.GetDisplacementNubmer(speed)
        return res'''

    def GetContexts(self):
        res = {}
        time = self.GenerateTime()
        timeDiff = self.GetDiffInTime(time)
        distance = self.GetDistances()
        speed = self.GetSpeed(distance, timeDiff)
        distance.insert(0, 0.0)
        context = self.GetContext(speed, distance)
        res['Total Distance'] = round(sum(distance)/1000, 3)
        res['Traffic Jam'] =  round(context[0]/sum(distance)*100, 3) #= round(context[0]/1000, 3) #=  round(context[0]/sum(distance)*100, 3) 
        res['Heavy urban traffic'] = round(context[1]/sum(distance)*100, 3) #= round(context[1]/1000, 3) #
        res['City'] = round(context[2]/sum(distance)*100, 3) #= round(context[2]/1000, 3)# 
        res['Suburban'] = round(context[3]/sum(distance)*100, 3) #= round(context[3]/1000, 3) #
        res['Expressways'] = round(context[4]/sum(distance)*100, 3) #= round(context[4]/1000, 3) #
        return res


    def ReturnSpeed(self):
        res = {}
        distance = self.GetDistances()
        time = self.GenerateTime() 
        timeDiff = self.GetDiffInTime(time)
        speed =  self.GetSpeed(distance, timeDiff)
        speedkm = [i*3.6 for i in speed]
        y = np.array(speedkm)
        w = savgol_filter(y, 15, 1)
        speed_filtered = w.tolist()
        res['time'] = time
        res['speed'] = speed_filtered
        return res

    
    def ReturnRunStopTime(self):
        time = self.GenerateTime()
        timeDiff = self.GetDiffInTime(time)
        distance = self.GetDistances()
        speed = self.GetSpeed(distance, timeDiff)
        stop_run_time = self.GetStopRunTimes(speed, time)
        return stop_run_time


    '''def GetStatistics(self):
        res = {}
        tot_time = self.GetTotalTime(self.GetTimes())
        tot_dist = self.GetTotalDistance(self.GetDistances())
        avg_speed = self.GetAverageSpeed(self.GetSpeed(self.GetDistances(), self.GetDiffInTime()))
        stop_run_time = self.GetVehiStopRunTime(self.GetSpeed(self.GetDistances(), self.GetDiffInTime()), self.GetTimes())
        res['Total Time'] = tot_time
        res['Total Distance'] = tot_dist
        res['avg_speed'] = avg_speed
        res['Vehicule Run time'] = stop_run_time[0]
        res['Vehicule Stop Time'] = stop_run_time[1]
        return res'''

    
    def GetAnalytics(self):
        res = {}
        time = self.GenerateTime()
        timeDiff = self.GetDiffInTime(time)
        distance = self.GetDistances()
        speed = self.GetSpeed(distance, timeDiff)
        accelerations = self.GetAcceleration(speed, time)
        stop_run_time = self.GetStopRunTimes(speed, time)
        distance.insert(0, 0.0)
        context = self.GetContext(speed, distance)

        res['Average Speed'] = round((sum(speed)/len(speed))*3600/1000, 1)
        res['Total Distance'] = round(sum(distance)/1000, 3)
        res['Total Time'] = str(datetime.timedelta(seconds=time[len(time)-1]))
        res['Acceleration Count'] = self.GetAccelerationNumber(accelerations, speed, time)
        res['Deceleration Count'] = self.GetDecelerationNumber(accelerations, speed, time)
        res['Vehicule Stops '] = self.CountVehiculeStops(speed)
        res['Vehicule Run time'] = str(datetime.timedelta(seconds=stop_run_time[1]))
        res['Vehicule Stop Time'] = str(datetime.timedelta(seconds=stop_run_time[0]))
        res['Displacement number'] = self.GetDisplacementNubmer(speed)
        res['Traffic Jam'] = round(context[0]/1000, 3) #=  round(context[0]/sum(distance)*100, 3) 
        res['Heavy urban traffic'] = round(context[1]/1000, 3) #= round(context[1]/sum(distance)*100, 3)
        res['City'] =  round(context[2]/1000, 3)# = round(context[2]/sum(distance)*100, 3)
        res['Suburban'] = round(context[3]/1000, 3) #= round(context[3]/sum(distance)*100, 3)
        res['Expressways'] = round(context[4]/1000, 3) #= round(context[4]/sum(distance)*100, 3)
        self.stats = res
        return res


if __name__ == "__main__": 
    with open('trajet2.json') as f:
        data = json.loads(f.read())
    test = Analysis(data)
    #print(test.stats)
    #print(test.GetAnalytics())
    #print(test.GetStatistics())
    #print(test.GetTripLength())
    #print(test.ReturnSpeed())