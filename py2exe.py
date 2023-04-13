from py2exe import freeze

freeze(
    console=[{'script': 'recover.py'}],

    options={'py2exe': {'bundle_files': 1, 'compressed': True}},

    zipfile=None

)