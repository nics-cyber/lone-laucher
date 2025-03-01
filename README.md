# Minecraft Launcher

A custom Minecraft launcher built with Python. This launcher supports cracked (offline) players, mods, shaders, resource packs, and more!

---

## Features

### 1. **Cracked (Offline) Support**
   - Play Minecraft without a premium account.
   - Generates a UUID for offline players.

### 2. **Mod Support**
   - Supports **Fabric** and **Forge** mod loaders.
   - Add and remove mods via the GUI.

### 3. **Shader Support**
   - Add and manage shaders for enhanced visuals.

### 4. **Resource Pack Management**
   - Add and enable/disable resource packs.

### 5. **Cosmetic Customization**
   - Add capes, wings, and emotes for personalization.

### 6. **Performance Optimization**
   - Includes JVM arguments for better performance.
   - Adjustable RAM allocation.

### 7. **Server Integration**
   - Connect to any Minecraft server (e.g., Hypixel, Mineplex).

### 8. **Real-Time Analytics**
   - Track FPS and ping in real-time (simulated for now).

### 9. **User-Friendly GUI**
   - Built with `tkinter` for ease of use.
   - Light and dark themes.

---

## How to Run

### Prerequisites
1. **Python 3.7 or higher**:
   - Download and install Python from [python.org](https://www.python.org/).
   - Make sure to check **"Add Python to PATH"** during installation.

2. **Required Libraries**:
   - Install the required Python libraries using `pip`:
     ```bash
     pip install requests ttkthemes psutil
     ```

### Steps to Run
1. **Download the Script**:
   - Clone this repository or download the `minecraft_launcher.py` file.

2. **Run the Script**:
   - Open a terminal (Command Prompt or PowerShell).
   - Navigate to the folder containing the script:
     ```bash
     cd path\to\your\folder
     ```
   - Run the script:
     ```bash
     python minecraft_launcher.py
     ```

3. **Use the Launcher**:
   - Enter your **username**.
   - Select the **Minecraft version**.
   - Configure settings like RAM allocation, mods, shaders, and resource packs.
   - Click **"Launch Minecraft"** to start the game.

---

## Advanced Features

### 1. **Real-Time Analytics Integration**
   - Track FPS and ping using Minecraft's debug screen or mods like OptiFine.

### 2. **Shader Pack Management**
   - Add and manage shaders for enhanced visuals.

### 3. **Resource Pack Management**
   - Enable/disable resource packs from the GUI.

### 4. **Cosmetic Customization**
   - Add capes, wings, and emotes for personalization.

### 5. **Cracked Support**
   - Play Minecraft without a premium account.

---

## Troubleshooting

### 1. **Python Not Found**
   - Ensure Python is added to your system PATH during installation.
   - Verify the installation by running:
     ```bash
     python --version
     ```

### 2. **Missing Libraries**
   - If you see an error like `ModuleNotFoundError`, install the required libraries:
     ```bash
     pip install requests ttkthemes psutil
     ```

### 3. **Minecraft Not Launching**
   - Ensure the correct Minecraft version is installed.
   - Make sure the `.minecraft` folder exists in your system's AppData directory.

---

## Contributing
Feel free to contribute to this project! Open an issue or submit a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author
[Your Name]  
[Your GitHub Profile](https://github.com/your-username)

---

Enjoy playing Minecraft with your custom launcher! 🚀
