
## **prpip**
**Reconstruct pupil size during blinks in eye-tracking data** with a physiologically inspired approach.

### **Features**
- Automatically detects blink intervals in eye-tracking data.
- Reconstructs pupil size during blinks using:
  - **Logarithmic recovery** with dynamic adjustment of the recovery time constant (\(\tau\)).
  - Incorporates **Gaussian noise** to mimic natural variability in pupil size measurements.
- Validates input data to ensure compatibility and provides clear error messages for invalid inputs.
- Supports multiple input formats: CSV, Excel, JSON, Parquet, and TXT.
- Flexible output:
  - Add a new column for reconstructed data.
  - Replace the original pupil size column with reconstructed values.

---

## **Changelog**

<details>
  <summary>See the Changes in versions</summary>

### **Version 0.0.post1**
- Initial release of `prpip`.
- Implemented logarithmic recovery for long blinks and linear blending for short blinks.
- Added stochastic variability to mimic natural pupil fluctuations.
- Supported batch processing of datasets and individual trials.

### **Version 1.1.0dev1 - Pre-Release**
- Enhanced noise scaling for long-blink reconstructions.
- Added advanced parameter customization (`tau`, `noise_scale`).
- Improved boundary smoothing for blink transitions.

### **Version 1.2.1**
- Introduced additional output format options.
- Optimized performance for large datasets.

### **Version 1.2.3**
- Added a check in `detect_blinks` to print a message when no blinks are detected in the trial data.
- Improved handling of floating-point time indices during pupil reconstruction, ensuring compatibility with non-integer time formats.
- Fixed minor bugs related to batch processing of trials.
- Improved error messages for invalid inputs, making debugging easier for users.

### **Version 1.3.0**
- Unified reconstruction method: removed distinctions between short and long blinks.
- Added support for multiple file formats: CSV, Excel, JSON, TXT, and Parquet.
- Incorporated comprehensive input validation to ensure consistent and robust data processing.
- Enhanced the Gaussian noise model for more realistic reconstruction.
- Optimized compatibility with `pandas` and modern data workflows.

</details>

---

### **Installation**
Install the latest version of `prpip` from PyPI:

```bash
pip install prpip
```

---

### **Quick Start**

#### **1. Import the Package**
```python
from prpip import process_pupil
```

#### **2. Process an Entire Dataset**
```python
import pandas as pd

data = pd.read_csv("input.csv")
processed_data = process_pupil(data)
processed_data.to_csv("reconstructed.csv", index=False)
```

#### **3. Process Data from Other Formats**
```python
processed_data = process_pupil("input.parquet")
processed_data.to_excel("reconstructed.xlsx", index=False)
```

#### **4. Plot the Results**
```python
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))
plt.plot(processed_data['Trial Time'], processed_data['Pupil Size'], label='Original Pupil Size (with Blinks)', alpha=0.6)
plt.plot(processed_data['Trial Time'], processed_data['Reconstructed Pupil Size'], label='Reconstructed Pupil Size', linestyle='--')
plt.xlabel('Time (ms)', fontsize=14)
plt.ylabel('Pupil Size (AU)', fontsize=14)
plt.title('Original vs Reconstructed Pupil Size', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
```

---

### **Input Requirements**
The input data must be in one of the following formats: CSV, Excel, JSON, TXT, or Parquet. It should contain the following columns:
- **`Trial`**: Identifies the trial number.
- **`Pupil Size`**: The measured pupil size.

### **Output**
The output DataFrame includes a new column:
- **`Reconstructed Pupil Size`**: Contains the reconstructed values during blinks.

Alternatively, you can replace the original `Pupil Size` column with the reconstructed values.

---

### **Advanced Parameters**
You can customize reconstruction behavior by adjusting the following optional parameters:

- **`blink_threshold`**:
  Threshold for detecting blinks. Default is `1000`.

- **`tau_base`**:
  Base recovery time constant for logarithmic reconstruction. Default is `50`.

- **`noise_scale`**:
  Scale of Gaussian noise added to reconstructions. Default is `0.05`.

#### Example:
```python
processed_data = process_pupil(
    "input.json",
    blink_threshold=1200,
    tau_base=60,
    noise_scale=0.1
)
```

---

### **License**
This project is licensed under the **MIT License**.

---

### **Contributing**
We welcome contributions! To contribute:
1. Fork the repository on GitHub.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request.

---

### **Author**
- **Mohammad Ahsan Khodami**
- Email: [ahsan.khodami@gmail.com](mailto:ahsan.khodami@gmail.com)
- GitHub: [AhsanKhodami](https://github.com/AhsanKhodami)

---

### **Example Input and Output**
#### **Input:**
| Trial | Trial Time | Pupil Size |
|-------|------------|------------|
| 1     | 0          | 4500       |
| 1     | 10         | 0          |
| 1     | 20         | 0          |
| 1     | 30         | 4800       |

#### **Output:**
| Trial | Trial Time | Pupil Size | Reconstructed Pupil Size |
|-------|------------|------------|--------------------------|
| 1     | 0          | 4500       | 4500                    |
| 1     | 10         | 0          | 4600                    |
| 1     | 20         | 0          | 4700                    |
| 1     | 30         | 4800       | 4800                    |
```

### Key Updates:
1. **Unified Methodology**: Removed references to distinct handling of short and long blinks.
2. **File Format Support**: Added examples and documentation for processing multiple file formats.
3. **Gaussian Noise Model**: Clarified the enhanced noise integration process.
4. **Updated Changelog**: Documented the new features added in version `1.3.0`.
