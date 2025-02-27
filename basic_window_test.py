import subprocess

def test_subprocess():
    try:
        result = subprocess.run(["powershell", "-Command", "Write-Output 'Subprocess test success'"],
                                 capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Subprocess failed: {e.stderr}")

if __name__ == "__main__":
    test_subprocess()
