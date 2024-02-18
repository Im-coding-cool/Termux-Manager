#!/bin/sh

if [ "$1" = "-time" ]; then
    shift
    start=$(date -d "$1" +%s)
    end=$(date +%s)
    echo $(($end - $start))
else
    # 处理没有-a选项的情况
    echo 0
fi
