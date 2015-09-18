#coding:cp936
import os

import arcpy
import time
import sys

import getpass
__author__ = 'jiangmb'

from arcpy import mapping
import xml.dom.minidom as DOM
import os
import tempfile
import argparse
class CreateSddraft:
    def CreateSddraft(self,mapDocPath,con,serviceName,copy_data_to_server=True,folder=None):

        """
        :param mapDocPath: mxd path
        :param con: arcgis server connection file
        :param serviceName: service name
        :param clusterName: cluster name
        :param folder: folder to contain the publishing service
        :return: the file path of the sddraft
        """

        mapDoc=mapping.MapDocument(mapDocPath)
        sddraft=mapDocPath.replace(".mxd",".sddraft")
        result= mapping.CreateMapSDDraft(mapDoc, sddraft, serviceName, 'ARCGIS_SERVER', con, copy_data_to_server, folder)
        return sddraft



    def setTheClusterName(self,xml,clusterName):# the new description

        doc = DOM.parse(xml)
        # find the Item Information Description element
        doc.getElementsByTagName('Cluster')[0].childNodes[0].nodeValue=clusterName
        # output to a new sddraft
        outXml =xml
        f = open(outXml, 'w')
        doc.writexml( f )
        f.close()
        return  outXml


class CreateContectionFile(object):
    def __init__(self):

        self.__filePath = None
        self.__loginDict = None

    def CreateContectionFile(self):
        """
        wrkspc: store the ags file
        loginDict: dictionary stored login information

        """
        # con = 'http://localhost:6080/arcgis/admin'
        try:
            server_url = "http://{}:{}/arcgis/admin".format(self.__loginDict['server'],self.__loginDict['port'])
            connection_file_path = str(self.__filePath)            #
            use_arcgis_desktop_staging_folder = False
            if os.path.exists(connection_file_path):
                os.remove(connection_file_path)
            out_name = os.path.basename(connection_file_path)

            path = os.path.split(self.filePath)[0]
            result = mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",
                                                           path,
                                                           out_name,
                                                           server_url,
                                                           "ARCGIS_SERVER",
                                                           use_arcgis_desktop_staging_folder,
                                                           path,
                                                           self.__loginDict['userName'],
                                                           self.__loginDict['passWord'],
                                                           "SAVE_USERNAME"
                                                           )

            print "++++++++INFO:链接文件创建成功++++++++"

            return connection_file_path
        except Exception, msg:
            print msg

    #
    @property
    def filePath(self):

        return self.__filePath

    @filePath.setter
    def filePath(self, value):
        self.__filePath = value

    @property
    def loginInfo(self):
        return self.__loginDict

    @loginInfo.setter
    def loginInfo(self, value):

        self.__loginDict = value




class CreateSddraft:
    def CreateSddraft(self,mapDocPath,con,serviceName,copy_data_to_server=True,folder=None):

        """
        :param mapDocPath: mxd path
        :param con: arcgis server connection file
        :param serviceName: service name
        :param clusterName: cluster name
        :param folder: folder to contain the publishing service
        :return: the file path of the sddraft
        """

        mapDoc=mapping.MapDocument(mapDocPath)
        sddraft=mapDocPath.replace(".mxd",".sddraft")
        result= mapping.CreateMapSDDraft(mapDoc, sddraft, serviceName, 'ARCGIS_SERVER', con, copy_data_to_server, folder)
        return sddraft



    def setTheClusterName(self,xml,clusterName):# the new description

        doc = DOM.parse(xml)
        # find the Item Information Description element
        doc.getElementsByTagName('Cluster')[0].childNodes[0].nodeValue=clusterName
        # output to a new sddraft
        outXml =xml
        f = open(outXml, 'w')
        doc.writexml( f )
        f.close()
        return  outXml

