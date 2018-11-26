package main

import (
	"fmt"
	"strconv"
	"io/ioutil"
	"strings"
)

type Registers map[string]int

func (r Registers) getValue(inputString string) int {
	if inputInt, err := strconv.Atoi(inputString); err == nil {
		return inputInt
	}
	inputInt, _ := r[inputString]
	return inputInt
}

func (r Registers) add(x, y string) {
	xInt := r.getValue(x)
	yInt := r.getValue(y)

	if yInt < 0 {
		yInt = yInt * -1
	}

	newVal := xInt + yInt
	r[y] = 0
	r[x] = newVal
}

func (r Registers) set(x, y string) {
	inputInt := r.getValue(y)
	r[x] = inputInt
}

func (r Registers) sub(x, y string) {
	xInt := r.getValue(x)
	yInt := r.getValue(y)

	newVal := xInt - yInt

	r[x] = newVal
}

func (r Registers) mul(x, y string) {
	xInt := r.getValue(x)
	yInt := r.getValue(y)

	newVal := xInt * yInt

	r[x] = newVal
}

func (r Registers) jnz(x, y string) int {
	xInt := r.getValue(x)
	yInt := r.getValue(y)

	if xInt != 0 {
		return yInt - 1
	}

	return 0
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func deleteEmpty (s []string) []string {
    var r []string
    for _, str := range s {
        if str != "" {
            r = append(r, str)
        }
    }
    return r
}

func parseInstruction(instructionLine string) (token, x, y string) {
	instructionList := strings.Split(instructionLine, " ")

	token = instructionList[0]
	x = instructionList[1]
	y = instructionList[2]

	return
}

func main(){
	data, err := ioutil.ReadFile("/home/alexander/repo/advent_of_code_2017/lagerstrom-python/day23/puzzle_input.txt")
	check(err)
	dataString := string(data)

	mulInstructions := 0

	instructionList := strings.Split(dataString, "\n")
	instructionList = deleteEmpty(instructionList)

	cp := Registers{}

	//cp.set("a", "1")
	/*cp.set("d", "2")
	cp.set("e", "108340")
	cp.set("g", "0")
	cp.set("f", "1")
	cp.set("b", "108400")
	*/

	for i := 0; i < len(instructionList); i++ {
		token, x, y := parseInstruction(instructionList[i])

		switch token {
		case "set":
			cp.set(x, y)
		case "sub":
			cp.sub(x, y)
		case "mul":
			cp.mul(x, y)
			mulInstructions += 1
		case "jnz":
			i += cp.jnz(x, y)
		case "add":
			cp.add(x, y)
		}


	}

	fmt.Println(mulInstructions)
}
