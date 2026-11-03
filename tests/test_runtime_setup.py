import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('prepare_runtime',Path(__file__).resolve().parents[1]/'prepare_runtime.py')
setup=importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class RuntimeSetupTests(unittest.TestCase):
    def test_environment_is_independent_of_package_location_and_requirements_versioned(self):
        base=Path('short')
        self.assertEqual(setup.environment_path(base,b'package==1'),setup.environment_path(base,b'package==1'))
        self.assertNotEqual(setup.environment_path(base,b'package==1'),setup.environment_path(base,b'package==2'))
        self.assertLess(len(str(setup.environment_path(base,b'package==1'))),40)

    def test_marker_only_after_successful_native_import(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);requirements=base/'requirements.txt';requirements.write_text('test==1')
            env=setup.environment_path(base,requirements.read_bytes())
            python=env/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
            calls=[]
            def runner(args,**kwargs):
                calls.append(args)
                if 'venv' in args:
                    python.parent.mkdir(parents=True);python.touch()
                if '-c' in args:
                    raise subprocess.CalledProcessError(1,args)
            with self.assertRaises(subprocess.CalledProcessError):setup.prepare(base,requirements,runner)
            self.assertFalse((env/'.ready').exists())
            setup.prepare(base,requirements,lambda *args,**kwargs:None)
            self.assertTrue((env/'.ready').exists())
            cached=[]
            setup.prepare(base,requirements,lambda args,**kwargs:cached.append(args))
            self.assertFalse(any('pip' in args for args in cached))
            self.assertTrue(any('-c' in args for args in cached))
