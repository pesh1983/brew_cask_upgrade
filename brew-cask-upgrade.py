#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import argparse
import os
import subprocess

import sys


def get_current_version(program_info):
    # e.g. program_info[0] == 'keepassx: 2.0.3'
    program_name, version = program_info[0].split(':')
    return version.strip()


def get_new_version(program_info):
    # e.g. program_info[2] == '/usr/local/Caskroom/keepassx/2.0.2 (217B)'
    return os.path.basename(program_info[2].split(' ')[0])


def upgrade_program(program_name):
    sys.stdout.write('Uninstalling an old version ...\n')
    run(['brew', 'cask', 'uninstall', program_name], write_to_stdout=True)
    sys.stdout.write('Installing a new version ...\n')
    run(['brew', 'cask', 'install', program_name], write_to_stdout=True)


def run(args, write_to_stdout=False):
    process = subprocess.Popen(
        args,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    stdoutdata = process.communicate()[0] or ''
    stdoutdata = stdoutdata.decode('utf-8')

    if stdoutdata:
        if write_to_stdout or process.returncode != 0:
            sys.stdout.write(stdoutdata)

    if process.returncode != 0:
        exit(process.returncode)

    return stdoutdata


def get_brew_program_list():
    stdoutdata = run(
        ['brew', 'cask', 'list']
    )
    return stdoutdata.strip().split('\n')


def get_brew_program_info(program_name):
    stdoutdata = run(
        ['brew', 'cask', 'info', program_name]
    )
    return stdoutdata.split('\n')


def check_and_update_program(program_name):
    sys.stdout.write('%s ... ' % program_name)
    program_info = get_brew_program_info(program_name)
    current_version = get_current_version(program_info)
    new_version = get_new_version(program_info)
    sys.stdout.write('{}\n'.format(new_version))
    if current_version != new_version:
        sys.stdout.write('Upgrading {program_name}: '
                         '{cur_ver} -> {new_ver} ...\n'.format(
            program_name=program_name,
            cur_ver=current_version,
            new_ver=new_version,
        ))
        upgrade_program(program_name)
        sys.stdout.write('Done.\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check versions and upgrade brew cask programs.'
    )
    parser.add_argument(
        'program',
        help='program to check and update if necessary.',
        type=str,
        nargs='?',
    )
    args = parser.parse_args()

    if args.program:
        check_and_update_program(args.program)
    else:
        program_name_list = get_brew_program_list()
        for program_name in program_name_list:
            check_and_update_program(program_name)
