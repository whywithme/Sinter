# Sinter Archiver 🗃️

Sinter is a simple and convenient graphical archiver for Windows that supports `.sntr` and `.zip` formats. The program has a modern dark interface and allows you to easily create, open, add files, and unpack archives.

## ✨ Features

- 🖥️ Modern dark interface based on PyQt6
- 📁 Support for `.sntr` (native) and `.zip` formats
- ➕ Add files to an archive with protection against corruption
- ⬇️ Unpack all files in the archive
- 🗂️ Displaying archive contents in a table with sizes
- 🔗 Associating `.sntr` files with the program (via the installer)
- 🛡️ Secure work with archives via temporary files

## 📦 Installation

### Requirements
- Windows 7 or higher
- Python 3.8+ (if running from source code)
- Installed libraries: `PyQt6`

### Running from source code
1. Install Python 3.8+ from the [official website](https://python.org)
2. Install the necessary libraries:
```bash
   pip install PyQt6
```
3. Download or clone the repository
4. Run the program:
    ```bash
    python sinter.py
    ```

## 🚀 Usage

### Main interface buttons:
- **✨ New** — create a new archive
- **📂 Open** — open an existing archive (`.sntr` or `.zip`)
- **➕ Add file** — add files to the current archive
- **⬇️ Extract all** — unpack all files from the archive

### How to create an archive:
1. Click **“✨ New”**
2. Select a save location and specify a file name with the extension `.sntr` or `.zip`
3. Click **“Save”**

### How to add files to an archive:
1. Open the archive via **“📂 Open”**
2. Click **“➕ Add file”**
3. Select one or more files
4. Click **“Open”**

### How to unpack an archive:
1. Open the archive
2. Click **“⬇️ Extract all”**
3. Select a folder to unpack
4. Click **“Select folder”**

## ⚠️ Important information

- The program works **only on Windows**
- The `.sntr` format is technically a ZIP archive with a different extension
- **Administrator rights** are required for the association installer to work
- It is recommended to save archives in folders with full access (for example, “Documents”)

## 🛠️ Technical details

- The standard Python `zipfile` library is used to work with archives
- The interface is built on **PyQt6**
- File associations are registered via the Windows registry
- A secure method with a temporary copy of the archive is used when adding files

## 📄 License

The project is distributed under the MIT license. You are free to use, modify, and distribute the code

## 🤝 Support

If you find a bug or have suggestions for improvement, please create an issue in the project repository

---

**Note**: To run from the source code, you need to install PyQt6. If you do not trust executable files, it is recommended to run `sinter.py` directly



