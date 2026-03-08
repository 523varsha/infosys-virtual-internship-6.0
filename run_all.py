import subprocess
import time

try:
    print('Starting server...')
    process = subprocess.Popen(['.\\venv\\Scripts\\python.exe', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)
    
    print('Running tests...')
    test_process = subprocess.run(['.\\venv\\Scripts\\python.exe', 'test_api.py'], capture_output=True, text=True)
    print('Test Output:')
    print(test_process.stdout)
    if test_process.stderr:
        print('Test Errors:', test_process.stderr)
finally:
    print('Killing server...')
    process.terminate()
