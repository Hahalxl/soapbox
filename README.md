# How to download

1. Open CMD and type this in

    ```bash
    git clone https://github.com/Hahalxl/PythonFlasking531/
    ```

2. Open VScode

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
