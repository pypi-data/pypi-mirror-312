from setuptools import setup

setup(
    name='pysdlstrap',
    version='0.1.0',
    description='PySDLStrap - is a wrapper for SDL2 library for writting optimized apps in python on high-level language.',
    long_description=open('README.md').read(),
    url='https://github.com/nesquikcode/pysdlstrap',
    author='nesquik',
    author_email='nesquik@nishine.ru',
    license='MIT',
    keywords='app apps pygame sdl sdl2 wrapper python bootstrap framework game engine',
    packages=['psdls'],
    install_requires=['PySDL2==0.9.16', 'pysdl2-dll>=2.30.9'],
    package_data={}
)