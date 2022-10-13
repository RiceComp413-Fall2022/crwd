import os
import sys
import subprocess

def enable_monitor_mode(adapter):
    '''
    Note: tshark has a -I flag to request monitor mode itself.
    This explicit configuration is being done because tshark reports an error when -I is used with our driver.
    '''
    if os.name == 'nt':
        print('Windows is not supported.')
        sys.exit(-1)

    print(f"Enabling monitor mode on adapter: {adapter}")
    subprocess.run(['ifconfig', adapter, 'down'])
    subprocess.run(['iwconfig', adapter, 'mode', 'monitor'])
    subprocess.run(['ifconfig', adapter, 'up'])
