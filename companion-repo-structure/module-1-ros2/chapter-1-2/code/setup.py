from setuptools import setup

package_name = 'simple_ros2_examples'

setup(
    name=package_name,
    version='0.1.0',
    packages=[],
    py_modules=['simple_publisher', 'simple_subscriber'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='example@example.com',
    description='Simple ROS 2 publisher and subscriber examples',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_publisher = simple_publisher:main',
            'simple_subscriber = simple_subscriber:main',
        ],
    },
)