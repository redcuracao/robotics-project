from setuptools import find_packages, setup

package_name = 'cocktail_bot'

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
        	'shake = cocktail_bot.shaker_node:main',
        	'open_lid = cocktail_bot.open_lid_node:main',
            'close_lid = cocktail_bot.close_lid_node:main'
        	'motion = cocktail_bot.motion_node:main',
        	'pour = cocktail_bot.pour_node:main',
            'make_cocktail = cocktail_bot.cocktail_fsm:main'
        ],
    },
)
