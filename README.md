# 📄 PDF to Image Converter

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A cross-platform GUI application that converts PDF files to high-quality PNG images with progress tracking and automatic file numbering.

![Application Screenshot](docs/screenshot.png) <!-- Replace with actual screenshot path -->

## 🌟 Features

- **Intuitive GUI** with file/folder selection dialogs
- **Real-time progress tracking** with progress bar
- **Auto-numbering** (001, 002, ...) for output files
- **High-resolution conversion** (300 DPI default)
- **Conversion logging** for transparency
- **Cross-platform support** (Windows, macOS, Linux)
- **Error handling** with user-friendly messages

## 📋 Table of Contents

- [📄 PDF to Image Converter](#-pdf-to-image-converter)
  - [🌟 Features](#-features)
  - [📋 Table of Contents](#-table-of-contents)
  - [🛠 Prerequisites](#-prerequisites)
  - [📦 Installation](#-installation)
    - [1. Clone the repository](#1-clone-the-repository)

## 🛠 Prerequisites

- Python 3.8+
- [Poppler-utils](#poppler-installation)
- pip package manager

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/pdf-to-image-converter.git
cd pdf-to-image-converter

2. Install Python dependencies
bash
Copy

pip install -r requirements.txt

3. Install Poppler
Windows

    Download poppler-windows

    Add the bin folder to your system PATH

macOS
bash
Copy

brew install poppler

Linux
bash
Copy

sudo apt-get install poppler-utils

🚀 Usage

    Run the application:

bash
Copy

python src/pdf_converter.py

    In the GUI:

        Click Browse PDF to select your PDF file

        Click Browse Folder to select output directory

        Click Convert to Images to start conversion

    Find your images in the output folder named page_001.png, page_002.png, etc.

🗺 Roadmap

    Add multi-PDF batch processing

    Support additional image formats (JPEG, TIFF)

    Implement PDF page range selection

    Add dark mode theme

    Create executable builds for all platforms

🤝 Contributing

We welcome contributions! Please follow these steps:

    Fork the repository

    Create your feature branch:

bash
Copy

git checkout -b feature/amazing-feature

    Commit your changes:

bash
Copy

git commit -m 'Add some amazing feature'

    Push to the branch:

bash
Copy

git push origin feature/amazing-feature

    Open a Pull Request

See CONTRIBUTING.md for detailed guidelines.
📜 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See LICENSE for more information.
🙏 Acknowledgements

    pdf2image - PDF conversion library

    Poppler - PDF rendering engine

    Tkinter - GUI framework

Tip: For large PDF files, consider increasing your system's temporary storage allocation. Conversion time depends on PDF complexity and system resources.