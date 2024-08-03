import os
import subprocess
import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser, Tree

class FileHandler:
    def __init__(self, file_path: str, doxyfile_path: str):
        self.file_path = file_path
        self.cpp_language = Language(tscpp.language())
        self.doxyfile_path = doxyfile_path
        self.bash_script = "run_doxygen.sh"

    def read_source_file(self) -> str:
        if self.file_path.endswith(".cpp"):
            source_code_file = open(self.file_path, "r", encoding="utf-8")
            return source_code_file.read()
        else: raise TypeError("File exception: the provided file is not a cpp file!")

    def generate_ast_from_source_code(self, source_code: str) -> Tree:
        parser = Parser(self.cpp_language)
        tree = parser.parse(bytes(source_code, "utf8"))
        return tree
    
    def set_up_doxyfile(self):
        # Check if Doxyfile exists
        if not os.path.exists(self.doxyfile_path):
            raise TypeError("File exception: the provided Doxfile could not be found!")

        with open(self.doxyfile_path, 'r') as file:
            doxyfile_content = file.readlines()

        # Modify the Doxyfile settings (if necessary)
        with open(self.doxyfile_path, 'w') as file:
            for line in doxyfile_content:
                if line.startswith("INPUT "):
                    line = f"INPUT = {self.file_path}\n"
                file.write(line)
    
    def run_doxygen(self):
        # Make the bash script executable
        os.chmod(self.bash_script, 0o755)

        # Run the bash script
        try:
            subprocess.run([f"./{self.bash_script}"], check=True)
            print("Doxygen documentation generation complete.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the Doxygen script: {e}")
        

            
