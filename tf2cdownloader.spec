# -*- mode: python ; coding: utf-8 -*-

file_datas=[]
file_datas=[ ('tf2c.ico', '.'), ('tf2cbanner.png', '.') ]
if os.name == 'nt':  # Windows
    file_datas += [ ('Binaries/', '.') ]
else:
    file_datas += [ ('Binaries_linux/', '.') ]
    
a = Analysis(
    ['tf2cdownloader.py'],
    pathex=[],
    binaries=[],
    datas=file_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'jedi', 'numpy', 'babel', 'typeshed'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TF2CDownloader-Tk-1.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    icon='tf2c.ico',
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)
