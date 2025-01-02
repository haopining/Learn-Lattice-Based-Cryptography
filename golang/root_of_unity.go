package main

import (
	"fmt"
	"math"
	"math/cmplx"
)

func main() {
	n := 4 // Change 'n' to compute nth roots of unity
	roots := RootsOfUnity(n)
	for i, root := range roots {
		fmt.Printf("Root %d: %v\n", i, root)
	}
}

func RootsOfUnity(n int) []complex128 {
	roots := make([]complex128, n)
	for k := 0; k < n; k++ {
		theta := 2 * math.Pi * float64(k) / float64(n)
		roots[k] = cmplx.Exp(complex(0, theta))
	}
	return roots
}
