import time

def sleep(seconds):
    time.sleep(seconds)

def wait_for_condition(driver, condition_func, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(1)
    return False

