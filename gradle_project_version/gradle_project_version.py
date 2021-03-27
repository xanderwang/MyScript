#!python3
# -*- coding=utf-8 -*-

# 遍历并修改所有的 gradle 项目为本地下载的版本
# 第一步，找到最新的本地 gradle 版本
# 第二步，找到 gradle 项目
# 第三步，修改 gradle 配置

import os
import re
import platform

MAC_GRADLE_PATH = '/Users/xander/.gradle'
WIN_GRADLE_PATH = '/Users/xander/.gradle'
platformName = platform.system()
print("platform system:", platformName)
if (platformName == 'Windows'):
    IS_MAC_OS = False
elif (platformName == "Darwin"):
    IS_MAC_OS = True
GRADLE_PATH = MAC_GRADLE_PATH if IS_MAC_OS else WIN_GRADLE_PATH
GRADLE_DISTS_PATH = GRADLE_PATH + '/wrapper/dists'
print('gradle dists path:', GRADLE_DISTS_PATH)


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


GRADLE_VERSION_NAME = findMaxVersionName() + '.zip'
GRADLE_VERSION_NAME = 'distributionUrl=https\://services.gradle.org/distributions/' + GRADLE_VERSION_NAME
GRADLE_VERSION_NAME = 'distributionUrl=https\://services.gradle.org/distributions/gradle-5.6.4-all.zip'
BUILD_VERSION_NAME = 'com.android.tools.build:gradle:3.6.4'

print('gradle version is', GRADLE_VERSION_NAME)
print('biuld plugin version is', BUILD_VERSION_NAME)

BUILD_FILE_NAME = 'build.gradle'
GRADLE_FILE_NAME = 'gradle' + os.sep + 'wrapper' + os.sep + 'gradle-wrapper.properties'


def _modifyProjectGradleFile(projectPath):
    gradleFilePath = projectPath + os.sep + GRADLE_FILE_NAME
    print('start modify:', gradleFilePath)
    gradleFile = open(gradleFilePath, 'r')
    allLines = gradleFile.readlines()
    gradleFile.close()
    gradleFile = open(gradleFilePath, 'w')
    for line in allLines:
        # print(line)
        if len(re.findall('distributionUrl=', line)) > 0:
            gradleFile.writelines(GRADLE_VERSION_NAME + "\n")
        else:
            gradleFile.writelines(line)
    gradleFile.close()
    print('end modify:', gradleFilePath)


def _modifyProjectBuildFile(projectPath):
    buildFilePath = projectPath + os.sep + BUILD_FILE_NAME
    print('start modify:', buildFilePath)
    buildFile = open(buildFilePath, 'r')
    allLines = buildFile.readlines()
    buildFile.close()
    buildFile = open(buildFilePath, 'w+')
    for line in allLines:
        # print(line)
        if len(re.findall('com.android.tools.build:gradle', line)) > 0:
            line = line[0:line.find("'")] + "'" + BUILD_VERSION_NAME + "'\n"
            buildFile.writelines(line)
        else:
            buildFile.writelines(line)
    buildFile.close()
    print('end modify:', buildFilePath)


def modifyAndroidProjectConfig(projectPath):
    _modifyProjectGradleFile(projectPath)
    _modifyProjectBuildFile(projectPath)


# modifyAndroidProjectConfig('/Users/xander/data/github/performance')
WORK_DIR_PATH = '/Users/xander/Data/github'

projects = os.listdir(WORK_DIR_PATH)
for project in projects:
    projectPath = WORK_DIR_PATH + os.sep + project
    buildFilePath = projectPath + os.sep + BUILD_FILE_NAME
    gradleFilePath = projectPath + os.sep + GRADLE_FILE_NAME
    if os.path.exists(buildFilePath) and os.path.exists(gradleFilePath):
        print('find %s' % (projectPath))
        modifyAndroidProjectConfig(projectPath)
