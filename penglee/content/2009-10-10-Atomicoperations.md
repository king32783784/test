Title: 原子操作
Date:2009-10-10
Author:李鹏
Slug: UNIX
Tags:unix编程
category:unix环境编程

#### 一、追加至一个文件

一个进程，将数据添加到一个文件尾端。早期不支持open的O_APPEND选项。所有程序被编写成下列形式

    if (lseek(fd, 0L, 2 ) < 0) /* position to EOF*/

        err_sys("lseek error");

    if (write(fd, buf, 100) != 100) /* and write */

        err_sys("write error");

单个进程而言，可以正常工作，但若有多个进程同事使用这种方法将数据添加到同一文件，则会产生问题。

UNIX系统提供了一种方法使这种操作成为原子操作。该方法是在打开文件时设置O_APPEND标志。使内核每次对这种文件进行写之前，都将当前偏移量设置到该文件的尾端处，每次写之前就不在需要调用lseek。


#### 二、pread和 pwrite函数

原型如下：

    #include　＜unistd.h>

    ssize_t pread (int filedes, void *buf, size_t nbytes, off_t offset);

    返回值：读到的字节数，若已到文件结尾则返回0，若出错则返回-1

    ssize_t pwrite(int filedes, const void *buf, size_t nbytes, off_t offset);

    若成功，返回已写的字节数，若出错则返回-1
    调用pread相当于顺序调用lseek和read,但是pread与这种顺序调用存在区别
    调用pread时，无法中断其定位和读写作。
    不能更新文件指针


#### 三、创建一个文件

当用open进行打开文件时，如果该文件已经存在，open将失败。检查文件是否存在和创建该文件这两个操作是作为一个原子操作执行的。如果没有这个原子操作，需要用下面程序段。

    if((fd = open(pathname, O_WRONLY)) < 0 ) {

        if （errno == ENOENT) {

            if ((fd = creat(pathname, mode)) < 0)
                err_sys("creat error");
        } else {

            err_sys("open error");

        }

    }

如果在open和creat之间，另一个进程创建了该文件，那么就会引起问题。例如，若在这两个函数调用之间，另一个进程创建了该文件，并且写进了一些数据。然后，原先的进程执行这段程序的creat。刚由另一个进程写上去的数据就会被擦除。这样两则合并为一个原子操作，就不会发生该问题。


一般而言，原子操作，指的是由多步组成的操作，如果操作原子地执行，那么执行完所有步骤，要么不执行，不可能只执行一部分。

Top[^]()
