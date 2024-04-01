import customtkinter as ctk
from tkinter import filedialog
from frame_widgets import LeftImageButton, RightImageButton
import settings
import os
from PIL import Image, ImageTk


class Frame(ctk.CTkFrame):
    def __init__(self, parent, flag_fun, path, left_image, right_image, text, initial_image_path, initial_image_index):
        super().__init__(master=parent, fg_color=settings.BACKGROUND_COLOR)
        self.pack(expand=True, fill='both')
        self.flag_fun = flag_fun
        self.path = path
        self.left_image = left_image
        self.right_image = right_image
        self.image_index = initial_image_index
        self.image_ind = 0
        self.total_images = 0
        self.images = initial_image_path
        self.total_images = len(self.images)
        print(text)

        # image navigation
        header_frame = ctk.CTkFrame(self, fg_color=settings.BACKGROUND_COLOR)
        header_frame.grid(row=0, column=1, columnspan=3, sticky='ew')

        inner_frame = ctk.CTkFrame(header_frame)
        inner_frame.pack(expand=True)

        left_button_image = ctk.CTkImage(dark_image=Image.open(settings.left_image_button))
        left_button = LeftImageButton(parent=inner_frame, func=self.left_img, image=left_button_image)
        left_button.pack(pady=5, side='left')

        self.img_num_text = ctk.CTkLabel(inner_frame, text=' --/-- ')
        self.img_num_text.pack(pady=5, side='left')

        right_button_image = ctk.CTkImage(dark_image=Image.open(settings.right_image_button))
        right_button = RightImageButton(parent=inner_frame, func=self.right_img, image=right_button_image)
        right_button.pack(pady=5, side='left')

        # Vertical Frame on the Left
        left_vertical_frame = ctk.CTkFrame(self, fg_color='lightgrey', width=50)
        left_vertical_frame.grid(row=0, column=0, rowspan=2, sticky='ns', pady=10)

        inner_frame = ctk.CTkFrame(left_vertical_frame, fg_color='yellow')
        inner_frame.pack(expand=True)

        button1 = ctk.CTkButton(inner_frame, text='open', width=10, command=self.open_image)
        button1.pack(padx=2, pady=10)
        button2 = ctk.CTkButton(inner_frame, text='Edit', width=10, command=self.edit_flag)
        button2.pack(padx=2, pady=10)
        button3 = ctk.CTkButton(inner_frame, text='Button 3', width=10)
        button3.pack(padx=2, pady=10)

        # Canvas for Image Viewer
        self.canvas = ctk.CTkCanvas(self, bg=settings.BACKGROUND_COLOR, relief='ridge',
                         bd=0, highlightthickness=0)
        self.canvas.grid(row=1, column=1, columnspan=2, sticky='nsew', padx=1, pady=2)
        # self.canvas.bind('<Configure>', self.resize_image)
        self.canvas.bind('<Configure>', self.resize_image)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def open_image(self):
        # Open a file dialog to select a directory
        directory = filedialog.askdirectory()
        print('hit the')

        if directory:
            # Get a list of image files in the selected directory
            image_files = [file for file in os.listdir(directory) if
                           file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.jfif', '.bmp', '.tiff', '.ico'))]

            if image_files:
                # Load and store the images
                self.images.clear()

                for file in image_files:
                    # Construct the full file path
                    file_path = os.path.join(directory, file)
                    self.images.append(file_path)
        self.path(self.images)
        self.total_images = len(self.images)
        self.image_number(0)
        self.image_show()

    def edit_flag(self):
        self.flag_fun(True)
        print(self.images)

    def image_number(self, check):
        if check == 2:
            self.image_ind = self.image_index
        elif check > 0 and self.image_index < self.total_images-1:
            self.image_index += 1
            if self.image_index >= 0:
                self.image_ind = self.image_index
            else:
                self.image_ind = self.total_images + self.image_index
        elif check < 0 and -1*self.image_index < self.total_images-1:
            self.image_index -= 1
            if self.image_index >= 0:
                self.image_ind = self.image_index
            else:
                self.image_ind = self.total_images + self.image_index
        else:
            self.image_index = 0
            self.image_ind = 0
        self.img_num_text.configure(text=f' {str(self.image_ind + 1)} / {str(self.total_images)} ')

    '''
    def image_number(self, check):
        if check == 0:
            self.image_index = 0
        elif check > 0:
            self.image_index = min(self.image_index + 1, self.total_images - 1)
        elif check < 0:
            self.image_index = max(self.image_index - 1, 0)

        if self.image_index >= 0:
            self.image_ind = self.image_index
        else:
            self.image_ind = self.total_images + self.image_index

        self.img_num_text.configure(text=f' {str(self.image_ind + 1)} / {str(self.total_images)} ')
        '''

    def left_img(self):
        print('left image')
        self.image_number(-1)
        self.left_image(self.image_index)
        self.image_show()

    def right_img(self):
        print('right image')
        self.image_number(1)
        self.right_image(self.image_index)
        self.image_show()

    def image_show(self):
        print('image show')
        self.image = Image.open(self.images[self.image_index])
        self.image_ratio = self.image.size[0] / self.image.size[1]
        # self.imagetk = ImageTk.PhotoImage(self.image)

        # resize
        if self.canvas_ratio > self.image_ratio:
            self.image_height = int(self.event_height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(self.event_width)
            self.image_height = int(self.image_width / self.image_ratio)

        self.place_image()

    def resize_image(self, event):
        print(event)
        self.canvas_ratio = event.width / event.height

        # update canvas attributes
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.event_width = event.width
        self.event_height = event.height

        if self.images:
            self.image_number(2)
            self.image_show()


    def place_image(self):
        # place image
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)
