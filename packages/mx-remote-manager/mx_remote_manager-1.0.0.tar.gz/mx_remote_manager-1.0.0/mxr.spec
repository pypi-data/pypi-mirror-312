# -*- mode: python ; coding: utf-8 -*-
import os
import site

typelib_path = os.path.join(site.getsitepackages()[-1], 'gi')

a = Analysis(
    ['mxr.py'],
    pathex=[],
    binaries=[(os.path.join(typelib_path, tl), 'gi_typelibs') for tl in os.listdir(typelib_path)],
    datas=[('./mx_remote_manager/ui.gresource', './mx_remote_manager'), ('./mx_remote_manager/resources/svd.csv', './mx_remote/proto')],
	hiddenimports=['aes3tool', 'mx_remote'],
    hookspath=[],
    hooksconfig={
        "gi": {
            "icons": ["Adwaita"],
            "themes": ["Adwaita"],
            "languages": ["en_GB", "en_US"],
            "module-versions": {
                "Gtk": "4.0",
            },
        },
    },
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='mxr',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon=['mx_remote_manager/resources/icons/eu.opdenkamp.mx_remote_manager.ico'],
)
