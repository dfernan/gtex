# This module contains functions that output a cmd string for calling executables, should be broad/odyssey compatible

import os, sys, subprocess
script_path = os.path.dirname(__file__)
sys.path.append(script_path)
import myos

def start_java_cmd(mem_usage, additional_option):
    return 'java -Xmx%sm %s -jar' %(mem_usage, additional_option)

def fastx_trimmer(options, input_fn, output_fn):
    ''' writes command for running fastx_trimmer 
    options should be a string -Q 33 -f 16'''
    en = 'fastx_trimmer'
    cmd = '%s %s -i %s -o %s;' %(en, options, input_fn, output_fn)
    return cmd

def casava_quality_filter(input_fn, output_fn):
    ''' writes command for running fastx_trimmer 
    options should be a string -Q 33'''
    en = 'perl /seq/epiprod/de/Cerebellum/code/casava_filter.pl'
    cmd = '%s -i %s -o %s;' %(en, input_fn, output_fn)
    return cmd

def fastx_adaptor_filter(adaptor_seq, options, input_fn, output_fn):
    ''' writes command for running fastx_clipper
    options should be a string -Q 33'''
    en = 'fastx_clipper'
    cmd = '%s -a %s %s -i %s -o %s;' %(en, adaptor_seq, options, input_fn, output_fn)
    return cmd

def fastq_quality_filter(options, input_fn, output_fn):
    ''' writes command for running fastx_trimmer 
    options should be a string -Q 33'''
    en = 'fastq_quality_filter'
    cmd = '%s %s -i %s -o %s;' %(en, options, input_fn, output_fn)
    return cmd

def fastx_artifacts_filter(options, input_fn, output_fn):
    ''' writes command for running fastx_trimmer 
    options should be a string -Q 33'''
    en = 'fastx_artifacts_filter'
    cmd = '%s %s -i %s -o %s;' %(en, options, input_fn, output_fn)
    return cmd

def fastqc(input_fns, output_dir):
    ''' writes command for running fastx_trimmer 
    options should be a string -Q 33'''
    server = myos.which_server()
    if server == 'broad':
      en = 'perl /broad/software/free/Linux/redhat_5_x86_64/pkgs/fastqc_0.10.1/FastQC/fastqc'
    elif server == 'odyssey':
      en = 'perl /n/dulacfs2/Users/dfernand/de/software/FastQC/fastqc'
    cmd = '%s -o %s %s' %(en, output_dir, input_fns)
    return cmd

def trim_galore_filter(adapter_seq, options, input_fn, output_dir):
    ''' writes command for running fastx_trimmer 
    options should be a string -Q 33'''
    server = myos.which_server()
    if server == 'broad':
      en = '/home/unix/dfernand/bin/trim_galore/trim_galore'
      cmd = '%s -o %s -a %s %s %s' %(en, output_dir, adapter_seq, options, input_fn)
    elif server == 'odyssey':
      en = '/n/dulacfs2/Users/dfernand/de/software/trim_galore_v0.3.3/trim_galore'
      cmd = 'module load centos6/cutadapt-1.2.1_python-2.7.3;%s -o %s -a %s %s %s' %(en, output_dir, adapter_seq, options, input_fn)
    return cmd

def bowtie_1_run(options, index_fn, input_fn, output_fn):
    ''' writes command for running bowtie mapper 
        NOTE: output_fn always needs to be a basefullname with .sorted, it will add the .bam
    '''
    en = "/home/unix/dfernand/bin/bowtie-1.0.0/bowtie"
    cmd = "%s %s %s %s | samtools view -bS - | samtools sort -n - %s" %(en, options, index_fn, input_fn, output_fn)
    return cmd

def phasedBam2bed(bam_in_fn, bed_p_fn, bed_m_fn):
    ''' command for nimrod executable phasedBam2bed 
    '''
    en = "/seq/epiprod/de/scripts/nimrod/samtoolsUtils/phasedBam2bed"
    cmd = "%s -b %s -p %s -m %s" %(en, bam_in_fn, bed_p_fn, bed_m_fn)
    return cmd

class bedops:
    def __init__(self):
        self.server = myos.which_server()
        if self.server == 'broad':
           self.dep_cmd = myos.load_dependencies_cmd(['.bedops-2.0.0b'])
        elif self.server == 'odyssey':
            self.dep_cmd = myos.load_dependencies_cmd(['centos6/bedops-2.3.0'])
    def sortbed(self, bed_in_fn, bed_out_fn, options=''):
        if options == '':
            en = 'sort-bed %s > %s' %(bed_in_fn, bed_out_fn)
        else:
            en = 'sort-bed %s %s > %s' %(options, bed_in_fn, bed_out_fn)
        return self.dep_cmd+en
    def vcf2bed(self, vcf_in_fn, vcf_out_fn):
        en = 'vcf2bed < %s > %s' %(vcf_in_fn, vcf_out_fn)
        return self.dep_cmd+en
    def bedmap(self, bedmap_options, reference_in_fn, map_fn, out_fn):
        en = 'bedmap %s %s %s > %s' %(bedmap_options, reference_in_fn, map_fn, out_fn)
        return self.dep_cmd+en
            
class igvtools:
    def __init__(self):
        self.server = myos.which_server()
        if self.server == 'broad':
           self.igv_fn = '/home/unix/dfernand/bin/IGVTools/igvtools.jar'
        elif self.server == 'odyssey':
            self.dep_cmd = myos.load_dependencies_cmd(['bio/igvtools-2.2.2'])
            self.igv_fn = '/n/sw/igvtools-2.2.2/igvtools.jar'
    def index(self, in_fn):
        java_cmd = start_java_cmd('3000', '-Djava.awt.headless=true')
        en = '%s %s index %s' %(java_cmd, self.igv_fn, in_fn)
        if self.server == 'odyssey':
            return self.dep_cmd+en
        elif self.server == 'broad':
            return en
    def sort(self, in_fn, sort_fn):
        java_cmd = start_java_cmd('3000', '-Djava.awt.headless=true')
        en = '%s %s sort %s %s' %(java_cmd, self.igv_fn, in_fn, sort_fn)
        if self.server == 'odyssey':
            return self.dep_cmd+en
        elif self.server == 'broad':
            return en
