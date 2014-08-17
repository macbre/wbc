#!/bin/bash
ack-grep -i "$1" -C 10 --text --color --pager="less -R"
