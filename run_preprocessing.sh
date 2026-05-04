echo run this inside "preprocessing" folder
ls 
IXI_TEST=../data/IXI_test
SAMPLE_NAME=IXI012-HH-1211-T1
SAMPLE=$IXI_TEST/$SAMPLE_NAME.nii.gz
export OMP_NUM_THREADS=8 # for multithreading in bet and fast
mkdir -p ${IXI_TEST}_pre/bet && echo Running bet
bet $SAMPLE ${IXI_TEST}_pre/bet/$SAMPLE_NAME
mkdir -p ${IXI_TEST}_pre/fast && echo Running fast
fast -B -o ${IXI_TEST}_pre/fast/$SAMPLE_NAME ${IXI_TEST}_pre/bet/$SAMPLE_NAME.nii.gz
mkdir -p ${IXI_TEST}_pre/fnirt && echo Running fnirt
fnirt --in=${IXI_TEST}_pre/fast/${SAMPLE_NAME}_restore.nii.gz --config=my_fnirt.cnf --iout=${IXI_TEST}_pre/fnirt/${SAMPLE_NAME}

# fnirt --in=../data/IXI_test_pre/fast/IXI012-HH-1211-T1_restore.nii.gz --config=my_fnirt.cnf --iout=../data/IXI_test_pre/fnirt/IXI012-HH-1211-T1
echo Running voxel-norm
echo finished