package main

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

func main() {
	r := gin.Default()

	// Health check for Kubernetes Liveness/Readiness probes
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "UP"})
	})

	// Metrics endpoint for Prometheus
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))

	// API Routes
	r.GET("/users/:id", func(c *gin.Context) {
		id := c.Param("id")
		// Simulate database lookup
		c.JSON(http.StatusOK, User{
			ID:    id,
			Name:  "Netflix Engineer",
			Email: "engineer@netflix-lab.io",
		})
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8081"
	}

	r.Run(":" + port)
}
