#author: Jacky.Shi distribute under General Public License v3
#ShiJianGang.sh@gmail.com
#!/usr/bin/python3
# -*- coding:utf-8 -*-

from MindWay import *  #pyuic5 -o MindWay.py MindWay.ui ui文件转换py文件
from tempfile import TemporaryFile,NamedTemporaryFile
import sys,math,random  
from PyQt5 import QtWidgets    #导入相应的包
from PyQt5.QtCore import *
#QCoreApplication
#from PyQt5.uic import loadUi #重点,如何直接导用ui文件
#from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QDialog,QApplication,QFileDialog
import sys, os
#fileName_choose=''
class MindWay(QDialog):
	fileName_choose=""#全局变量
	MyOutput=""
	CheckedRowNuber=[]
	JustNum=-1
	mystr=""
	PosFound=-1
	numt1=["","","","",""]
	numt1id=[0,0,0,0,0]
	fmt=4
	def __init__(self):
		QDialog.__init__(self)
		self.initMindWay()
	def initMindWay(self):
		self.cwd = os.getcwd() # 获取当前程序文件位置
		self.resize(900,600)   # 设置窗体大小
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self) #前两行调入后缀为py的界面与下行效果一致
#		self.ui = Ui_Dialog()
#		self.ui = loadUi('MindWay.ui')#调入对话框界面
#		print("hello this is intiMindWay",self)

#		self.ui.dockWidget.setFixedSize(600,460)

		self.ui.listView.setFixedSize(600,460)
		self.ui.toolButton_7.setFixedSize(20,100)
		self.ui.toolButton_1.setToolTip("下一页")

		self.ui.toolButton_8.setToolTip("文式")

		self.ui.toolButton_12.setToolTip("计算")

		self.ui.toolButton_2.setFixedSize(40,20)
		self.ui.toolButton_6.setFixedSize(40,20)
		self.ui.toolButton_8.setFixedSize(40,20)
		self.ui.toolButton_12.setFixedSize(40,20)

		self.ui.toolButton_3.setFixedSize(200,20)
		self.ui.toolButton_4.setFixedSize(200,20)
		self.ui.toolButton_5.setFixedSize(200,20)

		self.ui.toolButton_9.setFixedSize(200,20)
		self.ui.toolButton_10.setFixedSize(200,20)
		self.ui.toolButton_11.setFixedSize(200,20)

		self.ui.toolButton_1.setFixedSize(20,100)
		self.ui.toolButton_7.setFixedSize(20,100)
		self.ui.toolButton_7.setToolTip("上一页")

#        self.horizontalLayout_5.setFixedSize(450,21)
		self.ui.toolButton_9.setFixedSize(200,20)
		self.ui.toolButton_9.setToolTip("定位文件")
#		self.ui.toolButton_8.setFixedSize(200,20)
		self.ui.toolButton_11.setFixedSize(200,20)
		self.ui.toolButton_11.setToolTip("打开文件")

		self.model = QStandardItemModel()
		self.ui.listView.clicked.connect(self.ViewOp)

#		self.ui.pushButton.clicked.connect(self.slot_btn_chooseFile)
		self.ui.toolButton_9.clicked.connect(self.slot_btn_chooseFile)#选择文件

		self.ui.toolButton_10.clicked.connect(self.AddItem)#增加项

#		self.ui.pushButton_2.clicked.connect(self.slot_btn_openFile)
		self.ui.toolButton_11.clicked.connect(self.slot_btn_openFile)#打开文件

		self.ui.toolButton_6.clicked.connect(self.SearchRow)#搜索内容

#		self.ui.pushButton_3.clicked.connect(self.CopyText)#引用文式
		self.ui.toolButton_8.clicked.connect(self.CopyText)#V

#		self.ui.pushButton_4.clicked.connect(self.handle)
		self.ui.toolButton_12.clicked.connect(self.handle)#计算

		self.ui.toolButton_1.clicked.connect(self.Extract)#摘录显示

		self.ui.toolButton_2.clicked.connect(QCoreApplication.instance().quit)#退出
#		self.ui.pushButton_5.clicked.connect(QCoreApplication.instance().quit)
		self.model = QStandardItemModel()
		item = QStandardItem("本行为输入显示行")
		item.setCheckState(False)
		item.setCheckable(True)
		self.model.clear()
		self.model.appendRow(item)
		self.ui.listView.setModel(self.model)
#		self.ui.show()
		self.show()
###setCurrentIndex(
	def SearchRow(self):
		ss=self.model.item(0).index().data()#获取listView的0行内容***
		print("进入SearchRow搜索->",ss)
#		sslist=ss.split()
#		sslen=len(sslist)
#		ic=self.OnOpNumber()
#		if(ic>=self.PosFound):self.PosFound=ic
		if(self.PosFound==-1):
			i=1
		else:
			i=self.PosFound
		print("\n\ti=",i,"行发现,指针定位->",self.PosFound)
		it=self.model.rowCount()
		while (i<it):
