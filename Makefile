SHELL := /bin/bash # Use bash syntax
RUNTIME=1
R=2

afl-c: put_n
	-rm -r results/afl-c/results
	cd afl/afl && ./run_all_c.sh $(RUNTIME) $(R)
	echo -e '\n*** Generating input traces ... ***\n'
	(cd input-eval && python3 afl_statistics_calculator.py)
	echo -e '\n*** Generation of input traces ended ***\n'

afl-c-q: put_q # Run AFL in Q mode instead of the traditional mode.
	-rm -r results/afl-c/results
	cd afl/afl && ./run_all_c.sh $(RUNTIME) $(R)
	#echo -e '\n*** Generating input traces ... ***\n'
	(cd input-eval && python3 afl_statistics_calculator.py)
	#echo -e '\n*** Generation of input traces ended ***\n'

afl-gp:
	cd afl/afl && ./run_all_gp.sh $(RUNTIME) $(R)

run_all:
	make pfuzzer
	echo -e "\n+++ pFuzzer runs completed +++\n"
	make cdecoder
	echo -e "\n+++ C Decoder runs completed +++\n"
	make run_gpdecoder
	echo -e "\n+++ Gp Decoder runs completed +++\n"
	make run_pydecoder
	echo -e "\n+++ PyP Decoder runs completed +++\n"

run_pfuzzer:
	sudo -- sh -c 'echo core >/proc/sys/kernel/core_pattern'
	cd pfuzzer/samples/ && sh run_all.sh $(RUNTIME)

run_cdecoder:
	cd cdecoder && make all_subjects RUNTIME=$(RUNTIME)
	echo -e "\nDone with input generation for CParsers.\n"
	make eval_c

run_gpdecoder:
	cd gpdecoder && make all_subjects RUNTIME=$(RUNTIME)
	echo -e "\nDone with input generation for GeParsers.\n"
	make eval_gp

run_vmdecoder:
	cd vmdecoder && make all_subjects RUNTIME=$(RUNTIME)
	echo -e "\nDone with input generation for VMs.\n"
	cd vmdecoder && make eval_lua
	cd vmdecoder && make eval_python

c99_reeval:
	cd gpdecoder/examples/c99 && make
	cd gpdecoder && make c99
	make eval_c99

run_pydecoder:
	cd pydecoder; make all_subjects RUNTIME=$(RUNTIME)
	echo -e "\nDone with input generation for PyParsers.\n"
	make -j eval_pydecoder

pfuzzer:
	rm -rf results/pfuzzer/run_*
	sudo -- sh -c 'echo core >/proc/sys/kernel/core_pattern'
	for run in {1..$(R)}; do \
		cd pfuzzer/samples/ && sh run_all.sh $(RUNTIME) ; \
		cd /home/vagrant ; \
		mkdir results/pfuzzer/run_$$run ; \
		cp -a pfuzzer/samples/. results/pfuzzer/run_$$run/ ; \
		echo -e "\n- pFuzzer run" $$run "completed -\n" ; \
	done
	rm -f results/pfuzzer_runs.csv
	cd results && python3 extract_pfuzzer.py


pure_random: generate_prand
	-rm -r results/cdecoder/results
	rm -rf results/cdecoder/run_*
	for run in {1..$(R)}; do \
		make run_cdecoder ; \
		mkdir results/cdecoder/run_$$run ; \
		cp -a cdecoder/examples/. results/cdecoder/run_$$run/ ; \
		echo -e "\n- Decoder run" $$run "completed -\n" ; \
	done
	rm -f results/cdecoder_runs.csv
	cd results && python3 extract_cdecoder.py
	echo -e '\n*** Generating input traces ... ***\n'
	(cd input-eval && python3 cdecoder_statistics_calculator.py)
	echo -e '\n*** Generation of input traces ended ***\n'

cdecoder: generate_decoder
	-rm -r results/cdecoder/results
	rm -rf results/cdecoder/run_*
	for run in {1..$(R)}; do \
		make run_cdecoder ; \
		mkdir results/cdecoder/run_$$run ; \
		cp -a cdecoder/examples/. results/cdecoder/run_$$run/ ; \
		echo -e "\n- Decoder run" $$run "completed -\n" ; \
	done
	rm -f results/cdecoder_runs.csv
	cd results && python3 extract_cdecoder.py
	echo -e '\n*** Generating input traces ... ***\n'
	(cd input-eval && python3 cdecoder_statistics_calculator.py)
	echo -e '\n*** Generation of input traces ended ***\n'

generator_prand:
	cp
