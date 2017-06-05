# CS229S_Project

To run the quantification script:

Environment Requirements:
1. Linux/Mac OS
2. python3 and required python packages
3. Install all 4 tools, and add executable binaries to environment paths
4. Rscript
5. Polyester R package

Setup for script execution:
1. set project_dir in init() to point to your chosen project directory
2. This project_dir should contain the following:
    - salmon_adapter.py, sailfish_adapter.py, rnaskim_adapter.py, kallisto_adapter.py
    - general_utils.py, data_processing.py
    - simulation_script.R
    - directories: (x = 1 to 10)
  
        - project_dir/salmon/index, project_dir/salmon/output/sample[x]_result
        - project_dir/sailfish/index, project_dir/sailfish/output/sample[x]_result
        - project_dir/kallisto/index, project_dir/kallisto/output/sample[x]_result
        - project_dir/rnaskim/index, project_dir/rnaskim/output/sample[x]_result


Execution:

  - In terminal, type:
        
        python3 [project_dir]/quantification_script.py
        

    Options:

        -h,   --help                                show this help message and exit
        -q,   --quiet                               don't print execution outputs
        -t,   --transcript=NUMBER_OF_TRANSCRIPTS    int, default=10, number of transcripts to use in the simulation
