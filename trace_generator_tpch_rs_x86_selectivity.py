# coding=utf-8  ## 1MB => 262144
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

VECTOR_SIZE = 1000
QUERY = "Query06"
QUERY_ENGINE = "pipelined"
BASEDIR = "/Users/diegogomestome/Dropbox/1-UFPR/1-Mestrado_Diego_Tome/EXPERIMENTOS/"


def writeOnDynamicAndMemoryFilesPipelined():
    global column, tuple
    ######### WRITES ON DYNAMIC AND MEMORY FILE COLUMN-AT-A-TIME################3
    for tuple in range(len(tuples)):
        for column in range(numberOfPredicates):
            FILE_DYN.write(dynamic_block[column][tuple])
            if memory_block[column][tuple] != 0:
                FILE_MEM.write(memory_block[column][tuple])


for REGISTER_SIZE in (16, 32, 64):
    for SELECTIVITY in ("0001", "001", "01", "1", "10", "100"):
        
        DATA_ADDR_READ = 1024 * 1024 * 1024
        DATA_ADDR_WRITE = 1024 * 1024 * 4096
        INSTRUCTION_ADDR = 1024
        DATA_SIZE = 4
    
        input_file = BASEDIR + "bitmap_files/resultQ06.txt"
        dynamic_trace = BASEDIR + "traces/" + QUERY + "/rowStore/x86/" + str(
            REGISTER_SIZE) + "/" + SELECTIVITY + "/" + SELECTIVITY + "/output_trace.out.tid0.dyn.out"
        memory_trace = BASEDIR + "traces/" + QUERY + "/rowStore/x86/" + str(
            REGISTER_SIZE) + "/" + SELECTIVITY + "/output_trace.out.tid0.mem.out"
        static_trace = BASEDIR + "traces/" + QUERY + "/rowStore/x86/" + str(
            REGISTER_SIZE) + "/" + SELECTIVITY + "/output_trace.out.tid0.stat.out"
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
        address_base = [DATA_ADDR_READ, DATA_ADDR_READ + (DATA_SIZE),  # READ
                        DATA_ADDR_READ + (DATA_SIZE * 2)]
        address_base2 = [DATA_ADDR_READ, DATA_ADDR_READ + (DATA_SIZE),  # READ
                        DATA_ADDR_READ + (DATA_SIZE * 2)]
    
        address_target = [DATA_ADDR_WRITE, DATA_ADDR_WRITE + (qtdTuples * DATA_SIZE) + 1,  # WRITE
                          DATA_ADDR_WRITE + (qtdTuples * DATA_SIZE * 2) + 1]
    
        address_target_bitmap = [int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3)),  # BITMAP
                                 int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3) + qtdTuples),
                                 int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3) + (2 * qtdTuples))]
    
    
        FILE_STAT = open(static_trace, 'w')
        FILE_STAT.write("# SiNUCA Trace Static\n")
    
        basicBlock = 0
        print("Generating Traces Files For x86... " + str(REGISTER_SIZE) + "/" + SELECTIVITY + " Bytes Selectivity" + SELECTIVITY)
        #################### STATIC FILE #########################
        print "Generating Static File..."
        for i in range(numberOfPredicates):
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # LAÇO FOR POR TUPLA#
            FILE_STAT.write("ADD 1 " + str(INSTRUCTION_ADDR) + " 4 1 5 1 5 0 0 0 0 0 3 0 0 0\n")
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 3 1 5 1 6 0 0 0 0 0 3 0 0 0\n")
            INSTRUCTION_ADDR += 3
            FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 6 1 7 0 0 0 0 0 4 0 0 0\n")
            INSTRUCTION_ADDR += 2
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # If (QUALIFICA PREDICADO)#
            FILE_STAT.write("LD 8 " + str(INSTRUCTION_ADDR) + " 6 1 8 1 9 0 0 1 0 0 3 0 0 0\n")  # R
            INSTRUCTION_ADDR += 6
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 3 1 9 1 8 0 0 0 0 0 3 0 0 0\n")
            INSTRUCTION_ADDR += 3
            # FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 10 1 7 0 0 0 0 0 4 0 0 0\n")
            # INSTRUCTION_ADDR += 2
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # MATERIALIZAÇÃO (LOAD -> STORE)#
            FILE_STAT.write("MOV 8 " + str(INSTRUCTION_ADDR) + " 6 1 11 1 12 0 0 1 0 0 3 0 0 0\n")  # R
            INSTRUCTION_ADDR += 6
            FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 12 1 13 0 0 0 0 1 3 0 0 0\n")  # W
            INSTRUCTION_ADDR += 6
            FILE_STAT.write("ADD 1 " + str(INSTRUCTION_ADDR) + " 4 1 1 1 1 0 0 0 0 0 3 0 0 0\n")
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 3 1 1 1 2 0 0 0 0 0 3 0 0 0\n")
            INSTRUCTION_ADDR += 3
            FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 2 1 3 0 0 0 0 0 4 0 0 0\n")
            INSTRUCTION_ADDR += 2
            # basicBlock += 1
            # FILE_STAT.write("@" + str(basicBlock) + "\n")  # LAÇO FOR POR ATRIBUTO#
            # FILE_STAT.write("ADD 1 " + str(instructionAddress) + " 4 1 14 1 14 0 0 0 0 0 3 0 0 0\n")
            # instructionAddress += 4
            # FILE_STAT.write("CMP 1 " + str(instructionAddress) + " 3 1 14 1 15 0 0 0 0 0 3 0 0 0\n")
            # instructionAddress += 3
            # FILE_STAT.write("JNE 7 " + str(instructionAddress) + " 2 1 15 1 16 0 0 0 0 0 4 0 0 0\n")
            # instructionAddress += 2
    
        FILE_STAT.write("# eof")
        FILE_STAT.close()
        print "Static File Ok!"
    
        FILE_DYN = open(dynamic_trace, 'w')
        FILE_MEM = open(memory_trace, 'w')
        FILE_DYN.write("# SiNUCA Trace Dynamic\n")
        FILE_MEM.write("# SiNUCA Trace Memory\n")
        #################### DYNAMIC AND MEMORY FILE #########################
        print "Generating Data For Dynamic and Memory Files..."
        tuplesByOperation = REGISTER_SIZE / 64
        lastFieldSum = 0
        loadsByTuple = 1
        if REGISTER_SIZE < 64:
            loadsByTuple = 64 / REGISTER_SIZE
            tuplesByOperation = 1
        fieldsByInstruction = tuplesByOperation
    
        for tuple in range(len(tuples)):
            elem = tuples[tuple]
            elem = elem.split()
            basicBlock = 0
            for column in range(numberOfPredicates):
                bitColSum[column] += int(elem[column])
                ########################################################################
                ##  HMC INSTRUCTION WILL BE SENDED
                ########################################################################
                if fieldsByInstruction == 1:
                    dynamic_block[column][tuple] += str(str(basicBlock + 1) + "\n")
                    ########################################################################
                    ##  MATCH FOUND
                    ########################################################################
                    if bitColSum[column] > 0 or column == 0:
                        lastFieldSum = bitColSum[column]
                        bitColSum[column] = 0
                        if column == numberOfPredicates - 1:
                            fieldsByInstruction = tuplesByOperation + 1
                        ########################################################################
                        ##  APPLY PREDICATE
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                        memory_block[column][tuple] += (
                            "R " + str(REGISTER_SIZE) + "/" + SELECTIVITY + " " + str(address_base[column]) + " " + str(
                                basicBlock + 2) + "\n")
                        address_base[column] += REGISTER_SIZE * loadsByTuple
                        ########################################################################
                        ## CREATE THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        if lastFieldSum > 0:
                            address_base[column] -= REGISTER_SIZE * loadsByTuple
                            for i in range(loadsByTuple):
                                dynamic_block[column][tuple] += str(str(basicBlock + 3) + "\n")
                                memory_block[column][tuple] += (
                                    "R " + str(REGISTER_SIZE) + "/" + SELECTIVITY + " " + str(address_base[column]) + " " + str(
                                        basicBlock + 3) + "\n")
                                address_base[column] += REGISTER_SIZE
                                memory_block[column][tuple] += str(
                                    "W " + str(REGISTER_SIZE) + "/" + SELECTIVITY + " " + str(address_base2[column]) + " " + str(
                                        basicBlock + 3) + "\n")
                                address_base2[column] += REGISTER_SIZE
                    elif column > 0:
                        if column == numberOfPredicates - 1:
                            fieldsByInstruction = tuplesByOperation + 1
                        if lastFieldSum > 0:
                            lastFieldSum = 0
                            ########################################################################
                            ##  APPLY PREDICATE
                            ########################################################################
                            dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                            memory_block[column][tuple] += (
                                "R " + str(REGISTER_SIZE) + "/" + SELECTIVITY + " " + str(address_base[column]) + " " + str(
                                    basicBlock + 2) + "\n")
                            address_base[column] += (REGISTER_SIZE)
                basicBlock += 3
            lastFieldSum = 0
            fieldsByInstruction -= 1
    
    
        print "Writing on Dynamic and Memory File..."
        ######### WRITES ON DYNAMIC AND MEMORY FILE ################3
        writeOnDynamicAndMemoryFilesPipelined()
    
        FILE_MEM.close()
        FILE_DYN.close()
        print "Dynamic and Memory Files Ok!"
        print "Compressing Files..."
        os.system("rm -f " + BASEDIR + "traces/" + QUERY + "/rowStore/x86/" + str(
            REGISTER_SIZE) + "/" + SELECTIVITY + "/" + "*gz")
        os.system("gzip " + BASEDIR + "traces/" + QUERY + "/rowStore/x86/" + str(
            REGISTER_SIZE) + "/" + SELECTIVITY + "/" + "*.out")
        print "ALL Done!"
