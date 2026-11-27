from pathlib import Path
import nbformat
from nbclient import NotebookClient
root=Path(__file__).resolve().parents[1]
path=root/'notebooks/ait_lds_eda.ipynb'
notebook=nbformat.read(path,as_version=4)
NotebookClient(notebook,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
nbformat.write(notebook,path)
print('Executed',sum(c.cell_type=='code' for c in notebook.cells),'code cells')
