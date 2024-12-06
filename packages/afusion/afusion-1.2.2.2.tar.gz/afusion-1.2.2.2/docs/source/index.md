# 🔬 AFusion: AlphaFold 3 GUI & Toolkit

![image](https://github.com/user-attachments/assets/d1d894c7-c0cc-4218-9677-1917c1ad7b88)

## Introduction
**AFusion** is a user-friendly graphical interface designed to simplify AlphaFold 3 usage, making advanced protein structure modeling accessible to everyone. Whether you prefer a GUI over command-line interactions or need an API for batch predictions, AFusion has you covered.

[**Demo Site**](https://af3gui.streamlit.app/) *(generates input JSON files ONLY)*

[**Usable visualization site**](https://af3vis.streamlit.app/) *(fully usable)*

## Features

- **🧭 Guided Installation**: GUI-based installer to simplify the installation process, easily set up the application through step-by-step guidance.
- **✨ Intuitive Interface**: Easily configure job settings, sequences, and execution parameters through a clean and modern GUI.
- **📋 Entity Management**: Add multiple entities (Protein, RNA, DNA, Ligand) with support for modifications, MSA options, and templates.
- **⚙️  Dynamic JSON Generation**: Automatically generates the required JSON input file for AlphaFold 3 based on user inputs.
- **🚀 Integrated Execution**: Run AlphaFold 3 directly from the GUI with customizable Docker execution settings.
- **🖥️ Visual Feedback**: Provides command output within the interface for monitoring and debugging.
- **🖥️ Console Output**: Track processes and debug more effectively with backend console output.
- **🧩 API for Batch Predictions**: Perform batch predictions using the AFusion API in Python scripts.

### **🌟 New Feature!**
- **AlphaFold 3 Output Analysis System**: Automatically analyze and visualize results with customizable visualizations and generate detailed PDF reports for streamlined insights.

## Acknowledgements

- **AlphaFold 3**: This GUI is designed to work with [AlphaFold 3](https://github.com/google-deepmind/alphafold3) by DeepMind.
- **Streamlit**: AFusion is built using [Streamlit](https://streamlit.io/), an open-source app framework for machine learning and data science teams.
- **Contributors**: Waiting for more!

```{toctree}
:caption: Contents
:maxdepth: 1

installation
tutorial
api
release
```
---

If you encounter any issues or have suggestions for improvements, please open an [issue](https://github.com/Hanziwww/AlphaFold3-GUI/issues) or submit a [pull request](https://github.com/Hanziwww/AlphaFold3-GUI/pulls).

Happy Folding! 🧬
