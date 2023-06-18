import pygame
import math
from pygame.locals import *
from gui_form import Form
from gui_button import Button
from gui_textbox import TextBox
from gui_progressbar import ProgressBar
from gui_graph import Graph
from gui_label import Label
from constantes import *


class FormMenuC(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)

        self.boton1 = Button(master=self,x=0,y=150,w=200,h=40,color_background=C_GREEEN_2,color_border=C_YELLOW_2,on_click=self.on_click_boton1,on_click_param="form_menu_A",text="BACK",font="Verdana",font_size=30,font_color=C_BLACK)
        self.boton2 = Button(master=self,x=0,y=200,w=200,h=40,color_background=C_PINK,color_border=C_RED,on_click=self.on_click_boton2,on_click_param="",text="CARGAR XY",font="Verdana",font_size=30,font_color=C_BLACK)
        self.boton3 = Button(master=self,x=0,y=250,w=200,h=40,color_background=C_PINK,color_border=C_RED,on_click=self.on_click_boton3,on_click_param="",text="ROTAR DE",font="Verdana",font_size=30,font_color=C_BLACK)
        self.boton4 = Button(master=self,x=0,y=300,w=200,h=40,color_background=C_PINK,color_border=C_RED,on_click=self.on_click_boton4,on_click_param="",text="-",font="Verdana",font_size=30,font_color=C_BLACK)
        
        self.graph1 = Graph(master=self,x=400,y=0,w=500,h=500,color_background=C_BLACK,color_border=C_RED)
       
        self.label_xy0 = Label(master=self,x=0,y=50,w=60,h=40,color_background=C_BLACK,color_border=C_BLUE,image_background=None,text="X0 Y0",font="Verdana",font_size=20,font_color=C_WHITE)
        self.txt_x0 = TextBox(master=self,x=70,y=50,w=100,h=40,color_background=C_BLACK,color_border=C_BLUE,image_background=None,text="0",font="Verdana",font_size=30,font_color=C_WHITE)
        self.txt_y0 = TextBox(master=self,x=180,y=50,w=100,h=40,color_background=C_BLACK,color_border=C_BLUE,image_background=None,text="0",font="Verdana",font_size=30,font_color=C_WHITE)
        
        self.label_xy1 = Label(master=self,x=0,y=100,w=60,h=40,color_background=C_BLACK,color_border=C_RED,image_background=None,text="X1 Y1",font="Verdana",font_size=20,font_color=C_WHITE)
        self.txt_x1 = TextBox(master=self,x=70,y=100,w=100,h=40,color_background=C_BLACK,color_border=C_RED,image_background=None,text="100",font="Verdana",font_size=30,font_color=C_WHITE)
        self.txt_y1 = TextBox(master=self,x=180,y=100,w=100,h=40,color_background=C_BLACK,color_border=C_RED,image_background=None,text="100",font="Verdana",font_size=30,font_color=C_WHITE)
         
        self.label_angulo = Label(master=self,x=0,y=350,w=60,h=40,color_background=C_BLACK,color_border=C_BLUE,image_background=None,text="ANG",font="Verdana",font_size=20,font_color=C_WHITE)
        self.txt_angulo_r = TextBox(master=self,x=70,y=350,w=100,h=40,color_background=C_BLACK,color_border=C_RED,image_background=None,text="-",font="Verdana",font_size=20,font_color=C_WHITE)
        self.txt_angulo_d = TextBox(master=self,x=180,y=350,w=100,h=40,color_background=C_BLACK,color_border=C_RED,image_background=None,text="-",font="Verdana",font_size=20,font_color=C_WHITE)

        self.label_cos = Label(master=self,x=0,y=400,w=60,h=40,color_background=C_BLACK,color_border=C_BLUE,image_background=None,text="COS",font="Verdana",font_size=20,font_color=C_WHITE)
        self.txt_cos = TextBox(master=self,x=70,y=400,w=210,h=40,color_background=C_BLACK,color_border=C_RED,image_background=None,text="-",font="Verdana",font_size=20,font_color=C_WHITE)

        self.label_sin = Label(master=self,x=0,y=450,w=60,h=40,color_background=C_BLACK,color_border=C_BLUE,image_background=None,text="SIN",font="Verdana",font_size=20,font_color=C_WHITE)
        self.txt_sin = TextBox(master=self,x=70,y=450,w=210,h=40,color_background=C_BLACK,color_border=C_RED,image_background=None,text="-",font="Verdana",font_size=20,font_color=C_WHITE)

        self.label_longitud = Label(master=self,x=0,y=500,w=60,h=40,color_background=C_BLACK,color_border=C_BLUE,image_background=None,text="Lenght",font="Verdana",font_size=20,font_color=C_WHITE)
        self.txt_longitud = TextBox(master=self,x=70,y=500,w=210,h=40,color_background=C_BLACK,color_border=C_RED,image_background=None,text="-",font="Verdana",font_size=20,font_color=C_WHITE)
                       

        self.lista_widget = [   self.boton1,self.boton2,self.boton3,self.boton4,self.txt_x0,self.txt_y0,self.txt_x1,
                                self.txt_y1,self.graph1,self.label_xy0,self.label_xy1,self.label_angulo,
                                self.txt_angulo_r,self.txt_angulo_d,self.label_cos,self.label_sin,self.txt_cos,
                                self.txt_sin,self.label_longitud ,self.txt_longitud
                            ]
  
                   
        

    def on_click_boton1(self, parametro):
        self.set_active(parametro)

    def on_click_boton2(self, parametro):
        self.graph1.x0 = int(self.txt_x0._text)
        self.graph1.x1 = int(self.txt_x1._text)
        self.graph1.y0 = int(self.txt_y0._text)
        self.graph1.y1 = int(self.txt_y1._text)
        self.calcular()

    def on_click_boton3(self, parametro):
        self.graph1.x0 = int(self.txt_x0._text)
        self.graph1.x1 = int(self.txt_x1._text)
        self.graph1.y0 = int(self.txt_y0._text)
        self.graph1.y1 = int(self.txt_y1._text)
        angulo_radianes = math.atan2(self.graph1.y1 - self.graph1.y0, self.graph1.x1 - self.graph1.x0)
        longitud_vector = math.sqrt(math.pow(self.graph1.y1 - self.graph1.y0,2)+math.pow(self.graph1.x1 - self.graph1.x0))
        self.txt_longitud._text = "{0:.8f}".format(longitud_vector)

    def on_click_boton4(self, parametro):
        pass

    def calcular(self):

        angulo_radianes = math.atan2(self.graph1.y1 - self.graph1.y0, self.graph1.x1 - self.graph1.x0)
        longitud_vector = math.sqrt(math.pow(self.graph1.y1 - self.graph1.y0,2)+math.pow(self.graph1.x1 - self.graph1.x0,2))

        self.txt_angulo_r._text = "r:{0:.2f}".format(angulo_radianes)
        self.txt_angulo_d._text = "d:{0:.2f}".format(angulo_radianes*180/math.pi)
    
        self.txt_cos._text  = "{0:.8f}".format(math.cos(angulo_radianes))
        self.txt_sin._text  = "{0:.8f}".format(math.sin(angulo_radianes))

        self.txt_longitud._text = "{0:.8f}".format(longitud_vector)

    def update(self, lista_eventos,keys,delta_ms):
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

    def draw(self): 
        
        super().draw()
        for aux_widget in self.lista_widget:    
            aux_widget.draw()

        
