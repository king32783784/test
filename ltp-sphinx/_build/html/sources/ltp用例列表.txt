LTP－Case list
==============

主要模块
---------------

case主要分为”commands"、“kdump"、"kernel"、"misc"、"network"、"open_posix_testsuite"、"realtime"、"lib"等部分，主要内容如下：

==========  ========
　分类        包含内容
==========  ========
commands    ade、cpio、df、eject、gzip、logrotate、mail、mkfs、sshd、tar、unzip、
            which、at、cron、du、fileutils、insmod、lsmod、mkswap、su tmp-tools、wc
kernel      connectors、controllers、firmware、hotplug、input、ipc、logging、mce-test、module、power_management、sched、syscalls、tracing、containers、device-drivers、fs、include、io、lib、mem、numa、pty、security、times
misc        crash、f00f、math
open_posix  functional、tools、bin、conformance、stress
network     busy_poll、dctcp、iptables、netstress、nfsv4、rpc、stress、tcp_fstopen、virt、can、dhcp iproute、lib6、multicast、nfs、sockets、tcp_cmds、traceroute、xinetd
realtime    perf、profiles、stress
==========  ========

commands部分
---------------

commands包含用例:

=========  =========
  case        包含用例
=========  =========
ade          ar、file、ld、ldd、nm、objdump、size
at           at
pio          cpio
cron         cron
cp           ln、mkdir、mv
gzip         gzip
insmod       insmod 
logrotate    logrotate
lsmod        lsmod
mail         mail
mkfs         mkfs
mkswap       mkswap
sssd         sssd
su           su
tar          tar
tpm-tools    tmp、tpmtoken
unzip        unzip
wc           wc 
which        which
=========  =========


kernel部分
-----------

主要case包括:

================= =========
 case              包含用例　
================= =========
connectors         connector,pec
containers         libclone,mountns,mqns,netns,pidns,share,sysvipc,userns,utsname
controllers        cgroup,cgroup_xattr,cpuctl,cpuset,io-throttle,memcg,pids,cgroup_fg,cpuacct,cpuctl_fj,freezer,libcontrollers,memctl
device-drivers     acpi,base,cpufreq,drm,locking,misc_modules,pci,tbio,usb,zram,agp,block,dev_sim_framework,nls,rcu,rtc,uaccess,v4l
firmware           fw_load_kernel,fw_load_user,
fs                 acl,dmapi,ext4-new-features,fs_blnd,fs_inod,fs_perms,fsstress,ftest,iso9660,linktest,mongo,proc,racer,stram,acls,doio,fs-bench,fs_di,fs_main,fs_readonly,fsx-linux,inode,lftest,openfile,quota_remount,scsi
hotplug            cpu_hotplug,memory_hotplug
input              input
io                 aio,direct_io,disktest,ltp-aiodio,stress_cd,stress_floppy,writetest
ipc                pipeio,semaphore
logging            kmsg
mem                cpuset,mem,mtest01,mtest06,oom,shmt,thp,vma,hugetlb,ksm,mmapstress,mtest05,mtest07,page,swapping,tunable,vmtests
moudle             create_module,delete_module,query_module
numa               numa
power_management   pm_ilb_test,runpwtests01-06,runpwtests_exelusive01-06,pm_cpu_consolidation,pm_include,pm_sched_domain
pty                hangup,ptem,pty
sched              cfs-scheduler,clisrv,hypertherading,nptl,process_stress,pthreads,sched_stress,tool
security           cap_bound,filecaps,integrity,mmc_security,prot_hsymlinks,securbits,smack,tomoyo
syscalls           abort,accept,accept4,access,acct,add_key,adjtimex,alarm,asyncio,bdflush,bind,brk,cacheflush,capget,capset,chdir,chmod,chown,chroot,clock_getres,clock_nanosleep,clock_nanosleep2,clone,close,cma,confstr,connect,creat,dup,dup2,dup3,epoll,epoll2,epoll_create1,epoll_ctl,epoll_pwait,epoll_wait,eventfd,eventfd2,execl,execle,execlp,execv,execve,execvp,exit,exit_group,faccessat,fadvise,fallocate,fanotify,fchdir,fchmod,fchmodat,fchown,fchownat,fcntl,fdatasync,flock,fmtmsg,fork,fpathconf,fstat,fstatat,fstatfs,fsync,ftruncate,futex,futimesat,getcontext,getcpu,getcwd,getdents,getdomainname,getdtablesize,getegid,geteuid,getgid,getgroups,gethostbyname_r,gethostid,gethostname,getitimer,get_mempolicy,getpagesize,getpeername,getpgid,getpgrp,getpid,getppid,getpriority,getrandom,getresgid,getresuid,getrlimit,get_robust_list,getrusage,getsid,getsockname,getsockopt,gettid,gettimeofday,getuid,getxattr,inotify,inotify_init,io_cancel,ioctl,io_destroy,io_getevents,ioperm,iopl,io_setup,io_submit,ipc,kcmp,keyctl,kill,lchown,lgetxattr,link,linkat,listen,llistxattr,llseek,lseek,lstat,madvise,Makefile,mallopt,mbind,memcmp,memcpy,memmap,memset,migrate_pages,mincore,mkdir,mkdirat,mknod,mknodat,mlock,mlockall,mmap,modify_ldt,mount,move_pages,mprotect,mq_notify,mq_open,mq_timedreceive,mq_timedsend,mq_unlink,mremap,msync,munlock,munlockall,munmap,nanosleep,newuname,nftw,nice,open,openat,paging,pathconf,pause,perf_event_open,personality,pipe,pipe2,poll,ppoll,prctl,pread,preadv,profil,pselect,ptrace,pwrite,pwritev,quotactl,read,readahead,readdir,readlink,readlinkat,readv,reboot,recv,recvfrom,recvmsg,remap_file_pages,removexattr,rename,renameat,renameat2,request_key,rmdir,rt_sigaction,rt_sigprocmask,rt_sigqueueinfo,rt_sigsuspend,rt_sigtimedwait,sbrk,sched_getaffinity,sched_getattr,sched_getparam,sched_get_priority_max,sched_get_priority_min,sched_getscheduler,sched_rr_get_interval,sched_setaffinity,sched_setattr,sched_setparam,sched_setscheduler,sched_yield,select,send,sendfile,sendmsg,sendto,setdomainname,setegid,setfsgid,setfsuid,setgid,setgroups,sethostname,setitimer,setns,setpgid,setpgrp,setpriority,setregid,setresgid,setresuid,setreuid,setrlimit,set_robust_list,setsid,setsockopt,set_thread_area,set_tid_address,settimeofday,setuid,setxattr,sgetmask,sigaction,sigaltstack,sighold,signal,signalfd,signalfd4,sigpending,sigprocmask,sigrelse,sigsuspend,sigtimedwait,sigwait,sigwaitinfo,socket,socketcall,socketpair,sockioctl,splice,ssetmask,stat,statfs,statvfs,stime,string,swapoff,swapon,switch,symlink,symlinkat,sync,sync_file_range,syscall,sysconf,sysctl,sysfs,sysinfo,syslog,tee,time,timerfd,timer_getoverrun,timer_gettime,times,tkill,truncate,ulimit,umask,umount,umount2,uname,unlink,unlinkat,unshare,ustat,utils,utime,utimensat,utimes,vfork,vhangup,vmsplice,wait,wait4,waitid,waitpid,write,writev
timers             clock_gettime,clock_settime,leapsec,timer_create,timer_delete,timer_settime
tracing            ftrace
================= =========

