# coding=utf-8
## 1MB => 262144
## 2MB => 524288
## 4MB => 1048576
## 8MB => 2097152
## 16MB => 4194304
## 32MB => 8388608
## 64MB => 16777216
## 1GB => 268435456

##HEADER | NumberOfTables | ...TuplesByTable ... | TotalNumberOfAttributes | NumberOfPredicates |

import subprocess
import os
import sys

hmc_size = 0
for operandSize in (4, 8, 16, 32, 64):
    HMC_OPERATION_CAPACITY = operandSize

    DATA_ADDR_READ = 1024 * 1024 * 1024 #Bytes
    DATA_ADDR_WRITE = 1024 * 1024 * 4096 #Bytes
    REGISTER_SIZE = 4 #Bytes
    INST_ADDR = 1024 #Bytes
    BASEDIR = "/Users/diegogomestome/Dropbox/UFPR/Mestrado_Diego_Tome/EXPERIMENTOS/"

    input_file = BASEDIR + "bitmap_files/resultQ06.txt"
    dynamic_trace = BASEDIR + "traces/HMC/Q06/columnStore/" + str(
        HMC_OPERATION_CAPACITY * REGISTER_SIZE) + "/output_trace.out.tid0.dyn.out"

    memory_trace = BASEDIR + "traces/HMC/Q06/columnStore/" + str(
        HMC_OPERATION_CAPACITY * REGISTER_SIZE) + "/output_trace.out.tid0.mem.out"

    static_trace = BASEDIR + "traces/HMC/Q06/columnStore/" + str(
        HMC_OPERATION_CAPACITY * REGISTER_SIZE) + "/output_trace.out.tid0.stat.out"

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

    address_base = [DATA_ADDR_READ, DATA_ADDR_READ + (qtdTuples * REGISTER_SIZE),         #READ
                    DATA_ADDR_READ + (qtdTuples * REGISTER_SIZE * 2)]

    address_target = [DATA_ADDR_WRITE, DATA_ADDR_WRITE + (qtdTuples * REGISTER_SIZE) + 1, #WRITE
                      DATA_ADDR_WRITE + (qtdTuples * REGISTER_SIZE * 2) + 1]

    address_target_bitmap = [int(DATA_ADDR_READ + (qtdTuples * REGISTER_SIZE * 3)),            #BITMAP
                             int(DATA_ADDR_READ + (qtdTuples * REGISTER_SIZE * 3) + qtdTuples),
                             int(DATA_ADDR_READ + (qtdTuples * REGISTER_SIZE * 3) + (2 * qtdTuples))]


    FILE_STAT = open(static_trace, 'w')
    FILE_STAT.write("# SiNUCA Trace Static\n")

    basicBlock = 0
    print("Generating Traces Files For HMC... " + str(hmc_size * 4) + " Bytes")
    #################### STATIC FILE #########################
    print "Generating Static File..."
    for tuple in range(numberOfPredicates):
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # COLUMN-AT-A-TIME#
        FILE_STAT.write("ADD 1 " + str(INST_ADDR) + " 4 1 5 1 5 0 0 0 0 0 3 0 0 0\n")
        INST_ADDR += 4
        FILE_STAT.write("CMP 1 " + str(INST_ADDR) + " 3 1 5 1 6 0 0 0 0 0 3 0 0 0\n")
        INST_ADDR += 3
        FILE_STAT.write("JNE 7 " + str(INST_ADDR) + " 2 1 6 1 7 0 0 0 0 0 4 0 0 0\n")
        INST_ADDR += 2
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE)#
        FILE_STAT.write("HMC_CMP 12 " + str(INST_ADDR) + " 4 1 9 1 10 0 0 1 0 0 3 0 0 0\n")  # R HMC_SIZE
        INST_ADDR += 4
        FILE_STAT.write("JNE 7 " + str(INST_ADDR) + " 2 1 10 1 7 0 0 0 0 0 4 0 0 0\n")
        INST_ADDR += 2
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # READ BITMAP)#
        FILE_STAT.write("HMC_CMP 12 " + str(INST_ADDR) + " 4 1 13 1 14 0 0 1 0 0 3 0 0 0\n")  # R 1Byte
        INST_ADDR += 4
        FILE_STAT.write("JNE 7 " + str(INST_ADDR) + " 2 1 10 1 7 0 0 0 0 0 4 0 0 0\n")
        INST_ADDR += 2
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # MATCH POSITION (STORE)#
        FILE_STAT.write("MOV 9 " + str(INST_ADDR) + " 6 1 10 1 13 0 0 0 0 1 3 0 0 0\n")  # W 1Byte
        INST_ADDR += 6
        FILE_STAT.write("ADD 1 " + str(INST_ADDR) + " 4 1 1 1 1 0 0 0 0 0 3 0 0 0\n")
        INST_ADDR += 4
        FILE_STAT.write("CMP 1 " + str(INST_ADDR) + " 3 1 1 1 2 0 0 0 0 0 3 0 0 0\n")
        INST_ADDR += 3
        FILE_STAT.write("JNE 7 " + str(INST_ADDR) + " 2 1 2 1 3 0 0 0 0 0 4 0 0 0\n")
        INST_ADDR += 2

    FILE_STAT.write("# eof")
    FILE_STAT.close()
    print "Static File Ok!"


    FILE_DYN = open(dynamic_trace, 'w')
    FILE_MEM = open(memory_trace, 'w')
    FILE_DYN.write("# SiNUCA Trace Dynamic\n")
    FILE_MEM.write("# SiNUCA Trace Memory\n")

    fieldCount = HMC_OPERATION_CAPACITY
    lastSum = 0
    countLoads = 0
    loadSize = 32
    readCount = [0, 0, 0]
    #################### DYNAMIC AND MEMORY FILE #########################
    print "Generating Data For Dynamic and Memory Files..."
    for tuple in range(len(tuples)):
        elem = tuples[tuple]
        elem = elem.split()
        basicBlock = 0
        for column in range(numberOfPredicates):
            dynamic_block[column][tuple] += str(str(basicBlock + 1) + "\n")
            bitColSum[column] += int(elem[column])
            ########################################################################
            ##  HMC INSTRUCTION WILL BE SENDED
            ########################################################################
            if fieldCount == 1:
                ########################################################################
                ##  MATCH FOUND
                ########################################################################
                if bitColSum[column] > 0 or column == 0:
                    lastSum = bitColSum[column]
                    bitColSum[column] = 0
                    if column == numberOfPredicates - 1:
                        fieldCount = HMC_OPERATION_CAPACITY + 1
                    ########################################################################
                    ##  APPLY PREDICATE
                    ########################################################################
                    dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                    memory_block[column][tuple] += (
                        "R " + str(HMC_OPERATION_CAPACITY * REGISTER_SIZE) + " " + str(address_base[column]) + " " + str(
                            basicBlock + 2) + "\n")
                    address_base[column] += (REGISTER_SIZE * HMC_OPERATION_CAPACITY)
                    readCount[column] += 1

                    if readCount[column] == 2 and HMC_OPERATION_CAPACITY == 4:
                        loadSize = 16
                        readCount[column] = 0
                    ########################################################################
                    ## CREATE THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                    ########################################################################
                    for i in range(((REGISTER_SIZE * HMC_OPERATION_CAPACITY) / loadSize)):
                        if column > 0:
                            dynamic_block[column][tuple] += str(str(basicBlock + 3) + "\n")
                            memory_block[column][tuple] += (
                                "R 1 " + str(address_target_bitmap[column - 1] - 1) + " " + str(
                                    basicBlock + 3) + "\n")
                            address_target_bitmap[column - 1] += 1

                        dynamic_block[column][tuple] += str(str(basicBlock + 4) + "\n")
                        memory_block[column][tuple] += str(
                            "W 1 " + str(address_target_bitmap[column]) + " " + str(basicBlock + 4) + "\n")
                        address_target_bitmap[column] += 1
                elif column > 0:
                    if column == numberOfPredicates - 1:
                        fieldCount = HMC_OPERATION_CAPACITY + 1
                    if lastSum > 0:
                        countLoads += 1
                        dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                        memory_block[column][tuple] += (
                            "R " + str(HMC_OPERATION_CAPACITY * REGISTER_SIZE) + " " + str(address_base[column]) + " " + str(
                                basicBlock + 2) + "\n")
                        address_base[column] += (REGISTER_SIZE * HMC_OPERATION_CAPACITY)
                        readCount[column] += 1

                        if readCount[column] == 2 and HMC_OPERATION_CAPACITY == 4:
                            loadSize = 16
                            readCount[column] = 0
                    ########################################################################
                    ## CREATE THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                    ########################################################################
                    for i in range(((REGISTER_SIZE * HMC_OPERATION_CAPACITY) / loadSize)):
                        dynamic_block[column][tuple] += str(str(basicBlock + 3) + "\n")
                        dynamic_block[column][tuple] += str(str(basicBlock + 4) + "\n")
                        memory_block[column][tuple] += (
                            "R 1 " + str(address_target_bitmap[column - 1] - 1) + " " + str(
                                basicBlock + 3) + "\n")
                        address_target_bitmap[column - 1] += 1
                        memory_block[column][tuple] += str(
                            "W 1 " + str(address_target_bitmap[column]) + " " + str(basicBlock + 4) + "\n")
                        address_target_bitmap[column] += 1
            ######################################  if fieldCount == 1:
            basicBlock += 4
            loadSize = 32
        fieldCount -= 1

    print "Writing on Dynamic and Memory File..."
    ######### WRITES ON DYNAMIC AND MEMORY FILE ################3
    for column in range(numberOfPredicates):
        for tuple in range(len(tuples)):
            FILE_DYN.write(dynamic_block[column][tuple])
            if memory_block[column][tuple] != 0:
                FILE_MEM.write(memory_block[column][tuple])

    FILE_MEM.close()
    FILE_DYN.close()
    print "Dynamic and Memory Files Ok!"

    print "Compressing Files..."
    os.system("rm -f " + BASEDIR + "traces/HMC/Q06/columnStore/" + str(HMC_OPERATION_CAPACITY * REGISTER_SIZE) + "/" + "*gz")
    os.system("gzip " + BASEDIR + "traces/HMC/Q06/columnStore/" + str(HMC_OPERATION_CAPACITY * REGISTER_SIZE) + "/" + "*.out")
    print "ALL Done!"
