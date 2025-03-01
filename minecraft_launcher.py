import os
import sys
import requests
import subprocess
import uuid
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from ttkthemes import ThemedTk
import psutil
import threading
import time
import zipfile

# Set the Minecraft directory based on the operating system
if sys.platform == "win32":
    # Windows
    MINECRAFT_DIR = os.path.join(os.getenv('APPDATA'), '.minecraft')
elif sys.platform == "darwin":
    # macOS
    MINECRAFT_DIR = os.path.expanduser('~/Library/Application Support/minecraft')
else:
    # Linux and other platforms
    MINECRAFT_DIR = os.path.expanduser('~/.minecraft')

# Ensure the directory exists
os.makedirs(MINECRAFT_DIR, exist_ok=True)

# Constants
VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest.json"
FABRIC_API_URL = "https://meta.fabricmc.net/v2/versions/loader/{version}"
FORGE_INSTALLER_URL = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"
COSMETIC_PACK_URL = "https://example.com/cosmetic-pack.zip"  # Replace with actual URL

# Utility Functions
def download_file(url, path):
    response = requests.get(url, stream=True)
    with open(path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def get_version_manifest():
    return requests.get(VERSION_MANIFEST_URL).json()

def download_version(version_id):
    manifest = get_version_manifest()
    for version in manifest['versions']:
        if version['id'] == version_id:
            version_data = requests.get(version['url']).json()
            jar_url = version_data['downloads']['client']['url']
            jar_path = os.path.join(MINECRAFT_DIR, 'versions', version_id, f'{version_id}.jar')
            os.makedirs(os.path.dirname(jar_path), exist_ok=True)
            download_file(jar_url, jar_path)
            return version_data
    raise Exception(f"Version {version_id} not found")

def generate_offline_uuid(username):
    return str(uuid.uuid3(uuid.NAMESPACE_OID, username))

def install_fabric(version_id):
    fabric_url = FABRIC_API_URL.format(version=version_id)
    fabric_data = requests.get(fabric_url).json()
    loader_version = fabric_data['loader']['version']
    installer_url = fabric_data['installer']['url']
    installer_path = os.path.join(MINECRAFT_DIR, 'fabric-installer.jar')
    download_file(installer_url, installer_path)
    subprocess.run(['java', '-jar', installer_path, 'client', '-dir', MINECRAFT_DIR, '-mcversion', version_id, '-loader', loader_version])

def install_forge(version_id):
    forge_url = FORGE_INSTALLER_URL.format(version=version_id)
    installer_path = os.path.join(MINECRAFT_DIR, 'forge-installer.jar')
    download_file(forge_url, installer_path)
    subprocess.run(['java', '-jar', installer_path, '--installClient'])

def download_cosmetic_pack():
    cosmetic_path = os.path.join(MINECRAFT_DIR, 'resourcepacks', 'cosmetic_pack.zip')
    os.makedirs(os.path.dirname(cosmetic_path), exist_ok=True)
    download_file(COSMETIC_PACK_URL, cosmetic_path)
    with zipfile.ZipFile(cosmetic_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(MINECRAFT_DIR, 'resourcepacks'))

# Launcher Class
class MinecraftLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Minecraft Launcher")
        self.root.geometry("800x700")

        # Variables
        self.username = tk.StringVar(value="Player")
        self.version_id = tk.StringVar(value="1.16.5")
        self.offline_mode = tk.BooleanVar(value=True)
        self.ram_allocation = tk.IntVar(value=2)
        self.mod_loader = tk.StringVar(value="None")
        self.server_ip = tk.StringVar(value="hypixel.net")
        self.mod_list = tk.StringVar(value="")
        self.theme = tk.StringVar(value="light")
        self.selected_mods = []
        self.selected_shaders = []
        self.selected_resource_packs = []
        self.selected_cosmetics = []

        # GUI Elements
        tk.Label(root, text="Username:").pack()
        tk.Entry(root, textvariable=self.username).pack()

        tk.Label(root, text="Minecraft Version:").pack()
        tk.Entry(root, textvariable=self.version_id).pack()

        tk.Checkbutton(root, text="Offline Mode", variable=self.offline_mode).pack()

        tk.Label(root, text="RAM Allocation (GB):").pack()
        tk.Scale(root, from_=1, to=8, variable=self.ram_allocation, orient=tk.HORIZONTAL).pack()

        tk.Label(root, text="Mod Loader:").pack()
        ttk.Combobox(root, textvariable=self.mod_loader, values=["None", "Fabric", "Forge"]).pack()

        tk.Label(root, text="Server IP:").pack()
        tk.Entry(root, textvariable=self.server_ip).pack()

        tk.Label(root, text="Mods:").pack()
        self.mod_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.mod_listbox.pack()
        tk.Button(root, text="Add Mod", command=self.add_mod).pack()
        tk.Button(root, text="Remove Mod", command=self.remove_mod).pack()

        tk.Label(root, text="Shaders:").pack()
        self.shader_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.shader_listbox.pack()
        tk.Button(root, text="Add Shader", command=self.add_shader).pack()
        tk.Button(root, text="Remove Shader", command=self.remove_shader).pack()

        tk.Label(root, text="Resource Packs:").pack()
        self.resource_pack_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.resource_pack_listbox.pack()
        tk.Button(root, text="Add Resource Pack", command=self.add_resource_pack).pack()
        tk.Button(root, text="Remove Resource Pack", command=self.remove_resource_pack).pack()

        tk.Label(root, text="Cosmetics:").pack()
        self.cosmetic_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.cosmetic_listbox.pack()
        tk.Button(root, text="Add Cosmetic", command=self.add_cosmetic).pack()
        tk.Button(root, text="Remove Cosmetic", command=self.remove_cosmetic).pack()

        tk.Label(root, text="Theme:").pack()
        ttk.Combobox(root, textvariable=self.theme, values=["light", "dark"]).pack()

        tk.Button(root, text="Download Cosmetic Pack", command=download_cosmetic_pack).pack()

        tk.Button(root, text="Launch Minecraft", command=self.launch_minecraft).pack()

        # Analytics
        self.fps_label = tk.Label(root, text="FPS: N/A")
        self.fps_label.pack()
        self.ping_label = tk.Label(root, text="Ping: N/A")
        self.ping_label.pack()

        # Start analytics thread
        self.analytics_thread = threading.Thread(target=self.update_analytics, daemon=True)
        self.analytics_thread.start()

    def add_mod(self):
        mod_path = filedialog.askopenfilename(filetypes=[("JAR Files", "*.jar")])
        if mod_path:
            self.selected_mods.append(mod_path)
            self.mod_listbox.insert(tk.END, os.path.basename(mod_path))

    def remove_mod(self):
        selected_indices = self.mod_listbox.curselection()
        for index in reversed(selected_indices):
            self.selected_mods.pop(index)
            self.mod_listbox.delete(index)

    def add_shader(self):
        shader_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
        if shader_path:
            self.selected_shaders.append(shader_path)
            self.shader_listbox.insert(tk.END, os.path.basename(shader_path))

    def remove_shader(self):
        selected_indices = self.shader_listbox.curselection()
        for index in reversed(selected_indices):
            self.selected_shaders.pop(index)
            self.shader_listbox.delete(index)

    def add_resource_pack(self):
        resource_pack_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
        if resource_pack_path:
            self.selected_resource_packs.append(resource_pack_path)
            self.resource_pack_listbox.insert(tk.END, os.path.basename(resource_pack_path))

    def remove_resource_pack(self):
        selected_indices = self.resource_pack_listbox.curselection()
        for index in reversed(selected_indices):
            self.selected_resource_packs.pop(index)
            self.resource_pack_listbox.delete(index)

    def add_cosmetic(self):
        cosmetic_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
        if cosmetic_path:
            self.selected_cosmetics.append(cosmetic_path)
            self.cosmetic_listbox.insert(tk.END, os.path.basename(cosmetic_path))

    def remove_cosmetic(self):
        selected_indices = self.cosmetic_listbox.curselection()
        for index in reversed(selected_indices):
            self.selected_cosmetics.pop(index)
            self.cosmetic_listbox.delete(index)

    def launch_minecraft(self):
        username = self.username.get()
        version_id = self.version_id.get()
        offline_mode = self.offline_mode.get()
        ram_allocation = self.ram_allocation.get()
        mod_loader = self.mod_loader.get()
        server_ip = self.server_ip.get()

        try:
            version_data = download_version(version_id)
            jar_path = os.path.join(MINECRAFT_DIR, 'versions', version_id, f'{version_id}.jar')

            if offline_mode:
                uuid_str = generate_offline_uuid(username)
                access_token = "0"
                user_type = "legacy"
            else:
                uuid_str = "authenticated_uuid"  # Replace with actual UUID from authentication
                access_token = "authenticated_token"  # Replace with actual token
                user_type = "mojang"

            # Install Mod Loader
            if mod_loader == "Fabric":
                install_fabric(version_id)
            elif mod_loader == "Forge":
                install_forge(version_id)

            # Add Selected Mods
            mods_dir = os.path.join(MINECRAFT_DIR, 'mods')
            os.makedirs(mods_dir, exist_ok=True)
            for mod in self.selected_mods:
                os.system(f'copy "{mod}" "{mods_dir}"')

            # Add Selected Shaders
            shaders_dir = os.path.join(MINECRAFT_DIR, 'shaderpacks')
            os.makedirs(shaders_dir, exist_ok=True)
            for shader in self.selected_shaders:
                os.system(f'copy "{shader}" "{shaders_dir}"')

            # Add Selected Resource Packs
            resource_packs_dir = os.path.join(MINECRAFT_DIR, 'resourcepacks')
            os.makedirs(resource_packs_dir, exist_ok=True)
            for resource_pack in self.selected_resource_packs:
                os.system(f'copy "{resource_pack}" "{resource_packs_dir}"')

            # Add Selected Cosmetics
            cosmetics_dir = os.path.join(MINECRAFT_DIR, 'cosmetics')
            os.makedirs(cosmetics_dir, exist_ok=True)
            for cosmetic in self.selected_cosmetics:
                os.system(f'copy "{cosmetic}" "{cosmetics_dir}"')

            # JVM Arguments
            jvm_args = [
                'java',
                f'-Xmx{ram_allocation}G',
                f'-Xms{ram_allocation}G',
                '-XX:+UseG1GC',
                '-XX:+UnlockExperimentalVMOptions',
                '-XX:MaxGCPauseMillis=100',
                '-XX:+DisableExplicitGC',
                '-XX:TargetSurvivorRatio=90',
                '-XX:G1NewSizePercent=50',
                '-XX:G1MaxNewSizePercent=80',
                '-XX:G1MixedGCLiveThresholdPercent=35',
                '-XX:+AlwaysPreTouch',
                '-XX:+ParallelRefProcEnabled',
                '-Dfml.ignorePatchDiscrepancies=true',
                '-Dfml.ignoreInvalidMinecraftCertificates=true',
                '-cp', jar_path,
                'net.minecraft.client.main.Main',
                '--username', username,
                '--version', version_id,
                '--gameDir', MINECRAFT_DIR,
                '--assetsDir', os.path.join(MINECRAFT_DIR, 'assets'),
                '--uuid', uuid_str,
                '--accessToken', access_token,
                '--userType', user_type,
                '--server', server_ip,
                '--port', '25565'
            ]

            subprocess.run(jvm_args)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_analytics(self):
        while True:
            # Simulate FPS and Ping (replace with actual tracking logic)
            fps = psutil.cpu_percent()  # Placeholder
            ping = psutil.net_io_counters().bytes_sent  # Placeholder
            self.fps_label.config(text=f"FPS: {fps}")
            self.ping_label.config(text=f"Ping: {ping}")
            self.root.update()
            time.sleep(1)

# Main Function
if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Use ttkthemes for better UI
    launcher = MinecraftLauncher(root)
    root.mainloop()
