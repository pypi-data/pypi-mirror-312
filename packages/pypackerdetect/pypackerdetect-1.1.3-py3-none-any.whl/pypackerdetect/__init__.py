# -*- coding: UTF-8 -*-
import json
import os
import peid
import re
from functools import lru_cache
from pefile import PE


__all__ = ["PyPackerDetect", "PACKERS", "SECTIONS"]


with open(os.path.join(os.path.dirname(__file__), "db", "packers.json")) as f:
    PACKERS = json.load(f)['packers']
with open(os.path.join(os.path.dirname(__file__), "db", "sections.json")) as f:
    SECTIONS = json.load(f)['sections']


@lru_cache
def _real_section_names(path, logger=None, timeout=10):
    from subprocess import Popen, PIPE, TimeoutExpired
    p, names = Popen(["objdump", "-h", path], stdout=PIPE, stderr=PIPE), []
    try:
        out, err = p.communicate(timeout=timeout)
    except TimeoutExpired:
        if logger:
            logger.debug(f"objdump: timeout ({timeout} seconds)")
        return
    if err:
        if logger:
            for l in err.decode("latin-1").strip().split("\n"):
                logger.debug(l)
        return
    for l in out.decode("latin-1").strip().split("\n"):
        m = re.match(r"\s+\d+\s(.*?)\s+", l)
        if m:
            names.append(m.group(1))
    return names


