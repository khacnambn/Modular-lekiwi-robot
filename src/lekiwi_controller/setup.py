from setuptools import setup

package_name = 'lekiwi_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/control.launch.py']),
        ('lib/' + package_name, ['scripts/omni_controller.py', 'scripts/omni_odometry.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your@email.com',
    description='ROS 2 package for LeKiwi robot controller',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'omni_controller = scripts.omni_controller:main',
            'omni_odometry = scripts.omni_odometry:main',
        ],
    },
)