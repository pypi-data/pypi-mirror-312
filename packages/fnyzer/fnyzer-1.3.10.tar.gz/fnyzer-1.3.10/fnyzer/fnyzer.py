# Use: optinet filename dictname
# Optimizes the flexible net in dictionary dictname of file filename
import argparse
import importlib.util
import sys
from fnyzer import FNFactory

def main():
    """Manage parameters"""
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Python file containing the flexible net dictionary")
    parser.add_argument("dictname", help="Python variable in 'filename' containing the flexible net dictionary")
    args = parser.parse_args()
    if args.filename.endswith(".py"):
        args.filename = args.filename[:-3]
    
    """Get data"""
    spec = importlib.util.spec_from_file_location(args.filename, f"{args.filename}.py")
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {args.filename}")
    
    allnets = importlib.util.module_from_spec(spec)
    sys.modules[args.filename] = allnets
    spec.loader.exec_module(allnets)
    
    netd = getattr(allnets, args.dictname)  # Flexible net dictionary
    
    """Build and optimize"""
    print("Building net...")
    net = FNFactory(netd)  # Build net object
    print("Optimizing...")
    model = net.optimize()  # Optimize net and save results
    print("Done.")

