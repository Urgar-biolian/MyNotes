## [File类](https://so.csdn.net/so/search?q=File类&spm=1001.2101.3001.7020)的概述和API

```java
  
import java.io.File;

/**
    目标：File类的概述和API

File类：代表操作系统的文件对象。
File类：是用来操作操作系统的文件对象的，删除文件，获取文件信息，创建文件（文件夹）...
广义来说操作系统认为文件包含（文件和文件夹）

File类的创建文件对象的API:
     包：java.io.File
    （1）构造器：
        -- public File(String pathname):根据路径获取文件对象
        -- public File(String parent , String child): 根据父路径和文件名称获取文件对象！
        -- public File(File parent , String child):

File类创建文件对象的格式:
    a.File f = new File("绝对路径/相对路径");
        绝对路径：从磁盘的的盘符一路走到目的位置的路径。
            -- 绝对路径依赖具体的环境，一旦脱离环境，代码可能出错！！
            -- 一般是定位某个操作系统中的某个文件对象。
        相对路径：不带盘符的。（重点）
            -- 默认是直接相对到工程目录下寻找文件的。
            -- 相对路径只能用于寻找工程下的文件。
            -- 能用相对路径就应该尽量使用，可以跨平台！

​    b.File f = new File("文件对象/文件夹对象");
​        广义来说：文件是包含文件和文件夹的。
小结：
​     File代表系统文件对象，然后操作它
​     File f = new File("绝对路径/相对路径")
​     File f = new File("文件对象/文件夹对象")

 */
public class FileDemo01 {
    public static void main(String[] args) {
        // 1、使用绝对路径创建文件对象
        // 文件是包含文件和文件夹的。
        File f1 = new File("C:/code");
        System.out.println(f1.exists()); // 判断这个文件是否存在

​    // 路径分隔符：
​    // a. 正斜杠 /
​    // b. 反斜杠 \
​    // c. API File.separator
​    File f2 = new File("C:/图片资源/meimei.jpg");
​    System.out.println(f2.length()); // 文件的字节大小

​    File f22 = new File("C:\\图片资源\\meimei.jpg");
​    System.out.println(f22.length()); // 文件的字节大小

​    File f222 = new File("C:"+File.separator + "图片资源"+File.separator +"meimei.jpg");
​    System.out.println(f222.length()); // 文件的字节大小

​    // 2、使用相对路径定位项目中的某个文件对象(重点)
​    //   定位到工程下寻找的，用于找项目中的文件
​    File file = new File("day10-demo/src/dlei01.txt");
​    System.out.println(file.length());

}

}
```



‘

## File类的获取功能的API

```java
import java.io.File;
import java.text.SimpleDateFormat;

/**
     目标：File类的获取功能的API
     - public String getAbsolutePath()  ：返回此File的绝对路径名字符串。
     - public String getPath()  ： 获取创建文件对象的时候用的路径
     - public String getName()  ： 返回由此File表示的文件或目录的名称。
     - public long length()  ：    返回由此File表示的文件的长度。
 */
public class FileDemo02 {
    public static void main(String[] args) {
        // 1.绝对路径创建一个文件对象
        File f1 = new File("C:\\图片资源\\meinv.jpg");
        // a.获取它的绝对路径。
        System.out.println(f1.getAbsolutePath());
        // b.获取文件定义的时候使用的路径。
        System.out.println(f1.getPath());
        // c.获取文件的名称：带后缀。
        System.out.println(f1.getName());
        // d.获取文件的大小：字节个数。
        System.out.println(f1.length());

​    System.out.println("------------------------");

​    // 2.相对路径
​    File f2 = new File("day10-demo/src/dlei01.txt");
​    System.out.println(f2.isDirectory()); //  false  是文件夹返回true 反之
​    System.out.println(f2.isFile()); //  true   是文件返回true ，反之
​    // a.获取它的绝对路径。
​    System.out.println(f2.getAbsolutePath());
​    // b.获取文件定义的时候使用的路径。
​    System.out.println(f2.getPath());
​    // c.获取文件的名称：带后缀。
​    System.out.println(f2.getName());
​    // d.获取文件的大小：字节个数。
​    System.out.println(f2.length());

​    // e.获取文件的最后修改时间
​    long time = f2.lastModified(); // 时间毫秒值
​    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss EEE a");
​    System.out.println(sdf.format(time));
}

}
```

