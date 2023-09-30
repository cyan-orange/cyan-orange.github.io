Linux系统中一切皆文件

# 关于系统信息
在Linux系统中，提供了proc文件系统显示系统的软硬件信息。如果想了解系统中CPU的提供商和相关配置信息，则可以通过`/proc/cpuinfo`文件得到。

使用以下命令来读取`/proc/cpuinfo`文件，查看cpu的信息
```
cat  /proc/cpuinfo
```

输出：
```
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 142
model name      : Intel(R) Core(TM) i7-7500U CPU @ 2.70GHz
stepping        : 9
microcode       : 0xd6
cpu MHz         : 2904.000
cache size      : 4096 KB
physical id     : 0
siblings        : 1
core id         : 0
cpu cores       : 1
apicid          : 0
initial apicid  : 0
fpu             : yes
fpu_exception   : yes
cpuid level     : 22
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon nopl xtopology tsc_reliable nonstop_tsc eagerfpu pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 invpcid rdseed adx smap clflushopt xsaveopt xsavec xgetbv1 arat md_clear spec_ctrl intel_stibp flush_l1d arch_capabilities
bogomips        : 5808.00
clflush size    : 64
cache_alignment : 64
address sizes   : 45 bits physical, 48 bits virtual
power management:
```
相关说明：
- processor：系统中逻辑处理核的编号。对于单核处理器，则可认为是其CPU编号，对于多核处理器则可以是物理核、或者使用超线程技术虚拟的逻辑核；它的计数是从0开始的。
- vendor_id：CPU制造商
- cpu family：CPU产品系列代号
- model：CPU属于其系列中的哪一代的代号
- model name：CPU属于的名字及其编号、标称主频
- stepping：CPU属于制作更新版本
- cpu MHz：CPU的实际使用主频
- cache size：CPU二级缓存大小
- physical id：单个CPU的标号
- siblings：单个CPU逻辑物理核数
- core id：当前物理核在其所处CPU中的编号，这个编号不一定连续
- cpu cores：该逻辑核所处CPU的物理核数
- apicid：用来区分不同逻辑核的编号，系统中每个逻辑核的此编号必然不同，此编号不一定连续
- fpu：是否具有浮点运算单元（Floating Point Unit）
- fpu_exception：是否支持浮点计算异常
- vcpuid level：执行cpuid指令前，eax寄存器中的值，根据不同的值cpuid指令会返回不同的内容
- wp ：表明当前CPU是否在内核态支持对用户空间的写保护（Write Protection）
- flags：当前CPU支持的功能
- vbogomips   ：在系统内核启动时粗略测算的CPU速度（Million Instructions Per Second）
- clflush size  ：每次刷新缓存的大小单位
- cache_alignment ：缓存地址对齐单位
- address sizes：可访问地址空间位数

如何不想获取cpu的全部信息，只是想要查看cpu型号，可以使用以下命令：
```
cat /proc/cpuinfo | grep 'model name' |uniq
```

查看物理CPU个数
```
cat /proc/cpuinfo | grep 'cpu cores' |uniq
```

查看系统内核版本
```
uname -r
```

查看系统的发行版本
```
cat /etc/redhat-release
```

# 查看文件内容

## more
`more info.log`分页查看文件内容
- 回车：下一行
- 空格：下一页
- Ctrl+ B：上一页
- B：回到文档第一页
- h：帮助
- q：退出

## less
`less -N info.log` 带行号查看文件内容
- k： 上一行
- f： 向下滚动一屏幕
- b： 向上滚动一屏幕
- g： 定位到文档头部
- G： 定位到文档最尾部
- 空格键：滚动一页(同f)
- 回车键：滚动一行(同j)

实时查看文档变动：
- F：实时滚动文档
- Ctrl + c：退出实时滚动模式

查找内容：
/keyword 向下查找
- n：向下匹配下一处匹配文本
- N：向上匹配下一处匹配文本


?keyword 向上查找
- n：向上匹配下一处匹配文本
- N：向下匹配下一处匹配文本

# 文件查找

## find
find命令是从指定目录递归遍历其子目录，将满足条件的文件或目录显示在终端
语法：find [搜索范围] [选项]
选项：
- `-name`：指定文件名查找
- `-user`：查找指定用户的所有文件
- `-size`：指定文件的大小查找（+n大于，-n小于，n等于，单位：k，M，G）

## locate

locate指令可以快速定位文件路径。locate指令利用事先建立的文件系统中所有文件名及其路径的locate数据库实现快速定位指定的文件。locate无需便遍历整个文件系统，查询速度较快。为了查询的准确度，管理员必须定期更新locate。

由于locate是基于数据库查询，所以第一次运行前，必须 使用updatedb指令创建locate数据库。

语法：locate 文件名


## 管道符`|` 和grep
管道符`|`：表示将前一个命令的处理结果传递给后面的命令
`grep`：过滤查找

`grep`基本语法：grep [选项] 查找内容 源文件
选项：
- -n：显示匹配及行号
- -i：忽略字母大小写

例如：查询nginx.conf文件中包含location字符所在的行
```
cat /usr/local/nginx/conf/nginx.conf | grep -n 'location'
```

# 压缩和解压缩

## gzip/gunzip

`gzip`用于将文件压缩为`.gz`文件
`gunzip`用于解压`.gz`文件

## zip/unzip

zip用于将文件压缩为`.zip`文件，unzip用于解压缩`.zip`文件

zip语法：zip [选项] xxx.zip 文件或目录
选项：
- -r：递归压缩，压缩目录

unzip语法：unzip [选项] xxx.zip
选项：
- -d：指定解压文件目录

## tar

tar用于将文件打包，打包后的格式为`.tar.gz`

打包：tar [选项] xxx.tar.gz ...文件或目录
解包：tar [选项] xxx.tar.gz

选项：
- -c：产生`.tar`打包文件
- -v：显示详细信息
- -f：指定压缩后的文件名
- -z：打包同时压缩
- -x：解包tar文件
        
