package main

import (
	"fmt"
	"html/template"
	"io"
	"log"
	"math/rand"
	"net/http"
)

type User struct {
    Name string
    Age int
}

type Todo struct {
    Title string
    Done bool
}

func initServer() { 
    fmt.Printf("Listening on http://localhost:8000\n")
    log.Fatal(http.ListenAndServe(":8000", nil))
}

func main(){
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request){
        log.Println(r.Method, r.URL.Path, r.RemoteAddr)
        io.WriteString(w, "Hello World")
    })

    http.HandleFunc("/json", func(w http.ResponseWriter, r *http.Request){
        w.Header().Set("Content-Type", "application/json")
        io.WriteString(w, `{"message": "Hello World"}`)
    })

    http.HandleFunc("/struct", func(w http.ResponseWriter, r *http.Request){
        w.Header().Set("Content-Type", "application/json")
        user := User{"John", 20}
        io.WriteString(w, `{"name": "` + user.Name + `", "age": ` + fmt.Sprintf("%d", user.Age) + `}`)
    })

    http.HandleFunc("/html", func(w http.ResponseWriter, r *http.Request){
        tpl := template.Must(template.ParseFiles("index.html"))
        ctx := map[string][]Todo{
            "Todos": {
                {Title: "Task 1", Done: true},
                {Title: "Task 2", Done: false},
            },
        }
        tpl.Execute(w, ctx)
    })

    http.HandleFunc("/random", func(w http.ResponseWriter, r *http.Request){
        fmt.Fprintf(w, "%d", rand.Intn(100))
    })

    initServer()
}
