#!/bin/env python3

import argparse 
from .pms import PMS

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='task', required=True)

setup_parser = subparsers.add_parser('setup')
setup_parser.add_argument('--mode', choices=['active', 'passive'], default='active')

sleep_parser = subparsers.add_parser('sleep')

measure_parser = subparsers.add_parser('measure')
measure_parser.add_argument('--mode', choices=['active', 'passive'], default='active')
measure_parser.add_argument('--duration', type=int, default=30)

args = parser.parse_args()

with PMS() as pms:
    if args.task == 'setup':
        pms.wakeup()
        pms.set_mode(args.mode)
    elif args.task == 'measure':
        pms.measure(args.duration, mode=args.mode)
    if args.task == 'sleep':
        pms.sleep()
