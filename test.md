# Bitcoin-Transaction-SigHash-Type

## 交易结构
### 交易完整结构
大小 | 字段 | 描述
--- |---|---
4字节 | 版本 | 明确这笔交易的规则
1-9字节 | 输入计数器 | 被包含输入的数量
不定 | 输入 | 一个或多个的交易输入
1-9字节 | 输出计数器 | 被包含输出的数量
不定 | 输出 | 一个或多个的交易输出
4字节 | 时钟时间 | 一个UNIX时间戳或区块号

### 交易输入结构
大小 | 字段 | 描述
--- |---|---
32字节 | 交易id | 指向交易包含的被花费的UTXO的哈希指针
4字节 | 输出索引 | 被花费的UTXO的索引号(第一个是0)
1-9字节(可变整数) | 解锁脚本尺寸 | 用字节表示的后面解锁脚本的长度
不定 | 解锁脚本 | 一个达到UTXO锁定脚本中的条件的脚本
4字节 | 序列号 | 用于交易替换功能


### 交易输出结构
大小 | 字段 | 描述
--- |---|---
8字节 | 总量 | 用聪表示的比特币值（10-8比特币）
1-9字节(可变整数) | 锁定脚本尺寸 | 用字节表示的后面锁定脚本的长度
不定 | 锁定脚本 | 一个定义了支付输出所需条件的脚本

### 交易序列化数据
```
020000000145be3643feeef08c916eaa214e1e548ae731faa627e81d5fbed8df4b4ff02309010000006a473044
022005890429142e03a473848b734048ca2a21d3f4899a7b6f2beb7746fd970418f0022035994cf1612ee846d6
e011edee91117af1ff7b72e175e6c0be8d527fbe37a97f0121036715c95e80a42bffaa3f9d4cc018611323647b
3949277456f6282cce78af7f2afeffffff02a0860100000000001976a9143bf7bf2d3b23ae5ca5510a473eb1e5
4b5019cc6f88ac329f1000000000001976a91472ee81a593469bc2127d5902f7562f98823d6fcc88acc5fd1100
```

### 反序列化交易数据
```
版本号 : 02000000
输入数量 : 01
交易id : 45be3643feeef08c916eaa214e1e548ae731faa627e81d5fbed8df4b4ff02309
输入输出索引 : 01000000
解锁脚本尺寸 : 6a
解锁脚本 : 473044022005890429142e03a473848b734048ca2a21d3f4899a7b6f2beb7746fd970418f00220359
          94cf1612ee846d6e011edee91117af1ff7b72e175e6c0be8d527fbe37a97f0121036715c95e80a42b
          ffaa3f9d4cc018611323647b3949277456f6282cce78af7f2afe
序列号 : ffffffff          
输出索引 : 01000000
输出数量 : 02
输出比特币总量: a086010000000000
锁定脚本尺寸 : 19
锁定脚本：76a91472ee81a593469bc2127d5902f7562f98823d6fcc88ac
时钟时间 : c5fd1100
```

## Bitcoin SIGHASH_TYPE(比特币签名类型)

```
SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
SIGHASH_ANYONECANPAY = 0x80
SIGHASH_ALL | SIGHASH_ANYONECANPAY = 0x81
SIGHASH_NONE | SIGHASH_ANYONECANPAY = 0x82
SIGHASH_SINGLE | SIGHASH_ANYONECANPAY = 0x83
```

### SIGHASH_ALL
```
SIGHASH_ALL : 对交易的所有输入和所有的输出进行签名，不能对输入以及输出进行更改
demo: 020000000145be3643feeef08c916eaa214e1e548ae731faa627e81d5fbed8df4b4ff02309010000006a473044
      022005890429142e03a473848b734048ca2a21d3f4899a7b6f2beb7746fd970418f0022035994cf1612ee846d6
      e011edee91117af1ff7b72e175e6c0be8d527fbe37a97f0121036715c95e80a42bffaa3f9d4cc018611323647b
      3949277456f6282cce78af7f2afeffffff02a0860100000000001976a9143bf7bf2d3b23ae5ca5510a473eb1e5
      4b5019cc6f88ac329f1000000000001976a91472ee81a593469bc2127d5902f7562f98823d6fcc88acc5fd1100
```

