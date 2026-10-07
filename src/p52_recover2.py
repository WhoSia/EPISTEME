from pathlib import Path
import shutil,sys
from p62_completion_lattice import main
sys.argv=['p62_completion_lattice']
main()
Path('receipts').mkdir(exist_ok=True)
shutil.copyfile('receipts/p62_result.json','receipts/p52_recovery2.json')
