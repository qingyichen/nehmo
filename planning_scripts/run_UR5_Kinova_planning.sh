# Heterogeneous UR5 + Kinova Gen3 experiment (paper Table IV).
# Paper hyperparameters: t_plan = 0.1 (--step_time, default), t_safe = 0.3, epsilon = 0.05.
# The 100 challenging start/goal pairs are read from envs/collision_initial_conditions.json.
n_trials=100
video=""

# Naive / Naive
python planning/DualArm_UR5_Kinova_planning.py --num_trials $n_trials --buffer 0.05 --safe_time 0.3 --save_stats --planner_mode simple $video
# NeHMO / NeHMO
python planning/DualArm_UR5_Kinova_planning.py --num_trials $n_trials --buffer 0.05 --safe_time 0.3 --save_stats --planner_mode hji --provide_initial_condition --use_symmetry --experiment_name experiment_symmetric_IC_seed1 $video
# NeHMO / Naive
python planning/DualArm_UR5_Kinova_planning.py --num_trials $n_trials --buffer 0.05 --safe_time 0.3 --save_stats --planner_mode hji_simple --provide_initial_condition --use_symmetry --experiment_name experiment_symmetric_IC_seed1 $video
