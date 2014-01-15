#!/usr/bin/env python

# Import modules
import subprocess, sys, os, optparse
script_path = os.path.dirname(__file__)
myutils_path = os.path.join(script_path, '../myutils')
sys.path.append(myutils_path)
import myos
import doe_reader
import execs_commands 
SCRIPTS = '/seq/epiprod/de/scripts/nimrod/'
dependencies_list = ['.fastqc-0.10.1']

def run_fastqc(doe_csv_fn, out_dir, logs_dir, header_name_of_in_fn, extension_name, in_dir, execute):
    myos.check_if_directory_exists_create_it(out_dir)
    qname = 'regevlab'
    mem_usage = '5000'
    if extension_name is not None:
      dict_fq_fns = doe_reader.create_experiment_fns(doe_csv_fn, 'name', in_dir, extension_name)
    elif header_name_of_in_fn is not None:
      dict_fq_fns = doe_reader.read_experiment_field(doe_csv_fn, 'name', header_name_of_in_fn)
    out_dir = out_dir
    dep_cmd = myos.load_dependencies_cmd(dependencies_list)
    dep_cmd = dep_cmd+'reuse .fastqc-0.10.1;'
    for exp_name, in_fn in dict_fq_fns.iteritems():
        bsubcmd = myos.create_bsub_string_no_rm_logs_dir(logs_dir, exp_name, qname = qname, mem_usage = mem_usage)
        runcmd = execs_commands.fastqc(in_fn, out_dir)
        fullcmd = bsubcmd+'\"'+runcmd+'\"'
        print fullcmd
        if execute:
            os.system(fullcmd)
    return 0

def main():
    parser = optparse.OptionParser()
    parser.add_option('-d', '--doe_csv_fn', action = "store") 
    parser.add_option('-o', '--out_dir', action = "store") 
    parser.add_option('-l', '--logs_dir', action = "store", help = "a log dir or n for default out_dir+'trimmed/'")
    parser.add_option('-n', '--header_name_of_in_fn', default = None, action = "store", help = "in case extension and in_fn are used it's HEADER_NAME_OF_ID")
    parser.add_option('-e', '--extension_name', action = "store", default = None, help = "i.e., .fastq, .gz, .fq, _trimmed.fastqc, etc. (add the dot if it's a .extn, or add the _ if it's a _ extn) it will run fastqc for each file with such extension in the out_dir; for a single file just do file_name, i.e, MF1i5_P8_trimmed.fastq")
    parser.add_option('-i', '--in_dir', action = "store", help = 'only if extension name is provided one needs an in_dir, otherwise, the in_fn will be read from doe_csv')
    parser.add_option('-x', '--execute', action = "store_true", default = False)
    (options, args) = parser.parse_args()
    run_fastqc(options.doe_csv_fn, options.out_dir, options.logs_dir, options.header_name_of_in_fn, options.extension_name, options.in_dir, options.execute)
    return 0

if __name__ == "__main__":
    main()
