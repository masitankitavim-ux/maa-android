package main

/*
#cgo LDFLAGS: -ldl
#include <stdlib.h>
#include <string.h>
#include <dlfcn.h>
#include <stdint.h>

typedef uint8_t AsstBool;
typedef uint64_t AsstSize;
typedef int32_t AsstId;
typedef void (*AsstApiCallback)(AsstId msg, char* details_json, void* custom_arg);

extern void maaCallback(AsstId msg, char* details_json, void* custom_arg);

static void* g_h = 0;

static AsstBool (*fSetUserDir)(const char*) = 0;
static AsstBool (*fLoadResource)(const char*) = 0;
static AsstBool (*fSetStaticOption)(int, const char*) = 0;
static void* (*fCreateEx)(AsstApiCallback, void*) = 0;
static void (*fDestroy)(void*) = 0;
static AsstBool (*fSetInstanceOption)(void*, int, const char*) = 0;
static AsstId (*fAsyncConnect)(void*, const char*, const char*, const char*, AsstBool) = 0;
static AsstId (*fAppendTask)(void*, const char*, const char*) = 0;
static AsstBool (*fSetTaskParams)(void*, AsstId, const char*) = 0;
static AsstBool (*fStart)(void*) = 0;
static AsstBool (*fStop)(void*) = 0;
static AsstBool (*fRunning)(void*) = 0;
static AsstBool (*fConnected)(void*) = 0;
static AsstBool (*fBackToHome)(void*) = 0;
static AsstSize (*fGetImage)(void*, void*, AsstSize) = 0;
static AsstSize (*fGetImageBgr)(void*, void*, AsstSize) = 0;
static AsstSize (*fGetNullSize)(void) = 0;
static AsstId (*fAsyncClick)(void*, int32_t, int32_t, AsstBool) = 0;
static AsstId (*fAsyncScreencap)(void*, AsstBool) = 0;
static const char* (*fGetVersion)(void) = 0;
static void (*fLog)(const char*, const char*) = 0;

static int maa_load(const char* path) {
    g_h = dlopen(path, RTLD_NOW | RTLD_GLOBAL);
    if (!g_h) return -1;
    *(void**)&fSetUserDir = dlsym(g_h, "AsstSetUserDir");
    *(void**)&fLoadResource = dlsym(g_h, "AsstLoadResource");
    *(void**)&fSetStaticOption = dlsym(g_h, "AsstSetStaticOption");
    *(void**)&fCreateEx = dlsym(g_h, "AsstCreateEx");
    *(void**)&fDestroy = dlsym(g_h, "AsstDestroy");
    *(void**)&fSetInstanceOption = dlsym(g_h, "AsstSetInstanceOption");
    *(void**)&fAsyncConnect = dlsym(g_h, "AsstAsyncConnect");
    *(void**)&fAppendTask = dlsym(g_h, "AsstAppendTask");
    *(void**)&fSetTaskParams = dlsym(g_h, "AsstSetTaskParams");
    *(void**)&fStart = dlsym(g_h, "AsstStart");
    *(void**)&fStop = dlsym(g_h, "AsstStop");
    *(void**)&fRunning = dlsym(g_h, "AsstRunning");
    *(void**)&fConnected = dlsym(g_h, "AsstConnected");
    *(void**)&fBackToHome = dlsym(g_h, "AsstBackToHome");
    *(void**)&fGetImage = dlsym(g_h, "AsstGetImage");
    *(void**)&fGetImageBgr = dlsym(g_h, "AsstGetImageBgr");
    *(void**)&fGetNullSize = dlsym(g_h, "AsstGetNullSize");
    *(void**)&fAsyncClick = dlsym(g_h, "AsstAsyncClick");
    *(void**)&fAsyncScreencap = dlsym(g_h, "AsstAsyncScreencap");
    *(void**)&fGetVersion = dlsym(g_h, "AsstGetVersion");
    *(void**)&fLog = dlsym(g_h, "AsstLog");
    if (!fSetUserDir || !fLoadResource || !fCreateEx || !fDestroy || !fSetInstanceOption ||
        !fAsyncConnect || !fAppendTask || !fStart || !fStop) return -2;
    return 0;
}

static int maa_set_user_dir(const char* p) { return fSetUserDir ? fSetUserDir(p) : 0; }
static int maa_load_resource(const char* p) { return fLoadResource ? fLoadResource(p) : 0; }
static void* maa_create(void) { return fCreateEx ? fCreateEx((AsstApiCallback)maaCallback, 0) : 0; }
static void maa_destroy(void* h) { if (fDestroy) fDestroy(h); }
static int maa_set_inst(void* h, int k, const char* v) { return fSetInstanceOption ? fSetInstanceOption(h, k, v) : 0; }
static AsstId maa_connect(void* h, const char* a, const char* addr, const char* cfg, int block) { return fAsyncConnect ? fAsyncConnect(h, a, addr, cfg, (AsstBool)block) : 0; }
static AsstId maa_append_task(void* h, const char* t, const char* p) { return fAppendTask ? fAppendTask(h, t, p) : 0; }
static int maa_set_task_params(void* h, AsstId id, const char* p) { return fSetTaskParams ? fSetTaskParams(h, id, p) : 0; }
static int maa_start(void* h) { return fStart ? fStart(h) : 0; }
static int maa_stop(void* h) { return fStop ? fStop(h) : 0; }
static int maa_running(void* h) { return fRunning ? fRunning(h) : 0; }
static int maa_connected(void* h) { return fConnected ? fConnected(h) : 0; }
static int maa_back_home(void* h) { return fBackToHome ? fBackToHome(h) : 0; }
static AsstSize maa_get_image(void* h, void* b, AsstSize n) { return fGetImage ? fGetImage(h, b, n) : (AsstSize)-1; }
static AsstSize maa_get_image_bgr(void* h, void* b, AsstSize n) { return fGetImageBgr ? fGetImageBgr(h, b, n) : (AsstSize)-1; }
static AsstSize maa_null_size(void) { return fGetNullSize ? fGetNullSize() : (AsstSize)-1; }
static AsstId maa_click(void* h, int32_t x, int32_t y, int block) { return fAsyncClick ? fAsyncClick(h, x, y, (AsstBool)block) : 0; }
static AsstId maa_screencap(void* h, int block) { return fAsyncScreencap ? fAsyncScreencap(h, (AsstBool)block) : 0; }
static const char* maa_version(void) { return fGetVersion ? fGetVersion() : ""; }
*/
import "C"

