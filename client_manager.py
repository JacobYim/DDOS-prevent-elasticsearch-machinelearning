from client import run_requesting_job
import keyboard  # using module keyboard
import threading
import random

thread_id_set = set()
id_counter = 0
def run_process(func,ip,rate,is_attacker):
    global id_counter
    thread_id = id_counter
    id_counter += 1
    thread_id_set.add(thread_id)
    def check_is_alive():
        return thread_id in thread_id_set
    t = threading.Thread(target=run_requesting_job, args=(func,ip,rate,is_attacker,check_is_alive)) 
    t.start()
    return thread_id

def killThread(thread_id):
    thread_id_set.remove(thread_id)

def get_random_ip():
    return '{0}.{1}.{2}.{3}'.format(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))

def creat_random_square_function(period,mean,variance,amplitude):
    def func(t):
        t = t - (t//period) * period
        if t >= mean - 0.5*variance and t <= mean + 0.5*variance:
            return amplitude
        t -= period
        if t >= mean - 0.5*variance and t <= mean + 0.5*variance:
            return amplitude
        t += period   
        if t >= mean - 0.5*variance and t <= mean + 0.5*variance:
            return amplitude
        return 0
    return func

attack_time = 280 * (0.6 + random.random()*0.8)
def creat_random_attack_function(period,variance,amplitude):
    def func(t):
        global attack_time
        if attack_time + 0.5*variance < t:
            attack_time += period * (0.6 + random.random()*0.8)
        t = t - (t//period) * period
        if t >= attack_time - 0.5*variance and t <= attack_time + 0.5*variance:
            return amplitude
        return 0
    return func

def attack(func):
    ip = get_random_ip()
    rate = 0.3
    run_process(func,ip,rate,True)

def random_model1(num,a_num):
    for _ in range(num):
        period = 144
        mean = random.randint(64,120) * 1.0
        variance = random.randint(1,18) * 1.0
        amplitude = random.randint(1,10)
        func = creat_random_square_function(period,mean,variance,amplitude)
        ip = get_random_ip()
        rate = 0.5
        run_process(func,ip,rate,False)
    variance = 1
    amplitude = 5000
    period = 280
    func = creat_random_attack_function(period=period,amplitude=amplitude,variance=variance)
    for _ in range(a_num):
        attack(func)

if __name__ == "__main__":
    random_model1(20,10)
