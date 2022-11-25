# Modules
import os
import time
import logging
import subprocess
import multiprocessing
from pathlib import Path
from datetime import datetime

# Loggin
logging.basicConfig(level = logging.DEBUG)

# Dumping
def start_dump():
    logging.info('Deleting old dumps...')

    total_files = 0
    critical_time = time.time() - 300 # 5 minutes

    for item in Path('/root/autodumper/').glob('*'):
        if item.is_file() and '.pcap' in item.name:
            # Delete old pcaps
            if item.stat().st_mtime < critical_time:
                logging.info(f'Deleting {item.name}...')
                os.system(f'rm {item.absolute()}')
                total_files += 1
                pass

    logging.info(f'Deleted files: {total_files}')

    logging.info('Capturing...')
    subprocess.Popen(f'screen -dm -S hyaxe_dump tcpdump -i any -w /root/autodumper/dump-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.pcap', shell = True, stdout = subprocess.PIPE)

if __name__ == '__main__':
    os.system('screen -X -S hyaxe_dump kill')
    logging.info("PCAP's Auto Dumper")

    while True:
        # Start dump
        p = multiprocessing.Process(target = start_dump)
        p.daemon = True
        p.start()

        # Dump delay
        time.sleep(1)

        # Terminate dump
        p.terminate()
        p.join()
        
        os.system('screen -X -S hyaxe_dump kill')
        logging.info('Captured!')

        time.sleep(3)
