package main

import (
	"cli/config"
	"cli/oauth2"
	"fmt"
	"log"
)

func main() {
	c, err := config.Parse()
	if err != nil {
		log.Fatal(err)
	}
	o, err := oauth2.NewOauth2(c)
	if err != nil {
		log.Fatal(err)
	}
	o.Authenticate()
	token := o.GetToken()
	fmt.Println(token)
}
