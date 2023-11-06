from sgp4.api import accelerated, Satrec, SatrecArray
import itertools 

from itertools import repeat
import numpy as np
import pyproj
import ray
import time
import os
from multiprocessing import Process, Pool


sat_list = []
global pos_x
global pos_y
global pos_z 

with open("30sats.txt", 'r') as f:
    for s, t in itertools.zip_longest(*[f]*2):
        sat = Satrec.twoline2rv(s, t)
        sat_list.append(sat)


def get_numpy_array_of_timestamps(curr_jd,time_step,days):
    one_sec_in_jd = time_step/(24*60*60)
    date = np.arange(curr_jd, curr_jd+days, one_sec_in_jd)
    jd = np.floor(date)
    fr = date - jd
    return jd, fr, date

def filter_lat_long():
    pass


def ecef2lla(i):
    
    transformer = pyproj.Transformer.from_crs(
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
    )
    lona, lata, alta = transformer.transform(
        pos_x[i], pos_y[i], pos_z[i], radians=False)
    return lona, lata, alta


sat_traj_list = []
time_array = []
def create_sat_traj_list(sat):
    curr_jd = sat.jdsatepoch + sat.jdsatepochF
    res = get_numpy_array_of_timestamps(curr_jd,1,.05)
    _, pos, vel = sat.sgp4_array(res[0], res[1])
    time_array = np.transpose([res[2]])
    sat_traj = np.concatenate((time_array, pos, vel), axis=1)
    sat_traj_list.append(sat_traj)
    pos_x = sat_traj[:, [1]]
    pos_y = sat_traj[:, [2]]
    pos_z = sat_traj[:, [3]]
    with Pool(6) as p:
        lat_long = p.starmap(ecef2lla,zip([i for i in range(len(time_array))]))
    #     print(lat_long)
    # for i in range(len(time_array)):
    #     # Process(target=ecef2lla,args=(i, sat_traj[:, [1]], sat_traj[:, [2]], sat_traj[:, [3]])).start()

    #     lat_long = ecef2lla(
    #         i, sat_traj[:, [1]], sat_traj[:, [2]], sat_traj[:, [3]])
    
    #     sat_traj[i][1] = lat_long[0]
    #     sat_traj[i][2] = lat_long[1]
    #     sat_traj[i][3] = lat_long[2]
    return 1

def main():
    for sat in sat_list:
        create_sat_traj_list(sat)
        break
        # Process(target=create_sat_traj_list,args=(sat,))
        
    

if __name__ == "__main__":
    start_time = time.time()
    px = Process(target=main)
    px.start()
    px.join()

    print(f"TOTAL TIME: {time.time()-start_time}")