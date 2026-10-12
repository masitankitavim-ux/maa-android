#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

typedef struct {
    uint32_t width;
    uint32_t height;
    uint32_t stride;
    uint32_t length;
    void* data;
    void* frame_ref;
} FrameInfo;

enum {
    M_START_GAME = 1,
    M_STOP_GAME = 2,
    M_INPUT = 4,
    M_TOUCH_DOWN = 6,
    M_TOUCH_MOVE = 7,
    M_TOUCH_UP = 8,
    M_KEY_DOWN = 9,
    M_KEY_UP = 10
};

typedef struct { int x, y; } Position;
typedef struct { const char* package_name; int force_stop; } StartGameArgs;
typedef struct { const char* client_type; } StopGameArgs;
typedef struct { const char* text; } InputArgs;
typedef struct { Position p; int contact; } TouchArgs;
typedef struct { int key_code; } KeyArgs;

typedef union {
    StartGameArgs start_game;
    StopGameArgs stop_game;
    InputArgs input;
    TouchArgs touch;
    KeyArgs key;
} ArgUnion;

typedef struct {
    int display_id;
    int method;
    ArgUnion args;
} MethodParam;

static unsigned char* g_rgba = NULL;
static size_t g_rgba_cap = 0;
static unsigned char* g_bgr = NULL;
static size_t g_bgr_cap = 0;
static uint32_t g_w = 0;       /* output (landscape) width  */
static uint32_t g_h = 0;       /* output (landscape) height */
static uint32_t g_raw_w = 0;   /* raw display width         */
static uint32_t g_raw_h = 0;   /* raw display height        */
static int g_rotated = 0;      /* 1 if raw was portrait      */

static int run_capture(void) {
    FILE* fp = popen("/system/bin/screencap", "r");
    if (!fp) return -1;

    unsigned char hdr[16];
    size_t got = fread(hdr, 1, sizeof(hdr), fp);
    if (got < 12) { pclose(fp); return -1; }

    uint32_t w = (uint32_t)hdr[0] | ((uint32_t)hdr[1] << 8) | ((uint32_t)hdr[2] << 16) | ((uint32_t)hdr[3] << 24);
    uint32_t h = (uint32_t)hdr[4] | ((uint32_t)hdr[5] << 8) | ((uint32_t)hdr[6] << 16) | ((uint32_t)hdr[7] << 24);
    uint32_t fmt = (uint32_t)hdr[8] | ((uint32_t)hdr[9] << 8) | ((uint32_t)hdr[10] << 16) | ((uint32_t)hdr[11] << 24);

    if (w == 0 || h == 0 || w > 8192 || h > 8192) { pclose(fp); return -1; }
    if (fmt != 1) { pclose(fp); return -1; } /* format 1 = RGBA_8888 */

    size_t px = (size_t)w * (size_t)h;
    size_t raw = px * 4;
    if (raw > g_rgba_cap) {
        unsigned char* n = (unsigned char*)realloc(g_rgba, raw);
        if (!n) { pclose(fp); return -1; }
        g_rgba = n; g_rgba_cap = raw;
    }

    size_t off = 0;
    while (off < raw) {
        size_t r = fread(g_rgba + off, 1, raw - off, fp);
        if (r == 0) break;
        off += r;
    }
    pclose(fp);
    if (off < raw) return -1;

    g_raw_w = w;
    g_raw_h = h;
    g_rotated = (h > w) ? 1 : 0;

    uint32_t out_w = g_rotated ? h : w;
    uint32_t out_h = g_rotated ? w : h;

    size_t bgr_len = (size_t)out_w * (size_t)out_h * 3;
    if (bgr_len > g_bgr_cap) {
        unsigned char* n = (unsigned char*)realloc(g_bgr, bgr_len);
        if (!n) return -1;
        g_bgr = n; g_bgr_cap = bgr_len;
    }

    if (g_rotated) {
        /* Rotate 90 degrees clockwise: out(x,y) <- raw(y, raw_h-1-x) */
        for (uint32_t oy = 0; oy < out_h; ++oy) {
            for (uint32_t ox = 0; ox < out_w; ++ox) {
                uint32_t rx = oy;
                uint32_t ry = h - 1 - ox;
                unsigned char* src = g_rgba + ((size_t)ry * w + rx) * 4;
                unsigned char* dst = g_bgr + ((size_t)oy * out_w + ox) * 3;
                dst[0] = src[2];
                dst[1] = src[1];
                dst[2] = src[0];
            }
        }
    }
    else {
        for (size_t i = 0; i < px; i++) {
            unsigned char* src = g_rgba + i * 4;
            unsigned char* dst = g_bgr + i * 3;
            dst[0] = src[2];
            dst[1] = src[1];
            dst[2] = src[0];
        }
    }

    g_w = out_w;
    g_h = out_h;
    return 0;
}

