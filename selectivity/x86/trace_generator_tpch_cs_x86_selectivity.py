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

VECTOR_SIZE = 1000
QUERY = "Query06"
QUERY_ENGINE = "pipelined"
BASEDIR = "/Users/diegogomestome/Dropbox/1-UFPR/1-Mestrado_Diego_Tome/EXPERIMENTOS/"


def writeOnDynamicAndMemoryFilesPipelined():
    global column, tuple
    ######### WRITES ON DYNAMIC AND MEMORY FILE COLUMN-AT-A-TIME #################
    for column in range(numberOfPredicates):
        for tuple in range(len(tuples)):
            FILE_DYN.write(dynamic_block[column][tuple])
            if memory_block[column][tuple] != 0:
                FILE_MEM.write(memory_block[column][tuple])


for REGISTER_SIZE in (16, 64):
    for SELECTIVITY in ("0001", "001", "01", "1", "10", "100"):

        DATA_ADDR_READ = 1024 * 1024 * 1024
        DATA_ADDR_WRITE = 1024 * 1024 * 4096
        INSTRUCTION_ADDR = 1024
        DATA_SIZE = 4

        ################### FILES #################################
        BASEDIR = "/Users/diegogomestome/Dropbox/1-UFPR/1-Mestrado_Diego_Tome/EXPERIMENTOS/"
        input_file = BASEDIR + "bitmap_files/q6_selectivity/q6_" + SELECTIVITY + ".txt"
        dynamic_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/x86/" + str(
            REGISTER_SIZE) + "/selectivity/" + SELECTIVITY + "/output_trace.out.tid0.dyn.out"
        memory_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/x86/" + str(
            REGISTER_SIZE) + "/selectivity/" + SELECTIVITY + "/output_trace.out.tid0.mem.out"
        static_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/x86/" + str(
            REGISTER_SIZE) + "/selectivity/" + SELECTIVITY + "/output_trace.out.tid0.stat.out"
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
        address_base = [DATA_ADDR_READ, DATA_ADDR_READ + (qtdTuples * DATA_SIZE),  # READ
                        DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 2)]

        address_target = [DATA_ADDR_WRITE, DATA_ADDR_WRITE + (qtdTuples * DATA_SIZE) + 1,  # WRITE
                          DATA_ADDR_WRITE + (qtdTuples * DATA_SIZE * 2) + 1]

        address_target_bitmap = [int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3)),  # BITMAP
                                 int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3) + qtdTuples),
                                 int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3) + (2 * qtdTuples))]

        FILE_STAT = open(static_trace, 'w')
        FILE_STAT.write("# SiNUCA Trace Static\n")

        basicBlock = 0
        print("Generating Traces Files For x86 - " + str(REGISTER_SIZE) + " Bytes Selectivity " + SELECTIVITY)
        #################### STATIC FILE #########################
        print "Generating Static File..."
        for tuple in range(numberOfPredicates):
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # COLUMN-AT-A-TIME#
            FILE_STAT.write("ADD 1 " + str(INSTRUCTION_ADDR) + " 4 1 5 1 5 0 0 0 0 0 3 0 0 0\n")
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 3 1 5 1 6 0 0 0 0 0 3 0 0 0\n")
            INSTRUCTION_ADDR += 3
            FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 6 1 7 0 0 0 0 0 4 0 0 0\n")
            INSTRUCTION_ADDR += 2
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # READ BITMAP)#
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 8 1 9 0 0 1 0 0 3 0 0 0\n")  # R 1 Byte
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 9 1 7 0 0 0 0 0 4 0 0 0\n")
            INSTRUCTION_ADDR += 2
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE)#
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 9 1 10 0 0 1 0 0 3 0 0 0\n")  # R 16 Byte
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 10 1 7 0 0 0 0 0 4 0 0 0\n")
            INSTRUCTION_ADDR += 2
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # MATCH POSITION (STORE)#
            FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 10 1 11 0 0 0 0 1 3 0 0 0\n")  # W 1Byte
            INSTRUCTION_ADDR += 6

        FILE_STAT.write("# eof")
        FILE_STAT.close()
        print "Static File Ok!"

        FILE_DYN = open(dynamic_trace, 'w')
        FILE_MEM = open(memory_trace, 'w')
        FILE_DYN.write("# SiNUCA Trace Dynamic\n")
        FILE_MEM.write("# SiNUCA Trace Memory\n")

        fieldsByInstruction = REGISTER_SIZE / 4
        lastFieldSum = 0
        bitmapSize = 1
        if REGISTER_SIZE > 16:
            bitmapSize = REGISTER_SIZE / 32
        #################### DYNAMIC AND MEMORY FILE #########################
        print "Generating Data For Dynamic and Memory Files..."
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
                            fieldsByInstruction = (REGISTER_SIZE / 4) + 1
                        ########################################################################
                        ## READ THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        if column > 0:
                            dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                            memory_block[column][tuple] += (
                                "R " + str(bitmapSize) + " " + str(address_target_bitmap[column - 1] - 1) + " " + str(
                                    basicBlock + 2) + "\n")
                            address_target_bitmap[column - 1] += bitmapSize
                        ########################################################################
                        ##  APPLY PREDICATE
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 3) + "\n")
                        memory_block[column][tuple] += (
                            "R " + str(REGISTER_SIZE) + " " + str(address_base[column]) + " " + str(
                                basicBlock + 3) + "\n")
                        address_base[column] += (REGISTER_SIZE)
                        ########################################################################
                        ## CREATE THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 4) + "\n")
                        memory_block[column][tuple] += str(
                            "W " + str(bitmapSize) + " " + str(address_target_bitmap[column]) + " " + str(
                                basicBlock + 4) + "\n")
                        address_target_bitmap[column] += bitmapSize
                    elif column > 0:
                        if column == numberOfPredicates - 1:
                            fieldsByInstruction = (REGISTER_SIZE / 4) + 1
                        ########################################################################
                        ## READ THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                        memory_block[column][tuple] += (
                            "R " + str(bitmapSize) + " " + str(address_target_bitmap[column - 1] - 1) + " " + str(
                                basicBlock + 2) + "\n")
                        address_target_bitmap[column - 1] += bitmapSize
                        if lastFieldSum > 0:
                            lastFieldSum = 0
                            ########################################################################
                            ##  APPLY PREDICATE
                            ########################################################################
                            dynamic_block[column][tuple] += str(str(basicBlock + 3) + "\n")
                            memory_block[column][tuple] += (
                                "R " + str(REGISTER_SIZE) + " " + str(address_base[column]) + " " + str(
                                    basicBlock + 3) + "\n")
                            address_base[column] += (REGISTER_SIZE)
                        ########################################################################
                        ## CREATE THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 4) + "\n")
                        address_target_bitmap[column - 1] += bitmapSize
                        memory_block[column][tuple] += str(
                            "W " + str(bitmapSize) + " " + str(address_target_bitmap[column]) + " " + str(
                                basicBlock + 4) + "\n")
                        address_target_bitmap[column] += bitmapSize
                basicBlock += 4
            lastFieldSum = 0
            fieldsByInstruction -= 1

        print "Writing on Dynamic and Memory File..."
        vectorCounter = 0
        startIndex = 0
        ######### WRITES ON DYNAMIC AND MEMORY FILE ################
        writeOnDynamicAndMemoryFilesPipelined()

        FILE_MEM.close()
        FILE_DYN.close()
        print "Dynamic and Memory Files Ok!"
        print "Compressing Files..."

        os.system("rm -f " + BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/x86/" + str(
            REGISTER_SIZE) + "/selectivity/" + SELECTIVITY + "/*gz")
        os.system("gzip " + BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/x86/" + str(
            REGISTER_SIZE) + "/selectivity/" + SELECTIVITY + "/*.out")
        print "ALL Done!"


        ##################### Unrolled 8x ############################

        DATA_ADDR_READ = 1024 * 1024 * 1024
        DATA_ADDR_WRITE = 1024 * 1024 * 4096
        INSTRUCTION_ADDR = 1024
        DATA_SIZE = 4

        BASEDIR = "/Users/diegogomestome/Dropbox/1-UFPR/1-Mestrado_Diego_Tome/EXPERIMENTOS/"
        input_file = BASEDIR + "bitmap_files/q6_selectivity/q6_" + SELECTIVITY + ".txt"

        dynamic_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/x86/" + str(
            REGISTER_SIZE) + "/unrolled8x/selectivity/" + SELECTIVITY + "/output_trace.out.tid0.dyn.out"
        memory_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/x86/" + str(
            REGISTER_SIZE) + "/unrolled8x/selectivity/" + SELECTIVITY + "/output_trace.out.tid0.mem.out"
        static_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/x86/" + str(
            REGISTER_SIZE) + "/unrolled8x/selectivity/" + SELECTIVITY + "/output_trace.out.tid0.stat.out"
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
        address_base = [DATA_ADDR_READ, DATA_ADDR_READ + (qtdTuples * DATA_SIZE),  # READ
                        DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 2)]

        address_target = [DATA_ADDR_WRITE, DATA_ADDR_WRITE + (qtdTuples * DATA_SIZE) + 1,  # WRITE
                          DATA_ADDR_WRITE + (qtdTuples * DATA_SIZE * 2) + 1]

        address_target_bitmap = [int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3)),  # BITMAP
                                 int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3) + qtdTuples),
                                 int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3) + (2 * qtdTuples))]

        FILE_STAT = open(static_trace, 'w')
        FILE_STAT.write("# SiNUCA Trace Static\n")

        basicBlock = 0
        print("Generating Traces Files For x86...Unrolled 8x - " + str(REGISTER_SIZE) + " Bytes Selectivity " + SELECTIVITY)
        #################### STATIC FILE #########################
        print "Generating Static File..."
        for tuple in range(numberOfPredicates):
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # COLUMN-AT-A-TIME#
            FILE_STAT.write("ADD 1 " + str(INSTRUCTION_ADDR) + " 4 1 5 1 5 0 0 0 0 0 3 0 0 0\n")
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 3 1 5 1 6 0 0 0 0 0 3 0 0 0\n")
            INSTRUCTION_ADDR += 3
            FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 6 1 7 0 0 0 0 0 4 0 0 0\n")
            INSTRUCTION_ADDR += 2
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # READ BITMAP)#
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 8 1 9 0 0 1 0 0 3 0 0 0\n")  # R 1 Bytes
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 10 1 11 0 0 1 0 0 3 0 0 0\n")  # R 1 Bytes
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 12 1 13 0 0 1 0 0 3 0 0 0\n")  # R 1 Bytes
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 14 1 15 0 0 1 0 0 3 0 0 0\n")  # R 1 Bytes
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 1 1 2 0 0 1 0 0 3 0 0 0\n")  # R 1 Bytes
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 3 1 4 0 0 1 0 0 3 0 0 0\n")  # R 1 Bytes
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 5 1 6 0 0 1 0 0 3 0 0 0\n")  # R 1 Bytes
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 7 1 16 0 0 1 0 0 3 0 0 0\n")  # R 1 Bytes
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 16 1 7 0 0 0 0 0 4 0 0 0\n")
            INSTRUCTION_ADDR += 2
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE)#
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 1 1 2 0 0 1 0 0 3 0 0 0\n")  # R 16 Byte
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 3 1 4 0 0 1 0 0 3 0 0 0\n")  # R 16 Byte
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 9 1 10 0 0 1 0 0 3 0 0 0\n")  # R 16 Byte
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 11 1 12 0 0 1 0 0 3 0 0 0\n")  # R 16 Byte
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 13 1 14 0 0 1 0 0 3 0 0 0\n")  # R 16 Byte
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 15 1 16 0 0 1 0 0 3 0 0 0\n")  # R 16 Byte
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 5 1 6 0 0 1 0 0 3 0 0 0\n")  # R 16 Byte
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 4 1 17 1 8 0 0 1 0 0 3 0 0 0\n")  # R 16 Byte
            INSTRUCTION_ADDR += 4
            FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 8 1 7 0 0 0 0 0 4 0 0 0\n")
            INSTRUCTION_ADDR += 2
            basicBlock += 1
            FILE_STAT.write("@" + str(basicBlock) + "\n")  # MATCH POSITION (STORE)#
            FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 2 1 5 0 0 0 0 1 3 0 0 0\n")  # W 1 Byte
            INSTRUCTION_ADDR += 6
            FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 4 1 6 0 0 0 0 1 3 0 0 0\n")  # W 1 Byte
            INSTRUCTION_ADDR += 6
            FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 10 1 7 0 0 0 0 1 3 0 0 0\n")  # W 1 Byte
            INSTRUCTION_ADDR += 6
            FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 12 1 8 0 0 0 0 1 3 0 0 0\n")  # W 1 Byte
            INSTRUCTION_ADDR += 6
            FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 14 1 9 0 0 0 0 1 3 0 0 0\n")  # W 1 Byte
            INSTRUCTION_ADDR += 6
            FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 16 1 10 0 0 0 0 1 3 0 0 0\n")  # W 1 Byte
            INSTRUCTION_ADDR += 6
            FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 6 1 11 0 0 0 0 1 3 0 0 0\n")  # W 1 Byte
            INSTRUCTION_ADDR += 6
            FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 8 1 13 0 0 0 0 1 3 0 0 0\n")  # W 1 Byte
            INSTRUCTION_ADDR += 6

        FILE_STAT.write("# eof")
        FILE_STAT.close()
        print "Static File Ok!"

        FILE_DYN = open(dynamic_trace, 'w')
        FILE_MEM = open(memory_trace, 'w')
        FILE_DYN.write("# SiNUCA Trace Dynamic\n")
        FILE_MEM.write("# SiNUCA Trace Memory\n")

        fieldsByInstruction = REGISTER_SIZE * 2
        lastFieldSum = 0
        bitmapSize = 1
        if REGISTER_SIZE > 16:
            bitmapSize = REGISTER_SIZE / 32
        #################### DYNAMIC AND MEMORY FILE #########################
        print "Generating Data For Dynamic and Memory Files..."
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
                            fieldsByInstruction = (REGISTER_SIZE * 2) + 1
                        ########################################################################
                        ## READ THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        if column > 0:
                            dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                            for i in range(8):
                                memory_block[column][tuple] += (
                                    "R " + str(bitmapSize) + " " + str(
                                        address_target_bitmap[column - 1] - 1) + " " + str(
                                        basicBlock + 2) + "\n")
                                address_target_bitmap[column - 1] += bitmapSize
                        ########################################################################
                        ##  APPLY PREDICATE
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 3) + "\n")
                        for i in range(8):
                            memory_block[column][tuple] += (
                                "R " + str(REGISTER_SIZE) + " " + str(address_base[column]) + " " + str(
                                    basicBlock + 3) + "\n")
                            address_base[column] += (REGISTER_SIZE)
                        ########################################################################
                        ## CREATE THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 4) + "\n")
                        for i in range(8):
                            memory_block[column][tuple] += str(
                                "W " + str(bitmapSize) + " " + str(address_target_bitmap[column]) + " " + str(
                                    basicBlock + 4) + "\n")
                            address_target_bitmap[column] += bitmapSize
                    elif column > 0:
                        if column == numberOfPredicates - 1:
                            fieldsByInstruction = (REGISTER_SIZE * 2) + 1
                        ########################################################################
                        ## READ THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                        for i in range(8):
                            memory_block[column][tuple] += (
                                "R " + str(bitmapSize) + " " + str(address_target_bitmap[column - 1] - 1) + " " + str(
                                    basicBlock + 2) + "\n")
                            address_target_bitmap[column - 1] += bitmapSize
                        if lastFieldSum > 0:
                            lastFieldSum = 0
                            ########################################################################
                            ##  APPLY PREDICATE
                            ########################################################################
                            dynamic_block[column][tuple] += str(str(basicBlock + 3) + "\n")
                            for i in range(8):
                                memory_block[column][tuple] += (
                                    "R " + str(REGISTER_SIZE) + " " + str(address_base[column]) + " " + str(
                                        basicBlock + 3) + "\n")
                                address_base[column] += (REGISTER_SIZE)
                        ########################################################################
                        ## CREATE THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 4) + "\n")
                        for i in range(8):
                            address_target_bitmap[column - 1] += bitmapSize
                            memory_block[column][tuple] += str(
                                "W " + str(bitmapSize) + " " + str(address_target_bitmap[column]) + " " + str(
                                    basicBlock + 4) + "\n")
                            address_target_bitmap[column] += bitmapSize
                basicBlock += 4
            lastFieldSum = 0
            fieldsByInstruction -= 1

        print "Writing on Dynamic and Memory File..."
        if QUERY_ENGINE == "pipelined":
            writeOnDynamicAndMemoryFilesPipelined()

        FILE_MEM.close()
        FILE_DYN.close()
        print "Dynamic and Memory Files Ok!"
        print "Compressing Files..."

        os.system("rm -f " + BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/x86/" + str(
            REGISTER_SIZE) + "/unrolled8x/selectivity/" + SELECTIVITY + "/" + "*gz")
        os.system("gzip " + BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/x86/" + str(
            REGISTER_SIZE) + "/unrolled8x/selectivity/" + SELECTIVITY + "/" + "*.out")
        print "ALL Done!"
