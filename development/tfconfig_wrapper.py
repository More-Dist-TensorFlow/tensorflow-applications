#!/usr/bin/env python3
import os, json
import sys
import logging
import subprocess

def subprocess_run(*popenargs, input=None, check=False, **kwargs):
    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr)
    return retcode, stdout, stderr

########################
old_args = sys.argv

tf_config_json = os.environ.get("TF_CONFIG", "{}")
tf_config = json.loads(tf_config_json)

worker = tf_config.get("worker", {})
arg_ = '--worker_hosts=' + ','.join(worker)
old_args.append(arg_)

ps = tf_config.get("ps", {})
arg_ = '--ps_hosts=' + ','.join(ps)
old_args.append(arg_)

task = tf_config.get("task")
arg_ = '--job_name=' + task['type']
old_args.append(arg_)
arg_ = '--task_index=' + task['index']
old_args.append(arg_)

old_args[0] = 'worker.py'
old_args = ['python'] + old_args
print('Running:', old_args)

try:
    completed = subprocess.run(old_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exit(completed.returncode)
except: # Lower than python3.5
    completed = subprocess_run(old_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exit(completed[0])