class publishServices:

    def checkfileValidation(self,mxdLists):
        print "++++++++INFO:开始检查文档的有效性++++++++"
        file_to_be_published=[]
        for file in mxdLists:
            mxd=mapping.MapDocument(file)
            brknlist=mapping.ListBrokenDataSources(mxd)
            if not len(brknlist)==0:
                print "++++++++ERROR:地图文档,"+os.path.split(file)[1]+"损坏，无法发布服务++++++++"
            else:
                file_to_be_published.append(file)
        print "++++++++INFO:地图文档有效性检查完毕++++++"
        return file_to_be_published


    def publishServices(self,mxdLists,con,clusterName='default',copy_data_to_server=True,folder=None):

        for file in self.checkfileValidation(mxdLists):
            ###tmp:
            serviceslist=[]
            serviceName=os.path.splitext(os.path.split(file)[1])[0]

            print "++++++++INFO:服务_"+serviceName+"开始创建服务定义文件++++++++"
            clsCreateSddraft=CreateSddraft()
            sddraft=clsCreateSddraft.CreateSddraft(file,con,serviceName,copy_data_to_server,folder)
            print "++++++++INFO:开始分析服务:"+serviceName+"++++++++"
            analysis = arcpy.mapping.AnalyzeForSD(sddraft)
            dirName=os.path.split(file)[0]
            if analysis['errors'] == {}:
               print "++++++++WARNING:不存在错误，但是有如下提示信息。这些内容可能会影响服务性能+++++++"
               print analysis['warnings']
               if(not self.checkWarnings(analysis['warnings'])):
                   try:
                        sd=dirName+"\\"+serviceName+".sd"
                        if(os.path.exists(sd)):
                            os.remove(sd)
                        arcpy.StageService_server(sddraft, sd)
                        print "++++++++INFO:服务:"+serviceName+"打包成功+++++++"
                        arcpy.UploadServiceDefinition_server(sd, con,in_cluster=clusterName)
                        print "++++++++INFO:服务:"+str(serviceName)+"发布成功++++++"
                        os.remove(sd)
                        ####停止服务


                   except Exception,msg:
                        print msg


               else:
                   print "++++++++WARNING:强烈建议，退出当前程序，去注册数据源。如不退出，6s后发布服务继续+++"
                   # time.sleep(10)
                   try:
                    sd=dirName+"\\"+serviceName+".sd"
                    if(os.path.exists(sd)):
                        os.remove(sd)
                    arcpy.StageService_server(sddraft, sd)
                    print "++++++++INFO:打包成功++++++++"
                    arcpy.UploadServiceDefinition_server(sd, con,in_cluster=clusterName)
                    print "++++++++INFO:"+serviceName+"发布成功+++++++"
                    os.remove(sd)
                   except Exception,msg:
                    print msg

            else:
                print '++++++++ERROR:存在如下错误:'+analysis['errors']+'++++++++'

                #五秒后退出控制台
                time.sleep(5)
                sys.exit(1)


    def  checkWarnings(self,warnings):
        for warning in warnings:
            if warning[1]==24011:
                print "++++++++当前数据位置没有注册，数据会拷贝到服务器上,拷贝过程会影响发布速度+++++++"
                return True
        return False

    def GetMxFileList(self,filePath):
            #判断文件夹是否存在
        if not os.path.exists(filePath):
            print "++++++++ERROR:文件夹不存在+++++++"
            sys.exit(1)
        #获取文件夹中的所有mxd文件
        list=[]
        for root,dirname, files in os.walk(filePath):

                 for file in files:

                    if os.path.splitext(file)[1]=='.mxd':
                        mxdfile=os.path.join(root,file)

                        list.append(mxdfile)

        if list==[]:
          print "++++++++INFO:在当前目录下不存在有效的mxd文件++++++++"
          time.sleep(5)
          sys.exit(1)
        return list
def GetInfo():

    server = raw_input("请输入GIS Server IP:")
    userName=raw_input("请输入站点管理员用户名:")
    passWord=getpass.getpass("请输入站点管理员密码:")
    port=raw_input("请输入端口号(6080)：")

    logDict={'server':server,
            'userName':userName,
                 'passWord':passWord,
             'port':port}

    contionfile=os.path.join(tempfile.mkdtemp(),'server.ags')

    #调用创建链接文件的参数
    instace=CreateContectionFile()
    instace.filePath=contionfile
    instace.loginInfo=logDict
    instace.CreateContectionFile()
    if(os.path.isfile(contionfile)==False):
        print "++++++++ERROR:创建链接失败++++++++"
        time.sleep(5)
        sys.exit(1)

    #输入mxd文件的文件夹e
    mxdDir=raw_input('请输入mxd所在文件夹:')
    clsPublishservice=publishServices()
    fileList=clsPublishservice.GetMxFileList(mxdDir)

    servic_dir=raw_input("请指定发布到服务器目录，默认为root。使用默认值直接回车:")
    if len(servic_dir)==0:
        servic_dir==None
    clusterName=raw_input("请指定发布到集群，默认为cluster。如没有集群环境，请直接回车:")
    if len(clusterName)==0:
        clusterName='default'
    clsPublishservice=publishServices()
    clsPublishservice.publishServices(fileList,contionfile,clusterName,copy_data_to_server=False,folder=servic_dir)


if __name__=='__main__':
    GetInfo()

    """logDict = {'server': 'localhost',
               'userName': "arcgis",
               'passWord': "Super123",
               'port':'6080'}
    dd = CreateContectionFile()
    dd.loginInfo = logDict
    path =os.path.join(tempfile.mkdtemp(),'server.ags')
    print path
    dd.filePath = path

    dd.CreateContectionFile()
    clsPublishservice=publishServices()
    #get
    file=r"d:\workspace\New folder\10"
    fileList=clsPublishservice.GetMxFileList(file)


    clusterName='default'
    servic_dir=''

    clsPublishservice.publishServices(fileList,path,clusterName,copy_data_to_server=False,folder=servic_dir)
"""
