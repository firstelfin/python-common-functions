###### <sub>命令行参数</sub><br />python 命令行参数<br />——<br /><sup>2021/10/29</sup><br />**firstelfin**

[TOC]

# 导入命令行参数解析包

```python
import argparse
```

> 导入包没有什么难度，我们只需要记住库的名字即可！这个库的主要作用就是对命令行参数进行解析，这里我们可以分开记忆：`arg` + `parse`。这两部分分别是**参数argument**和**解析器parser**的缩写，几乎是见名知义。

# 解析器实例化

在python中将一个类实例化获得一个具体的对象，这是一个非常常见的操作。我们需要在这个对象下进行相应的操作，在`argparse`库中，我们经常会不加思索实例化一个`ArgumentParser`类型的`parser`对象。明显类的名字就阐述了这个包的用途，类名的记忆完全可以参考库名的记忆。

```python
parser = argparse.ArgumentParser()
```

​	上面的代码即可实现一个解析器对象，剩余的工作只需要告诉这个解析器它需要解析什么！在做这一步之前，我们先思考这个对象初始化的时候我们可以给它添加一些基础配置吗？这当然是可以的，python类的`__init__`函数就是实现这个功能的。

​	*若你只想了解argparse大概并快速上手，可跳过本章剩余内容。*

* **prog**: 进程名
* **usage**: 用法消息（默认值：根据参数自动生成）
* **description**: 程序功能的描述
* **epilog**: 参数描述后面的文本
* **parents**: 应将其参数复制到此解析器中的解析器（类似于**继承**）
* **formatter_class**: 用于打印帮助消息的HelpFormatter类
* **prefix_chars**: 作为可选参数前缀的字符
* **fromfile_prefix_chars**: 作为包含附加参数的文件前缀的字符
* **argument_default**: 所有参数的默认值
* **conflict_handler**: 指示如何处理冲突的字符串
* **add_help**: 添加-h/-help选项
* **allow_abbrev**: 允许长选项明确缩写

## 案例一：添加程序名、描述、参数后描述文本

**配置参数后的描述文本**

```python
examples = """examples:
    # 初始化解析器
    parser = argparse.ArgumentParser(description=%(prog)s程序的简单介绍)
    # 添加参数
    parser.add_argument('--name', default='', help='Add parameter description')
"""
```

**解析器初始化**

```python
parser = argparse.ArgumentParser(
    prog="argpsrse_test",
    description="命令行参数使用及其功能说明",
    epilog=examples,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
args = parser.parse_args()
```

**命令行查看帮助文档**

```shell
$ python argparse_ana/parser_ana.py -h
usage: argpsrse_test [-h]

命令行参数使用及其功能说明

optional arguments:
  -h, --help  show this help message and exit

examples:
    # 初始化解析器
    parser = argparse.ArgumentParser(description=argpsrse_test程序的简单介绍)
    # 添加参数
    parser.add_argument('--name', default='', help='Add parameter description')
```

**小结**

通过实例化并查看帮助文档，我们可以知道：
* **prog**: 这个参数我们一般用于表示当前程序的程序名,如在参数后描述文本中我们可以使用%(prog)s进行引用
* **epilog**: 参数后描述文本，一般我们先用字符串进行配置好
* **formatter_class**: 这个参数我们配置了RawDescriptionHelpFormatter类，没有使用默认的HelpFormatter类，因为前者可以保持字符串的格式！
* **parser.parse_args()**： parser.parse_args()方法必须要被调用，不然help命令无法使用(不会正常显示)

## 实例化的其他参数说明

* **prefix_chars**: 参数的前缀字符，默认是"-"，不建议更换！比如上面我们要添加"name"参数使用的是"--name"而不是"name"
* **allow_abbrev**: 这个参数控制是否允许参数缩写，添加的时候我们都可以配置缩写，但是配置此项位False则在命令行不能使用缩写传参。这个参数不需要管就好！

---

# 添加参数

