all: main
CC = g++
LD = g++
OBJ = build/*.o
SRC = src/*.cpp
INC = -Iinclude/

main: $(OBJ)
	$(LD) $(OBJ) -o build/main -pthread -L/usr/local/opt/openssl/lib -lcrypto -lpqxx -lpq -lssl 


$(OBJ): $(SRC)
	$(CC) -c $(INC) $(SRC) -std=gnu++2a -Wall -DIS_PROD=$$PRODUCTION -DCROW_ENABLE_SSL
	mv *.o build/


.PHONY: clean
clean:
	find build ! -name '.gitignore' ! -name 'build' -delete

