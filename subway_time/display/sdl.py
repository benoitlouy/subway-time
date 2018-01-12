import io
import sdl2
import sdl2.sdlimage


class Display:
    def __init__(self, width, height, scale=1):
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        self.window = sdl2.SDL_CreateWindow(b"Subway Time", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
                                            width * scale, height * scale, sdl2.SDL_WINDOW_SHOWN)
        self.window_surface = sdl2.SDL_GetWindowSurface(self.window)
        self.scale = scale

    def refresh(self, image):
        bytes_io = io.BytesIO()
        size = image.size
        image.resize((size[0] * self.scale, size[1] * self.scale)).save(bytes_io, "PPM")
        image_bytes = bytes_io.getvalue()
        rw_ops = sdl2.SDL_RWFromMem(image_bytes, len(image_bytes))
        sdl_image = sdl2.sdlimage.IMG_Load_RW(rw_ops, 1)
        sdl2.SDL_BlitSurface(sdl_image, None, self.window_surface, None)
        sdl2.SDL_UpdateWindowSurface(self.window)
        sdl2.SDL_FreeSurface(sdl_image)