## File类的创建和删除的方法

```java
import java.io.File;
import java.io.IOException;

/**
     目标：File类的创建和删除的方法
     - public boolean createNewFile() ：当且仅当具有该名称的文件尚不存在时，
              创建一个新的空文件。 （几乎不用的，因为以后文件都是自动创建的！）
     - public boolean delete() ：删除由此File表示的文件或目录。 （只能删除空目录）
     - public boolean mkdir() ：创建由此File表示的目录。（只能创建一级目录）
     - public boolean mkdirs() ：可以创建多级目录（建议使用的）
 */
public class FileDemo03 {
    public static void main(String[] args) throws IOException {
        File f = new File("day10-demo/src/dlei02.txt");
        // a.创建新文件，创建成功返回true ,反之 ,不需要这个，以后文件写出去的时候都会自动创建
        System.out.println(f.createNewFile());

        // b.mkdir创建一级目录
        File f2 = new File("C:/图片资源/aaa");
        System.out.println(f2.mkdir());

        // c.mkdirs创建多级目录(重点)
        File f3 = new File("C:/图片资源/ggg/ccc/ddd");
        System.out.println(f3.mkdirs());

        // d.删除文件或者空文件夹
        File f4 = new File("day10-demo/src/dlei02.txt");
        System.out.println(f4.delete());

        // 只能删除空文件夹,不能删除非空文件夹.
        File f5 = new File("C:/图片资源/");
        System.out.println(f5.delete());
    }
}


```

## File针对目录的遍历

```java

import java.io.File;
import java.util.Arrays;

/**

    目标：File针对目录的遍历
    - public String[] list()：
         获取当前目录下所有的"一级文件名称"到一个字符串数组中去返回。
    - public File[] listFiles()(常用)：
         获取当前目录下所有的"一级文件对象"到一个文件对象数组中去返回（重点）
 */
public class FileDemo04 {
    public static void main(String[] args) {
        // 1、定位一个目录
        File f = new File("C:\\course");
        // 获取当前目录下所有的"一级文件名称"到一个字符串数组中去返回。
        String[] names = f.list();
        for (String name : names) {
            System.out.println(name);
        }

        // 2.一级文件对象
        // 获取当前目录下所有的"一级文件对象"到一个文件对象数组中去返回（重点）
        File[] files = f.listFiles();
        for (File file : files) {
            System.out.println(file.getAbsolutePath());
        }

        // 注意事项
        File f2 = new File("C:/图片资源/meimei.jpg");
        File[] files2 = f2.listFiles();
        System.out.println(files2);
    }
}


```

## [递归](https://edu.csdn.net/course/detail/40020?utm_source=glcblog&spm=1001.2101.3001.7020)实现文件搜索(非规律递归)

```java
import java.io.File;
import java.io.IOException;

/**
    目标：递归实现文件搜索(非规律递归)
    需求：希望去C:目录寻找出“传智加密器.exe”文件。
    分析：
        （1）定义一个方法用于做搜索。
        （2）进入方法中进行业务搜索分析。

 */
public class FileSearchExecDemo05 {
    public static void main(String[] args) {
        searchFiles(new File("C:/") , "传智加密器");
    }
    /**
      去某个磁盘中寻找某个文件
     * @param dir  磁盘路径
     * @param fileName  文件名称
     */
    public static void searchFiles(File dir , String fileName){
        if(dir != null && dir.isDirectory() && fileName != null){
            // 开始搜素文件夹
            // 1、得到全部的一级文件对象的数组
            File[] files = dir.listFiles();
            if(files != null && files.length > 0){
                // 2、存在一级文件对象，遍历全部一级文件对象。
                for (File file : files) {
                    // 3、看当前这个file对象是否是文件，是文件就判断是否是我要找的
                    if(file.isFile()){
                        if(file.getName().contains(fileName)){
                            System.out.println("找到了地址：" + file.getAbsolutePath());
//                            try {
//                                Runtime r = Runtime.getRuntime();
//                                r.exec(file.getAbsolutePath()); // 启动该软件
//                            } catch (Exception e) {
//                                e.printStackTrace();
//                            }
                        }
                    }else {
                        // 4、如果当前file是文件夹，递归进入继续寻找
                        searchFiles(file , fileName);
                    }
                }
            }
        }else{
            System.out.println("你传入的参数有问题，不满足查询条件！");
        }
    }
}






```

