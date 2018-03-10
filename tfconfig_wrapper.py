#!/usr/bin/env python3
# Usage: Set env "TF_CONFIG" correctly, and I'll get worker_hosts,ps_hosts,job_name,task_index from the env var, 
#        and call ./worker.py with arg formatted like: --ps_hosts=127.0.0.1:8887 \
#           --worker_hosts=127.0.0.1:8888,127.0.0.1:8889 \
#           --job_name=worker \
#           --task_index=0
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

import sys
import os

def whereami():
    mypos = sys.argv[0]
    if mypos[0] == '/' or mypos[0] == '~':
        return os.path.dirname(mypos)
    else:
        mypos = './' + mypos
        return os.path.dirname(os.path.realpath(mypos))

########################
old_args = sys.argv

tf_config_json = os.environ.get("TF_CONFIG", "{}")
print('DEBUG: env TF_CONFIG is', tf_config_json)
tf_config = json.loads(tf_config_json)

cluster = tf_config.get("cluster", {})

master = cluster.get("master", {})
arg_ = '--master_hosts=' + ','.join(master)
old_args.append(arg_)

worker = cluster.get("worker", {})
arg_ = '--worker_hosts=' + ','.join(worker)
old_args.append(arg_)

ps = cluster.get("ps", {})
arg_ = '--ps_hosts=' + ','.join(ps)
old_args.append(arg_)

try:
    task = tf_config.get("task")
    arg_ = '--job_name=' + task['type']
    old_args.append(arg_)
    arg_ = '--task_index=' + str(task['index'])
    old_args.append(arg_)
except TypeError as err:
    print('Warning, typerr {0}'.format(err))

old_args[0] = whereami() + 'worker.py'
old_args = ['python'] + old_args
print('Running:', old_args)

try:
    completed = subprocess.run(old_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exit(completed.returncode)
except: # Lower than python3.5
    completed, stdout, stderr = subprocess_run(old_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('stdout:', stdout, '\nstderr:', stderr)
    exit(completed)
