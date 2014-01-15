#!/usr/bin/env python

# Import modules
import subprocess, sys, os, optparse
script_path = os.path.dirname(__file__)
myutils_path = os.path.join(script_path, '../myutils')
sys.path.append(myutils_path)
import myos
import general
import doe_reader
import execs_commands 

def run_trim_galore(logs_dir, out_dir, doe_csv_fn, header_name_of_in_fn, header_name_of_adapter_seq, header_name_of_read_length, trim_galore_options, rm_shorter_than_space, tissue, execute):
    trim_galore_options_list = trim_galore_options.split(' ')
    clip_R1_value_index = general.index_in_unique_list(trim_galore_options_list, '--clip_R1')+1
    print trim_galore_options_list[clip_R1_value_index]
    clip_R1_value = int(trim_galore_options_list[clip_R1_value_index])
    qname = 'regevlab'
    mem_usage = '5000'
    dict_fq_fns = doe_reader.read_experiment_field(doe_csv_fn, 'name', header_name_of_in_fn)
    dict_adapter_seq = doe_reader.read_experiment_field(doe_csv_fn, 'name', header_name_of_adapter_seq)
    dict_read_length = doe_reader.read_experiment_field(doe_csv_fn, 'name', header_name_of_read_length)
    myos.remove_all_files_given_dir(out_dir)
    myos.check_if_directory_exists_create_it(out_dir)
    for exp_name, in_fn in dict_fq_fns.iteritems():
        adapter_seq = dict_adapter_seq[exp_name]
        read_length = int(dict_read_length[exp_name])
        bsubcmd = myos.create_bsub_string_no_rm_logs_dir(logs_dir, exp_name+'_'+tissue, qname = qname, mem_usage = mem_usage)
        runcmd_tgf = execs_commands.trim_galore_filter(adapter_seq, trim_galore_options+' --length %s' %(read_length-clip_R1_value-rm_shorter_than_space), in_fn, out_dir)
        fullcmd = bsubcmd+'\"'+runcmd_tgf+'\"'
        print fullcmd
        myos.write_fullcmd(fullcmd, logs_dir, exp_name+'_'+tissue)
        if execute:
            os.system(fullcmd)
    return 0

def main():
    parser = optparse.OptionParser("Input: fastq files in DoE csv file, Output: trimmed fastq files with trim_galore")
    parser.add_option('-o', '--out_dir', action = "store")
    parser.add_option('-l', '--logs_dir', action = "store") 
    parser.add_option('-d', '--doe_csv', action = "store", help = "fullname to csv files containing experiment names and adaptor seqs")
    parser.add_option('-n', '--header_name_of_in_fn', default = None, action = "store")
    parser.add_option('-a', '--header_name_of_adapter_seq', default = None, action = "store")
    parser.add_option('-e', '--header_name_of_read_length', default = None, action = "store")
    parser.add_option('-r', '--rm_shorter_than_space', action = "store", help = "remove reads that after trimming are shorter than read_length - clip_R1 - rm_shorter_than_space") 
    parser.add_option('--trim_galore_options', action = "store", help = "options as a string i.e., --trim_galore_options='--clip_R1 14 --phred33 --stringency 5 -q 20 -e 0.05'")
    parser.add_option('--tissue', action = "store")
    parser.add_option('-x', '--execute', action = "store_true", default=False)
    (options, args) = parser.parse_args()
    run_trim_galore(options.logs_dir, options.out_dir, options.doe_csv, options.header_name_of_in_fn, options.header_name_of_adapter_seq, options.header_name_of_read_length, options.trim_galore_options, int(options.rm_shorter_than_space), options.tissue, options.execute)
    return 0

if __name__ == "__main__":
    main()