#		for i in range(self.model.rowCount()):
			s=self.model.item(i).index().data()#获取内容
			print("第",i,"项：",s)
			newpos=s.find(ss)
			if(newpos>=0):#发现0项内容
				self.PosFound=i+1
				print("搜索[",ss,"]内容在",i,"行发现,指针定位->",self.PosFound)
				si=self.model.item(i).index()#获取所在行的索引号***
				self.ui.listView.setCurrentIndex(si)#定位索引号行***
				itemc=self.model.item(i)
				itemc.setData(QVariant(Qt.Checked),Qt.CheckStateRole)#改变索引行勾选态***
				if not self.model.item(0).checkState():
					break
			i+=1
		if(i==it):
			self.PosFound=1
			print("\n***搜索到达尾部***\n")
		
	def AddItem(self):#将0行内容插入操作行后
		print("进入AddItem")
		lnum=self.OnOpNumber()#1016
		lstr=self.model.item(0).index().data()#获取0行内容
		mylist=[]
		i=0
		for i in range(self.model.rowCount()):
			s=self.model.item(i).index().data()#获取内容
			print("第",i,"项：",s)
			mylist.append(s)
			if(i==lnum):#操作行时，将0行内容插入列表
				print("插入",i+1,"项：",lstr)
				mylist.append("="+lstr)
			i+=1
		i=0
		for task in mylist:
			item = QStandardItem(task)
			item.setCheckState(False)
			item.setCheckable(True)
			if i == 0 :
				self.model.clear()
				self.model.appendRow(item)
			else :
				self.model.appendRow(item)
			self.ui.listView.setModel(self.model)
			i=i+1
		i=0
		it=self.model.rowCount()
		print("\tAddItem表有",it,"项")
		for i in range(it):
			print("第",i,"项：")
			if(i<=lnum):
				if(i in self.CheckedRowNuber):
					print("插入行前第",i,"行在选中表中")
					it=self.model.item(i)
					it.setData(QVariant(Qt.Checked),Qt.CheckStateRole)
			if(i>lnum):
				if(i-1 in self.CheckedRowNuber):
					print("插入行后第",i-1,"行在选中表中")
					it=self.model.item(i)
					it.setData(QVariant(Qt.Checked),Qt.CheckStateRole)
			i+=1

		self.ui.show()
			
###
	def Extract(self):
		print("\n进入　Extract")
		i=0
		for i in range(self.model.rowCount()):
			if self.model.item(i).checkState():
#				print("选中第",i,"行……",self.mylist[i])
				self.CheckedRowNuber.append(i)
			i = i + 1
		f = TemporaryFile('w+t',encoding='utf-8' )
		for i in self.CheckedRowNuber:
			print("\n选中第",i,"项")
#			si=self.model.item(i).index()
#			print("\n\t选中项索引：",si)          
#			s=si.data()
			s=self.model.item(i).index().data()
			print("\t\t选中项内容：",s)          
			f.write(s+"\n")
#			f.write(self.mylist[i]+"\n")
		f.seek(0)#注意读取文件时候要将文件指针指向第一个
		s=f.read()
		self.ui.textEdit.setText(s)
#self.text_browser.setText(self.text_edit.toPlainText())
		print(s)          

	def CopyText(self):#操作行显示于０行，如果没有操作行，显示操作行选中行
		print("\n进入　CopyText,listview 共",self.model.rowCount(),"行")
		i=self.OnOpNumber()
		print("\t获取正在操作行i=",i)
		if(i==0):
			print("listview 显示文件名：",self.fileName_choose)
			self.FirstLine(self.fileName_choose)
		else:
#			if (i=="") :
#				i=self.JustCheckedNumber;
#				if(i==""):
#					i=0
			slecstr=self.model.item(i).index().data()#获取列表内容***
			self.myStr=slecstr
			print("\ti=",i,"内容slecstr=",slecstr)
			self.FirstLine(slecstr)
###
	def FirstLine(self,myStr):
		i1=self.model.item(0).index()#获取0行索引
		self.model.setData(i1, myStr)#更新0行数据
		self.ui.listView.setModel(self.model)
	
	def JustCheckedNumber(self):#获取刚选中的行号

		print("进入获取最新　勾选　行号方法\n")
#		print("勾选　行序号表",self.CheckedRowNuber)
		i=0
		if(len(self.CheckedRowNuber)==0):
			for i in range(self.model.rowCount()):
				if self.model.item(i).checkState():
					self.JustNum=i
#					print("\n\t只选中一项，为第",i,"行……")
					break
				i = i + 1
		else:
			for i in range(self.model.rowCount()):
				if self.model.item(i).checkState():
					if i not in self.CheckedRowNuber:
						self.JustNum=i
#						print("\n\t不在表中，刚选第",self.JustNum,"行……")
				i = i + 1
		self.CheckedRowNuber=[]
		i=0
		for i in range(self.model.rowCount()):
			if self.model.item(i).checkState():
#				print("选中第",i,"行……",self.mylist[i])
				self.CheckedRowNuber.append(i)
			i = i + 1
#		print("\n\t勾选　行序号表",self.CheckedRowNuber)
#		print("\n\t***刚选中第",self.JustNum,"行")
		
	def OnOpNumber(self):#获取正在操作的行号
		print("进入获取正在操作行号方法\n")
		ic=self.ui.listView.currentIndex()
		i=0
		for i in range(self.model.rowCount()):
			i0=self.model.item(i).index()
			if(ic==i0):
				print("正在操作第",i,"行……")
				break
			i = i + 1
		return i

	def ViewOp(self):
		print("\n\t列表操作")
		it1=self.OnOpNumber()
		self.JustCheckedNumber()
		if (it1==0):#0行选中全表选中，0行取消，全表取消
			if (self.JustNum!=-1):
				if(self.JustNum==0):
					if self.model.item(0).checkState():
						i=0
						for i in range(self.model.rowCount()):
							it=self.model.item(i)
							it.setData(QVariant(Qt.Checked),Qt.CheckStateRole)
