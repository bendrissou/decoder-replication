SRC=examples/c99/ examples/ccalc/ examples/expr/ examples/lua/ examples/lemon/
V=examples/hellodecoder.py
RUNTIME=1

run:
	env LC_ALL=C python3 main.py $(V) $(RUNTIME) >/dev/null

drun:
	env LC_ALL=C python3 -m pudb main.py $(V)


clean:
	find . -name __pycache__ -type d -print0 -prune | xargs -0 -- rm -r
	for i in $(SRC); do (cd $$i; make clean); done
	rm -rf examples/results_*.json

compile:
	for i in $(SRC); do (cd $$i; make); done

eval_python:
	- cd examples/python/Python-3.10.9/Python && rm *.gcda *.gcno
	cd examples/python/Python-3.10.9 && make clean && make coverage
	#cd examples/python && python3 eval-python.py

eval_lua:
	- cd examples/lua/lua-5.1.5/src && rm *.gcda *.gcno
	cd examples/lua/lua-5.1.5 && make clean && make linux INSTR='-fprofile-arcs -ftest-coverage'
	cd examples/lua && python3 eval-lua.py

compile_lua:
	cd examples/lua/lua-5.1.5 && make clean && make linux

lua: compile_lua
	- cd examples/lua && time timeout -k9 $(RUNTIME)h python3 driver.py

compile_python:
		cd examples/python/Python-3.10.9 && make clean && make

python: compile_python
	cd examples/python && time timeout -k9 $(RUNTIME)h python3 driver.py

all_subjects:
	make -j run_subjects

run_subjects: lua python
	@echo -e "\nDONE generating inputs for VMs.\n"
