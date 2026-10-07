from __future__ import annotations
import argparse,sys
from p63_analyze_shards import main as p63_main

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rows-root',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    sys.argv=['p63_analyze_shards','--rows-root',a.rows_root,'--out',a.out]
    p63_main()

if __name__=='__main__':main()
