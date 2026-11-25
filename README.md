## Requirements
Make sure that the following software is present and properly configured in your system.
1. **Python 3**
2. **Java JDK 17**
3. **Android SDK Platform Tools (ADB):** make sure to add it also to your system PATH
4. On your Android device: **Magisk** and **LSPosed**

## Installation
Clone the repository:
```bash
git clone https://github.com/LorenzoCorbinelli/C2S.git
```

## Usage
1. Specify the methods/constructors to hook inside the `src/main/res/raw/hooks.json` file.
   
   For each JSON entry (which specifies a method or constructor to hook), you need to provide the class name, the method name (only for methods), and the list of parameter types, if any.

   For example, if you want to hook method `m` of class `com.example.A`, which takes an `int`, a `char[]`, and a `String` as arguments, you should add an entry like this:
   ```
   {
    "className": "com.example.A",
    "methodName": "m",
    "parametersType": ["int", "char[]", "java.lang.String"]
   }
   ```
   For a constructor of the same class that takes no arguments, you simply need to specify:
   ```
   {
    "className": "com.example.A",
    "parametersType": []
   }
   ```
2. Run the installer to compile and install the module on the connected Android device:
   ```bash
   python install.py
   ```
    **Important:** Every time you modify the `hooks.json` file you must run the installer (`python install.py`) again to update the module.
  
3. Enable the module through LSPosed and select the target app.
4. The slice is printed to Logcat: you can filter the logs directly using the `LSPosedLog` tag, and `LSPosedDebug` tag to check for any module-related errors.