前面我们实际上已经使用了解析器的**add_argument**方法进行参数添加，这里就不卖关子，我们直接讲此方法的调用参数如何选择！

## 基础参数配置

**add_argument**方法的常用参数有：
* **flag1**: 带前缀或不带前缀的参数名，如"--name"、"name(位置参数)"
* **flag2**: 带前缀的参数名，如"-n"，一般用于简称，flag1与flag2位置可以交换
* **default**: 默认值
* **help**: 当前参数的帮助信息
* **required**: True/False，是否此参数是必须的!
* **choices**: 允许的值集合。如果命令行传入参数解析成相应的格式后，如果不在choices中将会引发异常

带前缀的是可选参数，不带前缀是位置参数

**基础案例**：
```python
parser.add_argument("-n", "--name", default='firstelfin', help="所有者姓名")
```
如上所示，参数name，简称为n，默认值为'firstelfin'(参数没有传值时的默认值),help用于对参数说明，类似于解析器的description.
需要注意的是，在传参的时候我们可以使用简称，但是在参数调用时使用简称会报错！如果我们直接调用n，则会报如下错误：
`AttributeError: 'Namespace' object has no attribute 'n'`
这个时候必须使用name.

带`-`的参数名解析后，默认是会解析为下划线"\_"的。

## dest参数

dest参数用于指定解析后的参数名，需要注意的是我们使用了dest参数后，后面调用就只能使用这个值。


```python
parser.add_argument("-n", "--name", default='firstelfin', dest="n", help="所有者姓名")
```

无论使用`n`还是`name`，参数都会被解析为`n`。
需要注意的是不同参数可以使用dest解析为一个参数！

解析器解析后，参数名究竟是什么优先级？答案是：`dest > --(两个前缀符号的可选参数) > -(一个前缀符号的可选参数)`

## nargs参数

这个参数如其名n + args表示多个参数值，即我们在命令行可以给这个参数传多个参数。但是究竟要传几个值呢？我们需要通过nargs的值进行控制：
* `nargs=n`: 我们需要传入n个参数值
* `nargs=?`: 我们需要传入1个参数值或者不传值，注意这里的不传值是命令行不写参数值，但是参数要写！
 当不传值时，位置参数默认使用default的值，可选参数默认使用const的值。需要注意如果命令行没有写参数，那么都默认使用default的值。
 ```python
 parser.add_argument("--city", nargs="?", const="chengdu", default="guangzhou", help="city name")
 parser.add_argument("home", nargs="?", const="chengdu", default="guangzhou", help="city name")
 ```
 ```shell
 # ----------------------------------------------- #
 $ python argparse_ana/parser_ana.py --city
 # city、home的值分别是：
    chengdu 、guangzhou
 $ python argparse_ana/parser_ana.py
 # city、home的值分别是：
    guangzhou 、guangzhou
 ```
* `nargs=+`: 我们需要传入至少1个参数值
* `nargs=*`: 可以传入任意个参数值,此时不能有const参数，除非使用了action参数

## action参数

action参数用于指定我们的参数进行传参需要执行什么动作，即命令行出现了这个参数，我们需要执行什么操作。
* `action=store`: action参数的默认值，不传参，命令行参数初始化为None
* `action=store_true`: 即使没有默认值default，命令行参数也会初始化，初始化的值为False
* `action=store_false`: 即使没有默认值default，命令行参数也会初始化，初始化的值为True
* `action=store_const`: 命令行没有传参的时候，初始化为None; 命令行出现参数，但是没有传参时初始化为const参数对应的值 
* `action=append`: 允许命令行参数多次出现，最终将同一个命令行参数的参数值合并
 ```python
 parser.add_argument("--performance", action="append",  help="performance")
 ```
 ```shell
 $ python argparse_ana/parser_ana.py --performance 3 --performance 3 --performance 3
 # 此时performance参数的值为：
    ['3', '3', '3']
 # 那么问题来了，如果我们想多次传入参数，又不想限制住每次只能传一个值，该证明操作？
 ```
