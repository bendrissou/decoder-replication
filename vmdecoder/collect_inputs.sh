# Before we compute the aggregated total coverage of 10 runs of gpdecoder,
# we need to collect all generated inputs into a single place.

echo -n '' > examples/c99/inputs.txt
echo -n '' > examples/ccalc/inputs.txt
echo -n '' > examples/lemon/inputs.txt
echo -n '' > examples/expr/inputs.txt
echo -n '' > examples/lua/inputs.txt
echo -n '' > examples/pcalc/inputs.txt
echo -n '' > examples/pjson/inputs.txt
echo -n '' > examples/pyc/inputs.txt

R=$1
echo -e '\n*** Collect all gpdecoder inputs ***\n'
for i in $(seq 1 $R)
do
        cat ../results/gpdecoder/run_${i}/c99/inputs.txt >> examples/c99/inputs.txt
        cat ../results/gpdecoder/run_${i}/ccalc/inputs.txt >> examples/ccalc/inputs.txt
        cat ../results/gpdecoder/run_${i}/lemon/inputs.txt >> examples/lemon/inputs.txt
        cat ../results/gpdecoder/run_${i}/expr/inputs.txt >> examples/expr/inputs.txt
        cat ../results/gpdecoder/run_${i}/lua/inputs.txt >> examples/lua/inputs.txt
        cat ../results/gpdecoder/run_${i}/pcalc/inputs.txt >> examples/pcalc/inputs.txt
        cat ../results/gpdecoder/run_${i}/pjson/inputs.txt >> examples/pjson/inputs.txt
        cat ../results/gpdecoder/run_${i}/pyc/inputs.txt >> examples/pyc/inputs.txt
done
awk -i inplace '!seen[$0]++' examples/c99/inputs.txt
awk -i inplace '!seen[$0]++' examples/ccalc/inputs.txt
awk -i inplace '!seen[$0]++' examples/lemon/inputs.txt
awk -i inplace '!seen[$0]++' examples/expr/inputs.txt
awk -i inplace '!seen[$0]++' examples/lua/inputs.txt
awk -i inplace '!seen[$0]++' examples/pcalc/inputs.txt
awk -i inplace '!seen[$0]++' examples/pjson/inputs.txt
awk -i inplace '!seen[$0]++' examples/pyc/inputs.txt

echo -e '\n*** Finished collecting all gpdecoder inputs ***\n'

