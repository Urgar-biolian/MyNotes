

public String() ：初始化新创建的 String对象，以使其表示空字符序列
String(String original)： 初始化一个新创建的 String 对象，使其表示一个与参数相同的字符序列；换句话说，新创建的字符串是该参数字符串的副本
public String(char[] value) ：通过当前参数中的字符数组来构造新的String
public String(char[] value,int offset, int count) ：通过字符数组的一部分来构造新的String

```java
import java.util.Scanner;

public class Main {
 public static void str (String[] args) {
        // 使用无参构造函数创建一个空字符串
        String emptyString = new String();
        System.out.println(emptyString); // 输出: ""
    }
    public static void main(String[] args) {
        // 创建一个字符数组
        char[] charArray = {'H', 'e', 'l', 'l', 'o'};
        // 使用字符数组构造一个新的字符串
        String stringFromCharArray = new String(charArray);
        System.out.println(stringFromCharArray); // 输出: Hello
    }
    public static void main(String[] args) {
        // 创建一个字符数组
        char[] charArray = {'H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd'};
        // 使用字符数组的一部分构造一个新的字符串
        // 从索引2开始，取5个字符
        String stringFromCharArrayPart = new String(charArray, 2, 5);
        System.out.println(stringFromCharArrayPart); // 输出: llo W
    }

}
```

## 二`String`与字节数组的转换（编码与解码）

### 字符串 --> 字节[数组](https://edu.csdn.net/course/detail/40020?utm_source=glcblog&spm=1001.2101.3001.7020)：（编码）

public byte[] getBytes() ：使用平台的默认字符集将此 String 编码为 byte 序列，并将结果存储到一个新的 byte 数组中
public byte[] getBytes(String charsetName) ：使用指定的字符集将此 String 编码到 byte 序列，并将结果存储到新的 byte 数组

```java
byte[] b_gbk = "中".getBytes("gbk");
byte[] b_utf8 = "中".getBytes("utf-8");
byte[] b_iso88591 = "中".getBytes("iso-8859-1");
```



### 字节数组 --> 字符串：（解码）

```java
String(byte[])：通过使用平台的默认字符集解码指定的 byte 数组，构造一个新的 String
String(byte[]，int offset，int length) ：用指定的字节数组的一部分，即从数组起始位置offset开始取length个字节构造一个字符串对象
String(byte[], String charsetName ) 或 new String(byte[], int, int,String charsetName )：解码，按照指定的编码方式进行解码

```

```java
String s_gbk = new String(b_gbk, "gbk");
String s_utf8 = new String(b_utf8, "utf-8");
String s_iso88591 = new String(b_iso88591, "iso-8859-1");
```

*打印出s_gbk、s_utf8、s_iso88591可以看到，s_gbk和s_utf8都是"中"，而s_iso88591是一个乱码*
*这是因为iso-8859-1的编码表中，根本就没有包含汉字*
*因此"中".getBytes(“iso-8859-1”)得到的是"?“的字节数组表示*
*再通过new String(b_iso88591, “iso-8858-1”)还原得到的是”?"*
*————————————————*

### iso-8859-1的特殊用法

有时候，为了让中文字符适应某些特殊要求(如http header要求其内容必须是iso-8859-1编码)
可能会通过将中文字符按照字节方式来编码的情况，如：

```java
String s_iso88591 = new String("中".getBytes("utf-8"), "iso-8859-1");

```

 得到的字符串s_iso88591实际上是三个在iso-8859-1中的字符，在将这些字符传送到目的地后，再通过相反的方式，即：

```java
String s_utf8 = new String(s_iso88591.getBytes("iso-8859-1"), "utf-8");
```


从而得到正确的中文汉字"中"，这样就既保证了遵守协议规定，也支持了中文

## 三、常用API

1、常用方法
boolean isEmpty()：字符串是否为空
int length()：返回字符串的长度
String concat(xx)：拼接
boolean equals(Object obj)：比较字符串是否相等，区分大小写
boolean equalsIgnoreCase(Object obj)：比较字符串是否相等，不区分大小写
int compareTo(String other)：比较字符串大小，区分大小写，按照Unicode编码值比较大小
int compareToIgnoreCase(String other)：比较字符串大小，不区分大小写
String toLowerCase()：将字符串中大写字母转为小写
String toUpperCase()：将字符串中小写字母转为大写
String trim()：去掉字符串前后空白符
public String intern()：结果在常量池中共享

