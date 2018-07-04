#!/bin/bash
# Program
#       run the qqbot server and set the arguments.
# History
# 2018/06/28    e0e   first release
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

if [[ "$QQ_NUM_SENDER" ]]; then
    sed -i "s/2590870063/${QQ_NUM_SENDER}/g" /bots/qqbot-sv.py
fi
if [[ "$QQ_AUTH_PORT" ]]; then
    sed -i "s/8189/${QQ_AUTH_PORT}/g" /bots/qqbot-sv.py
fi
if [[ "$QQ_RCV_NICK" ]]; then
    sed -i "s/jack/${QQ_RCV_NICK}/g" /bots/qqbot-sv.py
fi

if [[ "$WX_QR_PORT" ]]; then
    sed -i "s/8289/${WX_QR_PORT}/g" /bots/wxbot-sv.py
fi
if [[ "$WX_NICKNAME" ]]; then
    sed -i "s/anquantest/${WX_NICKNAME}/g" /bots/wxbot-sv.py
fi

# cycle time (seconds)
sec=3600

while true
do
    PIDS=`ps -ef |grep /bots/qqbot-sv.py |grep -v grep | awk '{print $2}'`
    time=`date`
    if [ "$PIDS" != "" ]; then
        echo "[$time]  qqbot is runing!" >>/bots/logs/start.log
    else
        # start the qqbot
        echo "[$time] ------------ qqbot abort ------------" >>/bots/logs/start.log
        nohup python /bots/qqbot-sv.py >>/bots/logs/qqbot.log 2>&1 &
        echo "[$time] ------------ qqbot restart ------------" >>/bots/logs/start.log
    fi

    PIDS_WX=`ps -ef |grep /bots/wxbot-sv.py |grep -v grep | awk '{print $2}'`
    time=`date`
    if [ "$PIDS_WX" != "" ]; then
        echo "[$time]  wxbot is runing!" >>/bots/logs/start.log
    else
        # start the qqbot
        echo "[$time] ------------ wxbot abort ------------" >>/bots/logs/start.log
        nohup python /bots/wxbot-sv.py >>/bots/logs/wxbot.log 2>&1 &
        echo "[$time] ------------ wxbot restart ------------" >>/bots/logs/start.log
    fi
    sleep $sec
done

