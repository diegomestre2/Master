# coding=utf-8
## 1MB => 262144
## 2MB => 524288
## 4MB => 1048576
## 8MB => 2097152
## 16MB => 4194304
## 32MB => 8388608
## 64MB => 16777216
## 1GB => 268435456

##HEADER | TotalNumberOFAttributes | NumberOfPredicates |

import subprocess
import os
import sys

VECTOR_SIZE = 999
QUERY = "Query06"
QUERY_ENGINE = "vectorized"
BASEDIR = "/Users/diegogomestome/Dropbox/1-UFPR/1-Mestrado_Diego_Tome/EXPERIMENTOS/"


def writeOnDynamicAndMemoryFilesVectorized():
    global column, tuple
    vectorCounter = 0
    VECTOR_SIZE = 1
    ######### WRITES ON DYNAMIC AND MEMORY FILE ################
    while vectorCounter < len(tuples):
        for column in xrange(numberOfPredicates):
            startIndex = vectorCounter
            for tuple in xrange(startIndex, startIndex + VECTOR_SIZE):
                if tuple < len(tuples):
                    FILE_DYN.write(dynamic_block[column][tuple])
                    if memory_block[column][tuple] != 0:
                        FILE_MEM.write(memory_block[column][tuple])
        vectorCounter += VECTOR_SIZE

