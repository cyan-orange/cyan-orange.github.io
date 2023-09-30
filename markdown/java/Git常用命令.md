每天使用 Git ，但是很多命令记不住
 ![](../../image/7fc00fc0-40c3-46f1-8bd3-cd77e4cfe5d1.png)


- Workspace：工作区
- Index / Stage：暂存区
- Repository：仓库区（或本地仓库）
- Remote：远程仓库



# 新建代码仓库


在当前目录新建一个Git代码库
```bash
git init
```
新建一个目录，将其初始化为Git代码库
```bash
git init [project-name]
```
下载一个项目和它的整个代码历史
```bash
git clone [url]
```


# 配置
```bash
# 显示当前的Git配置
git config --list

# 编辑Git配置文件
git config -e [--global]

# 设置提交代码时的用户信息
git config [--global] user.name "[name]"
git config [--global] user.email "[email address]"
```

# 查看信息
```bash
# 显示有变更的文件
git status

# 显示当前分支的版本历史
git log

# 显示commit历史，以及每次commit发生变更的文件
git log --stat

# 显示commit历史，以及每次commit发生变更的文件
git log --stat

# 搜索提交历史，根据关键词
git log -S [keyword]

# 显示所有提交过的用户，按提交次数排序
git shortlog -sn

显示指定文件是什么人在什么时间修改过
git blame [file]

# 显示暂存区和上一个commit的差异
git diff --cached [file]

# 显示工作区与当前分支最新commit之间的差异
git diff HEAD [file]

# 显示今天你写了多少行代码
git diff --shortstat "@{0 day ago}"

# 显示某次提交发生变化的文件
git show --name-only [commit]

# 显示某次提交时，某个文件的内容
git show [commit]:[filename]

# 显示两次提交之间的差异
git diff [first-commit] [second-commit] [file]
```

# 版本管理


显示有变更的文件
```bash
git status
```


工作区查看文件的修改
```bash
git diff <file>
```


清除工作区所有的修改
```bash
git checkout .
```


将工作区的修改添加到暂存区
```bash
git add <file>...
```


清除暂存区所有的修改
```bash
git reset .
```


将暂存区的修改提交到本地库
```bash
git commit -m "这是必填的提交信息"
```


查看提交记录
```bash
git log
```


撤销本次提交
```bash
git reset --hard HEAD~1
```


回退到指定版本 reset后的参数说明

- `mixed`：不删除工作空间改动代码，撤销commit，并且撤销git add . 操作这个为默认参数,git reset --mixed HEAD^ 和 git reset HEAD^ 效果是一样的。
- `soft`：不删除工作空间改动代码，撤销commit，不撤销git add .
- `hard`：删除工作空间改动代码，撤销commit，撤销git add . 注意完成这个操作后，就恢复到了上一次的commit状态

```bash
git reset --hard 版本号
```


# 分支管理


列出本地所有分支


```bash
git branch
```


列出远程所有分支


```bash
git branch -a
```


创建分支并切换


```bash
git checkout -b 分支名
```


合并分支
比如 `master` 分支要合并 `dev` 分支,首先要切换到 `master` 分支


```bash
git merge dev
```

推送分支到远程库，如果在主分支上可以直接省略 `origin` 及 `master`，直接 `git push`


```bash
git push origin 分支名
```


删除本地分支


```bash
git branch -d 分支名
```


删除远程分支


```bash
git push origin -d 分支名
```

# 标签管理
```
# 列出所有tag
$ git tag

# 新建一个tag在当前commit
$ git tag [tag]

# 新建一个tag在指定commit
$ git tag [tag] [commit]

# 删除本地tag
$ git tag -d [tag]

# 删除远程tag
$ git push origin :refs/tags/[tagName]

# 查看tag信息
$ git show [tag]

# 提交指定tag
$ git push [remote] [tag]

# 提交所有tag
$ git push [remote] --tags

# 新建一个分支，指向某个tag
$ git checkout -b [branch] [tag]
```


# 撤销


```bash
# 恢复暂存区的指定文件到工作区
$ git checkout [file]

# 恢复某个commit的指定文件到暂存区和工作区
$ git checkout [commit] [file]

# 恢复暂存区的所有文件到工作区
$ git checkout .

# 重置暂存区的指定文件，与上一次commit保持一致，但工作区不变
$ git reset [file]

# 重置暂存区与工作区，与上一次commit保持一致
$ git reset --hard

# 重置当前分支的指针为指定commit，同时重置暂存区，但工作区不变
$ git reset [commit]

# 重置当前分支的HEAD为指定commit，同时重置暂存区和工作区，与指定commit一致
$ git reset --hard [commit]

# 重置当前HEAD为指定commit，但保持暂存区和工作区不变
$ git reset --keep [commit]

# 新建一个commit，用来撤销指定commit
# 后者的所有变化都将被前者抵消，并且应用到当前分支
$ git revert [commit]

# 暂时将未提交的变化移除，稍后再移入
$ git stash
$ git stash pop
```
        
