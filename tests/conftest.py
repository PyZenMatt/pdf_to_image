import pytest
import sys
import os
from pathlib import Path

# Aggiungi la cartella src al PATH
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def app():
    from main import PDFConverterApp
    import tkinter as tk
    
    root = tk.Tk()
    root.withdraw()
    app = PDFConverterApp(root)
    yield app
    root.destroy()