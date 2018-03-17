#coding: utf8
import os
import distutils
from uuid import uuid1
from cx_Freeze import setup, Executable
from conf.settings import VERSION

# Dependencies are automatically detected, but it might need
# fine tuning.
# if distutils.util.get_platform() == "win-amd64":
#     programFilesFolder = "[ProgramFiles64Folder]"
# else:
#     programFilesFolder = "[ProgramFilesFolder]"
buildOptions = dict(
    packages = [],
    excludes = [],
    include_files = [
        ('logs', os.path.join('lib', 'logs')),
        ('var', os.path.join('lib', 'var'))
      ],
    include_msvcr = True
  )

bdistMsiOptions = dict(
    add_to_path = True,
    upgrade_code = '{%s}' % str(uuid1()).upper()
  )

base = 'Console'

executables = [
    Executable(
    	script=os.path.join('bin', 'Client.py'),
    	base=base,
    	targetName='PROGRAM_Client.exe',
    	# icon='favicon.ico',
    	copyright=u"@ 2018 ShenZhen XXXX"
    	)
]

setup(name='PROGRAM_Client',
      version = VERSION[1:],
      description = 'PROGRAM Client Install Excute File.',
      options = dict(
        build_exe = buildOptions,
        bdist_msi = bdistMsiOptions
      ),
      executables = executables)

# 打包成msi文件
# python setup.py bdist_msi
# 打包成exe可执行程序
# python setup.py build
