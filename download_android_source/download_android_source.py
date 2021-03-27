import os
import re
import shutil

from xml.dom.minidom import parse
from subprocess import call, check_output

py_file_ptah = os.path.split(os.path.realpath(__file__))[0]

# 1. 整个工程的根目录
base_root_dir = py_file_ptah
custom_root_dir = input(u"输入工程根目录路径(不填表示使用默认路径:{}): ".format(base_root_dir))
if os.path.isdir(custom_root_dir):
    base_root_dir = custom_root_dir
print(u"工程根目录路径:", base_root_dir)
os.chdir(base_root_dir)
print(u"当前处于:", os.getcwd())

# 2. 设置 git 安装的路径
git_path = "C:/Program Files/Git/bin/git.exe"
custom_git_path = input(u"输入 git 程序路径(不填表示使用默认 git程序:{}): ".format(git_path))
if os.path.isfile(custom_git_path):
    git_path = custom_git_path
print(u"git 程序路径:", git_path)

# 3. 解析 manifest 项目
manifest_tsinghua = "https://aosp.tuna.tsinghua.edu.cn/platform/manifest.git"
manifest_dir = base_root_dir + "/manifest"
download_manifest = ""
if os.path.exists(manifest_dir):
    download_manifest = input(
        u"manifest 项目已存在，是否需要重新下载？(输入任意字符重新下载，默认不重新下载): ")
    download_manifest = download_manifest.strip()
if download_manifest != "":
    print(u"正在删除：", manifest_dir)
    shutil.rmtree(manifest_dir)
if not os.path.exists(manifest_dir):
    clone_manifest = "{0} clone {1}".format(git_path, manifest_tsinghua)
    print(u"cmd:", clone_manifest)
    call(clone_manifest)

os.chdir(manifest_dir)

# branch_bytes = check_output("{} branch -a".format(git_path))
# branch_text = branch_bytes.decode('utf-8')
# branch_list = branch_text.split(" ")
# branch_patten = re.compile(r"*")
# for branch_name in branch_list:
#     # branch_name = branchs[0]
#     # print(branch_name)
# branch_name = branch_name.strip()
# if branch_name.find("android") >= 0 and branch_name.find("cts") < 0:
#     print(branch_name)
# # print(len(branchs))

branch = "android-10.0.0_r47"
call("{0} checkout {1}".format(git_path, branch))
custom_branch = input(u"当前处于 {0} 分支，如果需要切换分支，请输入分支名: ".format(branch))
if custom_branch.strip() != "":
    branch = custom_branch
    call("{0} checkout {1}".format(git_path, branch))
# print(u"当前处于 {0} 分支".format(branch))

project_document = parse(manifest_dir + "/default.xml").documentElement
for default_branch in project_document.getElementsByTagName("default"):
    revision = default_branch.getAttribute("revision")
    branch = revision[revision.rfind("/") + 1:]
print(u"manifest 项目分支名:", branch)

source_root_dir = base_root_dir + "/source_" + branch
print("Android 源码将会保存到:", source_root_dir)
if os.path.exists(source_root_dir):
    delete = input(u"源码已存在，是否删除? 输入(yes)回车后删除，默认不删除: ")
    if delete == "yes":
        shutil.rmtree(source_root_dir)

#prefix = git + " clone -b " + branch + " --depth=1 https://android.googlesource.com/"
# 4. 没有梯子使用清华源下载
mirro_source_1 = "https://aosp.tuna.tsinghua.edu.cn/"
mirro_source_2 = "git://mirrors.ustc.edu.cn/aosp/"
mirrors_source = input(u"输入镜像源(1 表示清华镜像，2 表示科大源): ")
if mirrors_source == "1" or mirrors_source == "":
    mirrors_source = mirro_source_1
else:
    mirrors_source = mirro_source_2
# mirrors_source = mirro_source_1
print(u"镜像源:", mirrors_source)

prefix = git_path + " clone -b " + branch + " --depth=1 " + mirrors_source
suffix = ".git"

if not os.path.exists(source_root_dir):
    os.mkdir(source_root_dir)
os.chdir(source_root_dir)

# 只下载源码分析，不编译，所以下载部分源码就够了
learn_source_path_list = ["art", "dalvik", "frameworks", "Launcher3"]

def is_source_path(project_path):
    for item in learn_source_path_list:
        if project_path.find(item) >= 0:
            return True
    return False

# print("is_source_path", is_source_path("platform/prebuilts/misc"))

project_node_list = project_document.getElementsByTagName("project")
project_size = len(project_node_list)
project_index = 0
for project in project_node_list:
    project_index += 1
    project_path = project.getAttribute("path")
    print("\nnow in(", project_index, "/", project_size, ")", project_path)
    if not is_source_path(project_path):
        print("skip:", project_path)
        continue
    last = project_path.rfind("/")
    if last != -1:
        project_parent_dir = source_root_dir + "/" + project_path[:last]
        if not os.path.exists(project_parent_dir):
            os.makedirs(project_parent_dir)
    else:
        project_parent_dir = source_root_dir
    os.chdir(project_parent_dir)
    # project_parent_dir = os.getcwd()
    project_name = project.getAttribute("name")
    project_dir_name = project_name[project_name.rfind("/") + 1:]
    clone_project_cmd = prefix + project_name + suffix
    project_dir = os.path.join(project_parent_dir, project_dir_name)
    print("project parent dir:", project_parent_dir)
    print("project name:", project_name)
    print("project dir:", project_dir)
    if os.path.exists(project_dir):
        if os.path.isfile(project_dir):
            print("remove file:", project_dir)
            os.remove(project_dir)
        else:
            # 检测是否为完整的 git 目录，如果不是，就删除
            os.chdir(project_dir)
            git_fsck = 0
            git_fsck = call(git_path + " fsck --full")  #如果返回的非 0 表示
            if git_fsck == 0:
                continue
            else:
                print("remove dir:", project_dir)
                shutil.rmtree(project_dir)
    os.chdir(project_parent_dir)
    print("current dir:", project_parent_dir, "\ncmd:", clone_project_cmd, "\n")
    call(clone_project_cmd)