* `action=append_const`: 类似于append，区别在于命令行参数在命令行出现却没有传值时，默认append参数const对应的值；命令行不出现此命令行参数时，命令行参数初始化为None。注意这里我们不能对命令行参数传值，会报错。
* `action=count`: 统计命令行参数出现的次数，注意同样的不能传参 
* `action=extend`: 如果使用append追加结合nargs=+使用，则最后得到一个嵌套列表，如果我们想得到一个列表怎么办？就只能使用extend这个选项。
 ```python
 parser.add_argument("-p", action="extend", nargs="+", help="performance")
 ```
 ```shell
 $ python argparse_ana/parser_ana.py -p 1 2 -p 54 89
 ['1', '2', '54', '89']
 ```
* `action=version`: 用于显示版本信息
 ```python
 parser.add_argument('-V', action='version', version='parser_ana V20211029')
 ```
 ```shell
 $ python argparse_ana/parser_ana.py -V
 parser_ana V20211029
 ```
* `action=help`: 用于显示帮助信息，实际上就是默认的"-h",效果一模一样


关于`store_true`、`store_false`的初始化记忆可以理解为，这个参数是否store，`store_true`的默认动作是store了，没有值，那么实际就是False;`store_false`类似可得！

## 其他参数

* **metavar**: 控制命令行参数在帮助文档中使用格式信息的别称，你可以翻译为元变量
 ```python
 arg.add_argument("--subject1", nargs="+", dest="s1", metavar="e", default="mathematics", help="subject name")
 arg.add_argument("--subject2", nargs="+", dest="s2", default="mathematics", help="subject name")
 ```
 ```shell
 $ python argparse_ana/parser_ana.py -h
 #输出的帮助文档信息为：
 usage: parser_ana.py [-h] [--subject1 e [e ...]] [--subject2 S2 [S2 ...]]

 命令行参数使用及其功能说明

 optional arguments:
   -h, --help            show this help message and exit
   --subject1 e [e ...]  subject name
   --subject2 S2 [S2 ...]  subject name

 examples:
    # 初始化解析器
    parser = argparse.ArgumentParser(description=parser_ana.py程序的简单介绍)
    # 添加参数
    parser.add_argument('--name', default='', help='Add parameter description')
 ```

 这里注意到，不使用metavar参数时，默认调用信息元变量使用的是解析后变量名；使用metavar后就使用metavar的值替换了！

---

至此，argparse库的常用功能就讲解完了！关于其他类、方法都是围绕上面的知识展开的附属功能，下面我们简单介绍一下。

# 其他类

你是否会疑问，这个包只有这一个类吗？当然不是了，你掌握`ArgumentParser`类就可以很流畅使用这个命令行解析工具了，但是它还有很多其他类，如我们上面已经用到的`RawDescriptionHelpFormatter`。

1. **HelpFormatter**: 用于生成使用情况消息和参数帮助字符串的格式化程序。只有此类的名称被视为公共API。该类提供的所有方法都被视为一个实现细节。
2. **RawDescriptionHelpFormatter**: 帮助消息格式化程序，在description字符串中保留任何格式。只有此类的名称被视为公共API。该类提供的所有方法都被视为一个实现细节。
3. **RawTextHelpFormatter**: 帮助消息格式化程序，它保留所有帮助文本的格式。只有此类的名称被视为公共API。该类提供的所有方法都被视为一个实现细节。
4. **ArgumentDefaultsHelpFormatter**: 帮助消息格式化程序，它将默认值添加到参数帮助中。只有此类的名称被视为公共API。该类提供的所有方法都被视为一个实现细节。
5. **MetavarTypeHelpFormatter**: 使用参数“type”作为默认metavar值（而不是参数“dest”）的帮助消息格式化程序。
6. **ArgumentError**: 创建或使用参数（可选或位置）时出错。此异常的字符串值是消息，并添加了有关导致该异常的参数的信息。
7. **ArgumentTypeError**: 尝试将命令行字符串转换为type类型时出错。
8. **Action**: 自定义action的类。
9. **FileType**: 用于创建文件对象类型的工厂。FileType的实例通常作为type=参数传递给ArgumentParser add_argument（）方法。
 ```python
 parser.add_argument('infile', nargs='?',
              type=argparse.FileType(),
              help='give me a file here, i open it and reture to you',
              default=sys.stdin)
 parser.add_argument('outfile', nargs='?',
              type=argparse.FileType('w'),
              help='give me a file here, i write it for you with in file',
              default=sys.stdout)
 ```
 参考：https://www.pynote.net/archives/2353
