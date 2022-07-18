all: clean
	@ g++ -Wall -Wextra -o mazegen mazegen.cpp

clean:
	@ rm -rf mazegen