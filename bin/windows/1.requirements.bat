REM # https://github.com/bndr/pipreqs
REM # generate list of required packages

REM # set path as current location
cd ../../

REM # run pipreqs
python ./imhr/lib/pipreqs/pipreqs.py ./imhr/ --encoding=iso-8859-1 --debug --force --version=greater --exclude=rpy2,pylink,mdl,imhr,win32api,wmi,pyglet,pyobjc,AppKit,pip,psychopy,PyYAML --include=pytest,pandas,scipy,numpy --savepath=requirements.txt
