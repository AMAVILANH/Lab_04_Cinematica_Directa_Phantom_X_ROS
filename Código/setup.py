from setuptools import find_packages, setup

package_name = 'pincher_control'

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
    maintainer='juanmeza',
    maintainer_email='juanmeza@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'macarena = pincher_control.macarena:main',
            'control_servo = pincher_control.control_servo:main',
            'lumos = pincher_control.lumos:main',
            'pentando = pincher_control.pentando:main'
        ],
    },
)
