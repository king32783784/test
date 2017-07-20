Title: 快速排序
Date:2013-07-01
Author:李鹏
Slug: sort
Tags:算法
category:算法

#### 1.快速排序
对于一个给定的数组，从中选择一个元素，以该元素为界将其余元素划分为两个子集，
一个子集的所有元素都小于该元素，另一个子集的元素都大于或等于该元素，
对两个子集递归执行这一过程，当某个子集中的元素小于二时，
这个子集就不需要再次排序，终止递归。

#### 2.代码实现及测试
```c
    void qsort(int v[],int left,int right)
    {
        int i,last;
        void swap(int v[],int i,int j);
        if(left>=right)
            return;
        swap(v,left,(left+right)/2); //将中点的元素作为比较元素，放到整个数组的最左边
        last = left;
        for(i=left+1;i<=right;i++)
            if(v[i]<v[left])
            swap(v,++last,i);
        swap(v,left,last); //last位置放的将是比较元素，左边全是比它小的元素
        qsort(v,left,last-1);//对子集1进行递归调用
        qsort(v,last+1,right);//对子集2进行递归调用
    }
    void swap(int v[],int i,int j)
    {
        int temp;
        temp=v[i];
        v[i]=v[j];
        v[j]=temp;
    }
    main()
    {
        int k=0;
        int test[]={3,2,6,4,5,9,11,7,16,8};
        qsort(test,0,9);
        for(k=0;k<10;k++)
        {
            printf("%d,",test[k]);
        }
    }
```

Top[^]()

