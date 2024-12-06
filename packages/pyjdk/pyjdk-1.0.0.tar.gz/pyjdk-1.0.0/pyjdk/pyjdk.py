import os
import tarfile
import requests
import subprocess
import shutil
import logging

class PyJDK:
    def __init__(self, version=8, download_dir='jdk_download', extract_dir='jdk_extracted', logging_enabled=False):
        self.current_dir = os.getcwd()
        self.download_dir = os.path.join(self.current_dir, download_dir)
        self.extract_dir = os.path.join(self.current_dir, extract_dir)
        self.build_dir = os.path.join(self.current_dir, 'build')
        self.classes_dir = os.path.join(self.build_dir, 'classes')
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.extract_dir, exist_ok=True)
        os.makedirs(self.build_dir, exist_ok=True)
        self.version = version
        self.jdks = {
            8: {
                'url': 'https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u421/jdk/jdk-8u421-linux-x64.tar.gz',
                'path': 'jdk1.8.0_421'
            },
            11: {
                'url': 'https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java11/java11024/jdk-11.0.24_linux-x64_bin.tar.gz',
                'path': 'jdk-11.0.24'
            },
            17: {
                'url': 'https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java17/java17013/jdk-17.0.13_linux-x64_bin.tar.gz',
                'path': 'jdk-17.0.13'
            }
        }
        self.jdk_path = None
        self.logging_enabled = logging_enabled
        if self.logging_enabled:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.WARNING)
        self.download_jdk()

    def list_versions(self):
        logging.info("Available JDK versions:")
        for version in self.jdks.keys():
            status = 'Installed' if self.is_installed(version) else 'Not installed'
            logging.info(f"- JDK {version} [{status}]")

    def is_installed(self, version):
        if version in self.jdks:
            jdk_path = os.path.join(self.extract_dir, self.jdks[version]['path'])
            return os.path.exists(jdk_path)
        else:
            return False

    def download_jdk(self):
        if self.version in self.jdks:
            if self.is_installed(self.version):
                logging.info(f"JDK {self.version} is already installed.")
                self.jdk_path = os.path.join(self.extract_dir, self.jdks[self.version]['path'], 'bin')
                return
            url = self.jdks[self.version]['url']
            archive_name = f'jdk{self.version}.tar.gz'
            archive_path = os.path.join(self.download_dir, archive_name)
            if os.path.exists(archive_path):
                logging.info(f"Archive for JDK {self.version} is already downloaded.")
            else:
                logging.info(f"Downloading JDK {self.version} from {url}...")
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(archive_path, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    logging.info(f"JDK {self.version} successfully downloaded to {archive_path}.")
                else:
                    logging.error(f"Error downloading JDK {self.version}: {response.status_code}")
                    return
            self.extract_jdk(archive_path)
        else:
            logging.error(f"JDK version {self.version} is not available.")

    def extract_jdk(self, archive_path):
        logging.info(f"Extracting {archive_path} to {self.extract_dir}...")
        if tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(path=self.extract_dir)
            logging.info(f"Extraction of JDK {self.version} completed.")
            os.remove(archive_path)
            self.jdk_path = os.path.join(self.extract_dir, self.jdks[self.version]['path'], 'bin')
        else:
            logging.error(f"File {archive_path} is not a tar.gz archive.")

    def compile_code(self, java_file_path):
        javac = os.path.join(self.jdk_path, 'javac')
        os.makedirs(self.classes_dir, exist_ok=True)
        try:
            subprocess.run([javac, '-d', self.classes_dir, java_file_path], check=True)
            logging.info(f"Compilation of {java_file_path} completed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error compiling {java_file_path}: {e}")

    def pack_jar(self, main_class, jar_file_path):
        jar = os.path.join(self.jdk_path, 'jar')
        manifest_content = f'Main-Class: {main_class}\n'
        build_dir = os.path.dirname(jar_file_path)
        os.makedirs(build_dir, exist_ok=True)
        manifest_path = os.path.join(build_dir, 'MANIFEST.MF')
        with open(manifest_path, 'w') as f:
            f.write(manifest_content)
        try:
            subprocess.run([jar, 'cvmf', manifest_path, jar_file_path, '-C', self.classes_dir, '.'], check=True)
            logging.info(f"JAR file {jar_file_path} successfully created.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error creating JAR file {jar_file_path}: {e}")

    def run_jar(self, jar_path, args=None):
        java = os.path.join(self.jdk_path, 'java')
        cmd = [java, '-jar', jar_path]
        if args:
            cmd.extend(args)
        try:
            subprocess.run(cmd, check=True)
            logging.info(f"JAR file {jar_path} successfully run.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running JAR file {jar_path}: {e}")

    def cleanup(self):
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
            logging.info(f"Download directory {self.download_dir} deleted")
        if self.build_dir and os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
            logging.info(f"Build chache directory {self.build_dir} deleted")    
