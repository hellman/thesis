all: main test

test:
	sage2 generate_test_sbox.py
	g++ -O3 -std=c++11 -DTEST_SBOX invariant_equations.cpp -I../ -I./ -o invariant_equations_test
	time ./invariant_equations_test 1 >invariant_equations_test.txt
	sage2 solve.py invariant_equations_test.txt >result_test.txt

main:
	g++ -O3 -std=c++11 invariant_equations.cpp -I../ -o invariant_equations 

run:
	for i in 10 11 12 13 14 15 16 1 24 2 30 32 36 3 4 51 59 5 6 7 8 9; do \
		echo Iterate $$i times \
		[ -f eqs/eq$$i.txt ] || time ./invariant_equations $i >eqs/eq$$i.txt; \
		time sage2 solve.py eqs/eq$$i.txt | tee results/norx_iterated$$i.txt; \
	done