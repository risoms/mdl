:: https://github.com/bndr/pipreqs
:: generate list of required packages

:: run pipreqs
pipreqs mdl/ --encoding=iso-8859-1 --debug --force --version=exact --exclude=rpy2,pip,PIL,bokeh,pylink,mdl,imhr,AppKit,pyglet,wmi,pyobjc,yarg,scikit_learn,psd_tools,cv2,opencv_python --savepath=requirements.txt
