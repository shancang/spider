#!/bin/bash
kill -9 $(ps x | grep spider.py | grep -v grep | awk '{print $1}' )
