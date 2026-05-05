package main

import (
	"math/rand"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type Movie struct {
	ID       string `json:"id"`
	Title    string `json:"title"`
	Genre    string `json:"genre"`
	Duration string `json:"duration"`
}

func main() {
	r := gin.Default()

	// Health check
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "UP"})
	})

	// Metrics
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))

	// API Routes
	r.GET("/movies", func(c *gin.Context) {
		// Simulate network latency (between 10ms and 200ms)
		delay := rand.Intn(190) + 10
		time.Sleep(time.Duration(delay) * time.Millisecond)

		movies := []Movie{
			{ID: "1", Title: "Stranger Things", Genre: "Sci-Fi", Duration: "50m"},
			{ID: "2", Title: "The Crown", Genre: "Drama", Duration: "60m"},
			{ID: "3", Title: "Money Heist", Genre: "Crime", Duration: "45m"},
		}
		c.JSON(http.StatusOK, movies)
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8082"
	}

	r.Run(":" + port)
}
