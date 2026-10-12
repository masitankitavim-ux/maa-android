package main

import (
	"archive/tar"
	"bytes"
	"compress/gzip"
	"embed"
	"encoding/json"
	"fmt"
	"image"
	"image/color"
	"image/png"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"time"
)

//go:embed webui/*
var webui embed.FS

type Config struct {
	Port        int    `json:"port"`
	LibDir      string `json:"lib_dir"`
	DataDir     string `json:"data_dir"`
	ClientType  string `json:"client_type"`
	Package     string `json:"package"`
	Width       int    `json:"width"`
	Height      int    `json:"height"`
	DisplayID   int    `json:"display_id"`
	TouchMode   string `json:"touch_mode"`
	ForceStop   bool   `json:"force_stop"`
	AdbAddress  string `json:"adb_address"`
	AdbPort     int    `json:"adb_port"`
	AutoStart   bool   `json:"auto_start"`
	DefaultTask string `json:"default_task"`

	ScheduleEnabled bool           `json:"schedule_enabled"`
	ScheduleTime    string         `json:"schedule_time"`
	ScheduleLaunch  bool           `json:"schedule_launch"`
	ScheduleTasks   []ScheduleTask `json:"schedule_tasks"`
	ScheduleLastRun string         `json:"schedule_last_run"`
}

type ScheduleTask struct {
	Type   string `json:"type"`
	Params string `json:"params"`
}

var cfg Config
var cfgMu sync.Mutex
var cfgPath string

func defaultConfig(dataDir, libDir string) Config {
	return Config{
		Port:            8790,
		LibDir:          libDir,
		DataDir:         dataDir,
		ClientType:      "Official",
		Package:         "com.hypergryph.arknights",
		Width:           1280,
		Height:          720,
		DisplayID:       0,
		TouchMode:       "Android",
		ForceStop:       true,
		AdbAddress:      "",
		AdbPort:         0,
		AutoStart:       false,
		DefaultTask:     "StartUp,Fight,Recruit,Infrast,Mall,Award",
		ScheduleEnabled: false,
		ScheduleTime:    "04:00",
		ScheduleLaunch:  true,
		ScheduleTasks:   []ScheduleTask{},
	}
}

func loadConfig() {
	cfgMu.Lock()
	defer cfgMu.Unlock()
	b, err := os.ReadFile(cfgPath)
	if err != nil {
		return
	}
	var c Config
	if json.Unmarshal(b, &c) == nil {
		cfg = c
	}
}

func saveConfig() error {
	cfgMu.Lock()
	defer cfgMu.Unlock()
	b, _ := json.MarshalIndent(cfg, "", "  ")
	return os.WriteFile(cfgPath, b, 0600)
}

// ---- event hub ----
type eventHub struct {
	mu   sync.Mutex
	subs map[chan []byte]bool
	ring [][]byte
}

func newHub() *eventHub {
	return &eventHub{subs: map[chan []byte]bool{}}
}

func (h *eventHub) publish(e []byte) {
	h.mu.Lock()
	h.ring = append(h.ring, e)
	if len(h.ring) > 500 {
		h.ring = h.ring[len(h.ring)-500:]
	}
	for c := range h.subs {
		select {
		case c <- e:
		default:
		}
	}
	h.mu.Unlock()
}

func (h *eventHub) subscribe() chan []byte {
	h.mu.Lock()
	c := make(chan []byte, 256)
	h.subs[c] = true
	h.mu.Unlock()
	return c
}

func (h *eventHub) unsubscribe(c chan []byte) {
	h.mu.Lock()
	delete(h.subs, c)
	h.mu.Unlock()
}

func (h *eventHub) snapshot() [][]byte {
	h.mu.Lock()
	out := make([][]byte, len(h.ring))
	copy(out, h.ring)
	h.mu.Unlock()
	return out
}

var hub = newHub()

func eventLoop() {
	for e := range eventCh {
		b, _ := json.Marshal(e)
		hub.publish(b)
	}
}

func stateJSON() map[string]any {
	cfgMu.Lock()
	c := cfg
	cfgMu.Unlock()
	return map[string]any{
		"version":   coreVersionString(),
		"connected": maaConnected(),
		"running":   maaRunning(),
		"config":    c,
		"port":      c.Port,
	}
}

