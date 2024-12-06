import psutil
import os
import pynvml

def memory_usage():
    """
    Imprime la cantidad de memoria RAM utilizada por el proceso actual en megabytes (MB).

    Esta función utiliza la biblioteca `psutil` para acceder a la información del sistema, 
    específicamente al uso de memoria del proceso que está ejecutando el código. La memoria 
    utilizada se mide en bytes y se convierte a megabytes para una mejor legibilidad.

    Ejemplo:
        >>> obtener_uso_memoria()
        Uso de memoria: 120.35 MB
    """
    proceso = psutil.Process(os.getpid())
    memoria_en_mb = proceso.memory_info().rss / (1024 * 1024)
    print(f"Used Memory: {memoria_en_mb:.2f} MB")

def gpu_memory():
    """
    Displays the memory usage of the first GPU using NVIDIA's NVML (NVIDIA Management Library).

    This function initializes the NVML library, retrieves the memory usage statistics 
    (total, used, and free) for the first GPU (index 0), prints the results in MB, 
    and then shuts down the NVML library to release resources.

    Dependencies:
        - NVIDIA Management Library (pynvml)
        Install via: pip install nvidia-ml-py3

    Output:
        Prints:
        - Total GPU memory in MB
        - Used GPU memory in MB
        - Free GPU memory in MB

    Example:
        >>> gpu_memory()
        Total Memory: 16384.00 MB
        Used Memory: 2048.00 MB
        Free Memory: 14336.00 MB

    Notes:
        - Ensure that the NVIDIA drivers are installed and properly configured.
        - If there are multiple GPUs, this function will only display information for the first GPU.
        - Use `pynvml.nvmlDeviceGetHandleByIndex(<index>)` to retrieve stats for other GPUs.

    Raises:
        - pynvml.NVMLError: If NVML initialization or querying fails.

    """
    try:
        # Initialize NVML
        pynvml.nvmlInit()
        
        # Get handle for the first GPU (index 0)
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        
        # Retrieve memory info
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        print(f"Total Memory: {info.total / 1024**2:.2f} MB")
        print(f"Used Memory: {info.used / 1024**2:.2f} MB")
        print(f"Free Memory: {info.free / 1024**2:.2f} MB")
    except pynvml.NVMLError as e:
        print(f"Error accessing NVML: {e}")
    finally:
        # Shutdown NVML
        pynvml.nvmlShutdown()
