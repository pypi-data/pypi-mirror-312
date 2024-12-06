import importlib.resources
import numpy as np

def load_data(filename, folder='data'):
    """
    Load example data provided with the rnb-wavelet library.

    Parameters:
    ----------
    filename : The name of the file to load.
    folder : The folder where the data files are located. Defaults to 'data'.

    Returns:
    -------
    data : The loaded NumPy array.

    Raises:
    ------
    FileNotFoundError
        If the specified file does not exist in the folder.
    """
    try:
        with importlib.resources.path(f"rnb.{folder}", filename) as data_path:
            return np.load(data_path)
        
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filename}' was not found in the '{folder}' folder.")
        
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the file: {str(e)}")

def load_example_data(dataset_name='R37_N3.npz'):
    """
    Load a specified example data file.

    Parameters:
    ----------
    dataset_name : The name of the example dataset to load.

    Returns
    -------
    data : The loaded NumPy array.
    """
    # Metadata for datasets
    dataset_metadata = {
        'R37_N3.npz': "Loading data example extracted from the Atlas database (van Ellenrieder et al., 2019),"
                    "featuring intracranial sleep recordings from the hippocampal regions.",
    }

    if dataset_name not in dataset_metadata:
        raise ValueError(f"Dataset '{dataset_name}' is not available. Available datasets: {list(dataset_metadata.keys())}")


    print(f"{dataset_metadata[dataset_name]}")

    data = load_data(dataset_name)

    # Load and return the dataset
    return data['data_epochs'], data['fs'].flatten()

