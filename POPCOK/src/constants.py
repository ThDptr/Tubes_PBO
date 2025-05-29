# Game constants
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 32
EXPLOSION_DELAY = 3  # Faster explosion animation

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (200, 0, 0)
BROWN = (139, 69, 19)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Game states
START, PLAYING, GAME_OVER, SHOW_SURAT_1, SHOW_SURAT_2, CREDITS = 0, 1, 2, 3, 4, 5

# TILE MAP LEGEND:
# ' ' (spasi) = Area kosong/udara
# 'S' = Spawn point player (titik mulai)
# 'P' = Platform biasa (hijau, solid)
# 'T' = Trap/jebakan biasa (animasi 3 frame, membunuh player)
# 'K' = Piring trap (jebakan piring berputar, membunuh player)
# 'Q' = Moving piring trap (piring bergerak saat player dalam jarak 4 platform)
# 'A' = Moving piring down trap (piring bergerak ke bawah saat player di bawah)
# 'B' = Moving piring up trap (piring bergerak ke atas saat player di atas)
# 'C' = Box hadiah (bisa dipukul untuk spawn musuh) - CHANGED FROM 'B'
# 'E' = Enemy/musuh (bergerak patroli, bisa diinjak atau membunuh player)
# 'F' = Finish asli (tujuan level, menang jika disentuh)
# 'V' = Fake finish kill (finish palsu, membunuh player)
# 'U' = Fake finish teleport (finish palsu, teleport ke start)
# 'Y' = Fake finish hide (finish palsu, sembunyikan finish asli)
# 'I' = Hidden platform (platform tersembunyi, muncul saat player mendekat)
# 'J' = Fake platform tipe 1 (menghilang saat diinjak)
# 'O' = Timed platform tipe 2 (menghilang pada waktu tertentu: 3s, 7s, 11s, 35s, 40s)
# 'X' = Invisible platform (tidak terlihat 5 detik, terlihat 1.5 detik, tapi tetap solid)

TILE_MAP = [
    "                                                                                                   II                                                               ",
    "                                                                                                   II                                                             ",
    "                                                                                                   II                                   IIII                           ",
    "                                                                                                   II                                        I        I               ",
    "                                                                                                   II  Y                                     I   U I               ",
    "                                                                                         Y         II              II                        I         I              ",
    "                                                                                              PJJJJJ  IIIII                         X   X   X   X   IIII                     ",
    "                                    A                                                   PPPPPP                               III                                       ",
    "                                                                                   PPPPPP      KKKKK                                                                          ",
    "                                                                          PPPPPPPPP                                                                                            ",
    "                                                               I I II                                      IIIIIIIIIIIIIIII                                                  ",
    "                           CCCCCCC              I                   I                  IIIII             II             II                     PPP                        ",
    "                 P                                      P            I          I             II                            II                   PPPP                        ",
    "  S            B     Q  P              E   P    E     P                I        I              II                           II       Q         PPPPPKKKK        V     E       ",
    "POOOOPPPPPOOJJJJJJJJJPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP      PPPPPPPPPPPPPPPPPPPPJJJPPPPPPPPPPPPPPPJJJPPPPPPJJJJPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "                                                                                                                  II                                               ",
    "                                                                                                                  II                                                    ",
    "                                                                                                                  II                                  F                      ",
    "                                                                                                                  II       Q                                                  ",
    "                                                                                                                  IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII      "
]