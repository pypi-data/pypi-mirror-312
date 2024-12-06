# AlphaFold3 Batch Predictions with `afusion.api`

## Introduction

This tutorial demonstrates how to use the `afusion.api` module to create batch tasks from a pandas DataFrame and run batch predictions using AlphaFold. We'll guide you through the entire process—from preparing your data to interpreting the results—using a minimal example with protein sequences.

**Prerequisites**:

- Python 3.10 or higher
- AlphaFold 3 installed and configured
- The `afusion` package installed
- Basic knowledge of Python and pandas

---

## 1. Import Necessary Modules

Begin by importing the required modules:

```python
import pandas as pd
from afusion.api import create_tasks_from_dataframe, run_batch_predictions
```

- **`pandas`**: Used for data manipulation and analysis.
- **`afusion.api`**: Contains the functions we'll use to create tasks and run predictions.

---

## 2. Prepare the Data

We'll create a pandas DataFrame containing the necessary information for our batch predictions. In this example, we'll predict the structure of a minimal protein sequence for two jobs.

```python
# Define the DataFrame for the test
data = {
    'job_name': ['TestJob1', 'TestJob1', 'TestJob2'],
    'type': ['protein', 'protein', 'protein'],
    'id': ['A', 'B', 'A'],  # Entity IDs
    'sequence': ['MVLSPADKTNVKAAW', 'MVLSPADKTNVKAAW', 'MVLSPADKTNVKAAW'],  # Protein sequences
    # No modifications or optional parameters in this example
}

df = pd.DataFrame(data)
```

Let's display the DataFrame to verify its contents:

```python
df
```

**Output**:

|    | job_name | type    | id   | sequence        |
|----|----------|---------|------|-----------------|
| 0  | TestJob1 | protein | A    | MVLSPADKTNVKAAW |
| 1  | TestJob1 | protein | B    | MVLSPADKTNVKAAW |
| 2  | TestJob2 | protein | A    | MVLSPADKTNVKAAW |

**Explanation**:

- **`job_name`**: Specifies the name of the job. `TestJob1` has two entities, while `TestJob2` has one.
- **`type`**: Indicates the entity type; all are proteins in this case.
- **`id`**: Identifier for each entity.
- **`sequence`**: The protein sequences to be predicted.

---

## 3. Create Tasks from the DataFrame

We will use the `create_tasks_from_dataframe` function to convert our DataFrame into a list of task dictionaries suitable for AlphaFold predictions.

```python
# Create tasks from DataFrame
tasks = create_tasks_from_dataframe(df)
```

This function processes the DataFrame and creates tasks based on the parameters provided.

Let's inspect the tasks generated:

```python
tasks
```

**Output**:

```python
[
    {
        'name': 'TestJob1',
        'modelSeeds': [1],
        'sequences': [
            {
                'protein': {
                    'sequence': 'MVLSPADKTNVKAAW',
                    'unpairedMsa': None,
                    'pairedMsa': None,
                    'templates': [],
                    'id': 'A'
                }
            },
            {
                'protein': {
                    'sequence': 'MVLSPADKTNVKAAW',
                    'unpairedMsa': None,
                    'pairedMsa': None,
                    'templates': [],
                    'id': 'B'
                }
            }
        ],
        'dialect': 'alphafold3',
        'version': 1
    },
    {
        'name': 'TestJob2',
        'modelSeeds': [1],
        'sequences': [
            {
                'protein': {
                    'sequence': 'MVLSPADKTNVKAAW',
                    'unpairedMsa': None,
                    'pairedMsa': None,
                    'templates': [],
                    'id': 'A'
                }
            }
        ],
        'dialect': 'alphafold3',
        'version': 1
    }
]
```

**Explanation**:

- **`name`**: Corresponds to `job_name` in the DataFrame.
- **`modelSeeds`**: List of model seeds; defaults to `[1]` if not specified.
- **`sequences`**: Contains the sequences and related data for each entity.
  - **`protein`**: Dictionary with the protein sequence and optional parameters.
    - **`sequence`**: The protein sequence.
    - **`unpairedMsa`, `pairedMsa`, `templates`**: Set to `None` or empty lists as we didn't specify them.
    - **`id`**: Entity ID.
- **`dialect`**: Specifies the AlphaFold version; set to `'alphafold3'`.
- **`version`**: Version number; set to `1`.

