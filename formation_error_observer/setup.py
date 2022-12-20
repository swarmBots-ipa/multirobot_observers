from setuptools import setup

package_name = 'formation_error_observer'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kut-jr',
    maintainer_email='janavi.ramesh@ipa.fraunhofer.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [ 
            'pose_json = formation_error_observer.pose_json:main',
            'goal_json = formation_error_observer.goal_json:main',
            'plotter = formation_error_observer.plotter:main',
            'main = formation_error_observer.main:main'
        ],
    },
)
