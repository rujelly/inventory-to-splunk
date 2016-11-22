#!/usr/local/bin/python3
import csv
import queue
import subprocess
import sys
import threading
import time
import unittest

class NiktoThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__.self()
        self.queue = queue

    def run(self):
        while True:
            host = self.queue.get()
            ip = host[0]
            port = host[1]
            do_nikto_with(ip, port)
            self.queue.task_done()


class ParsingThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__.self()
        self.queue = queue

    def run(self):
        while True:
            # TODO
            self.queue.task_done()

class MyTest(unittest.TestCase):
    def test_build_command_with():
        ip = '10.218.152.107'
        port = '443'
        cmd = build_command_with(ip, port)
        correct_string = 'nikto -findonly -nolookup -h %s -p %s | tee -a ~/NiktoOutput/nikto_%s.out' % \
            (ip, port, time.strftime("%d%m%Y"))
        self.assertEqual(cmd, correct_string)

def do_nikto_with(ip, port):
    full_cmd = build_command_with(ip, port)
    subprocess.call(full_cmd, shell=True, timeout=20)

def build_command_with(ip, port):
    host_call = '-h ' + ip
    port_call = '-p ' + port
    nikto_switches = '-findonly -nolookup'
    output_cmd = '| tee -a ~/NiktoOutput/nikto_' + time.strftime("%d%m%Y") + '.out'
    full_cmd = 'nikto %s %s %s %s' % (nikto_switches, host_call, port_call, output_cmd)
    return full_cmd

def main():
    input_csv = open('sampleSockets.csv')
    output_txt = open('servers_found.txt', 'a')
    output_splunk_lookup = open('servers_lookup.csv', 'a')
    
    input_reader = csv.reader(input_csv)
    text_writer = csv.writer(output_txt)
    splunk_lookup_writer = csv.writer(output_splunk_lookup)

    input_rows = list(input_reader)
    host_queue = Queue.Queue()
    for ip_and_port in input_rows:
        host_queue.put(ip_and_port)

    '''for line in file_lines:
        if line[15] == '+':
            if "No web server" in line:
                values = line.split('+').strip()
            else:
                values = line.split('+').strip()
                values = [values[0], values[0]]
            output_writer.write(values)'''

if __name__ == '__main__':
    if sys.argv[1] == 'test':
        unittest = MyTest()
    else:
        main()