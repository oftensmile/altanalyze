import sys
import suds

_script = 'AltAnalyze.py'
_appName = "AltAnalyze"
_appVersion = '1.2.4'
_appDescription = "AltAnalyze is a freely available, open-source and cross-platform program that allows you to take RNASeq or "
_appDescription +="relatively raw microarray data (CEL files or normalized), identify predicted alternative splicing or alternative "
_appDescription +="promoter changes and view how these changes may affect protein sequence, domain composition, and microRNA targeting."
_authorName = 'Nathan Salomonis'
_authorEmail = 'nsalomonis@gmail.com'
_authorURL = 'http://www.altanalyze.org'
_appIcon = "AltAnalyze_W7.ico"

excludes = [] #["wxPython"] #"numpy","scipy","matplotlib"
includes = ["suds", "mpmath", "numpy"]
""" By default, suds will be installed in site-packages as a .egg file (zip compressed). Make a duplicate, change to .zip and extract
here to allow it to be recognized by py2exe (must be a directory) """


matplot_exclude = [] #['MSVCP90.dll']
scipy_exclude = [] #['libiomp5md.dll','libifcoremd.dll','libmmd.dll']

""" xml.sax.drivers2.drv_pyexpat is an XML parser needed by suds that py2app fails to include. Identified by looking at the line: parser_list+self.parsers in
/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/PyXML-0.8.4-py2.7-macosx-10.6-intel.egg/_xmlplus/sax/saxexts.py
check the py2app print out to see where this file is in the future """

if sys.platform.startswith("darwin"):
        ### example command: python setup.py py2app
        includes+= ["xml.sax.drivers2.drv_pyexpat"]
        from distutils.core import setup
        import py2app
        options = {"py2app":
                    {"excludes": excludes,
                     "includes": includes,
                     #argv_emulation = True,
                    "iconfile": "altanalyze.icns"}
        }
        setup(name=_appName,
                        app=[_script],
                        version=_appVersion,
                        description=_appDescription,
                        author=_authorName,
                        author_email=_authorEmail,
                        url=_authorURL,
                        options=options,
                        #data_files=data_files,
                        setup_requires=["py2app"]
        )

if sys.platform.startswith("win"):
        ### example command: python setup.py py2exe
        from distutils.core import setup
        import py2exe
        import suds
        import numpy
        import matplotlib
        import unique
        import sys
            
        #sys.path.append(unique.filepath("Config\DLLs")) ### This is added, but DLLs still require addition to DLL python dir
        from distutils.filelist import findall
        import os
        
        data_files=matplotlib.get_py2exe_datafiles()
        
        matplotlibdatadir = matplotlib.get_data_path()
        matplotlibdata = findall(matplotlibdatadir)
        matplotlibdata_files = []
        for f in matplotlibdata:
            dirname = os.path.join('matplotlibdata', f[len(matplotlibdatadir)+1:])
            matplotlibdata_files.append((os.path.split(dirname)[0], [f]))

        
        windows=[{"script":_script,"icon_resources":[(1,_appIcon)]}]
        options={'py2exe':
                        {
                        "includes": 'suds',
                        "includes": 'matplotlib',
                        "includes": 'mpl_toolkits',
                        "includes": 'matplotlib.backends.backend_tkagg',
                        "dll_excludes": matplot_exclude+scipy_exclude,
                        }}
        setup(
                        windows = windows,
                        options = options,
                        version=_appVersion,
                        description=_appDescription,
                        author=_authorName,
                        author_email=_authorEmail,
                        url=_authorURL,
                        data_files=matplotlibdata_files+data_files,
        )

if sys.platform.startswith("2linux"):
	# bb_setup.py
	from bbfreeze import Freezer
	 
	f = Freezer(distdir="bb-binary")
	f.addScript("AltAnalyze.py")
	f()

if sys.platform.startswith("linux"):
        ### example command: python setup.py build
        includes = ['matplotlib','mpl_toolkits','matplotlib.backends.backend_tkagg']
        includefiles = []

        from cx_Freeze import setup, Executable
        ### use to get rid of library.zip and move into the executable, along with appendScriptToLibrary and appendScriptToExe
        #buildOptions = dict(create_shared_zip = False) 

	setup(
		name = _appName,
		version=_appVersion,
		description=_appDescription,
		author=_authorName,
		author_email=_authorEmail,
		url=_authorURL,
		#options = dict(build_exe = buildOptions),
		options = {"build_exe": {"includes":includes, "include_files": includefiles}},
		executables = [Executable(_script,
				#appendScriptToExe=True,
				#appendScriptToLibrary=False,
				#icon='goelite.ico',
				compress=True)],
	)