func writeJSON(w http.ResponseWriter, v any) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(v)
}

func httpError(w http.ResponseWriter, code int, msg string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	fmt.Fprintf(w, `{"error":%q}`, msg)
}

func extractArchive(archive, dest string) error {
	f, err := os.Open(archive)
	if err != nil {
		return err
	}
	defer f.Close()
	gz, err := gzip.NewReader(f)
	if err != nil {
		return err
	}
	defer gz.Close()
	root, err := filepath.Abs(dest)
	if err != nil {
		return err
	}
	if err := os.MkdirAll(root, 0755); err != nil {
		return err
	}
	tr := tar.NewReader(gz)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			return nil
		}
		if err != nil {
			return err
		}
		name := strings.TrimPrefix(hdr.Name, "./")
		if name == "" || name == "." {
			continue
		}
		target := filepath.Join(root, filepath.FromSlash(name))
		rel, err := filepath.Rel(root, target)
		if err != nil || rel == ".." || strings.HasPrefix(rel, ".."+string(filepath.Separator)) {
			return fmt.Errorf("invalid path in archive: %s", hdr.Name)
		}
		switch hdr.Typeflag {
		case tar.TypeDir:
			if err := os.MkdirAll(target, 0755); err != nil {
				return err
			}
		case tar.TypeReg, tar.TypeRegA:
			if err := os.MkdirAll(filepath.Dir(target), 0755); err != nil {
				return err
			}
			out, err := os.OpenFile(target, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, os.FileMode(hdr.Mode)&0777)
			if err != nil {
				return err
			}
			if _, err := io.Copy(out, tr); err != nil {
				out.Close()
				return err
			}
			out.Close()
		case tar.TypeSymlink:
			if err := os.MkdirAll(filepath.Dir(target), 0755); err != nil {
				return err
			}
			_ = os.Remove(target)
			if err := os.Symlink(hdr.Linkname, target); err != nil {
				return err
			}
		case tar.TypeLink:
			linkTarget := filepath.Join(root, filepath.FromSlash(strings.TrimPrefix(hdr.Linkname, "./")))
			if err := os.MkdirAll(filepath.Dir(target), 0755); err != nil {
				return err
			}
			_ = os.Remove(target)
			if err := os.Link(linkTarget, target); err != nil {
				return err
			}
		default:
			// skip other entry types
		}
	}
}

func ensureCore() {
	if maaCoreReady() {
		return
	}
	cfgMu.Lock()
	libDir, dataDir := cfg.LibDir, cfg.DataDir
	cfgMu.Unlock()
	if libDir == "" {
		libDir = "/data/adb/maa/lib"
	}
	if dataDir == "" {
		dataDir = "/data/adb/maa"
	}
	if err := maaLoad(libDir + "/libMaaCore.so"); err != nil {
		log.Printf("ensureCore: load core failed: %v", err)
		return
	}
	maaSetUserDir(dataDir)
	if maaLoadResource(dataDir) {
		log.Printf("ensureCore: resource loaded from %s", dataDir)
	} else {
		log.Printf("ensureCore: resource load failed from %s", dataDir)
	}
	if maaCreate() {
		log.Printf("ensureCore: MAA core created, version=%s", coreVersionString())
	}
}

func connectConfig(c Config) string {
	ext := c.LibDir + "/libMaaNativeExt.so"
	obj := map[string]any{
		"library_path":      ext,
		"screen_resolution": map[string]any{"width": c.Width, "height": c.Height},
		"display_id":        c.DisplayID,
		"force_stop":        c.ForceStop,
	}
	b, _ := json.Marshal(obj)
	return string(b)
}

func doConnect() {
	ensureCore()
	cfgMu.Lock()
	c := cfg
	cfgMu.Unlock()
	maaSetInstanceOption(2, c.TouchMode)  // TouchMode
	maaSetInstanceOption(6, c.ClientType) // ClientType
	address := ""
	if c.AdbAddress != "" {
		address = c.AdbAddress
		if c.AdbPort > 0 {
			address = fmt.Sprintf("%s:%d", c.AdbAddress, c.AdbPort)
		}
	}
	maaConnect("", address, connectConfig(c), true)
}

