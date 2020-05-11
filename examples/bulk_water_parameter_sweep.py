from simulation_generator import generate_simulation
import os 

zHs = [0.40, 0.41, 0.42, 0.43]

simlation_path = "bulk_water_phase_transition_vashishta"
simulation_folder_name = "vashishta_water_z_H_series"

lmp_sim_dir = os.environ["HOME"]+"/simulations"

generate_simulation("bulk_water_phase_transition_vashishta", 
                        machine="kk_gpu", 
                        destination=lmp_sim_dir+"/scratch/henriasv/"+simulation_folder_name,
                        submit="bash")