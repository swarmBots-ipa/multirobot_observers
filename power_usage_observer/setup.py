from setuptools import setup

package_name = 'power_usage_observer'

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
    maintainer='ipa',
    maintainer_email='ragesh.ramachandran@ipa.fraunhofer.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'main = power_usage_observer.main:main',
            'power_observer_plotter = power_usage_observer.power_observer_plotter:main',
            'influxdata = power_usage_observer.influxData:main'

        ],
    },
)
