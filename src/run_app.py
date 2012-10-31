#!/usr/bin/env python

import sys
sys.path.insert(0, '..')

import resource_loader

import main
main.app.run(host='0.0.0.0')