#							print("\t复选第",i,"项;")
							i+=1
					else:
						i=0
						for i in range(self.model.rowCount()):
							it=self.model.item(i)
							it.setData(QVariant(Qt.Unchecked),Qt.CheckStateRole)
#							print("\t\t取消复选第",i,"项;")
							i+=1
			
					
				
			
#选择文件
	def	slot_btn_chooseFile(self):
#		print("选择方法中全局文件名为:",self.fileName_choose)#测试全局变量
		self.fileName_choose,filetype = QFileDialog.getOpenFileName(self,
									"选取文件",
									self.cwd,# 起始路径 
									"All Files (*);;Pthon Files (*.py);;Text Files (*.txt);;向导文件(*.xdf)")# 设置文件扩展名过滤,用双分号间隔
		if self.fileName_choose == "":
			print("没选中文件!")
			return

#		print("\n你选择的文件为:")
#		print(self.fileName_choose)
#		print("文件筛选器类型: ",filetype)
#https://blog.csdn.net/humanking7/article/details/80546728?utm_source=copy 
#		self.ui.lineEdit.setText(self.fileName_choose)
		model = QStandardItemModel()
		item = QStandardItem(self.fileName_choose)
		item.setCheckState(False)
		item.setCheckable(True)
		self.model.clear()
		self.model.appendRow(item)
		self.ui.listView.setModel(self.model)

#打开文件
	def	slot_btn_openFile(self):
#		fileName_choose=self.ui.lineEdit.text()
#		print("测试打开方法中全局文件名为:",self.fileName_choose)
#		print(self,"\n准备打开->",self.fileName_choose,"<-文件")
#		fh = ''
		fh=open(self.fileName_choose,mode='r',encoding='UTF-8')
#			with fh:
		data=fh.read()
#		print("完成打开文件->",self.fileName_choose,"<-。文件内容：\n",data)
		fh.close()
#		self.mylist = data.split("\n")	
		mylist = data.split("\n")
#			line = fh.readline().strip()         # 如果不加strip，会出现空行
		model = QStandardItemModel()
		i=0
		for task in mylist:#self.mylist:
			item = QStandardItem(task)
			item.setCheckState(False)
			item.setCheckable(True)
			if i == 0 :
				self.model.clear()
				self.model.appendRow(item)
			else :
				self.model.appendRow(item)
			self.ui.listView.setModel(self.model)
			i=i+1
		self.show()

#https://blog.csdn.net/weixin_41656968/article/details/80904491?utm_source=copy 
#		close(fh)


#https://blog.csdn.net/qq_33638791/article/details/53438161?utm_source=copy 

	def DivideStr(self):
		print("\n\n\t***计算字符串进入分解方法：")
#		str1=self.ui.lineEdit_2.text()
		slecstr=self.model.item(0).index().data()#获0行内容#1015
		self.myStr=slecstr
		strpara=" "
		str1=self.mystr
		print("字串为：",str1,"分隔符为[",strpara,"]")
		#strlist=[]
		strlist=str1.split(strpara)
		ns = len(strlist)
		i1 = len(strpara)
		print("一级分解后计算字符串成为表：",strlist,"\t共",ns,"项")
		if (i1==0):
			strpara0=""
		itt=0
		while(itt<ns):#各表项遍历
			self.mystr=str1t = strlist[itt]#分解的字串项
			print("\n分解的字串项：",str1t)
			bracketn = 0
			slen = len( str1t)
			nct =0 
			while(nct < slen):
				strn = str1t[nct]
				nct+=1
				if(strn == '('):
					bracketn = bracketn+1
			nct1=0
			k1=0
			while(k1<bracketn):#各层括号解析
				bracketnt = 0
				numn = 0
				bracketb = 0
				brackete = 0
				nct = 0
				sta = 1
				slen = len( str1t)
				while (nct < slen):#找出最内层括号序号
					if(nct>nct1):
						strn = str1t[nct]
						if(strn == '(') :
							bracketnt = nct
						elif(strn==')') :
							bracketb = bracketnt
							brackete = nct
							break
					nct +=1
				sta=brackete-bracketb-1
				print("\n第",k1,"层括号开始于：",bracketb,"\t结束于",brackete,"\t净字符数：",sta)
				prestr = str1t[0:bracketb]
				midstr = str1t[(bracketb+1):brackete]
				endstr = str1t[(brackete+1):]
				print("\n第",k1,"层括号分解后，前串：",prestr,"\t中串：",midstr,"\t后串：",endstr)
				if (len(midstr)!= 0):
					self.mystr=midstr
					self.strcacu(midstr)
					str1t=prestr+self.mystr
					str1t=str1t+endstr
					self.mystr=str1t
				print("\n第",k1,"层括号运算后，成为串：",str1t)

				k1+=1	
			self.strcacu(self.mystr)
			strlist[itt]=self.mystr
			print("\n第",itt,"表项运算后，成为串：",strlist[itt])
			if(itt==0):str1=strlist[itt]
			else:str1=str1+" "+strlist[itt]
			itt+=1

			self.mystr=str1
			self.FirstLine(self.mystr)
#			self.ui.lineEdit_3.setText(self.mystr)#1014
			print("\n第",k1,"层括号运算后，成为串：",self.mystr)

