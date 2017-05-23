import re
import sys
import os, shutil
import subprocess as sub
import numpy as np
from sklearn.metrics import average_precision_score


def remove_file_if_exists(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass


def get_command_output(command_string):

    command_args = command_string.split()
    #print("Executing command:\n" + command_string + "\n")
    output = sub.check_output(command_args)
    return output.decode("utf-8")


def execute_command(command_string, verbose):
    command_args = command_string.split()
    print("Executing command:\n" + command_string + "\n")
    #print(command_args)
    try:
        FNULL = open(os.devnull, 'w')
        #sub.check_call(command_args)        
        sub.check_call(command_args, stdout=FNULL, stderr=sub.STDOUT)
    except:
        print("\n*** Error while executing:\n" + command_string + "\n")
        raise


def cleanup_dir(target_dir):
    folder = target_dir
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def simulate_reads(
    script_path, 
    number_of_transcripts, 
    readlen, 
    error_rate, 
    coverage, 
    output_dir):
    
    remove_file_if_exists(output_dir + '/transcript_names.txt')
    remove_file_if_exists(output_dir + '/num_of_reads.txt')

    command = "Rscript --vanilla " \
        + script_path + " " \
        + str(number_of_transcripts) + " " \
        + str(readlen) + " " \
        + str(error_rate) + " " \
        + str(coverage) + " " \
        + str(output_dir) + " " \

    execute_command(command, True)

    transcript_names = np.genfromtxt(
        output_dir + '/transcript_names.txt',
        names = None,
        dtype= None,
        usecols = (0))
    num_of_reads = np.genfromtxt(
        output_dir + '/num_of_reads.txt',
        names = None,
        dtype= None,
        usecols = (0))

    ground_truth_map = dict(zip(transcript_names, num_of_reads))

    return ground_truth_map


def remove_gene_id_from_map(old_map):
    #print("old_map:")
    #print(old_map)
    new_map = {}
    for (key,value) in old_map.items():
        key_array = key.decode("utf-8").split("|")
        new_key = ""
        if(len(key_array)>1):
            new_key = key_array[1]
        else:
            new_key = key_array[0]
        new_map[new_key] = old_map[key]
    return new_map


def get_average_accuracy(ground_truth_map, quantification_map):
    # print(ground_truth_map)
    # print(quantificatoin_map)
    if len(ground_truth_map)!=len(quantification_map):
        print("ground truth len=\n"+str(len(ground_truth_map)))
        print("quantification len=\n"+str(len(quantification_map)))
    ground_truth_map = remove_gene_id_from_map(ground_truth_map)
    quantification_map = remove_gene_id_from_map(quantification_map)
    errors = []
    #print("truth map:,len=\n"+str(len(ground_truth_map)))
    #print(ground_truth_map.items())
    #print("quant map:\n")
    #print(quantification_map.items())
    for (key,ground_truth_value) in ground_truth_map.items():
        #print("key:\n")
        #print(key)
        #print(ground_truth_map.keys())


        quantification_value = quantification_map[key]
        error = abs(float(quantification_value) - float(ground_truth_value))/float(ground_truth_value)
        errors.append(error)

    return 1-np.mean(errors)





