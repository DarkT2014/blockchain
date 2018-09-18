package core

import (
	"crypto/sha256"
	"encoding/hex"
	"time"
)

type Block struct {
	Index int64 //区块编号
	Timestamp int64 //区块时间戳
	PreBlockHash string //上一个区块的hash值
	Hash string //当前区块的hash值
	Data string //区块数据
}

func calculateHash(b Block) string {
	blockData := string(b.Index) + string(b.Timestamp) + b.PreBlockHash + b.Data
	hashInBytes := sha256.Sum256([]byte(blockData))
	return hex.EncodeToString(hashInBytes[:])
}
func GenerateNewBlock(preBlock Block,data string) Block {
	newBlock := Block{}
	newBlock.Index = preBlock.Index + 1
	newBlock.PreBlockHash = preBlock.Hash
	newBlock.Timestamp = time.Now().Unix()
	newBlock.Hash = calculateHash(newBlock)
	return Block{}
}
func GenerteGenesisBlock()  Block{
	preBlock :=Block{}
	preBlock.Index = -1
	preBlock.Hash = ""
	return GenerateNewBlock(preBlock,"Genesis Block")
}