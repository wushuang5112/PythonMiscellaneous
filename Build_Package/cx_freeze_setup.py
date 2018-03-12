from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable(
    	script='bin\\Client.py',
    	base=base,
    	targetName = 'CMDB_Client.exe',
    	icon='favicon.ico',
    	copyright='copyright for me'
    	)
]

setup(name='CMDB_Client',
      version = '2.0.0',
      description = 'CMDB Client Install Excute File.',
      options = dict(build_exe = buildOptions),
      executables = executables)

# 打包成msi文件
# python setup.py bdist_msi
# 打包成exe可执行程序
# python setup.py build
