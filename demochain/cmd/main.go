package cmd

import "blockchain/demochain/core"

func main()  {
	bc := core.NewBlockchain()
	bc.SendData("Send 1")
	bc.SendData("Send 2")
	bc.SendData("Send 3")
}

