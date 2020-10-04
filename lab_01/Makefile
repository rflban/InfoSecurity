CC := gcc
CFLAGS := -std=c99 -Wall -pedantic -I./validator/inc -g3 -fsanitize=address,undefined -fno-omit-frame-pointer

INSTALLER_SOURCE := ./installer/main.c ./validator/src/utils.c
INSTALLER_NAME := install

APP_SOURCE := ./app/main.c ./validator/src/utils.c
APP_NAME := lab_01

all: build_installer build_app

build_installer:
	${CC} ${CFLAGS} ${INSTALLER_SOURCE} -o ${INSTALLER_NAME}

build_app:
	${CC} ${CFLAGS} ${APP_SOURCE} -o ${APP_NAME}

clean:
	rm -rf ${INSTALLER_NAME}
	rm -rf ${APP_NAME}
