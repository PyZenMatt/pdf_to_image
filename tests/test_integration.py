import unittest
import os
import tempfile
import time
from src.main import PDFConverterApp
import tkinter as tk

class TestPDFConverterIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configurazione iniziale per tutti i test"""
        cls.test_pdf = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_files",
            "sample.pdf"
        )
        
        # Verifica che il file di test esista
        if not os.path.exists(cls.test_pdf):
            raise unittest.SkipTest(f"Test PDF not found at {cls.test_pdf}")
        
        cls.root = tk.Tk()
        cls.root.withdraw()

    def setUp(self):
        """Prepara l'ambiente per ogni test"""
        self.app = PDFConverterApp(self.root)
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        """Pulizia dopo ogni test"""
        for f in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, f))
        os.rmdir(self.output_dir)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_real_conversion(self):
        """Test con un vero PDF piccolo"""
        # Configura l'app
        self.app.entry_pdf_path.delete(0, tk.END)
        self.app.entry_pdf_path.insert(0, self.test_pdf)
        self.app.entry_output_folder.delete(0, tk.END)
        self.app.entry_output_folder.insert(0, self.output_dir)
        self.app.dpi_var.set(100)  # Basso DPI per test veloci
        
        # Esegui conversione
        self.app.convert_pdf()
        
        # Attendi il completamento (massimo 10 secondi)
        start_time = time.time()
        while len(os.listdir(self.output_dir)) == 0 and (time.time() - start_time) < 10:
            self.app.root.update()
            time.sleep(0.1)
        
        # Verifica
        output_files = os.listdir(self.output_dir)
        self.assertGreater(len(output_files), 0, "Nessun file è stato creato")
        self.assertTrue(any(f.lower().endswith('.png') for f in output_files),
                      "Nessun file PNG trovato tra: " + str(output_files))