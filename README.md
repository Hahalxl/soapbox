# How to download

1. Open CMD and type this in

    ```bash
    cd ./desktop
    ```

    ```bash
    git clone https://github.com/Hahalxl/soapbox/
    ```

2. Open VScode and open file on desktop

3. Press that run code button ![image](https://github.com/user-attachments/assets/cca4968f-4591-48b4-b5a4-8b87afc0cf81)


4. Link: http://127.0.0.1:5000/

# How to Push Changes to GitHub

1. Make sure you’re in your project folder on your local machine:

    ```bash
    cd /path/to/your/project
    ```

2. Check if remote is set (should be already, but just to confirm):

    ```bash
    git remote -v
    ```

    You should see:

    ```
    origin  https://github.com/Hahalxl/PythonFlasking531.git (fetch)
    origin  https://github.com/Hahalxl/PythonFlasking531.git (push)
    ```

    If not set, add it:

    ```bash
    git remote add origin https://github.com/Hahalxl/PythonFlasking531.git
    ```

3. Stage all your changes:

    ```bash
    git add .
    ```

4. Commit your changes with a descriptive message:

    ```bash
    git commit -m "Describe what you changed"
    ```

5. Push changes to GitHub:

    If this is your first push on a new branch (usually `main`):

    ```bash
    git push -u origin main
    ```

    If you already pushed before, just:

    ```bash
    git push
    ```
# soapbox
