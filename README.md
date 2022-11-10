# Honest Mirror, Computer Version
The computer version of Honest Mirror ([also known as CHPE on github](https://github.com/huict/CHPE))

## The Following technologies are used in this project:
- Python 3.10
- Tensorflow Posenet (to recognize a person)
- Self-created Neural Network (to determine the poses)
- PyQt5 (UI)
- cv2 (retrieving frames from video)
- Developed in PyCharm -> **Find Pycharm alternatives to avoid future problems regarding licensing etc.**

## To create an .exe file (so that everyone can access the application on their local computer) it's recommended to use [PyInstaller](https://pyinstaller.org/en/stable/)

## Step-by-Step process:
1. The user opens the application.
2. The system shows a button to the user.
3. The user clicks on the button and selects the video they want to analyze.
4. The system takes the filepath of the video and starts taking frames.
5. The system takes each frame and puts them through the Tensorflow Posenet Neural Network.
6. The system uses the output of the Tensorflow Neural Network to find poses in the Feedback Neural Network.
7. The system returns de poses recognized during the analysis.

## Step-by-step process in code:
1. The application starts in **Load.UI.py**, in the function *MainWindow()* (You boot up the application in this file).
2. The application creates a button that refers to function *OpenFile()* within the same file.
3. The application receives the filepath of the to-be analysed video and moves on to FrameFetching() in **Extract_Frames.py**.
4. The application creates timestamps and uses each timeframe to fetch a frame from a video with given attributes (dimensions/frames per second).
5. The application obtains a bitarray with the pixels of the frame and uses it as parameter in *PerformAnalysis()* in **PerformAnalysis.py**.
6. The application uses the bitarray to obtain seventeen keypoints on the body from the PoseNet neural network. 
7. The application converts the output of Posenet into an {1, 34} array in **Convert_Posenet_to_Person.py**, as this is required for the Feedback neural network. 
8. The application uses the Person to run the Feedback neural network back in *PerformAnalysis()*. 
9. The application stores the results of the Feedback neural network in an list.
10. The application returns to *OpenFile()* as the function is done. Now *CountPosesWindow()* can be called to display the results.
11. The application creates a window featuring the poses and how often they occured. Every pose found 10 or more time displays a full feedbackmessage, read from the textfile *Feedbackmessages(EN).txt* in the assets folder.
12. The application also creates a table with the results in more detail when pressed on the button. *ShowAllFeedbackWindow()* will be called for this.

## Current issues that need to be fixed:
- The feedback is currently not accurate. This is likely due to the Tensorflow results not lining up with the android version of Honest Mirror. After researching the cause, it has come to my attention that both applications insert different lists into Tensorflow. The mobile version creates a ByteBuffer with ~30.000 values, while the Windows version creates an bitarray featuring pixels with ~120.000 values. This problem requires more research, including an answer to the question *why* the android version uses byte shuffling. 

## MUST HAVES: Functionalities that must be added to the app:
- Greatly improve the UI, as this is only a PoC as of writing (October 2022). 
- Work with PyInstaller to create builds of the application.
- Create a progress bar that shows how much of the analysis has been done and how much is left.

## SHOULD HAVES: Functionalities that should be added to the app:
- Create the UI based on literature, like the results from the thesis on which this application is based. Consult the project leader for more information.
- A decent amount of the code considers the current 6 poses when building the results. If, eventually, more poses will be added, the application will have to add multiple lines of code to adjust to these poses. If possible, revamp these sections to make it more flexible to more poses. 
- Not everyone has a windows computer. Luckily PyInstaller is able to adapt to the OS of the computer and thus is able to create IOS and Linux versions of the application as well. However, PyInstaller can only do this when the computer on which the project runs is also from that same system. Figure out a way to use Virtual Machines and have the application work on all systems. 

## COULD HAVES: Functionalities that could be added to the app:
- Send generated feedback to an user's mail if requested. 
- Consider the ability to (locally) store information, so that the user can refer back to previous presentations.
