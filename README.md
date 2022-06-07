# Honest Mirror, Computer Version
The computer version of Honest Mirror ([also known as CHPE on github](https://github.com/huict/CHPE))

## Step-by-Step process
- The user opens the application
- The system shows a button to the user
- The user clicks on the button and selects the video they want to analyze
- The system takes the filepath of the video and starts taking frames
- The system takes each frame and puts them through the Tensorflow Posenet Neural Network
- The system uses the output of the Tensorflow Neural Network to find poses in the Feedback Neural Network
- The system returns de poses recognized during the analysis