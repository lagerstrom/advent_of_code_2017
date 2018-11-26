package main

import (
	"fmt"
	"io/ioutil"
	"strings"
	"strconv"
	"time"
	"sync"
)

var inputMap map[int][]Component
var wg sync.WaitGroup
var highestScore int
var longestBridge Bridge

type Component struct {
	Num1 int
	Num2 int
}

func (c *Component) getScore() int {
	return c.Num1 + c.Num2
}

type Bridge struct {
	BridgeComponents map[Component]bool
	LastComponent Component
	NextNum int
}

func (b *Bridge) addComponent(c Component, currentNum int){
	if b.BridgeComponents == nil {
		b.BridgeComponents = map[Component]bool{}
	}

	b.BridgeComponents[c] = true
	b.LastComponent = c

	if currentNum == c.Num1 {
		b.NextNum = c.Num2
	}
	if currentNum == c.Num2 {
		b.NextNum = c.Num1
	}
}

func (b *Bridge) ComponentInBridge(c Component) bool {
	_, ok := b.BridgeComponents[c]
	return ok
}

func (b *Bridge) getLastComponent() Component {
	return b.LastComponent
}

func (b *Bridge) getBridge() map[Component]bool {
	return b.BridgeComponents
}

func (b *Bridge) getNextPort() int {
	return b.NextNum
}

func (b *Bridge) calculateScore() int {
	var score int
	for c := range b.BridgeComponents {
		score += c.getScore()
	}
	return score
}

func (b *Bridge) getLength() int {
	return len(b.BridgeComponents)
}

func parseInput(inputFile string) (returnMap map[int][]Component) {
	returnMap = map[int][]Component{}

	data, err := ioutil.ReadFile(inputFile)

	if err != nil {
		fmt.Println("ERROR READING: ", err.Error())
	}

	stringData := string(data)

	for _, line := range strings.Split(stringData, "\n") {
		if line == "" {
			continue
		}

		lineSplit := strings.Split(line, "/")
		var num1, num2 int
		num1, _ = strconv.Atoi(lineSplit[0])
		num2, _ = strconv.Atoi(lineSplit[1])

		c := Component{
			num1,
			num2,
		}

		returnMap[num1] = append(returnMap[num1], c)
		returnMap[num2] = append(returnMap[num2], c)
	}

	return
}

func worker(bridgeQueue chan Bridge, b Bridge) {
	if highestScore < b.calculateScore() {
		highestScore = b.calculateScore()
	}

	if b.getLength() >= longestBridge.getLength() {
		if b.getLength() == longestBridge.getLength() {
			if b.calculateScore() > longestBridge.calculateScore() {
				longestBridge = b
			}
		} else {
			longestBridge = b
		}
	}

	for _, c := range inputMap[b.getNextPort()] {
		if b.ComponentInBridge(c) == false {
			newBridge := Bridge{}
			for oldComponent := range b.getBridge() {
				newBridge.addComponent(oldComponent, b.getNextPort())
			}
			newBridge.addComponent(c, b.getNextPort())
			bridgeQueue <- newBridge
		}
	}

	wg.Done()
}

func main() {

	inputMap = parseInput("big_input.txt")
	bridgeQueue := make(chan Bridge, 300000)

	for _, c := range inputMap[0] {
		b := Bridge{}
		b.addComponent(c, 0)
		bridgeQueue <- b
	}

	outerLoop:for {
		select {
		case b := <-bridgeQueue:
			wg.Add(1)
			go worker(bridgeQueue, b)
		case <-time.After(time.Millisecond * 10):
			wg.Wait()
			break outerLoop
		}
	}

	fmt.Println("Solution 1: ", highestScore)
	fmt.Println("Solution 2: ", longestBridge.calculateScore())
}
