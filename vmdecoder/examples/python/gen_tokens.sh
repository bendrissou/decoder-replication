for i in {1..255};
do
  for j in {1..255};
  do
    echo $i $j;
    timeout 2 python3 gen_tokens.py I $i $j >> log 2>&1
    timeout 2 python3 gen_tokens.py S $i $j >> log 2>&1
  done;
done
