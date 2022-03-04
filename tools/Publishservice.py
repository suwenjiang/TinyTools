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

            print ("++++++++INFO:�����ļ������ɹ�++++++++")

            return connection_file_path
        except Exception as msg:
            print (msg)

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
        print ("++++++++INFO:��ʼ����ĵ�����Ч��++++++++")
        file_to_be_published=[]
        for file in mxdLists:
            mxd=mapping.MapDocument(file)
            brknlist=mapping.ListBrokenDataSources(mxd)
            if not len(brknlist)==0:
                print ("++++++++ERROR:��ͼ�ĵ�,"+os.path.split(file)[1]+"�𻵣��޷���������++++++++")
            else:
                file_to_be_published.append(file)
        print ("++++++++INFO:��ͼ�ĵ���Ч�Լ�����++++++")
        return file_to_be_published


    def publishServices(self,mxdLists,con,clusterName='default',copy_data_to_server=True,folder=None):

        for file in self.checkfileValidation(mxdLists):
            ###tmp:
            serviceslist=[]
            serviceName=os.path.splitext(os.path.split(file)[1])[0]

            print ("++++++++INFO:����_"+serviceName+"��ʼ�����������ļ�++++++++")
            clsCreateSddraft=CreateSddraft()
            sddraft=clsCreateSddraft.CreateSddraft(file,con,serviceName,copy_data_to_server,folder)
            print ("++++++++INFO:��ʼ��������:"+serviceName+"++++++++")
            analysis = arcpy.mapping.AnalyzeForSD(sddraft)
            dirName=os.path.split(file)[0]
            if analysis['errors'] == {}:
               print ("++++++++WARNING:�����ڴ��󣬵�����������ʾ��Ϣ����Щ���ݿ��ܻ�Ӱ���������+++++++")
               print (analysis['warnings'])
               if(not self.checkWarnings(analysis['warnings'])):
                   try:
                        sd=dirName+"\\"+serviceName+".sd"
                        if(os.path.exists(sd)):
                            os.remove(sd)
                        arcpy.StageService_server(sddraft, sd)
                        print ("++++++++INFO:����:"+serviceName+"����ɹ�+++++++")
                        arcpy.UploadServiceDefinition_server(sd, con,in_cluster=clusterName)
                        print ("++++++++INFO:����:"+str(serviceName)+"�����ɹ�++++++")
                        os.remove(sd)
                        ####ֹͣ����


                   except Exception as msg:
                        print (msg)
               else:
                   print ("++++++++WARNING:ǿ�ҽ��飬�˳���ǰ����ȥע������Դ���粻�˳���6s�󷢲��������+++")
                   # time.sleep(10)
                   try:
                    sd=dirName+"\\"+serviceName+".sd"
                    if(os.path.exists(sd)):
                        os.remove(sd)
                    arcpy.StageService_server(sddraft, sd)
                    print ("++++++++INFO:����ɹ�++++++++")
                    arcpy.UploadServiceDefinition_server(sd, con,in_cluster=clusterName)
                    print ("++++++++INFO:"+serviceName+"�����ɹ�+++++++")
                    os.remove(sd)
                   except Exception as msg:
                    print (msg)

            else:
                print ('++++++++ERROR:�������´���:'+analysis['errors']+'++++++++')

                #������˳�����̨
                time.sleep(5)
                sys.exit(1)


    def  checkWarnings(self,warnings):
        for warning in warnings:
            if warning[1]==24011:
                print ("++++++++��ǰ����λ��û��ע�ᣬ���ݻ´������������,�������̻�Ӱ�췢���ٶ�+++++++")
                return True
        return False

    def GetMxFileList(self,filePath):
            #�ж��ļ����Ƿ����
        if not os.path.exists(filePath):
            print ("++++++++ERROR:�ļ��в�����+++++++")
            sys.exit(1)
        #��ȡ�ļ����е�����mxd�ļ�
        list=[]
        for root,dirname, files in os.walk(filePath):

                 for file in files:

                    if os.path.splitext(file)[1]=='.mxd':
                        mxdfile=os.path.join(root,file)

                        list.append(mxdfile)

        if list==[]:
          print ("++++++++INFO:�ڵ�ǰĿ¼�²�������Ч��mxd�ļ�++++++++")
          time.sleep(5)
          sys.exit(1)
        return list
def GetInfo():

    server = raw_input("������GIS Server IP:")
    userName=raw_input("������վ�����Ա�û���:")
    passWord=getpass.getpass("������վ�����Ա����:")
    port=raw_input("������˿ں�(6080)��")

    logDict={'server':server,
            'userName':userName,
                 'passWord':passWord,
             'port':port}

    contionfile=os.path.join(tempfile.mkdtemp(),'server.ags')

    #���ô��������ļ��Ĳ���
    instace=CreateContectionFile()
    instace.filePath=contionfile
    instace.loginInfo=logDict
    instace.CreateContectionFile()
    if(os.path.isfile(contionfile)==False):
        print ("++++++++ERROR:��������ʧ��++++++++")
        time.sleep(5)
        sys.exit(1)

    #����mxd�ļ����ļ���e
    mxdDir=raw_input('������mxd�����ļ���:')
    clsPublishservice=publishServices()
    fileList=clsPublishservice.GetMxFileList(mxdDir)

    servic_dir=raw_input("��ָ��������������Ŀ¼��Ĭ��Ϊroot��ʹ��Ĭ��ֱֵ�ӻس�:")
    if len(servic_dir)==0:
        servic_dir==None
    clusterName=raw_input("��ָ����������Ⱥ��Ĭ��Ϊcluster����û�м�Ⱥ��������ֱ�ӻس�:")
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