###  SIGHASH_NONE
```
SIGHASH_NONE : 只对交易的所有输入进行签名，不能对输入进行更改，但可以更改输出部分
demo: 0100000001f7e816a5b7a1505fa112bc9a22c671f6fa6dd19c7b784903013ee121cbd2d24b000000006a473044
      02204b6099ff4db636b1785e18d00aa4c36691287cdeda07b26e371672c7597741d502202a48716deb1b03c752
      4906eace39f26f0372d50ca53c189f454458f4a037a2ad0221030c6eade5aab087c421ad7dff43f7ff0f3b68da
      1ca37329cf67ce37cf79ecf827ffffffff01a0491a01000000000000000000
```
### SIGHASH_SINGLE
```
SIGHASH_SINGLE : 对交易所有的输入与输出进行签名，其中输出的索引，必须与输入里的输出索引保持一致
demo: 0100000001e63404207fed9358691a1224f67d7dffb2d1d8457011c88b90dfaf6cc910cdf8000000006a473044
      02202d6deaaa443051e35c4b6564252fe01a832fef4bbb8fd03a938214e4192993a102202ba77fdafbdb614bee
      67898a0b23a2fd72ed0f26c7d7fbfc049d05aa285fcbb30321030c6eade5aab087c421ad7dff43f7ff0f3b68da
      1ca37329cf67ce37cf79ecf827ffffffff01e069f902000000001976a9143bf7bf2d3b23ae5ca5510a473eb1e5
      4b5019cc6f88ac00000000 
```
### SIGHASH_ANYONECANPAY
```
SIGHASH_ANYONECANPAY : 可以单独的对自己的交易输入进行签名,添加或删除交易的输入.此SIGHASH类型需和上述三种一起搭配使用

SIGHASH_ALL |SIGHASH_ANYONECANPAY : 对所有输出和一个输入进行签名，可以对交易的其他输入进行添加或者删除，但不可对输出进行更改
SIGHASH_NONE |SIGHASH_ANYONECANPAY : 对交易的一个输入进行签名，可以对交易的其他输入进行添加或删除，也可以对交易的输出进行添加或删除
SIGHASH_SIGNLE |SIGHASH_ANYONECANPAY : 对交易的一个输出以及对应输出索引的输入，可以对交易的其他输入进行添加或删除，但对输出不可更改
```

## Core Function
```
def RawSignatureHash(script, txTo, inIdx, hashtype):
    """Consensus-correct SignatureHash

    Returns (hash, err) to precisely match the consensus-critical behavior of
    the SIGHASH_SINGLE bug. (inIdx is *not* checked for validity)

    If you're just writing wallet software you probably want SignatureHash()
    instead.
    """
    HASH_ONE = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    if inIdx >= len(txTo.vin):
        return (HASH_ONE, "inIdx %d out of range (%d)" % (inIdx, len(txTo.vin)))
    txtmp = bitcoin.core.CMutableTransaction.from_tx(txTo)

    for txin in txtmp.vin:
        txin.scriptSig = b''
    txtmp.vin[inIdx].scriptSig = FindAndDelete(script, CScript([OP_CODESEPARATOR]))

    if (hashtype & 0x1f) == SIGHASH_NONE:
        txtmp.vout = []

        for i in range(len(txtmp.vin)):
            if i != inIdx:
                txtmp.vin[i].nSequence = 0

    elif (hashtype & 0x1f) == SIGHASH_SINGLE:
        outIdx = inIdx
        if outIdx >= len(txtmp.vout):
            return (HASH_ONE, "outIdx %d out of range (%d)" % (outIdx, len(txtmp.vout)))

        tmp = txtmp.vout[outIdx]
        txtmp.vout = []
        for i in range(outIdx):
            txtmp.vout.append(bitcoin.core.CTxOut())
        txtmp.vout.append(tmp)
        
        for i in range(len(txtmp.vin)):
            if i != inIdx:
                txtmp.vin[i].nSequence = 0
    if hashtype & SIGHASH_ANYONECANPAY:
        tmp = txtmp.vin[inIdx]
        txtmp.vin = []
        txtmp.vin.append(tmp)
        
    s = txtmp.serialize()
    s += struct.pack(b"<I", hashtype)
    hash = bitcoin.core.Hash(s)
    return (hash, None)
```
## Tests Function
```
def test():
    SIGHASH_ALL = 1
    SIGHASH_NONE = 2
    SIGHASH_SINGLE = 3
    SIGHASH_ANYONECANPAY = 0x80


    bitcoin.SelectParams('testnet')

    seckey = CBitcoinSecret("cNySSdN2BEHrmhPpeJxj68xKmgBYxKXZ7mmQMZ38RZbqLxbxdsuE")
    txid = lx('f8cd10c96cafdf908bc8117045d8d1b2ff7d7df624121a695893ed7f200434e6')
    vout = 0

    txin = CMutableTxIn(COutPoint(txid, vout))
    txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(seckey.pub), OP_EQUALVERIFY, OP_CHECKSIG])
    txout = [CMutableTxOut(0.499*COIN,CBitcoinAddress('mkz2x7w5QqqJQMYBWihWMYFHssdj8ANx4g').to_scriptPubKey())]  
    tx = CMutableTransaction([txin], txout)

    sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_SINGLE)

    k = set_secretbytes(seckey)
    set_compressed(True,k)
    sig = sign(sighash,k) + bytes([SIGHASH_SINGLE])
    txin.scriptSig = CScript([sig,seckey.pub])
    return b2x(tx.serialize())
```

## Reference Implementations
```
https://bitcoin.org/en/developer-guide#signature-hash-types
https://bitcoin.org/en/glossary/sighash-all
git@github.com:petertodd/python-bitcoinlib.git
```

