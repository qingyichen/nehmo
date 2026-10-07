import numpy as np

# Joint order within a single arm, from the base outwards.
UR5_JOINT_ORDER = [
    'shoulder_pan_joint',
    'shoulder_lift_joint',
    'elbow_joint',
    'wrist_1_joint',
    'wrist_2_joint',
    'wrist_3_joint',
]


def ur5_arm_joint_names(num_arms):
    '''Joint names per arm for the multi-UR5 URDFs, which prefix each joint with the arm index.'''
    return [[f'{arm}{joint}' for joint in UR5_JOINT_ORDER] for arm in range(1, num_arms + 1)]


def ur5_kinova_arm_joint_names():
    '''Joint names per arm for the heterogeneous UR5 + Kinova Gen3 URDF.'''
    return [
        [f'1{joint}' for joint in UR5_JOINT_ORDER],
        [f'kinova_joint_{i}' for i in range(1, 7)],
    ]


def build_mappings(robot, arm_joint_names):
    '''Build the mappings between the environment's joint order and the planner's arm-by-arm order.

    The environment indexes joints in `robot.actuated_joints` order. urchin produces that order by
    sorting joints on their distance to the base link with `np.argsort`, which is not stable, so
    joints sitting at the same depth (one per arm) are tied and their relative order is decided by
    the sort implementation. Hard-coding the resulting indices silently breaks whenever that
    tie-break changes, so derive them from the joint names instead.

    Args:
        robot: urchin URDF whose `actuated_joints` define the environment's joint order.
        arm_joint_names: list of per-arm joint-name lists, each in base-to-tip order.

    Returns:
        (env_to_qpos_mapping, qpos_to_env_mapping), inverse permutations of each other.
        `env_qpos[env_to_qpos_mapping]` groups the joints arm by arm.
    '''
    index_of = {joint.name: i for i, joint in enumerate(robot.actuated_joints)}
    missing = [n for arm in arm_joint_names for n in arm if n not in index_of]
    if missing:
        raise KeyError(f'joints missing from the URDF: {missing}')

    num_joints = sum(len(arm) for arm in arm_joint_names)
    if num_joints != len(index_of):
        raise ValueError(
            f'expected {len(index_of)} actuated joints, got {num_joints} across '
            f'{len(arm_joint_names)} arms'
        )

    env_to_qpos_mapping = np.array(
        [index_of[name] for arm in arm_joint_names for name in arm], dtype=np.int32
    )
    qpos_to_env_mapping = np.argsort(env_to_qpos_mapping).astype(np.int32)
    return env_to_qpos_mapping, qpos_to_env_mapping
