#!python3
# -*- coding=utf-8 -*-

# 遍历并修改所有的 gradle 项目为本地下载的版本
# 第一步，找到最新的本地 gradle 版本
# 第二步，找到 gradle 项目
# 第三步，修改 gradle 配置
# /Users/xander/.gradle/wrapper/dists

import os
import re

import wx


class GradleModel:
    gradleVersion = ''
    buildVersion = ''
    _allList = []

    def __init__(self, gVersion, bVersion):
        super().__init__()
        self.gradleVersion = gVersion
        self.buildVersion = bVersion

    def _findAllGradleModels(self):
        return [GradleModel('', '')]

    def all(self):
        if self._allList.lenth == 0:
            self._allList = self._findAllGradleModels()
        return self._allList



MAC_GRADLE_PATH = '/Users/Xander/.gradle'
WIN_GRADLE_PATH = '/Users/Xander/.gradle'
IS_MAC_OS = True
GRADLE_PATH = MAC_GRADLE_PATH
if not IS_MAC_OS:
    GRADLE_PATH = WIN_GRADLE_PATH
GRADLE_DISTS_PATH = GRADLE_PATH + '/wrapper/dists'


def findMaxVersionName():
    maxGradleVersion = 0
    maxGradleVersionName = ''
    distsDirPath = GRADLE_DISTS_PATH
    distsItems = os.listdir(distsDirPath)
    for distsItem in distsItems:
        itemPath = distsDirPath + os.sep + distsItem
        if os.path.isdir(itemPath):
            # print(file_path)
            version = re.findall('[1-9]\d*\.\d*|0\.\d*[1-9]\d*$', itemPath)
            if len(version) <= 0:
                continue
            version = float(version[0])
            if version > maxGradleVersion:
                maxGradleVersion = version
                maxGradleVersionName = distsItem
                print(maxGradleVersionName)
    return maxGradleVersionName


GRADLE_VERSION_NAME = '' + findMaxVersionName() + '.zip'
GRADLE_VERSION_NAME = 'distributionUrl=https\://services.gradle.org/distributions/' + \
    GRADLE_VERSION_NAME
GRADLE_VERSION_NAME = GRADLE_VERSION_NAME
print('max gradle version is %s' % GRADLE_VERSION_NAME)

BUILD_VERSION_NAME = 'com.android.tools.build:gradle:3.4.2'

BUILD_FILE_NAME = 'build.gradle'
GRADLE_FILE_NAME = 'gradle' + os.sep + 'wrapper' + \
    os.sep + 'gradle-wrapper.properties'


def modifyProjectGradleFile(projectPath):
    gradleFilePath = projectPath + os.sep + GRADLE_FILE_NAME
    print('start modify:', gradleFilePath)
    gradleFile = open(gradleFilePath, 'rb')
    seekPoint = 0
    needModify = False
    gradleFileLine = gradleFile.readline().decode('utf-8')
    while gradleFileLine:
        if len(re.findall('distributionUrl=', gradleFileLine)) > 0:
            needModify = True
            break
        seekPoint = gradleFile.tell()
        gradleFileLine = gradleFile.readline().decode('utf-8')
    gradleFile.close()
    if not needModify:
        return
    gradleFile = open(gradleFilePath, 'r+')
    gradleFile.seek(seekPoint, 0)
    gradleFile.writelines(GRADLE_VERSION_NAME)
    gradleFile.close()
    print('end modify:', gradleFilePath)


def modifyProjectBuildFile(projectPath):
    buildFilePath = projectPath + os.sep + BUILD_FILE_NAME
    print('start modify:', buildFilePath)
    buildFile = open(buildFilePath, 'rb')
    seekPoint = 0
    needModify = False
    buildFileLine = buildFile.readline().decode('utf-8')
    while buildFileLine:
        if len(re.findall('com.android.tools.build:gradle', buildFileLine)) > 0:
            needModify = True
            break
        seekPoint = buildFile.tell()
        buildFileLine = buildFile.readline().decode('utf-8')
    buildFile.close()
    if not needModify:
        print('end - modify:', buildFilePath)
        return
    buildFile = open(buildFilePath, 'r+')
    buildFile.seek(seekPoint, 0)
    index = buildFileLine.find("'")
    buildFileLine = buildFileLine[0:index] + "'" + BUILD_VERSION_NAME + "'"
    buildFile.writelines(buildFileLine)
    buildFile.close()
    print('end modify:', buildFilePath)


def modifyAndroidProjectConfig(projectPath):
    modifyProjectGradleFile(projectPath)
    modifyProjectBuildFile(projectPath)


# modifyAndroidProjectConfig('/Users/xander/Data/pptv_code/PersonalizedMode')
WORK_DIR_PATH = '/Users/Xander/Data/github'

# projects = os.listdir(WORK_DIR_PATH)
# for project in projects:
#     projectPath = WORK_DIR_PATH + os.sep + project
#     buildFilePath = projectPath + os.sep + BUILD_FILE_NAME
#     gradleFilePath = projectPath + os.sep + GRADLE_FILE_NAME
#     if os.path.exists(buildFilePath) and os.path.exists(gradleFilePath):
#         print('find %s' % (projectPath))
#         modifyAndroidProjectConfig(projectPath)


app = wx.App()
window = wx.Frame(None, title="Android Stuido Project Tools", size=(400, 300))
panel = wx.Panel(window)
# path
pathBox = wx.BoxSizer(wx.HORIZONTAL)
pathText = wx.StaticText(panel, label="根路径:")
pathBox.Add(pathText, 0,  wx.FIXED_MINSIZE)
pathInpute = wx.TextCtrl(panel)
pathBox.Add(pathInpute, 0, wx.ALIGN_CENTER_HORIZONTAL)
panel.SetSizer(pathBox) 

label = wx.StaticText(panel, label="Hello World", pos=(100, 100))
window.Show(True)
app.MainLoop()