############################################
	def strcacu (self,mystr):
		caculist1=["sin","cos","tg","ctg","arcsin","arccos","arctg","sinh","cosh","tgh","abs","rand"]
		caculist2=["^", "ln", "lg"]
		caculist3=["*","/"]
		caculist4=["+", "-"]
		listn = 12
		passt = 0
#		self.mystr=self.ui.lineEdit_2.text()
		found1 = len(self.mystr)
		rank =listn
		inow=0#1014
		i1=0
		value=""
		print("\n进入字符串计算strcacu，字符串为：",self.mystr)

		while i1<listn:
			foundt = self.mystr.find(caculist1[i1],inow)#1014
			if(foundt>=0): 
				print("计算字符串[ ",self.mystr," ]中发现一级优先计算符(",caculist1[i1],")位于",foundt)
				if(foundt <= found1):
					rank = i1
					found1 =foundt
				passt = 1
			i1 +=1
		print("\n位置1发现")#,self.mystr,"第[",rank,"]运算串",caculist1[rank])
		while(passt ==1):
			numbers = 0
			i5=0
			print("\t一级前strcacu->ArrangeStr中一级运算符:",caculist1[rank],",found1=",found1)
			if(found1>=0):self.ArrangeStr(caculist1[rank],self.mystr,inow)#1014
			value=""#1014
			if(self.numt1id[1]==1):#1014
				if(self.numt1[2]=="sin"):
					
					cacustrt = self.numt1[1]
					self.numt1[1]=""
					self.numt1id[1]=0
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = math.sin (para1)
						numbers = 1
#					print("\tself.IsNumber(cacustrt)值：",self.IsNumber(cacustrt))
					
					else:print("\tcacustrt.isalnum()值：",cacustrt.isalnum())
				if(self.numt1[2]=="cos" ):
					
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = math.cos (para1)
						numbers = 1
				if(self.numt1[2]=="tg"):
				
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = math.tan (para1)
						numbers = 1
				if(self.numt1[2]=="ctg"):
					
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = 1.0/math.tan (para1)
						numbers = 1
				if(self.numt1[2]=="arcsin"):
					
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = math.asin (para1)
						numbers = 1
				if(self.numt1[2]=="arccos"):
					
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = math.acos (para1)
						numbers = 1
				if(self.numt1[2]=="arctan"):
					
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = math.atan (para1)
						numbers = 1
				if(self.numt1[2]=="asinh"):
					
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = math.asinh (para1)
						numbers = 1
				if(self.numt1[2]=="acosh"):
					
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = math.acosh (para1)
						numbers = 1
				if(self.numt1[2]=="atanh"):
					
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = math.atanh (para1)
						numbers = 1
				if(self.numt1[2]=="abs"):
					
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						para1= float (cacustrt)
						value = math.fabs (para1)
						numbers = 1
				if(self.numt1[2]=="rand"):
					
					cacustrt = self.numt1[1]
					print("\tstrcacu函数输入值：",cacustrt)
					if(self.IsNumber(cacustrt)):
						value = radom.randint()
						numbers = 1
				else:
					passt=0

			if(value != ""):#滚动输出
				if(self.numt1id[0]==1):
					self.mystr=self.numt1[0]+str(round(value,self.fmt))
					self.numt1id[0]=0
					if(self.numt1id[4]==1):
						self.mystr=self.mystr+self.numt1[4]
						self.numt1id[4]=0
				else:
					self.mystr=str(value)
					if(self.numt1id[4]==1):
						self.mystr=self.mystr+self.numt1[4]
						self.numt1id[4]=0
				print("一级运算",cacustrt,")","\t计算结果值：",value,"mystr=",self.mystr)
			else:#1014
				inow+=found1+1

				#self.ui.lineEdit_3.setText(self.mystr)
		print("\n位置2",self.mystr)
		listn = 3
		passt = 0
		found1 = len(self.mystr)
		rank =listn
		inow=0#1014
		i1=0
		while (i1<listn):
			foundt = self.mystr.find(caculist2[i1],inow)#1014
			print("\t遍历一级计算串[",i1,"]=",caculist2[i1],"foundt=",foundt)
			if(foundt>=0): 
				print("计算字符串[ ",self.mystr," ]中发现二级优先计算符(",caculist2[i1],")")
				if(foundt <= found1):
					rank = i1
					found1 =foundt
				passt = 1
			i1+=1
		while(passt ==1):
			numbers = 0
			i3=rank
			print("\t二级前strcacu->ArrangeStr中运算符:",caculist2[rank])
			self.ArrangeStr(caculist2[rank],self.mystr,inow)#1014
			value=""#1014
			if(self.numt1id[1]==1):#1014
				if( self.numt1[2]=="^"):
					if(self.numt1id[1]==1):
						cacustrt1 = self.numt1[1]
						self.numt1id[1]=0
						print("\tstrcacu函数输入值",cacustrt1)
					if(self.numt1id[3]==1):					
						cacustrt2 = self.numt1[3]
						self.numt1id[3]=0
						print("\tstrcacu函数输入值",cacustrt1)
					if(self.IsNumber(cacustrt2)):
						para2= float (cacustrt2)
						self.numt1id[3]=0
					if((cacustrt1[0] == 'e') or (cacustrt1[0] == 'E')):
						self.numt1id[1]=0
						value = math.exp (para2)
					else :
						para1= float (cacustrt1)
						self.numt1id[1]=0
						value = math.pow (para1,para2)
						print(cacustrt1,"^",cacustrt2,"=",value)
				if( self.numt1[2]=="ln"):
					if(self.numt1id[1]==1):
						
						cacustrt = self.numt1[1]
						print("\tstrcacu函数ln输入值：",cacustrt)
						para1= float (cacustrt)
						numbers =1
						value = math.log (para1)
						self.numt1id[1]=0
						print("\tln",cacustrt,"=",value)
				if( self.numt1[2]=="lg"):
					if(self.numt1id[1]==1):
						
						cacustrt = self.numt1[1]
						print("\tstrcacu函数ln输入值：",cacustrt)
						para1= float (cacustrt)
						numbers =1
						value = math.log10 (para1)
						self.numt1id[1]=0
						print("\tlg",cacustrt,"=",value)
