from kivy.deps import sdl2, glew

# -*- mode: python -*-

block_cipher = None


a = Analysis(['src\\main.py'],
             pathex=['C:\\Users\\czaramo\\Desktop\\WGTS'],
             binaries=[],
             datas=[],
             hiddenimports=['win32timezone'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )

coll = COLLECT(exe, 
	       Tree('.\\src'),
               a.binaries,
               a.zipfiles,
               a.datas,
                *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='main')