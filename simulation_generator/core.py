from importlib import import_module
import importlib.resources
import pkgutil
import tempfile  
import os 
import shutil
import errno
import sys
import json
import subprocess

kk_gpu_1 = {"partition" : "normal", "ntasks" : 1, "gres" : "gpu:1"}
cpu_4 = {"partition":"normal", "ntasks":4}

def create_job_script(machine, job_settings, lammps_varargs):
    if machine =="kk_gpu":
        dict_args = kk_gpu_1
    elif machine =="cpu":
        dict_args = cpu_4
    else:
        raise ValueError

    for key, value in job_settings.items():
        dict_args[key] = value
    job_script = "#!/bin/bash\n"
    job_script += "\n".join([f"#SBATCH --{key}={value}" for key, value in dict_args.items()])

    varargs_string = " ".join([f"-var {key} {value}" for key, value in lammps_varargs.items()])

    if machine == "kk_gpu":
        job_script += f"\nmpirun -n {dict_args['ntasks']} lmp -k on g {dict_args['ntasks']} -sf kk -pk kokkos newton on neigh half {varargs_string} -in run.in\n"
    elif machine=="cpu":
        job_script += f"\nmpirun -n {dict_args['ntasks']} lmp {varargs_string} -in run.in\n"
    return job_script

def generate_simulation(simulation_name, machine="kk_gpu", simulation_settings={}, job_settings={}, destination = "/tmp/mysim", submit=""):
    path = os.path.abspath(simulation_name)

    print(f"Creating simulation from template at {path}")

    cwd_path = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)
        sys.path.append(tmp_dir)
        template_files_path = os.path.join(path, "template_files.txt")
        if not os.path.isfile(template_files_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), template_files_path)

        template_files = open(template_files_path, "r").read().splitlines()
        for filename in template_files:
            shutil.copyfile(os.path.join(path, filename), os.path.join(tmp_dir, filename))

        from generate import generate 
        lammps_varargs = generate(**simulation_settings)
        
        with open(os.path.join(tmp_dir, "job.sh"), "w") as ofile:
            job_script = create_job_script(machine, job_settings, lammps_varargs)
            ofile.write(job_script)

        all_settings = {"simulation_settings" : simulation_settings,
                        "lammps_varargs" : lammps_varargs,
                        "job_settings" : job_settings}

        with open("parameters.json", "w") as ofile:
            ofile.write(json.dumps(all_settings))

        shutil.copytree(tmp_dir, destination)

        os.chdir(destination)
        if submit == "sbatch":      
            subprocess.run(["sbatch", "job.sh"])
        elif submit == "bash":
            subprocess.run(["bash", "-x", "job.sh"])

        os.chdir(cwd_path)

    return destination


if __name__=="__main__":
    simulation_settings = {"Z_h": 0.41}
    destination = generate_simulation("bulk_water_phase_transition_vashishta", machine="cpu", simulation_settings=simulation_settings)

