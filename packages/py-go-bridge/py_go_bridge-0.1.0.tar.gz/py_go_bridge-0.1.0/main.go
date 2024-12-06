package main

import (
	"pygo/pkg/export"
)

func call_excel() {
	dbConfig := export.DBConfig{
		Host:     "localhost",
		Port:     3306,
		User:     "root",
		Password: "hashchat",
		Database: "llx",
	}
	export.ExportItemsTask("cobazaar", dbConfig, 500)
}

func main() {
	call_excel()
	// fmt.Printf("Export result: %+v\n", result)
}
