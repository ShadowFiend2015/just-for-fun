#!/bin/bash
# -vps and -vpc is not necessary
./splitwav -config vad.toml -f origin.wav 2>err.log 1>std.log &
#./splitwav -config vad.toml -f origin.wav -vps 99 -vpc 99 2>err.log 1>std.log &

