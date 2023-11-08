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
sat_traj_list = []

def get_numpy_array_of_timestamps(curr_jd, time_step, days):
    one_sec_in_jd = time_step/(24*60*60)
    date = np.arange(curr_jd, curr_jd+days, one_sec_in_jd)
    jd = np.floor(date)
    fr = date - jd
    return jd, fr, date

def ecef2lla(pos_x, pos_y, pos_z):

    transformer = pyproj.Transformer.from_crs(
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
    )
    lona, lata, alta = transformer.transform(
        pos_x, pos_y, pos_z, radians=False)
    return lona, lata, alta

def fx(s,t):
    sat = Satrec.twoline2rv(s, t)
    sat_list.append(sat)
    curr_jd = sat.jdsatepoch + sat.jdsatepochF
    res = get_numpy_array_of_timestamps(curr_jd, 1, 5)
    _, pos, vel = sat.sgp4_array(res[0], res[1])
    time_array = np.transpose([res[2]])
    sat_traj = np.concatenate((time_array, pos, vel), axis=1)
    sat_traj_list.append(sat_traj)
    lat_long = ecef2lla(
    sat_traj[:, [1]], sat_traj[:, [2]], sat_traj[:, [3]])
    return

def filter_lat_long():
    pass





# def create_sat_traj_list(sat_traj):
    
#     # sat_traj_list.append(sat_traj)

    
#     # print(lat_long[0])
#     # print(np.concatenate(lat_long[0], axis=0))
#     # sat_traj[:, 1] = np.concatenate(lat_long[0], axis=0)
#     # sat_traj[:, 2] = np.concatenate(lat_long[1], axis=0)
#     # sat_traj[:, 3] = np.concatenate(lat_long[2], axis=0)
#     return 1


def main():
    with open("27000sats.txt", 'r') as f:
        for s, t in itertools.zip_longest(*[f]*2):
            Process(target=fx,args=(s,t)).start()

    # for sat in sat_list:
        # create_sat_traj_list(sat)
        # break
        # with Pool(5) as p:
        #     p.map(create_sat_traj_list,[sat_traj for sat_traj in sat_traj_list])
        # # Process(target=create_sat_traj_list,args=(sat,)).start()
    return

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(len(sat_traj_list))

    print(f"TOTAL TIME: {time.time()-start_time}")
