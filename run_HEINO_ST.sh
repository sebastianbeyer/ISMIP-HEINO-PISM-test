#!/usr/bin/env bash


set -e


mpiexec -n 32 --use-hwthread-cpus pismr \
-i ./HEINO_4PISM_ST.nc \
-bootstrap \
-Mx 81 -My 81 -Mz 201 -Mbz 11 -z_spacing equal -Lz 8000 -Lbz 2000 \
-grid.recompute_longitude_and_latitude false -grid.registration corner \
-front_retreat_file ./HEINO_4PISM_ST.nc \
-ys -200000 -ye 0 \
-surface given \
-stress_balance ssa+sia \
-pseudo_plastic \
-pseudo_plastic_q 0.3  \
-till_effective_fraction_overburden 0.02 \
-tauc_slippery_grounding_lines  \
-sia_e 3.0 \
-ts_file ts_HEINO_ST.nc \
-ts_times -200000:100:0 \
-extra_file ex_HEINO_ST.nc \
-extra_times -200000:1000:0 \
-extra_vars diffusivity,temppabase,tempicethk_basal,bmelt,tillwat,velsurf_mag,mask,thk,topg,usurf,hardav,velbase_mag,tauc \
-o HEINO_ST.nc \

