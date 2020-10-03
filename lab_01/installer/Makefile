CC := gcc
CFLAGS := -std=c99 -Wall -pedantic -I../validator/inc

SOURCE := main.c ../validator/src/utils.c

APP := install

all: build

build:
	${CC} ${CFLAGS} ${SOURCE} -o ${APP}

clean:
	rm -rf ${APP}
