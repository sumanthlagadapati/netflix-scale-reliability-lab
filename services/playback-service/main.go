package main

import (
	"math/rand"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type PlaybackResponse struct {
	MovieID  string `json:"movie_id"`
	StreamURL string `json:"stream_url"`
	Quality  string `json:"quality"`
	Token    string `json:"token"`
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
	r.GET("/play/:id", func(c *gin.Context) {
		id := c.Param("id")

		// Simulate intermittent failure (5% chance) to test Chaos/Resiliency
		if rand.Intn(100) < 5 {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal Server Error - Chaos Simulation"})
			return
		}

		c.JSON(http.StatusOK, PlaybackResponse{
			MovieID:   id,
			StreamURL: "https://cdn.netflix-lab.io/stream/" + id + ".m3u8",
			Quality:   "4K-UltraHD",
			Token:     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
		})
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8083"
	}

	r.Run(":" + port)
}
