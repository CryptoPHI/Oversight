#!/bin/bash
set -evx

mkdir ~/.muecore/

# safety check
if [ ! -f ~/.muecore/mue.conf ]; then
  cp share/mue.conf.example ~/.muecore/mue.conf
fi