10. **Namespace**: 命名空间

# 子解析器

子解析器对应了我们命令行中的子命令。如：`python yolov5.py train --datasets /data/ --batchsize 64 -lr warmup`中的train，我们没有传入任何参数值，这种写法可能有如下情况：
* train是某个参数的参数值
* train是命令行参数，但是使用了默认值
* train是子命令

这一章我们是讨论子命令，所以假设上面的情况是一个子命令的命令行调用代码。那么如何配置子命令？为什么要使用子命令？

## 子命令配置

子命令配置前面我们要先实例化一个子解析器，载再添加子命令，zip后为子命令配置参数：
```python
import argparse

examples = """examples:
    # 初始化解析器
    parser = argparse.ArgumentParser(description=%(prog)s程序的简单介绍)
    # 添加参数
    parser.add_argument('--name', default='', help='Add parameter description')
"""

arg = argparse.ArgumentParser(
    description="命令行参数使用及其功能说明",
    epilog=examples,
    formatter_class=argparse.RawDescriptionHelpFormatter
)

arg.add_argument("--model", required=True, help="模型加载路径")
# 添加子解析器
subparsers = arg.add_subparsers(description="模型训练子解析器", dest="command", help="子解析器对象")

parser_train = subparsers.add_parser(name="train", help="训练一个模型")
parser_train.add_argument("--batchsize", default=64, help="Train batch size")
parser_train.add_argument("-lr", required=True, default="WarmUp", help="Learning rate of train")

parser_valid = subparsers.add_parser(name="valid", help="验证一个模型")
parser_valid.add_argument("--batchsize", default=64, help="Valid batch size")
parser_valid.add_argument("--out", type=str, required=True, help="Result output path")

args = arg.parse_args()
```

这里相当于对参数进行了分组！

## 子命令参数帮助文档查看

一般我们使用`-h`进行帮助文档查看，这里也是一样：

**解析器的帮助文档查看**
```shell
$ python argparse_ana/parser_ana.py -h
```
输出的结果为：
```shell
usage: parser_ana.py [-h] --model MODEL {train,valid} ...

命令行参数使用及其功能说明

optional arguments:
  -h, --help     show this help message and exit
  --model MODEL  模型加载路径

subcommands:
  模型训练子解析器

  {train,valid}  子解析器对象
    train        训练一个模型
    valid        验证一个模型

examples:
    # 初始化解析器
    parser = argparse.ArgumentParser(description=parser_ana.py程序的简单介绍)
    # 添加参数
    parser.add_argument('--name', default='', help='Add parameter description')
```
对比之前的帮助文档，这里已经发生了很大的变换，注意到花括号中即为我们的子命令。……什么你还想套娃？不妨自己再测试

**子命令的帮助文档查看**
```shell
$ python argparse_ana/parser_ana.py train -h
```
输出的结果为：
```shell
usage: parser_ana.py train [-h] [--batchsize BATCHSIZE] -lr LR

optional arguments:
  -h, --help            show this help message and exit
  --batchsize BATCHSIZE
                        Train batch size
  -lr LR                Learning rate of train
```
明显这样做相当于进行了参数、命令的分层，和我们平时使用别人的帮助文档类似！

## 子命令参数的使用

* 首先子命令可以直接使用
* 程序证明知道我们要train还是valid,这个时候注意一些子解析器我们使用了dest="command",调用command的值就知道是train还是valid。

###### 命令行听令