import (
	"fmt"
	"sync"
	"unsafe"
)

// Event is one callback message forwarded from MaaCore.
type Event struct {
	Msg  int    `json:"msg"`
	JSON string `json:"json"`
}

var (
	eventCh     = make(chan Event, 4096)
	coreMu      sync.Mutex
	coreHandle  unsafe.Pointer
	coreInited  bool
	coreVersion string
)

//export maaCallback
func maaCallback(msg C.AsstId, json *C.char, _ unsafe.Pointer) {
	if json == nil {
		return
	}
	select {
	case eventCh <- Event{Msg: int(msg), JSON: C.GoString(json)}:
	default:
	}
}

// DrainEvents returns all currently buffered events.
func DrainEvents() []Event {
	out := []Event{}
	for {
		select {
		case e := <-eventCh:
			out = append(out, e)
			if len(out) > 10000 {
				return out
			}
		default:
			return out
		}
	}
}

func maaLoad(path string) error {
	cpath := C.CString(path)
	defer C.free(unsafe.Pointer(cpath))
	if C.maa_load(cpath) != 0 {
		return fmt.Errorf("dlopen failed for %s", path)
	}
	coreVersion = C.GoString(C.maa_version())
	return nil
}

func maaSetUserDir(path string) bool {
	cpath := C.CString(path)
	defer C.free(unsafe.Pointer(cpath))
	return C.maa_set_user_dir(cpath) == 1
}

