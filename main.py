import random
from Blockchain import Blockchain
import time


def convert(seconds):
    seconds = seconds % (24 * 86400)

    day = seconds // 86400
    seconds %= 86400
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%02d:%02d:%02d:%02d" % (day, hour, minutes, seconds)


def sample_data(x):
    f = open("UAV_data.txt", "w")
    latitude = round(random.uniform(-90, 90), 2)
    longitude = round(random.uniform(-180, 180), 2)
    altitude = round(random.uniform(25, 50))
    clock = 0
    for i in range(x):
        file_line = "%07d %07.2f %07.2f %07.2f\n" % (clock, latitude, longitude, altitude)
        clock += random.uniform(1600, 2000)   # Random time intervals are ± 30 minutes
        latitude += random.uniform(-5, 5)  # Random latitude changes ± 5 degrees
        if 90 <= latitude or latitude <= -90:
            latitude = round(random.uniform(-90, 90), 2)
        longitude += random.randint(-5, 5)  # Random longitude changes ± 5 degrees
        if 180 <= longitude or longitude <= -180:
            longitude = round(random.uniform(-180, 180), 2)
        altitude += random.randint(-2, 2)  # Random altitude changes ± 2 feet
        latitude = round(latitude, 5)
        longitude = round(longitude, 5)
        altitude = round(altitude, 5)
        f.write(file_line)  # The data is written to the file line
    f.close()

def display_chain(m):
    blockchain = Blockchain()
    change = m * .25
    X = random.randint(int(m - change), int(m + change))
    sample_data(X)
    file = open("UAV_data.txt", "r")


    for line in file:
        data_line = line.rstrip().split(" ")
        # Text file data is converted to a dictionary
        data = {"time": data_line[0],
                "position": (data_line[1], data_line[2]),
                "altitude": data_line[3]}
        # Data of transmission is added to un-mined data of blockchain instance
        blockchain.add_new_data(data)
        # Un-mined data for the blockchain are 25% likely to be randomly mined after each line read
        miner = random.randint(1, 4)
        if miner == 1:
            blockchain.mine()

    # n counts the number of blocks
    n = 0
    for block in blockchain.chain:
        # Skips the genesis block of the blockchain
        if n == 0:
            pass
        # Prints block number and data from block
        else:
            print("\nBlock %d" % n)
            print("=" * 57)
            for blockdata in block.data:
                elapsed = str(convert(int(blockdata["time"])))
                final_lat = round(float(blockdata["position"][0]), 2)
                final_long = round(float(blockdata["position"][1]), 2)
                final_alt = float(blockdata["altitude"])
                full_data = "%s: (%05.2f, %05.2f) @ %2.fft" % (elapsed, final_lat, final_long, final_alt)
                print(full_data)
        n += 1



def test_chain(m):
    result = []
    for i in range(m):
        start = time.time()
        blockchain = Blockchain()
        change = 50 * .25
        X = random.randint(int(50 - change), int(50 + change))
        sample_data(X)
        file = open("UAV_data.txt", "r")

        for line in file:
            data_line = line.rstrip().split(" ")
            # Text file data is converted to a dictionary
            data = {"time": data_line[0],
                    "position": (data_line[1], data_line[2]),
                    "altitude": data_line[3]}
            # Data of transmission is added to un-mined data of blockchain instance
            blockchain.add_new_data(data)
            # Un-mined data for the blockchain are 25% likely to be randomly mined after each line read
            miner = random.randint(1, 4)
            if miner == 1:
                blockchain.mine()

        # n counts the number of blocks
        n = 0
        for block in blockchain.chain:
            # Skips the genesis block of the blockchain
            if n == 0:
                pass
            # Prints block number and data from block
            else:
                print("\nBlock %d" % n)
                print("=" * 57)
                for blockdata in block.data:
                    elapsed = str(convert(int(blockdata["time"])))
                    final_lat = round(float(blockdata["position"][0]), 2)
                    final_long = round(float(blockdata["position"][1]), 2)
                    final_alt = float(blockdata["altitude"])
                    full_data = "%s: (%05.2f, %05.2f) @ %2.fft" % (elapsed, final_lat, final_long, final_alt)
        result.append("%0.3f with nonce %d" % (time.time() - start, blockchain.difficulty))

    for i in result:
        print(i)


display_chain(10)




