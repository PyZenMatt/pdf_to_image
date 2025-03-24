import unittest
from unittest.mock import patch, MagicMock, call
from src.main import PDFConverterApp
import tkinter as tk
import time

class TestPDFConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()
    
    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()
    
    def setUp(self):
        self.app = PDFConverterApp(self.root)
    
    def test_initial_state(self):
        """Verifica lo stato iniziale dell'applicazione"""
        self.assertEqual(self.app.conversion_in_corso, False)
        self.assertEqual(self.app.should_stop, False)
        self.assertEqual(self.app.entry_pdf_path.get(), "")
        self.assertEqual(self.app.entry_output_folder.get(), "")
    
    @patch('src.main.filedialog.askopenfilename')
    def test_select_pdf(self, mock_openfilename):
        """Test selezione file PDF"""
        mock_openfilename.return_value = "/percorso/fake.pdf"
        self.app.select_pdf()
        self.assertEqual(self.app.entry_pdf_path.get(), "/percorso/fake.pdf")
    
    @patch('src.main.filedialog.askdirectory')
    def test_select_output_folder(self, mock_askdirectory):
        """Test selezione cartella output"""
        mock_askdirectory.return_value = "/percorso/output"
        self.app.select_output_folder()
        self.assertEqual(self.app.entry_output_folder.get(), "/percorso/output")
    
    @patch('src.main.convert_from_path')
    def test_convert_pdf_success(self, mock_convert):
        """Test conversione PDF con successo"""
        # Configura mock
        mock_page = MagicMock()
        mock_convert.return_value = [mock_page] * 1  # Simula 1 immagine per pagina
        
        with patch('src.main.pdfinfo_from_path') as mock_pdfinfo:
            mock_pdfinfo.return_value = {"Pages": 3}
            
            # Imposta percorsi
            self.app.entry_pdf_path.insert(0, "test.pdf")
            self.app.entry_output_folder.insert(0, "output")
            
            # Esegui conversione
            self.app.convert_pdf()
            
            # Simula l'avanzamento del progresso
            for i in range(1, 4):
                self.app.progress_var.set(i / 3 * 100)
                self.app.root.update()
            
            # Verifiche
            self.assertEqual(self.app.progress_var.get(), 100)
            self.assertIn("Conversion completed", self.app.log_text.get("1.0", tk.END))
            
            # Verifica che sia stato chiamato 3 volte (una per pagina)
            self.assertEqual(mock_convert.call_count, 3)
            
            # Verifica i parametri delle chiamate
            expected_calls = [
                call('test.pdf', dpi=200, first_page=1, last_page=1, thread_count=1),
                call('test.pdf', dpi=200, first_page=2, last_page=2, thread_count=1),
                call('test.pdf', dpi=200, first_page=3, last_page=3, thread_count=1)
            ]
            mock_convert.assert_has_calls(expected_calls, any_order=False)
