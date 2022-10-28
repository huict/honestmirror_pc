# Honest Mirror, Computer Version
The computer version of Honest Mirror ([also known as CHPE on github](https://github.com/huict/CHPE))

## The Following technologies are used in this project:
- Python 3.10
- Tensorflow Posenet (to recognize a person)
- Self-created Neural Network (to determine the poses)
- PyQt5 (UI)
- cv2 (retrieving frames from video)
- Developed in PyCharm

## To create an .exe file (so that everyone can access the application on their local computer) it's recommended to use [PyInstaller](https://pyinstaller.org/en/stable/)

## Step-by-Step process:
- The user opens the application
- The system shows a button to the user
- The user clicks on the button and selects the video they want to analyze
- The system takes the filepath of the video and starts taking frames
- The system takes each frame and puts them through the Tensorflow Posenet Neural Network
- The system uses the output of the Tensorflow Neural Network to find poses in the Feedback Neural Network
- The system returns de poses recognized during the analysis

## Current issues that need to be fixed:
- The feedback is currently not accurate. This is likely due to the Tensorflow results not lining up with the android version of Honest Mirror. After researching the cause, it has come to my attention that both applications insert different lists into Tensorflow. The mobile version creates a ByteBuffer with ~30.000 values, while the Windows version creates an bitarray featuring pixels with ~120.000 values. This problem requires more research, including an answer to the question *why* the android version uses byte shuffling. 

## MUST HAVES: Functionalities that must be added to the app:
- Greatly improve the UI, as this is only a PoC as of writing (October 2022). 
- Work with PyInstaller to create builds of the application.

## SHOULD HAVES: Functionalities that should be added to the app:
- Create the UI based on literature, like the results from the thesis on which this application is based. Consult the project leader for more information.
- A decent amount of the code considers the current 6 poses when building the results. If, eventually, more poses will be added, the application will have to add multiple lines of code to adjust to these poses. If possible, revamp these sections to make it more flexible to more poses. 
- Not everyone has a windows computer. Luckily PyInstaller is able to adapt to the OS of the computer and thus is able to create IOS and Linux versions of the application as well. However, PyInstaller can only do this when the computer on which the project runs is also from that same system. Figure out a way to use Virtual Machines and have the application work on all systems. 

## ## COULD HAVES: Functionalities that could be added to the app:
- Send generated feedback to an user's mail if requested. 
- Consider the ability to (locally) store information, so that the user can refer back to previous presentations.