for HMC_OPERATION in (256, 256):

    DATA_ADDR_READ = 1024 * 1024 * 1024
    DATA_ADDR_WRITE = 1024 * 1024 * 4096
    DATA_SIZE = 4
    INSTRUCTION_ADDR = 1024

    input_file = BASEDIR + "bitmap_files/resultQ06.txt"

    dynamic_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/HMC_NEW/" + str(
        HMC_OPERATION) + "/predication/output_trace.out.tid0.dyn.out"
    memory_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/HMC_NEW/" + str(
        HMC_OPERATION) + "/predication/output_trace.out.tid0.mem.out"
    static_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/HMC_NEW/" + str(
        HMC_OPERATION) + "/predication/output_trace.out.tid0.stat.out"

    ################### TREATING FILE INPUT ###################
    FILE_INPUT = open(input_file, 'r')

    header = FILE_INPUT.readline()
    header = header.split("|")
    numberOfTables = int(header[0])
    numberOfPredicates = int(header[(numberOfTables * 2) + 1])

    tuples = FILE_INPUT.readlines()
    FILE_INPUT.close()
    ##########################################################
    qtdTuples = len(tuples)
    w, h = qtdTuples, numberOfPredicates
    dynamic_block = [["" for x in range(w)] for y in range(h)]
    memory_block = [["" for x in range(w)] for y in range(h)]
    bitColSum = [0 for y in range(numberOfPredicates)]
    tuplesByTable = [0 for y in range(qtdTuples)]
    totalAttributes = [0 for y in range(3)]

    for i in range(numberOfTables):
        tuplesByTable[i] = int(header[i + 1])
        totalAttributes[i] = int(header[i + numberOfTables + 1])

    AttributesByStage = [totalAttributes, totalAttributes, totalAttributes]
    address_base = [DATA_ADDR_READ, DATA_ADDR_READ + (qtdTuples * DATA_SIZE),
                    DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 2)]
    address_target = [DATA_ADDR_WRITE, DATA_ADDR_WRITE + (qtdTuples * DATA_SIZE) + 1,
                      DATA_ADDR_WRITE + (qtdTuples * DATA_SIZE * 2) + 1]
    address_target_bitmap = [DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3),
                             DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3) + qtdTuples,
                             DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3) + (2 * qtdTuples)]

    FILE_STAT = open(static_trace, 'w')
    FILE_STAT.write("# SiNUCA Trace Static\n")

    basicBlock = 0
    print("Generating Traces Files For HMC_NEW... Predication Unrolled 32x " + str(HMC_OPERATION) + " Bytes")
    #################### STATIC FILE #########################
    print "Generating Static File..."
    for i in range(numberOfPredicates):

        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 1)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 2)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 3)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 4)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 5)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 6)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 7)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 8)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 9)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 10)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 11)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 12)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 13)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 14)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 15)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 16)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 17)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 18)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 19)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 20)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 21)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 22)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 23)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 23\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 24)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 23\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 24\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 25)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 23\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 24\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 25\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 26)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 23\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 24\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 25\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 26\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 27)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 23\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 24\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 25\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 26\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 27\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 28)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 23\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 24\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 25\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 26\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 27\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 28\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 29)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 23\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 24\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 25\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 26\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 27\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 28\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 29\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 30)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 23\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 24\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 25\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 26\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 27\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 28\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 29\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 30\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 31)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 23\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 24\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 25\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 26\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 27\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 28\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 29\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 30\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 31\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE 32)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 1\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 2\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 3\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 4\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 5\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 6\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 7\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 8\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 9\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 10\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 11\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 12\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 13\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 14\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 15\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 16\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 17\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 18\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 19\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 20\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 21\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 22\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 23\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 24\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 25\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 26\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 27\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 28\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 29\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 30\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 31\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 1 0 0 3 0 0 1 -1 -1 32\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 1 -1 1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 2 -1 2\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 3 -1 3\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 4 -1 4\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 5 -1 5\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 6 -1 6\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 7 -1 7\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 8 -1 8\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 9 -1 9\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 10 -1 10\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 11 -1 11\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 12 -1 12\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 13 -1 13\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 14 -1 14\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 15 -1 15\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 16 -1 16\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 17 -1 17\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 18 -1 18\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 19 -1 19\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 20 -1 20\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 21 -1 21\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 22 -1 22\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 23 -1 23\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 24 -1 24\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 25 -1 25\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 26 -1 26\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 27 -1 27\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 28 -1 28\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 29 -1 29\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 30 -1 30\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 31 -1 31\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_CMP 18 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 0 3 0 0 1 32 -1 32\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # COLUMN-AT-A-TIME#
        FILE_STAT.write("ADD 1 " + str(INSTRUCTION_ADDR) + " 4 1 5 1 5 0 0 0 0 0 3 0 0 0\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 3 1 5 1 6 0 0 0 0 0 3 0 0 0\n")
        INSTRUCTION_ADDR += 3
        FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 6 1 7 0 0 0 0 0 4 0 0 0\n")
        INSTRUCTION_ADDR += 2
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY LOCK)#
        FILE_STAT.write("HMC_LOCK 14 " + str(INSTRUCTION_ADDR) + " 4 1 7 0 0 0 0 0 0 3 0 0 1 -1 -1 -1\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY READ BITMAP)#
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 8 0 0 0 1 0 0 3 0 0 1 -1 -1 33\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 0 0 0 3 0 0 1 33 -1 33\n")
        INSTRUCTION_ADDR += 4
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY WRITE BITMAP)
        FILE_STAT.write("HMC_ST 17 " + str(INSTRUCTION_ADDR) + " 4 1 10 0 0 0 0 0 1 3 0 0 1 33 -1 -1\n")  # W
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_UNLOCK 15 " + str(INSTRUCTION_ADDR) + " 4 1 11 0 0 0 0 0 0 3 0 0 1 -1 -1 -1\n")
        INSTRUCTION_ADDR += 4

    FILE_STAT.write("# eof")
    FILE_STAT.close()
    print "Static File Ok!"

    FILE_DYN = open(dynamic_trace, 'w')
    FILE_MEM = open(memory_trace, 'w')
    FILE_DYN.write("# SiNUCA Trace Dynamic\n")
    FILE_MEM.write("# SiNUCA Trace Memory\n")

    fieldsByInstruction = HMC_OPERATION / 4
    totalFields = (HMC_OPERATION / 4) * 32
    lastFieldSum = 0
    loadCount = [0, 0, 0]
    bitmapSize = 1
    iterator = 0
    if HMC_OPERATION > 16:
        bitmapSize = (HMC_OPERATION / 32) * 32
    #################### DYNAMIC AND MEMORY FILE #########################
    print "Generating Data For Dynamic and Memory Files..."
    for tuple in range(len(tuples)):
        elem = tuples[tuple]
        elem = elem.split()
        basicBlock = 0
        for column in range(numberOfPredicates):
            bitColSum[column] += int(elem[column])
            ########################################################################
            ##  HMC INSTRUCTION WILL BE SENT
            ########################################################################
            if fieldsByInstruction == 1:
                if column == numberOfPredicates - 1:
                    fieldsByInstruction = (HMC_OPERATION / 4) + 1
                ########################################################################
                ##  MATCH FOUND
                ########################################################################
                if bitColSum[column] > 0:
                    if column > 0:
                        loadCount[column] += 1
                    lastFieldSum = bitColSum[column]
                    bitColSum[column] = 0

                    if totalFields == 1:
                        dynamic_block[column][tuple] += str(str(basicBlock + 33) + "\n")

                        if column == numberOfPredicates - 1:
                            fieldsByInstruction = (HMC_OPERATION / 4) + 1
                            totalFields = (HMC_OPERATION / 4) * 32 + 1

                        dynamic_block[column][tuple] += str(str(basicBlock + 34) + "\n")
                        ########################################################################
                        ## READ THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        if column > 0:
                            dynamic_block[column][tuple] += str(str(basicBlock + 35) + "\n")
                            memory_block[column][tuple] += str(
                                "R " + str(bitmapSize) + " " + str(
                                    address_target_bitmap[column - 1] - 1) + " " + str(basicBlock + 35) + "\n")
                            address_target_bitmap[column - 1] += bitmapSize
                        ########################################################################
                        ##  APPLY PREDICATE
                        ########################################################################
                        if column == 0:
                            iterator = 32
                        else:
                            iterator = loadCount[column]

                        dynamic_block[column][tuple] += str(str(basicBlock + iterator) + "\n")
                        for i in range(iterator):
                            memory_block[column][tuple] += (
                                "R " + str(HMC_OPERATION) + " " + str(address_base[column]) + " " + str(
                                    basicBlock + iterator) + "\n")
                            address_base[column] += HMC_OPERATION
                        loadCount[column] = 0
                        ########################################################################
                        # CREATE THE BITMAP 1 Byte Store by 32 Bytes of Loads
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 36) + "\n")
                        memory_block[column][tuple] += str(
                            "W " + str(bitmapSize) + " " + str(
                                address_target_bitmap[column]) + " " + str(basicBlock + 36) + "\n")
                        address_target_bitmap[column] += bitmapSize
                # bitColSum[column] > 0:
                else:
                    if column > 0 and lastFieldSum > 0:
                        lastFieldSum = 0
                        loadCount[column] += 1
                    # if column > 0 and lastFieldSum > 0:
                    if totalFields == 1:
                        dynamic_block[column][tuple] += str(str(basicBlock + 33) + "\n")

                        if column == numberOfPredicates - 1:
                            fieldsByInstruction = (HMC_OPERATION / 4) + 1
                            totalFields = (HMC_OPERATION / 4) * 32 + 1

                        dynamic_block[column][tuple] += str(str(basicBlock + 34) + "\n")
                        ########################################################################
                        ## READ THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        if column > 0:
                            dynamic_block[column][tuple] += str(str(basicBlock + 35) + "\n")
                            memory_block[column][tuple] += str(
                                "R " + str(bitmapSize) + " " + str(
                                    address_target_bitmap[column - 1] - 1) + " " + str(basicBlock + 35) + "\n")
                            address_target_bitmap[column - 1] += bitmapSize
                        ########################################################################
                        ##  APPLY PREDICATE
                        ########################################################################
                        if column == 0:
                            iterator = 32
                        else:
                            iterator = loadCount[column]

                        if iterator > 0:
                            dynamic_block[column][tuple] += str(str(basicBlock + iterator) + "\n")
                            for i in range(iterator):
                                memory_block[column][tuple] += (
                                    "R " + str(HMC_OPERATION) + " " + str(address_base[column]) + " " + str(
                                        basicBlock + iterator) + "\n")
                                address_base[column] += HMC_OPERATION
                            loadCount[column] = 0
                        ########################################################################
                        # CREATE THE BITMAP 1 Byte Store by 32 Bytes of Loads
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 36) + "\n")
                        memory_block[column][tuple] += str(
                            "W " + str(bitmapSize) + " " + str(
                                address_target_bitmap[column]) + " " + str(basicBlock + 36) + "\n")
                        address_target_bitmap[column] += bitmapSize
                        # bitColSum[column] > 0:
                    # if totalFields == 1:
                # else
            basicBlock += 36
        lastFieldSum = 0
        totalFields -= 1
        fieldsByInstruction -= 1

    print "Writing on Dynamic and Memory File..."
    ######### WRITES ON DYNAMIC AND MEMORY FILE ################
    writeOnDynamicAndMemoryFilesVectorized()

    FILE_MEM.close()
    FILE_DYN.close()
    print "Dynamic and Memory Files Ok!"

    print "Compressing Files..."
    os.system("rm -f " + BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/HMC_NEW/" + str(
        HMC_OPERATION) + "/predication/" + "*gz")
    os.system("gzip " + BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/HMC_NEW/" + str(
        HMC_OPERATION) + "/predication/" + "*.out")
    print "ALL Done!"

