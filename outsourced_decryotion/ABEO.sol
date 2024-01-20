pragma solidity ^0.4.22;
contract ABEO{
    //公钥以及转化公钥的hash值
    string public keyshash;
    //用于结算的hash值
    bytes32 public hashRoot;
    //验证秘钥
    string public wk;
    //密文数量
    uint256 public n;
   
    address public owner;
    address public cloud;
    // 验证状态，-1表示还未进行验证
    int F;
    int Q;
    uint256 fund;

    string transform;
    string signature;

    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Sender not authorized."
            );
        _;
    }

    modifier onlyCloud() {
        require(
            msg.sender == cloud,
            "Sender not authorized."
            );
        _;
    }

    //用户部署智能合约，公布pk，tk，vk以及各种参数的hash值
    constructor(bytes32  _hashroot,uint _n,string memory _keyshash) public payable {
        owner = msg.sender;
        hashRoot = _hashroot;
        keyshash = _keyshash;
        n = _n;
        F = -1;
        Q = -1;
        fund = msg.value;
        // emit getevent(msg.sender);

    }
    
    //获取公钥以及转化秘钥
    function getkeyshash(address _cloud) public returns(string memory) {
        //记录云账户，方便结算
        cloud = _cloud;
        return keyshash;
    }

    //验证转化秘钥-----只能用户调用
    function verifyTkVk(string memory _pk,string memory _tk,string memory _vk,string memory _rkeys,string memory _wk) public onlyOwner{
        wk = _wk;
        if(veriTV(_rkeys,_pk,_tk,_vk,_wk,keyshash) == true){
            F = 1;
        }
        else{
            F = 0;
            //用户提供的转化秘钥不正确，则默认云进行了正确的转化计算，无需再验证
            Q = 1;
        }
        //云计算的安全性还未验证
        if(Q == -1){
            if(bytes(transform).length == 0){
                //云未提交验证请求
                return;
            }
            else{
                // 云提交验证请求时，wk未提交，无法进行验证
                if(veriCipher(transform,signature,wk) == true){
                    //云计算正确
                    Q = 1;
                }
                else{
                    //云计算不正确
                    Q = 0;
                }
            }
        }
        else{
            if(F == 1 && Q == 1) {
            //两边计算都正确，则认为云提供了重复的计算结果
                owner.transfer(address(this).balance);            
            }
            else if(F == 1 && Q == 0){
            //用户提供了正确的转化秘钥，云计算错误
                owner.transfer(address(this).balance);            
            }
            else {
            //用户未提供正确的转化秘钥
                cloud.transfer(fund/n);
                owner.transfer(address(this).balance);            
            }   
        }

    } 
    //验证云计算结果----只能云调用
    function verifyCipher(string memory _transform, string memory _sig,bytes memory _hash) public onlyCloud {
        //首先结算已得酬金
        if (_hash.length > 0){
            payment(_hash);

        }
        if(F == 0){
            //用户为提供正确的转化秘钥，云计算的正确性无需再进行验证
            cloud.transfer(fund/n);
            owner.transfer(address(this).balance);  
            return;
        }
        //此时用户还未提交wk，无法进行验证
        if (bytes(wk).length == 0){
            transform = _transform;
            signature = _sig;
            return;
        }
        //验证云计算的正确性
        if(veriCipher(_transform,_sig,wk) == true){
            Q = 1;
        }
        else {
            Q = 0;
        }
        if(F == 1 && Q == 1) {
            //两边计算都正确，则认为云提供了重复的计算结果
            owner.transfer(address(this).balance); 
            return;           
        }
        else if(F == 1 && Q == 0){
            //用户提供了正确的转化秘钥，云计算错误
            owner.transfer(address(this).balance); 
            return;           
        }
        else {
            //用户未提供正确的转化秘钥
            cloud.transfer(fund/n);
            owner.transfer(address(this).balance); 
            return;           
        } 
    }
    //验证云hash值，结算酬金---只能云调用
    function payment(bytes memory _hash) public onlyCloud {
        fund = address(this).balance;
        uint256 x = 0;
        bytes32 temphash;
        bytes memory hashvalues = _hash;
        while(true){
            temphash = sha256(hashvalues);
            x++;
            if(temphash == hashRoot || x > n){
                if(x > n){
                    return;
                }else{
                    msg.sender.transfer(address(this).balance/n * x);
                    return;
                }
                
            }
            hashvalues = abi.encodePacked(temphash);
        }
    }
}