pydecoder:
	rm -rf results/pydecoder/run_*
	for run in {1..$(R)}; do \
		make run_pydecoder ; \
		mkdir results/pydecoder/run_$$run ; \
		cp -a pydecoder/examples/. results/pydecoder/run_$$run/ ; \
		echo -e "\n- PyDecoder run" $$run "completed -\n" ; \
	done
	rm -f results/pydecoder_runs.csv
	cd results && python3 extract_pydecoder.py

gpdecoder:
	rm -rf results/gpdecoder/run_*
	for run in {1..$(R)}; do \
		make run_gpdecoder ; \
		mkdir results/gpdecoder/run_$$run ; \
		cp -a gpdecoder/examples/. results/gpdecoder/run_$$run/ ; \
		echo -e "\n- GPDecoder run" $$run "completed -\n" ; \
	done
	rm -f results/gpdecoder_runs.csv
	cd results && python3 extract_gpdecoder.py

vmdecoder:
	rm -rf results/vmdecoder/run_*
	for run in {1..$(R)}; do \
		make run_vmdecoder ; \
		mkdir results/vmdecoder/run_$$run ; \
		cp -a vmdecoder/examples/. results/vmdecoder/run_$$run/ ; \
	echo -e "\n- VMDecoder run" $$run "completed -\n" ; \
	done
	rm -f results/vmdecoder_runs.csv
	cd results && python3 extract_vmdecoder.py


eval_c:
	make -j eval_cdecoder

eval_cdecoder: eval_cjson eval_tiny eval_ini eval_mjs eval_csv
	@echo -e "\nDONE evaluating C subjects.\n"

eval_gp:
	cd gpdecoder && make compile
	make -j eval_gpdecoder

eval_gpdecoder: eval_c99 eval_ccalc eval_expr eval_lua eval_lemonc
	@echo -e "\nDONE evaluating GpParsers subjects.\n"

eval_pydecoder: eval_url eval_ip eval_ssn eval_fourfn eval_pyc eval_pcalc eval_pjson
	@echo -e "\nDONE evaluating PyParser subjects.\n"

eval_url:
	awk -i inplace '!seen[$$0]++' pydecoder/examples/url/inputs.txt
	cd pydecoder/examples/url && python3 eval.py

eval_ip:
	awk -i inplace '!seen[$$0]++' pydecoder/examples/ip/inputs.txt
	cd pydecoder/examples/ip && python3 eval.py

eval_ssn:
	awk -i inplace '!seen[$$0]++' pydecoder/examples/ssn/inputs.txt
	cd pydecoder/examples/ssn && python3 eval.py

eval_fourfn:
	awk -i inplace '!seen[$$0]++' pydecoder/examples/fourfn/inputs.txt
	cd pydecoder/examples/fourfn && python3 eval.py


eval_cjson:
	cd cdecoder/examples/cjson && rm -rf *.o cjson __pycache__/ *.gcda *.gcno build *.cov* *.dSYM coverage.*
	cd cdecoder/examples/cjson && gcc -fprofile-arcs -ftest-coverage -g -o cjson.cov cJSON_o.c
	awk -i inplace '!seen[$$0]++' cdecoder/examples/cjson/inputs.txt
	awk -i inplace '!seen[$$0]++' cdecoder/examples/cjson/inputs.json
	cd cdecoder/examples/cjson && python3 eval-cjson.py

eval_csv:
	cd cdecoder/examples/csv && rm -rf *.o csv __pycache__/ *.gcda *.gcno build *.cov* *.dSYM coverage.*
	cd cdecoder/examples/csv && gcc -fprofile-arcs -ftest-coverage -g -o csvparser.cov csvparser_o.c
	awk -i inplace '!seen[$$0]++' cdecoder/examples/csv/inputs.txt
	awk -i inplace '!seen[$$0]++' cdecoder/examples/csv/inputs.json
	cd cdecoder/examples/csv && python3 eval-csv.py

eval_ini:
	cd cdecoder/examples/ini && rm -rf *.o ini __pycache__/ *.gcda *.gcno build *.cov* *.dSYM coverage.*
	cd cdecoder/examples/ini && gcc -fprofile-arcs -ftest-coverage -g -o ini.cov ini_o.c
	awk -i inplace '!seen[$$0]++' cdecoder/examples/ini/inputs.txt
	awk -i inplace '!seen[$$0]++' cdecoder/examples/ini/inputs.json
	cd cdecoder/examples/ini && python3 eval-ini.py