FrameInfo GetLockedPixels(void) {
    FrameInfo fi;
    fi.width = 0; fi.height = 0; fi.stride = 0; fi.length = 0;
    fi.data = NULL; fi.frame_ref = NULL;
    if (run_capture() != 0) return fi;
    fi.width = g_w;
    fi.height = g_h;
    fi.stride = g_w * 3;
    fi.length = (uint32_t)((size_t)g_w * (size_t)g_h * 3);
    fi.data = g_bgr;
    fi.frame_ref = NULL;
    return fi;
}

int UnlockPixels(FrameInfo fi) {
    (void)fi;
    return 0;
}

static int map_touch(int* x, int* y) {
    if (g_rotated && g_raw_w > 0 && g_raw_h > 0) {
        int lx = *x;
        int ly = *y;
        *x = ly;               /* raw_x = landscape_y */
        *y = (int)g_raw_h - 1 - lx;  /* raw_y = raw_h-1-landscape_x */
    }
    return 0;
}

static int shellf(const char* fmt, ...) {
    char cmd[2048];
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(cmd, sizeof(cmd), fmt, ap);
    va_end(ap);
    return system(cmd);
}

static int quote_append(char* dst, size_t cap, size_t* pos, const char* s) {
    if (!s) s = "";
    size_t p = *pos;
    if (p + 2 >= cap) return -1;
    dst[p++] = '\'';
    for (; *s; s++) {
        if (p + 4 >= cap) return -1;
        if (*s == '\'') {
            dst[p++] = '\'';
            dst[p++] = '\\';
            dst[p++] = '\'';
            dst[p++] = '\'';
        } else {
            dst[p++] = *s;
        }
    }
    if (p + 1 >= cap) return -1;
    dst[p++] = '\'';
    *pos = p;
    return 0;
}

int DispatchInputMessage(MethodParam param) {
    char cmd[4096];
    int r;
    int x, y;

    switch (param.method) {
    case M_START_GAME: {
        const char* pkg = param.args.start_game.package_name;
        if (!pkg || !*pkg) return -1;
        r = shellf("monkey -p %s -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1", pkg);
        return (r == 0) ? 0 : -1;
    }
    case M_STOP_GAME: {
        const char* pkg = param.args.stop_game.client_type;
        if (!pkg || !*pkg) return -1;
        r = shellf("am force-stop %s >/dev/null 2>&1", pkg);
        return (r == 0) ? 0 : -1;
    }
    case M_INPUT: {
        const char* text = param.args.input.text;
        if (!text) return -1;
        size_t pos = 0;
        memcpy(cmd, "input text ", 11);
        pos = 11;
        if (quote_append(cmd, sizeof(cmd), &pos, text) != 0) return -1;
        cmd[pos] = '\0';
        r = system(cmd);
        return (r == 0) ? 0 : -1;
    }
    case M_TOUCH_DOWN:
        x = param.args.touch.p.x;
        y = param.args.touch.p.y;
        map_touch(&x, &y);
        r = shellf("input motionevent DOWN %d %d >/dev/null 2>&1", x, y);
        return (r == 0) ? 0 : -1;
    case M_TOUCH_MOVE:
        x = param.args.touch.p.x;
        y = param.args.touch.p.y;
        map_touch(&x, &y);
        r = shellf("input motionevent MOVE %d %d >/dev/null 2>&1", x, y);
        return (r == 0) ? 0 : -1;
    case M_TOUCH_UP:
        x = param.args.touch.p.x;
        y = param.args.touch.p.y;
        map_touch(&x, &y);
        r = shellf("input motionevent UP %d %d >/dev/null 2>&1", x, y);
        return (r == 0) ? 0 : -1;
    case M_KEY_DOWN:
        r = shellf("input keyevent %d >/dev/null 2>&1", param.args.key.key_code);
        return (r == 0) ? 0 : -1;
    case M_KEY_UP:
        return 0;
    default:
        return -1;
    }
}
