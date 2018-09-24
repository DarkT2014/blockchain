// 版本声明
pragma solidity ^0.4.0;
// 引入
import "solidity_for_import";
// this is a test Contract
contract Test {
    uint a;
    // 函数
    function setA(uint x) public{
        a = x;
        emit Set_A(x);
    }
    // 事件
    event Set_A(uint a);

    // 定义结构类型
    struct Pos {
        int lat;
        int lng;
    }

    // 
    address public oweraddr;
    // 函数修改器 类似于装饰器
    modifier ower() {
        require(msg.sender==oweraddr);
        _;
    }
    function mine() public owner{
        a+=1;
    }
}