---

## 4. Configure Paths

Before running predictions, specify the input and output directories, as well as the locations of the model parameters and databases.

```python
# Path configurations (update these paths as needed)
af_input_base_path = "/path/to/af_input"
af_output_base_path = "/path/to/af_output"
model_parameters_dir = "/path/to/model_parameters"  # Update with the correct path
databases_dir = "/path/to/databases"                # Update with the correct path
```

**Note**: Replace `"/path/to/..."` with the actual paths on your system.

Ensure that the directories exist:

```python
import os

os.makedirs(af_input_base_path, exist_ok=True)
os.makedirs(af_output_base_path, exist_ok=True)
```

---

## 5. Run Batch Predictions

Now, run the batch predictions using the `run_batch_predictions` function.

```python
# Run batch predictions
results = run_batch_predictions(
    tasks=tasks,
    af_input_base_path=af_input_base_path,
    af_output_base_path=af_output_base_path,
    model_parameters_dir=model_parameters_dir,
    databases_dir=databases_dir,
    run_data_pipeline=False,  # Set to True to run the data pipeline
    run_inference=False,      # Set to True to run inference (requires GPU)
)
```

**Parameters**:

- **`tasks`**: The list of tasks generated from the DataFrame.
- **`af_input_base_path`**: Base directory for AlphaFold input files.
- **`af_output_base_path`**: Base directory for AlphaFold output files.
- **`model_parameters_dir`**: Directory containing the model parameters.
- **`databases_dir`**: Directory containing the required databases.
- **`run_data_pipeline`**: Whether to run the data pipeline (`True` or `False`).
- **`run_inference`**: Whether to run inference (`True` if you have a GPU).

**Important**: For this minimal test, we set `run_data_pipeline` and `run_inference` to `False`. In a real prediction scenario, you should set these to `True`.

---

## 6. Interpret the Results

After running the predictions, process and print the results:

```python
# Process and print results
for result in results:
    print(f"Job Name: {result['job_name']}")
    print(f"Output Folder: {result['output_folder']}")
    print(f"Status: {result['status']}")
    print("---")
```

**Sample Output**:

```
Job Name: TestJob1
Output Folder: /path/to/af_output
Status: Success
---
Job Name: TestJob2
Output Folder: /path/to/af_output
Status: Success
---
```

**Explanation**:

- **`job_name`**: The name of the job.
- **`output_folder`**: The directory where the output files are stored.
- **`status`**: The status of the prediction (`'Success'` or an error message).

---

## 7. Notes and Considerations

- **System Configuration**: This example was run on a system with the following configuration:
    - CPU: Xeon Silver 4410T
    - GPU: NVIDIA RTX 4090
    - Operating System: Ubuntu Server 24.04 LTS
   
     **Note**: Your hardware configuration can significantly affect the performance and runtime of AlphaFold predictions. Ensure that your system meets the necessary requirements, especially regarding GPU capabilities.

- **GPU Requirement**: AlphaFold predictions require substantial computational resources and are optimized for GPUs. Ensure that your system meets the hardware requirements if you plan to run actual predictions.

- **Database Availability**: The databases specified in `databases_dir` are essential for AlphaFold's operation. Make sure that you have downloaded and correctly configured all necessary databases.

- **Model Parameters**: The `model_parameters_dir` should contain the AlphaFold model parameters. Ensure that you have obtained these parameters and placed them in the specified directory.

- **Adjusting Parameters**: Depending on your use case, you may need to adjust additional parameters such as `model_seeds`, `msa_option`, and others. Refer to the `afusion.api` documentation for more details.

- **Error Handling**: The `run_batch_predictions` function returns a list of results with status messages. If any job fails, the status will contain the error message, which can be used for debugging.

---

## Conclusion

In this tutorial, we demonstrated how to use the `afusion.api` module to create batch tasks from a pandas DataFrame and run batch predictions using AlphaFold. By following these steps, you can streamline the process of setting up and executing multiple predictions, making it efficient to handle large-scale protein structure predictions.

---

## Additional Resources

- **AlphaFold GitHub Repository**: [https://github.com/deepmind/alphafold](https://github.com/deepmind/alphafold)

---

**Disclaimer**: Ensure that you comply with all licensing and usage terms when using AlphaFold and associated data.