func main() {
	if len(os.Args) >= 4 && os.Args[1] == "-extract" {
		if err := extractArchive(os.Args[2], os.Args[3]); err != nil {
			log.Fatalf("extract failed: %v", err)
		}
		return
	}

	dataDir := flagString("data", "/data/adb/maa", "MAA data directory")
	libDir := flagString("lib", "/data/adb/maa/lib", "MAA library directory")
	portFlag := flagInt("port", 0, "override listen port")

	cfgPath = dataDir + "/config.json"
	cfg = defaultConfig(dataDir, libDir)
	if portFlag != 0 {
		cfg.Port = portFlag
	}
	loadConfig()
	if cfg.LibDir == "" {
		cfg.LibDir = libDir
	}
	if cfg.DataDir == "" {
		cfg.DataDir = dataDir
	}

	// load core
	if err := maaLoad(libDir + "/libMaaCore.so"); err != nil {
		log.Printf("WARN: load core failed: %v (will retry on connect)", err)
	}
	maaSetUserDir(dataDir)
	if maaLoadResource(dataDir) {
		if maaCreate() {
			log.Printf("MAA core initialized, version=%s", coreVersionString())
		}
	} else {
		log.Printf("WARN: load resource failed from %s", dataDir)
	}

	go eventLoop()
	go scheduleLoop()

	mux := http.NewServeMux()
	mux.HandleFunc("/", serveUI)
	mux.HandleFunc("/api/state", func(w http.ResponseWriter, r *http.Request) { writeJSON(w, stateJSON()) })
	mux.HandleFunc("/api/connect", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			httpError(w, 405, "POST only")
			return
		}
		var c Config
		if err := json.NewDecoder(r.Body).Decode(&c); err == nil {
			cfgMu.Lock()
			cfg.ClientType = c.ClientType
			cfg.Package = c.Package
			cfg.Width = c.Width
			cfg.Height = c.Height
			cfg.DisplayID = c.DisplayID
			cfg.TouchMode = c.TouchMode
			cfg.ForceStop = c.ForceStop
			cfg.AdbAddress = c.AdbAddress
			cfg.AdbPort = c.AdbPort
			cfgMu.Unlock()
			saveConfig()
		}
		go doConnect()
		writeJSON(w, map[string]any{"ok": true, "state": stateJSON()})
	})
	mux.HandleFunc("/api/start", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]any{"ok": maaStart()})
	})
	mux.HandleFunc("/api/stop", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]any{"ok": maaStop()})
	})
	mux.HandleFunc("/api/back_home", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]any{"ok": maaBackToHome()})
	})
	mux.HandleFunc("/api/click", func(w http.ResponseWriter, r *http.Request) {
		x, _ := strconv.Atoi(r.URL.Query().Get("x"))
		y, _ := strconv.Atoi(r.URL.Query().Get("y"))
		maaClick(x, y)
		writeJSON(w, map[string]any{"ok": true})
	})
	mux.HandleFunc("/api/screencap", func(w http.ResponseWriter, r *http.Request) {
		maaScreencap()
		writeJSON(w, map[string]any{"ok": true})
	})
	mux.HandleFunc("/api/append_task", func(w http.ResponseWriter, r *http.Request) {
		var req struct {
			Type   string `json:"type"`
			Params string `json:"params"`
		}
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			httpError(w, 400, "bad json")
			return
		}
		id := maaAppendTask(req.Type, req.Params)
		writeJSON(w, map[string]any{"id": id})
	})
	mux.HandleFunc("/api/set_task_params", func(w http.ResponseWriter, r *http.Request) {
		var req struct {
			ID     int    `json:"id"`
			Params string `json:"params"`
		}
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			httpError(w, 400, "bad json")
			return
		}
		writeJSON(w, map[string]any{"ok": maaSetTaskParams(req.ID, req.Params)})
	})
	mux.HandleFunc("/api/settings", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost {
			var c Config
			if err := json.NewDecoder(r.Body).Decode(&c); err == nil {
				cfgMu.Lock()
				c.DataDir = cfg.DataDir
				c.LibDir = cfg.LibDir
				c.Port = cfg.Port
				cfg = c
				cfgMu.Unlock()
				saveConfig()
			}
		}
		cfgMu.Lock()
		writeJSON(w, map[string]any{"config": cfg})
		cfgMu.Unlock()
	})
	mux.HandleFunc("/api/schedule", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost {
			var req struct {
				Enabled bool           `json:"enabled"`
				Time    string         `json:"time"`
				Launch  *bool          `json:"launch"`
				Tasks   []ScheduleTask `json:"tasks"`
			}
			if err := json.NewDecoder(r.Body).Decode(&req); err == nil {
				cfgMu.Lock()
				cfg.ScheduleEnabled = req.Enabled
				if req.Time != "" {
					cfg.ScheduleTime = req.Time
				}
				if req.Launch != nil {
					cfg.ScheduleLaunch = *req.Launch
				}
				if req.Tasks != nil {
					cfg.ScheduleTasks = req.Tasks
				}
				cfgMu.Unlock()
				saveConfig()
			}
		}
		cfgMu.Lock()
		enabled, at, launch, tasks, lastRun := cfg.ScheduleEnabled, cfg.ScheduleTime, cfg.ScheduleLaunch, cfg.ScheduleTasks, cfg.ScheduleLastRun
		cfgMu.Unlock()
		writeJSON(w, map[string]any{"enabled": enabled, "time": at, "launch": launch, "tasks": tasks, "last_run": lastRun})
	})
	mux.HandleFunc("/api/schedule/run", func(w http.ResponseWriter, r *http.Request) {
		go runScheduled()
		writeJSON(w, map[string]any{"ok": true})
	})
	mux.HandleFunc("/api/events", sseHandler)
	mux.HandleFunc("/api/screenshot.png", screenshotHandler)
	mux.HandleFunc("/api/update", func(w http.ResponseWriter, r *http.Request) {
		go runUpdate()
		writeJSON(w, map[string]any{"ok": true})
	})
	mux.HandleFunc("/api/update/status", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]any{"status": updateStatus.String()})
	})

	addr := fmt.Sprintf("0.0.0.0:%d", cfg.Port)
	log.Printf("maaweb listening on %s", addr)
	log.Fatal(http.ListenAndServe(addr, mux))
}