#					self.mystr=str(value)
#					print("\n\t***mystr值更新为",self.mystr)

			if(value != ""):#滚动输出
				if(self.numt1id[0]==1):
					self.mystr=self.numt1[0]+str(round(value,self.fmt))
					self.numt1id[0]=0
					if(self.numt1id[4]==1):
						self.mystr=self.mystr+self.numt1[4]
						self.numt1id[4]=0
				else:
					self.mystr=str(value)
					if(self.numt1id[4]==1):
						self.mystr=self.mystr+self.numt1[4]
						self.numt1id[4]=0
				print("二级运算计算结果值：",value,"\tmystr=",self.mystr)
				#self.ui.lineEdit_3.setText(self.mystr)
			else:
				inow+=found1+1#1014

	
			passt = 0
			found1 = len(self.mystr)
			rank =listn
			i2=0
			while(i2<listn):
				foundt = self.mystr.find(caculist2[i2],inow)#1014
				#foundt = found(caculist2[i1],str)
				if(foundt>=0): 
					if(foundt <= found1):
						rank = i2
						found1 =foundt
					passt = 1
				i2+=1

		print("\n位置3",self.mystr)
		listn = 2
		passt = 0
		found1 = len(self.mystr)
		rank =listn
		inow=0#1014
		i1=0
		while(i1<listn):
			foundt = self.mystr.find(caculist3[i1],inow)#1014
			if(foundt>=0): 
				print("计算字符串[ ",self.mystr," ]中发现三级优先计算符(",caculist3[i1],")")
				if(foundt <= found1):
					rank = i1
					found1 =foundt
				passt = 1
			i1+=1
		while(passt ==1):
			numbers = 0
			i3=rank
#			i5=0
			print("\t三级前strcacu->ArrangeStr中运算符:",caculist3[rank])
			self.ArrangeStr(caculist3[rank],self.mystr,inow)#1014
			value=""#1014
			if(self.numt1id[3]==1):#1014
				if( self.numt1[2]=="*"):
					if(self.numt1id[1]==1):
						
						cacustrt1 = self.numt1[1]
						print("\tstrcacu函数输入值*：",cacustrt1)
						para1= float (cacustrt1)
						numbers +=1
						self.numt1id[1]=0
					if(self.numt1id[3]==1):
						
						cacustrt2 = self.numt1[3]
						print("\tstrcacu函数输入值：%s\n",cacustrt2)
						para2= float (cacustrt2)
						numbers +=1
						self.numt1id[3]=0
					if(numbers>1):
						value = para1 * para2
				if( self.numt1[2]=="/"):
					if(self.numt1id[1]==1):
						
						cacustrt1 = self.numt1[1]
						print("\tstrcacu函数输入值/：%s\n",cacustrt1)
						para1= float (cacustrt1)
						numbers +=1
						self.numt1id[1]=0
					if(self.numt1id[3]==1):
						
						cacustrt2 = self.numt1[3]
						print("\tstrcacu函数/输入值：%s\n",cacustrt2)
						para2= float (cacustrt2)
						numbers +=1
						self.numt1id[3]=0
					if(numbers>1):
						if(math.fabs(para2)<1e-10):
							print("除数不能为零！\n")
						else :
							value = para1 / para2
#					if(self.numt1id[0]!= 0):
#						str1 = self.numt1[0]+str1
#					if(self.numt1id[4]!= 0):
#						str1 = str1+self.numt1[4]
					
