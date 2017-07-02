#!/bin/bash
set -evx

mkdir ~/.muecore/

# safety check
if [ ! -f ~/.muecore/mue.conf ]; then
  cp share/coin.conf.example ~/.muecore/mue.conf
fi