func serveUI(w http.ResponseWriter, r *http.Request) {
	p := strings.TrimPrefix(r.URL.Path, "/")
	if p == "" {
		p = "webui/index.html"
	} else if !strings.HasPrefix(p, "webui/") {
		p = "webui/" + p
	}
	b, err := webui.ReadFile(p)
	if err != nil {
		b, _ = webui.ReadFile("webui/index.html")
	}
	ct := "text/html; charset=utf-8"
	if strings.HasSuffix(p, ".css") {
		ct = "text/css"
	} else if strings.HasSuffix(p, ".js") {
		ct = "application/javascript"
	} else if strings.HasSuffix(p, ".webp") {
		ct = "image/webp"
	} else if strings.HasSuffix(p, ".png") {
		ct = "image/png"
	} else if strings.HasSuffix(p, ".svg") {
		ct = "image/svg+xml"
	} else if strings.HasSuffix(p, ".ico") {
		ct = "image/x-icon"
	}
	w.Header().Set("Content-Type", ct)
	w.Write(b)
}

func sseHandler(w http.ResponseWriter, r *http.Request) {
	fl, ok := w.(http.Flusher)
	if !ok {
		httpError(w, 500, "streaming unsupported")
		return
	}
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	c := hub.subscribe()
	defer hub.unsubscribe(c)
	for _, e := range hub.snapshot() {
		fmt.Fprintf(w, "data: %s\n\n", e)
	}
	fl.Flush()
	ticker := time.NewTicker(15 * time.Second)
	defer ticker.Stop()
	for {
		select {
		case e := <-c:
			fmt.Fprintf(w, "data: %s\n\n", e)
			fl.Flush()
		case <-ticker.C:
			fmt.Fprintf(w, ": keepalive\n\n")
			fl.Flush()
		case <-r.Context().Done():
			return
		}
	}
}

