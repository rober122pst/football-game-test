FIXTURE_TOTAL_TIME = 90*60
TICK_TIME = 0.1

def start_match():
    current_time = 0
    while current_time < FIXTURE_TOTAL_TIME:
        current_time += TICK_TIME