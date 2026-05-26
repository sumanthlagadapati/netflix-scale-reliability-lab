package main

import (
	"log"
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
	// Open log file for appending
	f, err := os.OpenFile("catalog-service.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatalf("Failed to open log file: %v", err)
	}
	defer f.Close()
	log.SetOutput(f)
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	r := gin.Default()

	// Health check
	r.GET("/health", func(c *gin.Context) {
		log.Printf("Health check from %s", c.ClientIP())
		c.JSON(http.StatusOK, gin.H{"status": "UP"})
	})

	// Metrics
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))

	// API Routes
	r.GET("/movies", func(c *gin.Context) {
		log.Printf("Movies endpoint hit from %s", c.ClientIP())
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

	log.Printf("Catalog service started on :%s", port)
	r.Run(":" + port)
}
