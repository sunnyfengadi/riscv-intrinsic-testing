#!/bin/bash

export PROJ_ROOT=$(pwd)

export RISCV_ROOT=/opt/analog/riscv/1.0.1/Riscv
export PATH=${RISCV_ROOT}/software/host/bin/gcc/bin:${PATH}
export LD_LIBRARY_PATH=${RISCV_ROOT}/software/host/lib:${LD_LIBRARY_PATH}