func screenshotHandler(w http.ResponseWriter, r *http.Request) {
	cfgMu.Lock()
	wcfg, hcfg := cfg.Width, cfg.Height
	cfgMu.Unlock()
	pngBytes, bgrBytes, imgW, imgH := getImage(64*1024*1024, wcfg, hcfg)
	if len(pngBytes) > 0 {
		w.Header().Set("Content-Type", "image/png")
		w.Write(pngBytes)
		return
	}
	if len(bgrBytes) > 0 && imgW > 0 && imgH > 0 && len(bgrBytes) >= imgW*imgH*3 {
		img := image.NewRGBA(image.Rect(0, 0, imgW, imgH))
		for y := 0; y < imgH; y++ {
			for x := 0; x < imgW; x++ {
				off := (y*imgW + x) * 3
				img.SetRGBA(x, y, color.RGBA{R: bgrBytes[off+2], G: bgrBytes[off+1], B: bgrBytes[off], A: 255})
			}
		}
		var buf bytes.Buffer
		if png.Encode(&buf, img) == nil {
			w.Header().Set("Content-Type", "image/png")
			w.Write(buf.Bytes())
			return
		}
	}
	httpError(w, 404, "no image")
}

// update handling (runs maactl update as subprocess)
var updateStatus = &syncString{val: "idle"}

type syncString struct {
	mu  sync.Mutex
	val string
}

func (s *syncString) String() string {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.val
}

func (s *syncString) set(v string) {
	s.mu.Lock()
	s.val = v
	s.mu.Unlock()
}

func runUpdate() {
	updateStatus.set("running")
	defer updateStatus.set("done")
	cmd := exec.Command("sh", "/system/bin/maactl", "update")
	out, err := cmd.CombinedOutput()
	if err != nil {
		updateStatus.set("error: " + err.Error() + " " + string(out))
		return
	}
	updateStatus.set("ok: " + string(out))
}

func scheduleLoop() {
	for {
		time.Sleep(15 * time.Second)
		cfgMu.Lock()
		enabled, at, lastRun := cfg.ScheduleEnabled, cfg.ScheduleTime, cfg.ScheduleLastRun
		cfgMu.Unlock()
		if !enabled || at == "" {
			continue
		}
		now := time.Now()
		if now.Format("15:04") != at {
			continue
		}
		today := now.Format("2006-01-02")
		if lastRun == today {
			continue
		}
		cfgMu.Lock()
		cfg.ScheduleLastRun = today
		cfgMu.Unlock()
		saveConfig()
		log.Printf("schedule triggered at %s", at)
		runScheduled()
	}
}

func launchGame() {
	cfgMu.Lock()
	pkg := cfg.Package
	cfgMu.Unlock()
	if pkg == "" {
		pkg = "com.hypergryph.arknights"
	}
	cmd := exec.Command("sh", "-c", "monkey -p '"+pkg+"' -c android.intent.category.LAUNCHER 1")
	out, err := cmd.CombinedOutput()
	if err != nil {
		log.Printf("launchGame monkey failed: %v %s", err, out)
		return
	}
	log.Printf("launchGame ok: %s", strings.TrimSpace(string(out)))
	time.Sleep(8 * time.Second)
}

func runScheduled() {
	cfgMu.Lock()
	launch := cfg.ScheduleLaunch
	tasks := append([]ScheduleTask(nil), cfg.ScheduleTasks...)
	cfgMu.Unlock()
	if !maaConnected() {
		doConnect()
	}
	if launch {
		log.Printf("runScheduled: launching game")
		launchGame()
	}
	maaStop()
	for _, t := range tasks {
		if t.Type == "" {
			continue
		}
		maaAppendTask(t.Type, t.Params)
	}
	maaStart()
}

// tiny flag helpers (avoid flag package conflict with embedded usage)
func flagString(name, def, usage string) string {
	for i, a := range os.Args {
		if a == "-"+name && i+1 < len(os.Args) {
			return os.Args[i+1]
		}
		if strings.HasPrefix(a, "-"+name+"=") {
			return strings.TrimPrefix(a, "-"+name+"=")
		}
	}
	return def
}

func flagInt(name string, def int, usage string) int {
	s := flagString(name, "", usage)
	if s == "" {
		return def
	}
	v, _ := strconv.Atoi(s)
	return v
}

var _ = io.Discard
