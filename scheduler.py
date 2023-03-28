import schedule
import time
import subprocess

def run_programs():
    #Run parsin and formatting programs
    subprocess.run(['python3', 'parsing_wikipedia.py'])
    subprocess.run(['python3', 'parsing_iso.py'])
    #If the visualization is already running, it will kill the old version
    subprocess.run(['pkill', '-f', 'visualization.py'])
    #Start new version
    subprocess.Popen(['python3', 'visualization.py'])

run_programs()
schedule.every(30).seconds.do(run_programs)

while True:
    schedule.run_pending()
    time.sleep(10)
    print('working...')














# import schedule
# import time
# import subprocess

# def run_programs():
#     #subprocess.run(['python3', 'parsing_wikipedia.py'])

    
#     subprocess.run(['python3', 'parsing_iso.py'])
#     subprocess.run(['python3', 'visualization.py'])

# # Run the programs every hour
# schedule.every().second.do(run_programs)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
#     print('working...')



    #Laucnh pars1
    #Launch pars2
    #If VIS launched:
        #Stop vis
    #Launch vis