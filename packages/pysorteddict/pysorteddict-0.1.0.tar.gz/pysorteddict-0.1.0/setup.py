import os
import sysconfig

import setuptools

# If running on either one of Linux, macOS and Cygwin, or MSYS2, specify the
# argument the way the corresponding tools expect it.
cxx_standard_arg = "-std=c++14" if os.name != "nt" or sysconfig.get_platform().startswith("mingw") else "/std:c++14"

setuptools.setup(
    ext_modules=[
        setuptools.Extension(
            name="pysorteddict",
            extra_compile_args=[cxx_standard_arg],
            sources=["src/pysorteddict/pysorteddict.cc"],
            py_limited_api=True,
        )
    ]
)
