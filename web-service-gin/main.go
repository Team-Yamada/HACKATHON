package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// 1
type book struct {
	ID     string  `json:"id"`
	Title  string  `json:"title"`
	Author string  `json:"author"`
	Price  float64 `json:"price"`
}

// 2
var books = []book{
	{ID: "1", Title: "こころ", Author: "夏目　漱石", Price: 56.99},
	{ID: "2", Title: "人間失格", Author: "太宰　治", Price: 17.99},
	{ID: "3", Title: "羅生門", Author: "芥川　龍之介", Price: 39.99},
}

// 4
func main() {
	router := gin.Default()
	router.GET("/books", getBooks)

	router.Run("localhost:8080")
}

// 3
func getBooks(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, books)
}
