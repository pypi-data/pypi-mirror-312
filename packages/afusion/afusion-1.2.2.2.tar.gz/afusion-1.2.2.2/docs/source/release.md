# Release Notes

## v1.2.1 "Visualization Optimized" (Release Date: November 23, 2024)

### Improvements

- **Visualization Performance Optimization**: Enhanced the visualization module to improve rendering speed and reduce memory usage, enabling smoother analysis of large AlphaFold 3 output files.

- **Stability Improvements**: Addressed minor bugs and improved the stability of the visualization tools, ensuring a seamless user experience during structure analysis.


## v1.2.0 "Visualization & Analysis" (Release Date: November 21, 2024)

### New Features

- **Visualization Module**: Introduced a powerful visualization module for AlphaFold 3 results. Users can upload output files (e.g., `.pdb`, `.json`) to analyze predictions with detailed structure displays, customizable plots, and PDF report generation.

- **Integrated Visualization**: The visualization tools are now seamlessly integrated into the prediction GUI, allowing users to switch to the visualization tab immediately after predictions are complete.

- **Enhanced Output Analysis**: Added an automated AlphaFold 3 output analysis system that provides streamlined insights with customizable visualizations and detailed reports.

- **Batch Prediction API Improvements**: Updated the batch prediction API to support visualization integration and enhanced error handling.

## v1.1.2 "Guided Installation" (Release Date: November 21, 2024)

### New Features

- **Guided Installation**: Introduced a new GUI-based installer to simplify the installation process. Users can now easily set up the application through step-by-step guidance.

- **CLI Launch**: Added command-line interface support, allowing users to start the application or installation process directly from the command line using the `afusion` command.

---

Let me know if there's anything else I can help you with!
## v1.1.1 "Debug and Docs" (Release Date: November 20, 2024)

### New Features

- **Documentation Update**: Created and improved project documentation, providing more detailed usage guidance and API descriptions.

### Bug Fixes

- Resolved known issues, enhancing application stability and reliability.

---

## v1.1.0 "Console and API" (Release Date: November 19, 2024)

### New Features

- **Console Output**: Integrated console output functionality, allowing users to view the running process in real-time within the interface for easier tracking and debugging.
- **Batch Predictions API**: Added an API for AFusion, supporting batch predictions in Python scripts, increasing automation.

### Improvements

- **Performance Optimization**: Improved application performance and stability, enhancing user experience.
- **Interface Enhancements**: Made minor adjustments to the user interface for smoother and more user-friendly operation.

---

## v1.0.0 "Refactor" (Release Date: November 18, 2024)

### Overview

AFusion v1.0.0 has been officially released. This marks our first stable version, featuring a complete codebase refactor for improved performance and reliability.

### Installation

```bash
pip install afusion
```

### Run

```bash
afusion
```

### Features

- **Code Refactoring**: Comprehensive optimization of the codebase, improving maintainability and execution efficiency.
- **Stability Enhancements**: Fixed issues from previous versions, significantly enhancing application stability.

---

## v0.2.2 "Python Package" (Release Date: November 17, 2024)

### New Features

- **Released as a Python Package**: AFusion is now available as a Python package. Users can install and run it with a simple command, making it more convenient.

### Installation

```bash
pip install afusion
```

### Run

```bash
afusion
```

---

## v0.2.1 "Copies" (Release Date: November 16, 2024)

### New Features

- **Copy Number Specification**: Users can now specify the number of copies for each sequence/entity, making it easy to create multiple copies of a sequence. Each copy can be assigned a unique ID, providing greater flexibility when setting up simulations.
- **Enhanced ID Handling**: Maintained the original functionality where multiple IDs can be specified separated by commas (e.g., `A,B`), while adding the option to explicitly specify the number of copies, offering more customization possibilities.

### Improvements

- **User Interface Improvements**: Optimized the interface design to make the application more intuitive and user-friendly.
- **Performance Enhancements**: Fixed minor issues to enhance stability and performance.

---

## v0.2.0 "New Features" (Release Date: November 15, 2024)

### New Features

1. **Run Completion Detection**

   - **Automatic Success Check**: After running AlphaFold 3, the application now automatically checks whether the prediction completed successfully.
   - **Output Folder Verification**: Verifies the existence of the output directory named after your job (based on the name field in your input) to ensure results are generated.
   - **User Feedback**: Upon successful completion, a confirmation message is displayed along with the path to the results.

2. **Download Results as ZIP**

   - **In-App Download Option**: Users can now download the prediction results directly from the app without needing to access the server filesystem.
   - **Automatic Compression**: Compresses the output folder into a ZIP file for quick and efficient downloads.
   - **Seamless Integration**: The download button appears immediately after a successful run, streamlining the workflow.

### Important Notes

- **Ensure Correct Paths**: Before running, double-check that all directory paths in the execution settings are accurate and accessible by the application.
- **Docker Requirements**: The application runs AlphaFold 3 within a Docker container. Ensure that Docker and AlphaFold 3 are installed and properly configured on your system.
- **Permissions**: The application needs appropriate permissions to read and write to the specified directories.

---

## v0.1.1 "Flag Bucket" (Release Date: November 14, 2024)

### New Features

- **Compilation Buckets Configuration**

  - **Custom Bucket Sizes**: AFusion now supports specifying custom compilation bucket sizes introduced in AlphaFold 3. Users can define bucket sizes that match the input sequence lengths, reducing unnecessary model recompilations and improving performance.
  - **Usage**:
    1. **Enable Custom Buckets**: In the "AlphaFold 3 Execution Settings" section, check the "Specify Custom Compilation Buckets" option.
    2. **Input Bucket Sizes**: Provide a list of bucket sizes separated by commas in the "Bucket Sizes (comma-separated)" field, e.g., `256,512,768,1024`.
    3. **Run**: Review the generated Docker command to confirm it includes the `--buckets` flag, then click "Run AlphaFold 3 Now" to execute the prediction.
  - **Benefits**:
    - **Performance Optimization**: Matching bucket sizes to input sequences minimizes padding and reduces the number of model recompilations.
    - **Flexibility**: Customize bucket sizes to handle a diverse range of input lengths, ensuring efficient processing.

### Improvements

- **User Interface Updates**: Adjusted the execution settings section to include the new compilation buckets configuration in an intuitive manner. Provided helpful tooltips and validation messages to guide users through the new settings.

---

## v0.1.0 "First Release" (Release Date: November 13, 2024)

### Overview

AFusion v0.1.0 has been released, providing a user-friendly graphical interface for AlphaFold 3. It simplifies the prediction process, making it accessible to users who are not familiar with command-line interactions.

### Features

- **Intuitive Interface**: Easily configure job settings, sequences, and execution parameters through a clean and modern GUI.
- **Entity Management**: Add multiple entities (Protein, RNA, DNA, Ligand) with support for modifications, MSA options, and templates.
- **Dynamic JSON Generation**: Automatically generates the required JSON input file for AlphaFold 3 based on user inputs.
- **Integrated Execution**: Run AlphaFold 3 directly from the GUI with customizable Docker execution settings.

---
