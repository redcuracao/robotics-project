from setuptools import find_packages, setup

package_name = 'cock_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='suan',
    maintainer_email='suan@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        	'start_motion = cock_bot.a_motion_node:main',
            'start_motion_m = cock_bot.a1_motion_node:main',
            'put_shaker = cock_bot.b_put_shaker:main',
            'close_cap = cock_bot.c_close_cap:main',
            'get_shaker = cock_bot.d_get_shaker:main',
            'shaking = cock_bot.e_shaking:main',
            'put_shaker2 = cock_bot.f_put_shaker:main',
            'open_cap = cock_bot.g_twist_open_cap:main',
            'pour_drink = cock_bot.h_pour_drink:main',
            'cocktail_make = cock_bot.cocktail_orchestrator:main',
            'state_check = cock_bot.robot_state_checker:main',
            'spoon_spin_node = cock_bot.i_spoon:main',
            'robot_recovery_auto = cock_bot.robot_recovery_auto:main',
            'home = cock_bot.homepose:main',
            'no_shaking_1 = cock_bot.no_shaking:main',
            'no_shaking_2 = cock_bot.no_shaking_2:main',
            'no_shaking_3 = cock_bot.no_shaking_3:main',
        ],
    },
)
