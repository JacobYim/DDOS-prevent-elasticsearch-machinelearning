import requests, math, random, datetime, argparse, time

def run_requesting_job(func,ip,rate,is_attacker,check_is_alive = lambda : True, time_interval=0.01): 
    process_start_time = time.time()
    while check_is_alive():
        t = time.time() - process_start_time
        if not check_is_alive():
            return
        tic = time.time()
        if random.random() <= rate:
            number_of_request = round(func(t))
            for _ in range(number_of_request) :
                requests.get(url="http://localhost:5000", params={'ip':ip,'is_attacker':is_attacker})
            if number_of_request > 0:
                print('ip={0}, requests sent {1} times'.format(ip , number_of_request))
        toc = time.time()
        time.sleep(max(0, time_interval - (tic-toc)))