eval_mjs:
	cd cdecoder/examples/mjs && rm -rf *.o mjs __pycache__/ *.gcda *.gcno build *.cov* *.dSYM coverage.*
	cd cdecoder/examples/mjs && gcc -fprofile-arcs -ftest-coverage -g -o mjs.cov mjs_o.c -ldl
	awk -i inplace '!seen[$$0]++' cdecoder/examples/mjs/inputs.txt
	awk -i inplace '!seen[$$0]++' cdecoder/examples/mjs/inputs.json
	cd cdecoder/examples/mjs && python3 eval-mjs.py

eval_tiny:
	cd cdecoder/examples/tiny && rm -rf *.o tiny __pycache__/ *.gcda *.gcno build *.cov* *.dSYM coverage.*
	cd cdecoder/examples/tiny && gcc -fprofile-arcs -ftest-coverage -g -o tiny.cov tiny_o.c
	awk -i inplace '!seen[$$0]++' cdecoder/examples/tiny/inputs.txt
	awk -i inplace '!seen[$$0]++' cdecoder/examples/tiny/inputs.json
	cd cdecoder/examples/tiny && python3 eval-tiny.py

eval_c99:
	awk -i inplace '!seen[$$0]++' gpdecoder/examples/c99/inputs.txt
	cd gpdecoder/examples/c99 && python3 eval-c99.py

eval_ccalc:
	awk -i inplace '!seen[$$0]++' gpdecoder/examples/ccalc/inputs.txt
	cd gpdecoder/examples/ccalc && python3 eval-ccalc.py

eval_expr:
	awk -i inplace '!seen[$$0]++' gpdecoder/examples/expr/inputs.txt
	cd gpdecoder/examples/expr && python3 eval-expr.py

eval_lua:
	awk -i inplace '!seen[$$0]++' gpdecoder/examples/lua/inputs.txt
	cd gpdecoder/examples/lua && python3 eval-lua.py

eval_lemonc:
	awk -i inplace '!seen[$$0]++' gpdecoder/examples/lemon/inputs.txt
	cd gpdecoder/examples/lemon && python3 eval-lemonc.py

eval_pyc:
	awk -i inplace '!seen[$$0]++' pydecoder/examples/pyc/inputs.txt
	cd pydecoder/examples/pyc && python3 eval-pyc.py

eval_pcalc:
	awk -i inplace '!seen[$$0]++' pydecoder/examples/pcalc/inputs.txt
	cd pydecoder/examples/pcalc && python3 eval-pcalc.py

eval_pjson:
	awk -i inplace '!seen[$$0]++' pydecoder/examples/pjson/inputs.txt
	cd pydecoder/examples/pjson && python3 eval-pjson.py

clean:
	rm -f cdecoder/examples/cjson/coverage*
	rm -f cdecoder/examples/csv/coverage*
	rm -f cdecoder/examples/ini/coverage*
	rm -f cdecoder/examples/mjs/coverage*
	rm -f cdecoder/examples/tiny/coverage*
	rm -f pfuzzer/samples/cjson/*.html
	rm -f pfuzzer/samples/csv/*.html
	rm -f pfuzzer/samples/ini/*.html
	rm -f pfuzzer/samples/mjs/*.html
	rm -f pfuzzer/samples/tinyc/*.html
	rm -rf results/cdecoder/*
	rm -rf results/pfuzzer/*

generate_prand:
	cp cdecoder/stateless/generate-purerand.py cdecoder/stateless/generate.py

generate_decoder:
	cp cdecoder/stateless/generate-decoder.py cdecoder/stateless/generate.py

put_q:
	sed -i 's/-n/-Q/g' afl/afl/programs/cjson/run_exp_dm.sh
	sed -i 's/-n/-Q/g' afl/afl/programs/csv/run_exp_dm.sh
	sed -i 's/-n/-Q/g' afl/afl/programs/ini/run_exp_dm.sh
	sed -i 's/-n/-Q/g' afl/afl/programs/mjs/run_exp_dm.sh
	sed -i 's/-n/-Q/g' afl/afl/programs/tiny/run_exp_dm.sh

put_n:
	sed -i 's/-Q/-n/g' afl/afl/programs/cjson/run_exp_dm.sh
	sed -i 's/-Q/-n/g' afl/afl/programs/csv/run_exp_dm.sh
	sed -i 's/-Q/-n/g' afl/afl/programs/ini/run_exp_dm.sh
	sed -i 's/-Q/-n/g' afl/afl/programs/mjs/run_exp_dm.sh
	sed -i 's/-Q/-n/g' afl/afl/programs/tiny/run_exp_dm.sh
