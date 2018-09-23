# 构建自己的区块链
. 实现链式结构
. 实现一个简单的http server 对外暴露接口
. 效果展示

# 实现步骤
## 1. 创建block
> 新建工程demochain\
> 创建 Block 文件\
> 创建block结构体和相关函数
### 遇到问题
[字节切片与字符串疑惑](https://www.cnblogs.com/taoshihan/p/9156355.html)

## 2. 创建blockchain
> 创建blockchain文件\
> 创建blockchain结构体和相关方法

## 3. 创建http server
> 创建Http Server
> 提供api访问接口

## 总结
1. 了解了什么是区块链
2. 区块链的架构模型
3. 区块链基本模型的实现

## 运行方式

查看效果
http://localhost:8888/block/chain/write?data=%22send-2%22
http://localhost:8888/block/chain/get