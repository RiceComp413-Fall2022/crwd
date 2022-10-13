'''
This file is adapted from https://github.com/schollz/howmanypeoplearearound
'''

import os
import subprocess
import click

from howmanypeoplearearound.scan import run_scan
from howmanypeoplearearound.chooseadapter import choose_adapter

from util.monitor_mode import enable_monitor_mode

from crwd.reportndevices import report_n_devices

@click.command()
@click.option('-a', '--adapter', default='', help='adapter to use')
@click.option('-s', '--scantime', default='60', help='time in seconds to scan')
@click.option('-o', '--out', default='log.json', help='output cellphone data to file')
@click.option('-d', '--dictionary', default='oui.txt', help='OUI dictionary')
@click.option('-v', '--verbose', help='verbose mode', is_flag=True)
@click.option('--number', help='just print the number', is_flag=True)
@click.option('-j', '--jsonprint', help='print JSON of cellphone data', is_flag=True)
@click.option('-n', '--nearby', help='only quantify signals that are nearby (rssi > -70)', is_flag=True)
@click.option('--allmacaddresses', help='do not check MAC addresses against the OUI database to only recognize known cellphone manufacturers', is_flag=True)  # noqa
@click.option('-m', '--manufacturers', default='', help='read list of known manufacturers from file')
@click.option('--nocorrection', help='do not apply correction', is_flag=True)
@click.option('--sort', help='sort cellphone data by distance (rssi)', is_flag=True)
@click.option('--targetmacs', help='read a file that contains target MAC addresses', default='')
@click.option('-f', '--pcap', help='read a pcap file instead of capturing')
def main(adapter, scantime, verbose, dictionary, number, nearby, jsonprint, out, allmacaddresses, manufacturers, nocorrection, sort, targetmacs, pcap):
    # Check for root privelages
    if os.geteuid() != 0:
        "Please run as root (to enable switching adapter to monitor mode)."
    
    # Choose adapter
    if len(adapter) == 0:
        adapter = choose_adapter()
    
    # Enable monitor mode
    # TODO: periodically re-enable monitor mode in case it resets during execution
    enable_monitor_mode(adapter)

    # Loop forever
    while True:
        # Run scan
        adapter, num_people = run_scan(adapter, scantime, verbose, dictionary, number,
                nearby, jsonprint, out, allmacaddresses, manufacturers, nocorrection, True, sort, targetmacs, pcap)
        
        # Report to backend
        report_n_devices(num_people)

        print()

if __name__ == '__main__':
    main()
