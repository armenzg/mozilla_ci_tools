#! /usr/bin/env python
"""
This module helps us connect builds to tests since we don't have an API
to help us with this task.
"""
import logging

log = logging.getLogger()

# XXX: Once we have unit tests for this feature we will probably find
# issues, specially, in the b2g naming
PREFIX = {
    "Ubuntu VM 12.04": "Linux",
    "Ubuntu HW 12.04": "Linux",
    "Ubuntu VM 12.04 x64": "Linux x86-64",
    "Ubuntu HW 12.04 x64": "Linux x86-64",
    "Rev4 MacOSX Snow Leopard 10.6": "OS X 10.7",
    "Rev5 MacOSX Mountain Lion 10.8": "OS X 10.7",
    "Windows XP 32-bit": "WINNT 5.2",
    "Windows 7 32-bit": "WINNT 5.2",
    "Windows 8 64-bit": "WINNT 6.1 x86-64",
    "Android armv7 API 9": "Android armv7 API 9",
    "Android 4.0 armv7 API 11+": "Android armv7 API 11+",
    "Android 4.2 x86 Emulator": "Android 4.2 x86",
    "b2g_ubuntu32_vm": "b2g_%(repo_name)s_linux32_gecko",
    "b2g_ubuntu64_vm": "b2g_%(repo_name)s_linux64_gecko",
    "b2g_macosx64": "b2g_%(repo_name)s_macosx64_gecko",
    "b2g_emulator_vm": "b2g_%(repo_name)s_emulator_dep",
}

JOB_TYPE = {
    "opt": "build",
    "pgo": "pgo-build",
    # '-debug_dep' for ICS emulator jobs
    # '-debug build' for b2g desktop
    "debug": "leak test build",
    "talos": "build",
}


def associated_build_job(buildername, repo_name):
    '''
    The prefix and the post fix of a builder name can tell us
    the type of build job that triggered it.
    e.g. Windows 8 64-bit cedar opt test mochitest-1
    e.g. b2g_ubuntu64_vm cedar opt test gaia-unit

    We would prefer to have a non-mapping approach, however,
    we have not figured out an approach to determine the graph
    of dependencies.
    '''
    # XXX: This assumes that is not the buildername of a build
    # XXX: b2g jobs will need a different mapping logic
    prefix, job_type = buildername.split(" %s " % repo_name)
    job_type = job_type.split(" ")[0]
    associated_build = \
        "%s %s %s" % (PREFIX[prefix], repo_name, JOB_TYPE[job_type])
    log.debug("The build job that triggers %s is %s" % (buildername,
                                                        associated_build))
    return associated_build


def does_builder_need_files(buildername):
    # XXX: This is closely tied to the buildbot naming
    # We could determine this by looking if the builder belongs to
    # the right schedulers in allthethings.json
    for match in ("opt", "pgo", "debug", "talos"):
        if buildername.find(match) != -1:
            return True
    return False
