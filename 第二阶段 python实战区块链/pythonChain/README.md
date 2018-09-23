# 200行代码实现基础的区块链

## 实现功能函数
. 节点注册\
. 创建新的区块\
. 创建交易区块\
. 生成hash函数\
. 获取区块链最后一个元素\
. 工作量证明\
. 验证工作量证明\
. 验证是不是一个有效的链条\
. 共识机制 \
. 交易\

## 如果想验证共识机制
 1. python3 blockchain.py -p 5001  
 
 2. python3 blockchain.py -p 5000
 
 3. 127.0.0.1:5000/chain [get]
 
 4. 127.0.0.1:5000/transactions/new [post]
 
 > {\
	"sender":"mengjie",\
	"recipient":"quankang",\
	"amount":5\
}

 5. 127.0.0.1:5000/mine [get]
 
 6. 127.0.0.1:5001/nodes/register [post]
 > {\
	"nodes":["http://127.0.0.1:5000"]\
}

 7. 127.0.0.1:5000/nodes/register [post]
 > {\
	"nodes":["http://127.0.0.1:5001"]\
}

 8. 127.0.0.1:5001/chain [get]
 
 9. 127.0.0.1:5001/nodes/resolve [get]
 
 10. 127.0.0.1:5001/chain [get]