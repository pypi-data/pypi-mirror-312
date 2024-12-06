# MIPLIB Benchmark 
This python package allows the user to download and solve instances from the MIPLIB benchmark. 
We refer to the website (https://miplib.zib.de/) for more information on this dataset.

# Installation 

    pip install miplib_benchmark 
    miplib --help 

# Setup 
To download and unzip the dataset: 

    miplib setup 

Set the env variable MIPLIB_BENCHMARK_DIR to specify where to download it.

# Shows instances 
To show the first 5 instances: 

    miplib instances -c 5 

You can also call `miplib_benchmark.get_instances` to get the dataframe itself.

# Solve 
Via the CLI

    miplib solve -i "instance_name"

or in python 

    miplib_benchmark.solve("instance_name")