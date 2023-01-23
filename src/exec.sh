#!/bin/bash

rm */*.gch
gcc main.c bme/* crc/* display/* gpio/* pid/* uart/* -lwiringPi -lpthread