misc部分
--------

主要用例包括：

====== ===========
case    包含子case　
====== ===========
crash    crash
f00f     foof
math     abs、atof、float、fptests、nextafter
====== ===========


network部分
----------------

主要用例包括：

=============== ===========
case             包含子case
=============== ===========
can               filter-test
dctcp             dctcp
dhcp              dhcp_tests,dhcp_lib,,dnsmasq_tests
iproute           ip_tests
iptables          iptables_tests
lib6              asapi,getaddrinfo,in6,
multicast         mc_cmds,mc_commo,mc_gethost,mc_member,mc_opts
netstress         netstress
nfs               fsx-linux,nfslock01,nfsstat01,nfs_stress
nfsv4             acl,locks
rpc               basic_tests,rpc-tirpc
sockets           socket
stress            broken_ip,dns,ftp,http,icmp,interface,,ipsec,multicast,ns-tools,route,ssh,tcp,udp
tcp_cmds          arping,echo,ftp,netstat,rcp,rsh,sendfile,tcpdump,trackpath,clockdiff,finger,host,ipneigh,ping,rdist,rlogin,rwho,ssh,telnet
tcp_fastopen      tcp_fastopen
traceroute        traceroute
virt              gre01,ipvlan,macvlan,macvtap,vlan,vxlan
=============== ===========

open_posix_testsuite部分 
--------------------------------

主要用例包括:

============ ==========
case         包含子case
============ ==========
 bin          run-all-posix-option-group-tests
conformance   behavior definitions interfaces
functional    mqueues semaphores threads timers
stress        mqueues semaphores signals threads timers
============ ==========

realtime部分
---------------
主要用例包括:

=========== ==========
 case        包含子case
=========== ==========
func         async_handler hrtimer-prio matrix_mult periodic_cpu_load pi-tests prio-wake rt-migrate sched_jitter thrad_clock gtod_latency measurement pi_perf prio-preempt pthread_kill_latency sched_football sched_letency
m4           m4
perf         latency 
stress       pi-tests
=========== ==========

接下来会深入分析每个case的具体测试目的及内容。ltp测试用例主要采用shell和Ｃ编写。

