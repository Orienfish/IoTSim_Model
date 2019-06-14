#!/bin/bash
pid=$(ps aux | grep perf | grep -v grep | awk '{print $2}')
echo $pid
kill -9 $pid