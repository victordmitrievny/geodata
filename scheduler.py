import schedule
import time
import subprocess

def run_programs():
    #subprocess.run(['python', 'parsing_wikipedia.py'])
    #subprocess.run(['python', 'parsing_iso.py'])
    subprocess.run(['python', 'visualization.py'])

# Run the programs every hour
schedule.every().hour.do(run_programs)

while True:
    schedule.run_pending()
    time.sleep(15)
    print('working...')