#					self.mystr = str(value)
	
			if(value != ""):#滚动输出
				if(self.numt1id[0]==1):
					self.mystr=self.numt1[0]+str(round(value,self.fmt))
					self.numt1id[0]=0
					if(self.numt1id[4]==1):
						self.mystr=self.mystr+self.numt1[4]
						self.numt1id[4]=0
				else:
					self.mystr=str(value)
					if(self.numt1id[4]==1):
						self.mystr=self.mystr+self.numt1[4]
						self.numt1id[4]=0
				print("三级运算结果值：",value,"mystr=",self.mystr)
			else:
				inow+=found1+1#1014
					
					#self.ui.lineEdit_3.setText(self.mystr)
			passt = 0
			found1 = len(self.mystr)
			rank =listn
			i1=0
			while(i1<listn):
				foundt = self.mystr.find(caculist3[i1],inow)#1014
				#foundt = found(caculist3[i1],str)
				if(foundt>=0): 
					if(foundt <= found1):
						rank = i1
						found1 =foundt
					passt = 1
				i1+=1

		print("\n位置4",self.mystr)#四级运算开始，＋，－
		listn = 2
		passt = 0
		found1 = len(self.mystr)
		rank =listn
		inow=0#1014
		i1=0
		while(i1<listn):
			foundt = self.mystr.find(caculist4[i1],inow)#1014
			if(foundt>=0): 
				print("计算字符串[ ",self.mystr," ]中发现四级优先计算符(",caculist4[i1],")")
				if(foundt <= found1):
					rank = i1
					found1 =foundt
				passt = 1
			i1+=1
		while(passt ==1):
			numbers = 0
			i3=rank
			i5=0
			print("\t四级前strcacu->ArrangeStr中运算符:",caculist4[rank])
			self.ArrangeStr(caculist4[rank],self.mystr,inow)#1014
			value=""#1014
			if(self.numt1id[3]==1):#1014

				if( self.numt1[2]=="+" ):
					if(self.numt1id[1]==1):
						cacustrt1 = self.numt1[1]
						para1= float (cacustrt1)
						numbers +=1
						self.numt1id[1]=0
						print("\tstrcacu函数输入值1：",cacustrt1)
					if(self.numt1id[3]==1):
						cacustrt2 = self.numt1[3]
						para2= float (cacustrt2)
						numbers +=1
						self.numt1id[3]=0
						print("\tstrcacu函数输入值2：",cacustrt2)
					else :
						passt=1
						break
					if(numbers>1):
						value = para1 + para2
						numbers = 2
				if( self.numt1[2]=="-"):
					if(self.numt1id[1]==1):
						#i4=len(self.numt1[1])
						cacustrt1 = self.numt1[1]
						para1= float (cacustrt1)
						numbers +=1
						self.numt1id[1]=0
					if(self.numt1id[3]==1):
						#i4=len(self.numt1[3])
						cacustrt2 = self.numt1[3]
						para2= float (cacustrt2)
						numbers +=1
						self.numt1id[3]=0
					else :
						passt=1
						break
					if(numbers>1):
						value = para1 - para2
						numbers = 2
	
					passt = 0
					found1 = len(self.mystr)
					rank =listn
					i1=0
					while(i1<listn):
						foundt = self.mystr.find(caculist4[i1],inow)#1014
						if(foundt>=0): 
							if(foundt <= found1):
								rank = i1
								found1 =foundt
							passt = 1
						i1+=1
				else:
					passt=0


			if(value != ""):#滚动输出
				if(self.numt1id[0]==1):
					self.mystr=self.numt1[0]+str(round(value,self.fmt))
					self.numt1id[0]=0
					if(self.numt1id[4]==1):
						self.mystr=self.mystr+self.numt1[4]
						self.numt1id[4]=0
				else:
					self.mystr=str(value)
					if(self.numt1id[4]==1):
						self.mystr=self.mystr+self.numt1[4]
						self.numt1id[4]=0
				print("四级运算计算结果值：",value,"mystr=",self.mystr)
				#self.ui.lineEdit_3.setText(self.mystr)
			else:#1014
				inow+=found1+1

			print("\n位置5",self.mystr)
			listn = 2
			passt = 0
			found1 = len(self.mystr)
			rank =listn
			i1=0
			while(i1<listn):
				foundt = self.mystr.find(caculist4[i1],inow)#1014
				if(foundt>=0): 
					if(foundt <= found1):
						rank = i1
						found1 =foundt
						passt = 1
					print("计算字符串[ ",self.mystr," ]中发现四级优先计算符(",caculist4[i1],")","foundt=",foundt,",found1=",found1,",passt=",passt)
				i1+=1
	

#######
	def ArrangeStr (self,symb,lstr,inow):
		state = 0
		statet = 0
		n5=[]
		i1=0
		print("\n进入ArrangeStr,运算符为：[ ",symb," ]字符串为：[",lstr,"]\n")#30+50+70
