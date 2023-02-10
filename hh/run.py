import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cpu-machine', action='store_true', help='whether this is a cpu machine')
args = parser.parse_args()
is_cpu_machine = args.cpu_machine

if is_cpu_machine:
	subprocess.Popen(['python3', '/home/auto_stop.py', '--cpu-machine'])
else:
	subprocess.Popen(['python3', '/home/auto_stop.py'])