```java
@Test
public void test1(){
    String s1 = "hello";
    String s2 = "HellO";
    System.out.println(s1.equals(s2));
    System.out.println(s1.equalsIgnoreCase(s2));
```



```java
String s3 = "abcd";
String s4 = "adef";
System.out.println(s3.compareTo(s4));

String s5 = "abcd";
String s6 = "aBcd";
System.out.println(s5.compareTo(s6));
System.out.println(s5.compareToIgnoreCase(s6));

String s7 = "张ab";
String s8 = "李cd";
System.out.println(s7.compareTo(s8));

String s9 = " he  llo   ";
System.out.println("****" + s9.trim() + "*****");
}
```


2、查找
boolean contains(xx)：是否包含xx
int indexOf(xx)：从前往后找当前字符串中xx，即如果有返回第一次出现的下标，要是没有返回-1
int indexOf(String str, int fromIndex)：返回指定子字符串在此字符串中第一次出现处的索引，从指定的索引开始
int lastIndexOf(xx)：从后往前找当前字符串中xx，即如果有返回最后一次出现的下标，要是没有返回-1
int lastIndexOf(String str, int fromIndex)：返回指定子字符串在此字符串中最后一次出现处的索引，从指定的索引开始反向搜索
@Test
public void test2(){
    String s1 = "教育尚硅谷教育";
    System.out.println(s1.contains("硅谷")); // true

```java
System.out.println(s1.indexOf("教育")); // 0
System.out.println(s1.indexOf("教育",1)); // 5

System.out.println(s1.lastIndexOf("教育")); // 5
System.out.println(s1.lastIndexOf("教育",4)); // 0
```
}

11

```java
3、字符串截取
String substring(int beginIndex) ：返回一个新的字符串，它是此字符串的从beginIndex开始截取到最后的一个子字符串
String substring(int beginIndex, int endIndex) ：返回一个新字符串，它是此字符串从beginIndex开始截取到endIndex(不包含)的一个子字符串
@Test
public void test3(){
    String s1 = "教育尚硅谷教育";
    System.out.println(s1.substring(2)); // 尚硅谷教育
    System.out.println(s1.substring(2,5));//[2,5) // 尚硅谷
}

4、和字符/字符数组相关
char charAt(index)：返回[index]位置的字符
char[] toCharArray()： 将此字符串转换为一个新的字符数组返回
static String valueOf(char[] data) ：返回指定数组中表示该字符序列的 String
static String valueOf(char[] data, int offset, int count) ： 返回指定数组中表示该字符序列的 String
@Test
public void test4(){
    String s1 = "教育尚硅谷教育";
    System.out.println(s1.charAt(2)); // 尚
	// valueOf和copyValueOf源码一模一样的，就是用char数组new String(char[] ch)
    String s2 = String.valueOf(new char[]{'a', 'b', 'c'}); // abc
    String s3 = String.copyValueOf(new char[]{'a', 'b', 'c'}); // abc
}

5、开头与结尾
boolean startsWith(xx)：测试此字符串是否以指定的前缀开始
boolean startsWith(String prefix, int toffset)：测试此字符串从指定索引开始的子字符串是否以指定前缀开始
boolean endsWith(xx)：测试此字符串是否以指定的后缀结束
@Test
public void test5(){
    String s1 = "教育尚硅谷教育";
    System.out.println(s1.startsWith("教育a")); // false
    System.out.println(s1.startsWith("教育",5)); // true
}

6、替换
String replace(char oldChar, char newChar)：返回一个新的字符串，它是通过用 newChar 替换此字符串中出现的所有 oldChar 得到的。 不支持正则
String replace(CharSequence target, CharSequence replacement)：使用指定的字面值替换序列替换此字符串所有匹配字面值目标序列的子字符串
String replaceAll(String regex, String replacement)：使用给定的 replacement 替换此字符串所有匹配给定的正则表达式的子字符串
String replaceFirst(String regex, String replacement)：使用给定的 replacement 替换此字符串匹配给定的正则表达式的第一个子字符串
@Test

public void test6(){
    String s1 = "hello";
    String s2 = s1.replace('l', 'w');
    System.out.println(s1); // hello
    System.out.println(s2); // hewwo

String s3 = s1.replace("ll", "wwww");
System.out.println(s3); // hewwwwo

}


```

