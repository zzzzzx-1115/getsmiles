import psutil
import time
import argparse
import pynvml
import subprocess
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--cpu-machine', action='store_true', help='whether this is a cpu machine')
parser.add_argument('--check-interval', type=float, default=1800)
parser.add_argument('--cpu-threshold', '-c', type=float, help='if one cpu-percent is larger than this, it is working', default=0.1)
parser.add_argument('--gpu-threshold', '-g', type=int, help='if one cpu-percent is larger than this, it is working', default=0.1)
args = parser.parse_args()


def execute(command):
    # execute a shell command and return the result
    command_groups = command.split(" ")
    results = subprocess.check_output(command_groups)
    return results.decode("utf-8")


def stop_instance(instance_id):
    command = "aws ec2 stop-instances --instance-ids %s" % instance_id
    execute(command)
    print("Instance %s is stopped" % instance_id)


def main(args):
    is_cpu_machine = args.cpu_machine

    if is_cpu_machine:
        while True:
            using_cpu = False

            cpus_percent = psutil.cpu_percent(percpu=True)

            for cpu_percent in cpus_percent:
                if cpu_percent > args.cpu_threshold:
                    using_cpu = True
                    break
        
            if using_cpu:
                time.sleep(args.check_interval)
                continue
            else:
                break
    else:
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        while True:
            using_cpu = False

            cpus_percent = psutil.cpu_percent(percpu=True)

            for cpu_percent in cpus_percent:
                if cpu_percent > args.cpu_threshold:
                    using_cpu = True
                    break
        
            if using_cpu:
                time.sleep(args.check_interval)
                continue
            else:
                break

            using_gpu = False
            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                info = pynvml.nvmlDeviceGetUtilizationRates(handle)
                if info.gpu > args.gpu_threshold:
                    using_gpu = True
                    break

            if using_gpu:
                time.sleep(args.check_interval)
                continue
            else:
                break
        
    # stop instance
    command = "sudo shutdown now -h"
    execute(command)

main(args)