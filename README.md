# **CFHelp**

CFHelp is a command-line utility to manage Codeforces problem sets and solutions. It offers functionalities such as adding problems, testing solutions against sample test cases, updating compiler values, submitting solutions, seeing status of solution and retrieving compiler details.


## **Features**

- **Add Problem:** Adds a problem and creates a solution file based on the problem ID. The solution file name is a combination of the problem ID and the problem title, eliminating the need to provide the problem ID during testing or submission.
- **Test Solution:** Tests a solution file against sample test cases which are locally downloaded when we add the problem. We can only test those solution whose sample tests are downloaded locally using our command line utility add-problem funtion. 
- **Submit solution:** Submit a solution for a problem using one command line either by providing problem Id or if file is made by our cfhelp command it will automatically detect problem Id from solution file name itself.


## **Prerequisites (Linux OS)**

Before using this tool on Linux, ensure you have:

- Python installed on your system.
- A valid Codeforces account.
- Internet connectivity for submitting solutions.

## **Installation**

- **Clone the Repository**

    Clone the project repository to your local machine:

    ```bash
        https://github.com/lleviackermann/cfhelp.git
        cd cfhelp
    ```
   
- **Setup Environment Variables**

    Setup all the three environments variables.

    ```bash
        USERNAME=your_codeforces_username
        PASSWORD=your_codeforces_password
        DEFAULT_COMPILER_VALUE=default_compiler_value
    ```
    Replace your_codeforces_username, your_codeforces_password, and     default_compiler_value with your actual Codeforces credentials and default compiler value. You can also check .sample.env file. You can find all the compilers values and details in compiler_details.txt file or check out the usage section.

After completing these steps, ensure you add the cloned directory path to your `$PATH` variable on Linux. The process to do this is explained step-by-step in the next section, `Adding to PATH`. This is necessary for the `cfhelp` command to function correctly.

## **Adding to PATH**

To run the project commands from anywhere on your system, add the project directory to your $PATH variable.

-  **Copy the project directory path:**

    ```bash
        pwd
    ```
    Copy the output path.

-  **Edit `.bashrc` file:**

    Open the .bashrc file in a text editor:
    ```bash
        nano ~/.bashrc
    ```

- **Add the project directory to `$PATH`:**

    Add the following line at the end of the .bashrc file:
    ```bash
        export PATH="/path/to/your/project/directory:$PATH"
    ```
    Replace `/path/to/your/project/directory` with the path you copied.

- **Reload `.bashrc`:**

    Apply the changes by reloading the .bashrc file:
    ```bash
        source ~/.bashrc
    ```

Now, after doing all this we can use our command line funtions from anywhere in your laptop.


## **Usage**

To use the CFHelp utility, you need to provide specific commands and arguments as detailed below:

### **Adding a Problem**
To add a problem, use the following command:

``` bash
    cfhelp add-problem <codeforces_problem_id> [--ext=<programming_language>]
```
**Required argument:**
- `<problem_id>`: Unique identifier for the problem on the codeforces platform.

**Optional arguments:**
- `--ext=<programming_language>`: Specify the programming language for the solution (defaults to "cpp"). Currently only C and CPP are supported. More languages are coming soon.

### **Testing a Solution**
To test a solution, use the following command:

```bash
    cfhelp test <solution_file_name>
```
**Required argument:**
- `<solution_file_name>`: Path to the solution file.

### **Submitting a Solution**
To submit a solution on codeforces, use the following command:

```bash
    cfhelp submit <solution_file_name> [--pId=<problemId>] [--cVal=<compiler_value>]
```
**Required argument:**
- `<solution_file_name>`: Name of your solution file.

**Optional arguments:**

- `--pId=<problemId>`: Specify the problem ID if it's different from the filename.
- `--cVal=<compiler_value>`: Specify the compiler value (an integer).


### **Getting Compilers Values**
To get the list of compilers available on codeforces and their values, use the following command:

```bash
    cfhelp get compiler-details
```

### **Updating compilers values** 
To update the file `compiler_details.txt` if in future codeforces changes or added more compilers, use the following command:

```bash
    cfhelp update-compilers
```


## **Authors**

- [@lleviackermann](https://www.github.com/lleviackermann)


## **Feedback**

For any questions or feedback, please reach out to me at supritkumar30@gmail.com.

