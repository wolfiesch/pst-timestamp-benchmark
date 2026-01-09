package main

import (
	"fmt"
	"time"
)

func main() {
	loc, _ := time.LoadLocation("America/Los_Angeles")
	now := time.Now().In(loc)

	// Format: MM/DD/YYYY HH:MM AM/PM MST
	fmt.Println(now.Format("01/02/2006 03:04 PM MST"))
}
