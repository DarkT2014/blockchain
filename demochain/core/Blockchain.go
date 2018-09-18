package core

import "log"

type Blockchain struct {
	Blocks []*Block
}

func NewBlockchain()  *Blockchain{
	genesisBlock := GenerteGenesisBlock()
	blockchain := Blockchain{}
	blockchain.AppendBlock(&genesisBlock)
	return &blockchain
}
func (bc *Blockchain)SendData(data string)  {
	preBlock := bc.Blocks[len(bc.Blocks)-1]
	newBlock := GenerateNewBlock(*preBlock, data)
	bc.AppendBlock(&newBlock)
}

func (bc *Blockchain)AppendBlock(newBlock *Block)  {
	if isVaild(*newBlock,*bc.Blocks[len(bc.Blocks)-1]) {
		bc.Blocks = append(bc.Blocks,newBlock)
	} else {
		log.Fatal("inVaild block")
	}
}

func isVaild(newBlock Block,oldBlock Block) bool {
	if newBlock.Index - 1 != oldBlock.Index {
		return false
	}
	if newBlock.PreBlockHash != oldBlock.Hash {
		return false
	}
	if calculateHash(newBlock) != newBlock.Hash {
		return false
	}
	return true
}