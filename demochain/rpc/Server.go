package main

import (
	"blockchain/demochain/core"
	"encoding/json"
	"io"
	"net/http"
)

var blockchain  *core.Blockchain
func run()  {
	http.HandleFunc("/block/chain/get",blockchainGetHandle)
	http.HandleFunc("/block/chain/write",blockchainWriteHandle)
	http.ListenAndServe("localhost:8888",nil)
}
func blockchainGetHandle(w http.ResponseWriter,r *http.Request)  {
	bytes,err :=json.Marshal(blockchain)
	if err !=nil {
		http.Error(w,err.Error(),http.StatusInternalServerError)
		return
	}
	io.WriteString(w,string(bytes))
}
func blockchainWriteHandle(w http.ResponseWriter,r *http.Request)  {
	blockData := r.URL.Query().Get("data")
	blockchain.SendData(blockData)
	blockchainGetHandle(w,r)
}
func main()  {
	blockchain = core.NewBlockchain()
	run()
}