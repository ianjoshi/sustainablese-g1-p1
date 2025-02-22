from regex_engine_factory import RegexEngineFactory
import subprocess
import re
import os
from dotenv import load_dotenv

class RegexEnginesExecutor:

    engine_methods = {
        "engine_py": "run_python_engine",
        "engine_java": "run_java_engine",
        "engine_js": "run_javascript_engine",
        "engine_cpp": "run_boost_engine",
    }

    def __init__(self, regex_engine, corpus, pattern):
        self.regex_engine = regex_engine
        self.corpus = corpus
        self.pattern = pattern

    def setUp(self):
        self.factory = RegexEngineFactory(
            regular_expressions=[self.pattern],
            directory_to_store_engines="regex_engines",
            filepath_to_corpus=self.corpus
        )
        self.factory.create_engines()

    def tearDown(self):
        self.factory.destroy_engines()

    def run_python_engine(self):
        with open(self.corpus, "r") as file:
            content = file.read()
            matches = re.findall(self.pattern, content)
        return matches

    def run_java_engine(self):
        # Compile and start Java process
        subprocess.run(["javac", f"{self.factory.directory_to_store_engines}/RegexMatcher.java"])
        java_process = subprocess.Popen(
            ["java", "-cp", self.factory.directory_to_store_engines, "RegexMatcher"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # This makes communicate() use strings instead of bytes
        )
        
        # Wait for ready signal
        line = java_process.stdout.readline().strip()
        
        # Send start signal
        java_process.stdin.write("start\n")
        java_process.stdin.flush()
        
        # Read output until done
        output_lines = []
        while True:
            line = java_process.stdout.readline().strip()
            if line == "done":
                break
            if not line:
                # Check if there was an error
                error = java_process.stderr.read()
                if error:
                    break
            output_lines.append(line)
        
        return output_lines

    def run_javascript_engine(self):
        # Start Node.js process
        node_process = subprocess.Popen(
            ["node", f"{self.factory.directory_to_store_engines}/regex_matcher.js"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for ready signal
        line = node_process.stdout.readline().strip()
        
        # Send start signal
        node_process.stdin.write("start\n")
        node_process.stdin.flush()
        
        # Read output until done
        output_lines = []
        while True:
            line = node_process.stdout.readline().strip()
            if line == "done":
                break
            if not line:
                # Check if there was an error
                error = node_process.stderr.read()
                if error:
                    break
            output_lines.append(line)
        
        return output_lines

    def run_boost_engine(self):
        load_dotenv()
        boost_path = os.getenv("BOOST_PATH")
        if not boost_path:
            raise RuntimeError("BOOST_PATH environment variable not set.")
        
        # Print the directory contents to debug
        print("Checking library directory:")
        subprocess.run(["dir", f"{boost_path}/lib"], shell=True)
        
        compile_result = subprocess.run([
            "g++",
            f"{self.factory.directory_to_store_engines}/regex_matcher.cpp",
            "-o", f"{self.factory.directory_to_store_engines}/regex_matcher.exe",
            f"-I{boost_path}/include",
            f"-L{boost_path}/lib",
            "-Wl,-rpath," + boost_path + "/bin",
            "-lboost_regex-vc143-mt-x64-1_86",  # Exact library name without 'lib' prefix and '.dll.a' suffix
            "--verbose"
        ], capture_output=True, text=True)
        
        if compile_result.returncode != 0:
            print("Library path contents:")
            subprocess.run(["dir", f"{boost_path}/lib"], shell=True)
            raise RuntimeError(f"C++ compilation failed:\n{compile_result.stderr}")
        
        # Start C++ process
        cpp_process = subprocess.Popen(
            f"{self.factory.directory_to_store_engines}/regex_matcher.exe",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for ready signal
        line = cpp_process.stdout.readline().strip()
        
        # Send start signal
        cpp_process.stdin.write("start\n")
        cpp_process.stdin.flush()
        
        # Read output until done
        output_lines = []
        while True:
            line = cpp_process.stdout.readline().strip()
            if line == "done":
                break
            if not line:
                # Check if there was an error
                error = cpp_process.stderr.read()
                if error:
                    break
            output_lines.append(line)

        return output_lines