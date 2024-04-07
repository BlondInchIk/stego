# Stego

A windows application for performing steganography.

Using algorithm:
1. S-UNIWARD

## Instructions

This program work with .bmp files to put text into them, and with .txt files to take input text from this file for steganography. 

To perform steganography you must select the input bmp file, the name of the output bmp file and the input txt file (the text from which will be embedded). Once you have selected the files, the logo will change to the image you selected (for preview). To start the program you need to press the green button - RUN. After launching, the program will freeze waiting for the execution result, and a console will open in the background where you can monitor the execution progress. After embedding, the console will close, and the execution time (~20 sec) will be written in the logs.

If you want to make de-steganography, then you just have to press the black button - RUN REVERSE. For convenience, the name of the input file is taken from the text field (the name of the output file when embedding).


![image](https://github.com/BlondInchIk/stego/assets/90390586/ab9322dc-2a51-4434-a317-f00f937f423f)


### Option 1

Clone the project

```bash
  git clone https://github.com/BlondInchIk/stego
```

Build .exe program:

```bash
  python setup.py build 
```

And run (... is your python version):

```bash
  run ./build/exe.win-amd64-.../main.exe
```

### Option 2

Download release from [https://github.com/BlondInchIk/stego/releases](https://github.com/BlondInchIk/stego/releases "releases")
And run the installer to install the program on your computer.
The installer creates a shortcut on the desktop
This program install Stego by default in: C:\Users\USER\AppData\Local\Programs\Stego\
If you want to remove the program, then run the installer again

## Screenshots


![image](https://github.com/BlondInchIk/stego/assets/90390586/bb0547a6-49de-4790-82ee-0f3df8be834a)


![image](https://github.com/BlondInchIk/stego/assets/90390586/b0f93ed5-c632-4fd7-a203-02a30d682dac)


![show](https://github.com/BlondInchIk/stego/assets/90390586/82494605-fa98-40f2-a43b-4e7f5c8e99f1)


