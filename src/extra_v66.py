#!/usr/bin/env python3
import platform, sys, datetime, getpass, hashlib

def fingerprint():
    data = f"{platform.platform()}|{sys.version}|{datetime.datetime.utcnow().isoformat()}|{getpass.getuser()}".encode()
    return hashlib.sha256(data).hexdigest()[:12]

if __name__ == "__main__":
    print("Extra v66 demo")
    print("Python:", sys.version.split()[0])
    print("OS:", platform.system(), platform.release())
    print("UTC now:", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    print("Fingerprint:", fingerprint())