func maaLoadResource(path string) bool {
	cpath := C.CString(path)
	defer C.free(unsafe.Pointer(cpath))
	return C.maa_load_resource(cpath) == 1
}

func maaCoreReady() bool {
	return coreHandle != nil
}

func maaCreate() bool {
	h := C.maa_create()
	if h == nil {
		return false
	}
	coreHandle = h
	return true
}

func maaDestroy() {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle != nil {
		C.maa_destroy(coreHandle)
		coreHandle = nil
	}
	coreInited = false
}

func maaSetInstanceOption(key int, value string) bool {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return false
	}
	cv := C.CString(value)
	defer C.free(unsafe.Pointer(cv))
	return C.maa_set_inst(coreHandle, C.int(key), cv) == 1
}

func maaConnect(adbPath, address, config string, block bool) C.AsstId {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return 0
	}
	ca := C.CString(adbPath)
	defer C.free(unsafe.Pointer(ca))
	caddr := C.CString(address)
	defer C.free(unsafe.Pointer(caddr))
	cc := C.CString(config)
	defer C.free(unsafe.Pointer(cc))
	b := 0
	if block {
		b = 1
	}
	return C.maa_connect(coreHandle, ca, caddr, cc, C.int(b))
}

func maaAppendTask(taskType, params string) int {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return 0
	}
	ct := C.CString(taskType)
	defer C.free(unsafe.Pointer(ct))
	cp := C.CString(params)
	defer C.free(unsafe.Pointer(cp))
	return int(C.maa_append_task(coreHandle, ct, cp))
}

func maaSetTaskParams(id int, params string) bool {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return false
	}
	cp := C.CString(params)
	defer C.free(unsafe.Pointer(cp))
	return C.maa_set_task_params(coreHandle, C.AsstId(id), cp) == 1
}

func maaStart() bool {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return false
	}
	return C.maa_start(coreHandle) == 1
}

func maaStop() bool {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return false
	}
	return C.maa_stop(coreHandle) == 1
}

func maaRunning() bool {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return false
	}
	return C.maa_running(coreHandle) == 1
}

func maaConnected() bool {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return false
	}
	return C.maa_connected(coreHandle) == 1
}

func maaBackToHome() bool {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return false
	}
	return C.maa_back_home(coreHandle) == 1
}

func maaScreencap() {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return
	}
	C.maa_screencap(coreHandle, 1)
}

func maaClick(x, y int) {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return
	}
	C.maa_click(coreHandle, C.int32_t(x), C.int32_t(y), 1)
}

// getImage returns PNG bytes if possible, otherwise raw BGR bytes and its width/height.
func getImage(maxBytes int, width, height int) (png []byte, bgr []byte, w, h int) {
	coreMu.Lock()
	defer coreMu.Unlock()
	if coreHandle == nil {
		return nil, nil, 0, 0
	}
	buf := C.malloc(C.size_t(maxBytes))
	defer C.free(buf)
	n := int(C.maa_get_image(coreHandle, buf, C.AsstSize(maxBytes)))
	null := int(C.maa_null_size())
	if n > 0 && n != null && n < maxBytes {
		data := C.GoBytes(buf, C.int(n))
		if len(data) >= 8 && data[0] == 0x89 && data[1] == 0x50 && data[2] == 0x4e && data[3] == 0x47 {
			return data, nil, width, height
		}
	}
	// fallback: BGR raw
	n2 := int(C.maa_get_image_bgr(coreHandle, buf, C.AsstSize(maxBytes)))
	if n2 > 0 && n2 != null && n2 < maxBytes {
		return nil, C.GoBytes(buf, C.int(n2)), width, height
	}
	return nil, nil, 0, 0
}

func coreVersionString() string { return coreVersion }
