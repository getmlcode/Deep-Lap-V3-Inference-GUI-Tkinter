from matplotlib import pyplot as plt
from tkinter import *
from PIL import Image , ImageTk
from tkinter import filedialog
import tensorflow as tf

mainWindow = Tk()
sess = tf.Session()
class deepLabV3_GUI:
    TestImage = []
    SegmentedImage = []
    def __init__(self,master):
        master.title('Semantic Segmentation : Deep Lab V3')
        master.minsize(200, 200)

        #Setting Up Test Image Panel

        self.testImgFrame = Frame(master,highlightbackground="red",
                             width=300,height=300,
                             highlightthickness=1).\
                                 grid(row=0,column=0,padx=2,pady=2)

        self.testImgLabel = Label(self.testImgFrame,
                                  image = self.TestImage,
                                  text = 'Test Image Will Be Loaded Here',
                                  relief=SUNKEN)
        self.testImgLabel.grid(row=0,column=0)

        self.loadtestImg = Button(self.testImgFrame,
                                  text='Load Test Image', 
                                  command=self.loadTestImage).\
                                       grid(row=1, column=0,sticky=W,padx=2,pady=2)


        #Setting Up Segmented Image Panel

        self.userCommandsFrame = Frame(master,highlightbackground="blue",
                                  width=300,height=300,
                                  highlightthickness=1).\
                                      grid(row=0,column=1,sticky=E,padx=2,pady=2)

        self.segmentedImgLabel = Label(self.userCommandsFrame,
                                       image = self.SegmentedImage,
                                       text = 'Segmented Image Will Be Displayed Here',
                                       relief=SUNKEN)
        self.segmentedImgLabel.grid(row=0,column=1)

        self.setModelDirectory = Button(self.userCommandsFrame,
                                           text='Model Directory',
                                           state=DISABLED,
                                           command=self.setModelDirectory)
        self.setModelDirectory.grid(row=1, column=1,sticky=W,padx=2,pady=2)

        self.segmentTestImage = Button(self.userCommandsFrame,
                                           text='Segment Test Image',
                                           state=DISABLED,
                                           command=self.segmentImage)
        self.segmentTestImage.grid(row=2, column=1,sticky=W,padx=2,pady=2)                                      


        #Quit Button
        self.quitButton = Button(self.userCommandsFrame,
                                 text='Quit',
                                 command=master.destroy).\
                                     grid(row=3, column=1, sticky=W,padx=2,pady=2)


    def setModelDirectory(self):
        modelDir = filedialog.askdirectory()
        from semanticSegmentation import deepLabV3_InferenceEngine
        self.deepLab = deepLabV3_InferenceEngine(modelDir,sess)
        print('Deeplab Inference Object Created')
        self.segmentTestImage['state'] = NORMAL
    
    def loadTestImage(self):
        path=filedialog.askopenfilename(filetypes=[("Image Format",'.jpg'),("Image Format",'.png')])
        self.TestImage = Image.open(path)
        tkimage = ImageTk.PhotoImage(self.TestImage)
        self.testImgLabel.configure(image=tkimage)
        self.testImgLabel.image=tkimage
        self.testImgLabel.grid(row=0,column=0)
        self.setModelDirectory['state'] = NORMAL

    def segmentImage(self):
        self.SegmentedImage = self.deepLab.segmentImage(self.TestImage)

        #This produces a blacked out image , need to chek why !
        tkimage = ImageTk.PhotoImage(Image.fromarray(self.SegmentedImage.astype('uint8')))
        self.segmentedImgLabel.configure(image=tkimage)
        self.segmentedImgLabel.image = tkimage
        self.segmentedImgLabel.grid(row=0,column=1)

        #This displays correct segmented image
        plt.imshow(self.SegmentedImage)
        plt.show()
        
        
        
        
        
        
        
        
        
        
        
        



            
deepLabV3 = deepLabV3_GUI(mainWindow)
mainWindow.mainloop()