
# **ALOHA Data Collection**

![Placeholder for Project Image](#)  

---

## **Overview**
ALOHA Data Collection is a Python-based application designed for seamless and efficient robotic data collection. This guide will help you set up the project, troubleshoot common issues, and get started with ease.

---

## **Pre-Installation Setup**

Before installing the application, complete the following setup:

1. **Install Miniconda:**
   Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for your operating system.

2. **Create a Virtual Environment:**
   Use Miniconda to create a virtual environment:
   ```bash
   conda create -n aloha_env python=3.10 -y
   conda activate aloha_env
   ```

3. **Install LeRobot from GitHub:**
   Clone and install the [LeRobot repository](https://github.com/huggingface/lerobot):
   ```bash
   git clone https://github.com/huggingface/lerobot.git
   cd lerobot && pip install .[intelrealsense,dynamixel]
   ```

4. **Set `LD_PRELOAD` for Compatibility:**
   Run the following command to resolve `MESA-LOADER` errors:
   ```bash
   export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
   ```

---

## **Installation**

You can install ALOHA Data Collection directly using `pip`:

```bash
pip install aloha_data_collection
```

---

## **Post-Installation Setup**

After installing the application, follow these steps for troubleshooting and debugging:

### **Troubleshooting `LeRobot` Integration**
If you encounter issues, refer to these solutions:

1. **Resolving OpenCV Camera Issues:**
   Uninstall the `opencv-python` package and reinstall it using Conda:
   ```bash
   pip uninstall opencv-python
   conda install -c conda-forge opencv=4.10.0
   ```

2. **Fixing Video Encoding Errors:**
   ```bash
   conda install -c conda-forge ffmpeg
   ```

3. **Resolving OpenGL Errors (`MESA-LOADER`):**
   Ensure that the correct drivers are installed and set the `LD_PRELOAD` variable as mentioned above.

---

## **Usage**

Once installed, you can run the application as follows:
```bash
aloha_data_collection
```

---

## **Placeholder for Image**

Add an image or diagram here to better illustrate the setup or functionality of ALOHA Data Collection.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
