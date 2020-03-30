all: main test

test:
	sage2 generate_test_sbox.py
	g++ -O3 -std=c++11 -DTEST_SBOX invariant_equations.cpp -I../ -I./ -o invariant_equations_test
	time ./invariant_equations_test 1 >invariant_equations_test.txt
	sage2 solve.py invariant_equations_test.txt >result_test.txt

main:
	g++ -O3 -std=c++11 invariant_equations.cpp -I../ -o invariant_equations 

run:
	time ./invariant_equations 1 >invariant_equations.txt
	time sage2 solve.py invariant_equations.txt >result_norx.txt