class PyPackerDetect:
    def __init__(self, peid=True, peid_large_db=False, peid_ep_only=True, bad_ep_sections=True, low_imports=True,
                 packer_sections=True, unknown_sections=True, import_threshold=10, unknown_sections_threshold=3,
                 bad_sections_threshold=2, logger=None, **kwargs):
        """ Configure the detector with various parameters. """
        self.__config = {
            'peid_large_db': peid_large_db, 'peid_ep_only': peid_ep_only, 'packer_sections': packer_sections,
            'peid': peid, 'bad_ep_sec': bad_ep_sections, 'low_imports': low_imports, 'unknown_sec': unknown_sections,
        }
        self.__thresholds = {
            'bad_sections':     bad_sections_threshold,
            'imports':          import_threshold,
            'unknown_sections': unknown_sections_threshold,
        }
        self.logger = logger
    
    def detect(self, pe):
        """ Analyze the input PE file for suspicions and/or detections of packers. """
        r, s = {'detections': [], 'suspicions': []}, .0
        def __add(i, msg):
            if self.logger:
                self.logger.debug("%s:%s" % (['DETECTION', 'SUSPICION'][i], msg))
            r[['detections', 'suspicions'][i]].append(msg)
        if not isinstance(pe, PE):
            path = pe
            pe = PE(path)
            pe.path = path
        ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
        # parse the input PE file
        d = {'all': [], 'bad': [], 'ep': [], 'packer': [], 'unknown': []}
        for i, s in enumerate(pe.sections):
            try:
                n = s.Name.decode("ascii").strip().rstrip("\0")
                # special case: for some executables compiled with debug information, some sections may be named with
                #                the format "/[N]" where N is the offset in the string table ; in this case, we compute
                #                the real section names and map them to the shortened ones to compare the relevant names
                #                with the database of known section names
                if re.match(r"^\/\d+$", n) and _real_section_names(pe.path, logger=self.logger):
                    n = _real_section_names[i]
                d['all'].append(n)
                if ep >= s.VirtualAddress and ep <= (s.VirtualAddress + s.Misc_VirtualSize):
                    d['ep'].append(n)
                if n not in SECTIONS['known']:
                    d['unknown'].append(n)
                p = PACKERS.get(n)
                # even if found in the packers database, ensure the related section name does not clash with a known one
                if p is not None and n not in SECTIONS['known']:
                    d['packer'].append(n)
            except UnicodeDecodeError:
                d['bad'].append(s.Name.decode('latin1').strip().rstrip("\0"))
                __add(1, "Section name with invalid characters")
        # bad entry point sections
        __intersect = lambda l1, l2: len(set(l1).intersection(l2)) > 0
        if self.__config['bad_ep_sec']:
            ep_sec_list = "', '".join(d['ep'])
            if ep == 0:
                __add(1, "Null entry point")
            l_ep = len(d['ep'])
            if l_ep == 0:
                __add(0, "Entry point 0x%x falls in overlapping sections: '%s'" % (ep, ep_sec_list))
            else:
                if l_ep > 1:
                    __add(0, "Entry point 0x%x falls in overlapping sections: '%s'" % (ep, ep_sec_list))
                if not __intersect(SECTIONS['acceptable'], d['ep']):
                    bad_ep_sec = False
                    if __intersect(SECTIONS['delphi-bss'], d['all']):
                        # has bss, see if we have a delphi ep section
                        bad_ep_sec = not __intersect(SECTIONS['delphi'], d['ep'])
                    elif not __intersect(SECTIONS['acceptable'], d['all']):
                        # normal entry section doesn't exist anywhere, so check for alternatives
                        bad_ep_sec = not __intersect(SECTIONS['alternative'], d['ep'])
                    else:
                        # not regular ep section, not a delphi entry section, not an alternative entry section, and
                        #  regular entry section name exists, so the only possibility left is a driver entry section
                        bad_ep_sec = not __intersect(SECTIONS['driver'], d['ep'])
                    if bad_ep_sec:
                        __add(0, "Entry point 0x%x in irregular section(s): '%s'" % (ep, ep_sec_list))
        # low import count
        if self.__config['low_imports']:
            c = 0
            try:
                for lib in pe.DIRECTORY_ENTRY_IMPORT:
                    if lib.dll.decode("ascii").strip().rstrip("\0").lower() == "mscoree.dll":
                        c = -1  # .NET assembly, counting imports is misleading as they will have a low number
                        break
                    c += len(lib.imports)
            except AttributeError as e:
                pass
            if (0 <= c <= self.__thresholds['imports']):
                __add(0, "Too few imports (total: %d)" % c)
        # non standard sections
        if self.__config['unknown_sec']:
            u = len(d['unknown'])
            un_sec_list = "', '".join(d['unknown'])
            if u >= self.__thresholds['unknown_sections']:
                __add(0, "Detected %d non-standard sections: '%s'" % (u, un_sec_list))
            if len(d['bad']) >= self.__thresholds['bad_sections']:
                __add(0, "Detected %d sections with invalid names" % len(d['bad']))
        # packer sections
        if self.__config['packer_sections']:
            for n in d['packer']:
                __add(0, "Section name '%s' matches known packer: [%s]" % (n, PACKERS[n]))
        # apply PEiD
        if self.__config['peid']:
            db = os.path.join(os.path.dirname(__file__), "db", "sigs_long.txt") if self.__config['peid_large_db'] \
                 else os.path.join(os.path.dirname(__file__), "db", "sigs_short.txt")
            for m in peid.identify_packer(pe.path, db=db, ep_only=self.__config['peid_ep_only'], logger=self.logger):
                if len(m[1] or []) > 0:
                    __add(0, "Found PEID signature: %s" % ", ".join(m[1]))
        return r
    
    @staticmethod
    def report(pe, findings):
        """ Report findings like the original project. """
        print("Packer report for: %s" % (getattr(pe, "path", "unknown path") if isinstance(pe, PE) else pe))
        print("\tDetections: %d" % len(findings['detections']))
        print("\tSuspicions: %d" % len(findings['suspicions']))
        if len(findings['detections']) > 0 or len(findings['suspicions']) > 0:
            print("\tLog:")
            for d in findings['detections']:
                print("\t\t[DETECTION] %s" % d)
            for s in findings['suspicions']:
                print("\t\t[SUSPICION] %s" % s)

