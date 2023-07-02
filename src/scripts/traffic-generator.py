import requests
import os, random
import time, datetime
import logging

JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvb3QiLCJleHAiOjE2ODc4ODUwMTcsImlhdCI6MTY4Nzc5ODYxNywiYWRtaW4iOnRydWV9.S1qhr27kOy9DhVtmnsQb8O8mG0h_bAyWMoTO2XTpGOA"
FILES_PATH = "/Users/fdrobiazg/Workspace/thesis-project/images/"

URL = "http://clr2gray.com/upload"
TRAFFIC_INTENSITY = 30
SIMULATION_TIME = 120


logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.INFO)

if __name__ == "__main__":
    for i in range(int(SIMULATION_TIME * TRAFFIC_INTENSITY)):
        headers = {"Authorization": "Bearer " + JWT_TOKEN}
        file = random.choice(os.listdir(FILES_PATH))
        r = requests.post(URL, headers=headers, files={'file': open(FILES_PATH + "/" + file,'rb')})
        print(str(datetime.datetime.utcnow()) + " STATUS " + str(r.status_code))
        logging.info(str(datetime.datetime.utcnow()) + " STATUS " + str(r.status_code))
        time.sleep(1/TRAFFIC_INTENSITY)