#		while(i1<5):
#			numt1id[i1]=0
#			print("\nnumt1id[",i1,"]",numt1id[i1])
#			i1+=1
		bracketn = 0
		slen = len (symb)
		xlen = len (lstr)
		ncs = 0
		nct = 0
		nct1 = 0
		pd0 = 0
		pd1 =0 
		founds=0
		pd3 = 0 
		strt = ""#'\0'
		numtt=numt=""
		self.numt1=["","","","",""]
		self.numt1id=[0,0,0,0,0]
		founds=lstr.find(symb)
		numberp=self.IsNumber(lstr)
		print("\n字串中发现运行符的位置为 ",founds,"是否数字:",numberp)
		if(founds>=0 and (not numberp)):
			while(nct < xlen):
				strnl = lstr[nct]#字串遍历 10+30^2*sinln4
	#			strns = symb[ncs] 
				print("\n循环中,运算符为：[ ",symb," ]字符串为：[",lstr,"]\n")#30+50+70
				print("\nnct=",nct,"\txlen=",xlen,"\tnct1=",nct1,"\tstrnl=",strnl)
				print("\nnumt1[]",self.numt1,"\nnumt1id[]",self.numt1id,"\n")
				if ((strnl.isdigit( )) or (strnl == '.') or #字串是数字？
						(
							((strnl == '-')or(strnl=='+'))and
							((nct==0)#正负号
								or(strnl == 'e')or(strnl == 'E')#科学计数
							)
						)
					):
					state = 1
				else: state=0
				print("状态参数：statet=",statet,"\tstate=",state)
				if(statet == state):#数与非数状态不变
					print("\n\t数与非数状态不变")
					print("\tnumt：",numt,"\tnumtt=",numtt,"\tnct1=",nct1)
					if(nct == (xlen-1)):#末字符时
						numt=numt+strnl#字串追加
						numtt=numt#记录字串
						if(state==1):#是数字
							if(self.numt1id[1]==0):
								self.numt1[1]=numtt#写入“数1串”栈[前串，数1串,运算串,数2串，后串]
								self.numt1id[1]=1#标记有“数1串”
								print("\n\t分支1-1-1列表numt1：",self.numt1)
								print("\n\t分支1-1-1列表numt1id：",self.numt1id)
							else:
								self.numt1[3]=numtt#已有“数1串”时写入“数2串”栈
								self.numt1id[3]=1#标记有“数2串”
								print("\n\t分支1-1-2列表numt1：",self.numt1)
								print("\n\t分支1-1-2列表numt1id：",self.numt1id)
						else:#不是数字
							if(self.numt1id[4]==0):
								self.numt1[4]=numtt#写入“后串”
								self.numt1id[4]=1#标记有“后串”
								print("\n\t分支1-1-3列表numt1：",self.numt1)
								print("\n\t分支1-1-3列表numt1id：",self.numt1id)
	
						break

					elif(nct==founds):#非末字#运算符处10+30^2*sinln4 1+2^3					
						numtt=numt #记录之前串符
						numt=strnl
						if(self.numt1id[0]==0):#"前串"栈空时，压栈
							numtp=lstr[0:nct]
							self.numt1[0]=numtp#列表第1格记录"前串"
							self.numt1id[0]=1#标记有"前串"
							self.numt1[2]=symb#列表第3格记录"运算串"
							self.numt1id[2]=1#标记有"运算串"
							nct+=slen-1
							state=0
							nct1=0
							numt=numtt=""
							print("\n\t分支1-2高级运算符前串:",numtp)

					elif (strnl=="-"):#1014非末字为-号
						if(nct<xlen-1):
							if(lstr[nct+1].isdigit( )):
								numtt=numt #记录之前串符
								numt=strnl
								print("\t分支1-3数与非数状态未改变，但为‘－’号")
								print("\tnumt：",numt,"\tnumtt=",numtt,"\tnct1=",nct1)
								nct1=0
								state=1
					else:#非末字非运算符处
						numt=numt+strnl					
					nct1+=1
				else :#数与非数状态改变	
					numtt=numt #记录之前串符
					numt=strnl
					print("\t分支２数与非数状态改变")
					print("\tnumt：",numt,"\tnumtt=",numtt,"\tnct1=",nct1)
					nct1=0
					if(state==0):#分割串非数字时+
						print("\t分支２－１为非数字状态")
						if(nct == 0):#首字时
	#						numt=strnl
							print("\n\t分支2-1-1首字串numt：",numt,"\tnct1=",nct1)
							nct1+=1#设置变化位置
	
						else:
	#						numtt=numt #记录之前数符
	#						numt=strnl
							if (nct == (xlen-1)):#末字时
								print("\n\t分支2-1-3末字串numt：",numt,"\t串长nct1=",nct1,"\tnumtt=",numtt)
								if(self.numt1id[1]==0):#"数1"栈空时，压栈
									self.numt1[1]=numtt#列表第2格记录运算串
									self.numt1id[1]=1#标记有"数1"
								elif (self.numt1id[3]==0):#"数2"栈空时，压栈
									self.numt1[3]=numtt#列表第4格记录运算串
									self.numt1id[3]=1#标记有"数2"

								if (self.numt1id[4]==0):
	#								numt=numt+strnl
									self.numt1[4]=numt#字串追加压入[后串栈]
									self.numt1id[4]=1#标记有后串
	
							elif(nct==founds) :#中字达到高级运算符时压栈数据
								print("\n\t分支2-1-2中字串numt：",numt,"\tnumtt=",numtt)
								print("\n\t\t分支2-1-2-1“数1串”空,压栈")
								self.numt1[1]=numtt#压栈列表第2格
								self.numt1id[1]=1#标记有“数1串”
								self.numt1[2]=symb#压栈列表第3格
								self.numt1id[2]=1#标记有“运算串”
								nct1=len(numtt) #临时借用nct1变量							
								if(nct1<nct+1):
									self.numt1[0]=lstr[0:founds-nct1]#压栈列表第1格
									self.numt1id[0]=1#标记有“前串”
								nct+=slen-1
								nct1=0
							elif(nct>founds+slen):
								print("\n\t分支2-1-４中运算串后numtt：",numtt)						
								if(self.numt1id[1]==0) :#运算符后时，检查“数２串”栈
									print("\n\t分支2-1-4-1中数2串压栈")	
	#								if(IsNumber(numtt)):
									print("\n\t分支2-1-4-1-1中运算串后有数")						
									self.numt1[1]=numtt#压栈列表第2格
									self.numt1[4]=lstr[nct:]#压栈列表第5格
									self.numt1id[1]=1#标记有“数1串”
									self.numt1id[4]=1#标记有“后串”
								elif(self.numt1id[3]==0) :#运算符后时，检查“数２串”栈
									print("\n\t分支2-1-4-1中数2串压栈")	
	#								if(IsNumber(numtt)):
									print("\n\t分支2-1-4-1-1中运算串后有数")						
									self.numt1[3]=numtt#压栈列表第4格
									self.numt1[4]=lstr[nct:]#压栈列表第5格
									self.numt1id[3]=1#标记有“运算串”
									self.numt1id[4]=1#标记有“后串”
	#								else:	
	#									print("\n\t分支2-1-4-1-2中运算串后无数")						
	#									self.numt1[4]=lstr[nct-len(numtt)]#压栈列表第5格
	#									self.numt1id[4]=1#标记有“后串”
	#							else:
	#									print("\n\t分支2-2-4-2中数2串占位")						
								print("\n\t分支2-1-4列表numt1：",self.numt1)
								print("\n\t分支2-1-4列表numt1id：",self.numt1id)
	
								break	
									
								
					else:#分割串数字时5
						print("\t分支２－２为数字状态")
						if(nct == 0):#首字时
							numt=strnl
							print("\n\t分支2-2-1首字串numt：",numt,"\tnct1=",nct1)
							nct1+=1#设置变化位置
						else:#非首字时5
	#						numtt=numt
	#						numt=strnl
							if (nct == (xlen-1)):#末字时
								print("\n\t分支2-2-2末字串numt：",numt,"\t串长nct1=",nct1,"\tnumtt=",numtt)
								if(self.numt1id[2]==0):#"运算串"栈空时，压栈
									self.numt1[2]=numtt#列表第3格记录运算串
									self.numt1id[2]=1#标记"运算串"
								if(self.numt1id[1]==0):
									self.numt1[1]=numt#列表第2格记录"数1"串
									self.numt1id[1]=1#标记"数1"
								else:
									self.numt1[3]=numt#列表第4格记录"数2"串
									self.numt1id[3]=1#标记"数2"
							elif(nct==founds) :#运算符时
								print("\n\t分支2-2-3中运算串numtt：",numtt)						
								if(numtt==symb):#判断是"运算串"
									print("\n\t分支2-2-3-1是运算串！")						
									if(self.numt1id[2]==0):#“运算串”栈空时
										print("\n\t分支2-2-3-1-1运算串空 ，压栈")						
										self.numt1[2]=numtt#压栈列表第2格
										self.numt1id[2]=1#标记有“运算串”
									else:#“运算串”满时,压入后串栈
										print("\n\t分支2-2-3-1-1运算串满，压入后串退出！")						
										self.numt1[4]=lstr[nct-1:]#列表第5格记录后串
										self.numt1id[4]=1#标记有“后串”
										nct=xlen#退出
								else:#判断非"运算串"
									print("\n\t分支2-2-3-2非运算串！")						
									if(self.numt1id[0]==0):#“前串”栈空时，压栈
										self.numt1[0]=numtt#列表第3格记录“前串”
										self.numt1id[0]=1#标记有“前串”
							elif(nct>founds+slen):
								print("\n\t分支2-2-４中运算串后numtt：",numtt)						
								if(self.numt1id[3]==0) :#运算符后时，检查“数２串”栈
									if(self.IsNumber(numtt)):
										print("\n\t分支2-2-4-1中运算串后有数")						
										self.numt1[3]=numtt#压栈列表第2格
										self.numt1[4]=lstr[nct]#压栈列表第5格
										self.numt1id[3]=1#标记有“运算串”
										self.numt1id[4]=1#标记有“后串”
									else:	
										print("\n\t分支2-2-4-2中运算串后无数")						
										self.numt1[4]=lstr[nct-len(numtt)]#压栈列表第5格
										self.numt1id[4]=1#标记有“后串”
								break	
	
				print("\n字串栈：",self.numt1)
				print("\n字串栈标记：",self.numt1id)
								
				nct+=1
				strt = strnl
				statet =state 
