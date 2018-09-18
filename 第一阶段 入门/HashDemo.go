package main

import (
	"crypto/sha256"
	"encoding/hex"
	"log"
)

func calculateHash(toBeHashed string)  string{
	hashInBytes := sha256.Sum256([]byte(toBeHashed))
	log.Printf("%",[]byte(toBeHashed))
	log.Printf("%",hashInBytes)
	hashInStr := hex.EncodeToString(hashInBytes[:])
	log.Printf("%",hashInBytes[:])
	//log.Printf("% %",toBeHashed,hashInStr)
	return hashInStr
}
func main()  {
	calculateHash("test1")
	calculateHash("test1")
	calculateHash("test2")
}