CC := gcc
CFLAGS := -std=c99 -Wall -pedantic -I./validator/inc -g3 -fsanitize=address,undefined -fno-omit-frame-pointer

INSTALLER_SOURCE := ./installer/main.c ./validator/src/utils.c

INSTALLER_NAME := install

all: build_installer

build_installer:
	${CC} ${CFLAGS} ${INSTALLER_SOURCE} -o ${INSTALLER_NAME}

clean:
	rm -rf ${INSTALLER_NAME}