#######
	def IsNumber(self,localstr):
#		print("进入IsNumber",localstr)
		lens=len(localstr)
		i1=0
		state=0
		while(i1<lens):
			if(i1==0):
				if (localstr[i1].isdigit( )or (localstr[i1] == '.') or #字串是数字？
					(localstr[i1] == '-')or(localstr[i1]=='+')):
					state+=0
#					print(i1)
				else:
					state+=1
#					print("state=",state)
			else :
				if((localstr[i1] == 'e')or(localstr[i1] == 'E')or (localstr[i1] == '.')or 			localstr[i1].isdigit( )):#科学计数
					state+=0
#					print(i1)
					#continue
				else:
					state+=1
#					print("state=",state)
			
			i1+=1
		if state>0:
#			print("IsNumber state=",state)
			justnumber=False
		else: 
#			print("IsNumber state=",state)
			justnumber=True
		return justnumber

	def handle(self):
#		self.mystr=self.ui.lineEdit_2.text()
		i=self.OnOpNumber()#1016
		self.mystr=self.model.item(i).index().data()
		print("self.mystr=",self.mystr)
		numberp=self.IsNumber(self.mystr)
		if(numberp):	
			self.FirstLine(self.mystr)
#			self.ui.lineEdit_3.setText(self.mystr)#1014
#			print("numberp=",numberp)
		else:
#			print("numberp=",numberp)
			self.DivideStr()
#			self.strcacu(self.mystr)


if __name__ == '__main__':  
      
#	app = QtWidgets.QApplication(sys.argv)
#	loadUi('MindWay.ui')   #载入ui(重点)      
	app = QApplication(sys.argv)
	w=MindWay()
	w.show()
#	w.ui.pushButton_5.clicked.connect(QCoreApplication.instance().quit)
#	sys.exit( app.exec_() )  

	app.exec_()





