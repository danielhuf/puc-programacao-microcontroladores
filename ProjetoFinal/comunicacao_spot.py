import requests
from threading import Timer
from tkinter import *
from random import choice


scopes = {
    "saved_tracks": "user-library-read",
    "playlists": "playlist-read-private",
    "player": "user-modify-playback-state, playlist-read-private",
}

window = None

volume_player = 60

images = []

playlists_canvas = None
player_canvas = None

preto = "gray15"
cinza = "#52595E"
neon = "#98F5FF"
font_default = "Terminal"

is_session_active = False

dict_playlists = dict()

# prefixo = "http://127.0.0.1:5000"
prefixo = "https://fb4f-139-82-243-207.ngrok.io"

#id_playlists = []

def playTracks(playlist_id):
    global volume_player
    r = requests.get(prefixo + "/playTracks/" + playlist_id + "/" + str(volume_player), verify=False)

    if r.text == "SEM APARELHOS":
        warning_device()


def playOneTrack():

    # botar endereço do ngrok
    r = requests.get(prefixo + "/playOneTrack", verify=False)

    if r.text == "SEM APARELHOS":
        warning_device()


def get_user_playlists():
    global dict_playlists

    r = requests.get(prefixo + "/get_user_playlists", verify=False)
    playlists = r.json()

    # sp = spotipy.Spotify(
    #     auth_manager=SpotifyOAuth(
    #         client_id=CLIENT_ID,
    #         client_secret=CLIENT_SECRET,
    #         redirect_uri=REDIRECT_URI,
    #         scope=scopes["player"],
    #     )
    # )
    # playlists = sp.current_user_playlists(limit=8)

    for i, item in enumerate(playlists["items"]):

        dict_playlists[item["name"]] = item["id"]
        #print(item["name"])
        botao = Button(
            playlists_canvas,
            text=item["name"],
            command=lambda id=item["id"]: playTracks(id),
            font="Terminal",
            bg="#98F5FF",
            border=None,
            width=24,
        )

        botao.grid(column=(i % 2), row=(i // 2) + 1, sticky=W, padx=10, pady=10)
        #id_playlists.append(item["id"])

        # botao.grid(column=i % 4, row=(i // 4) * 2 + 1, sticky=W, padx=10, pady=10)
        # playlit_image(item["id"], i)

    # print(dict_playlists)


# def playlit_image(image_id, pos):

#     sp = spotipy.Spotify(
#         auth_manager=SpotifyOAuth(
#             client_id=CLIENT_ID,
#             client_secret=CLIENT_SECRET,
#             redirect_uri=REDIRECT_URI,
#             scope=scopes["player"],
#         )
#     )

#     img = sp.playlist_cover_image(image_id)

#     raw_data = urllib.request.urlopen(img[0]["url"]).read()
#     im = Image.open(io.BytesIO(raw_data))
#     im = im.resize((60, 60), Image.ANTIALIAS)
#     image = ImageTk.PhotoImage(im)
#     label1 = Label(playlists_canvas, image=image)
#     label1.grid(column=pos % 4, row=2 * (pos // 4), sticky=N, padx=10, pady=10)
#     images.append(image)


# pular de musica
def skipTrack():
    # botar endereço do ngrok
    r = requests.get(prefixo + "/skipTrack", verify=False)


# voltar musica
def previousTrack():
    # botar endereço do ngrok
    r = requests.get(prefixo + "/previousTrack", verify=False)


# pausar musica
def pauseTrack():
    # botar endereço do ngrok
    r = requests.get(prefixo + "/pauseTrack", verify=False)


def grow_volume():
    global volume_player
    if volume_player <= 95:
        volume_player += 5

    # botar endereço do ngrok
    r = requests.get(prefixo + "/set_volume/" + str(volume_player), verify=False)


def shrink_volume():
    global volume_player
    if volume_player >= 5:
        volume_player -= 5

    # botar endereço do ngrok
    r = requests.get(prefixo + "/set_volume/" + str(volume_player), verify=False)


def show_buttons():
    global images
    play_img1 = createImage("Imagens/forward-button.png", 32, 32)
    images.append(play_img1)
    botao = Button(
        player_canvas,
        text="Pular",
        command=skipTrack,
        font="Terminal",
        bg=preto,
        borderwidth=0,
        image=play_img1,
        activebackground=preto,
    )
    botao.grid(column=3, row=0, sticky=N, padx=10, pady=10)

    play_img2 = createImage("Imagens/pause.png", 32, 32)
    images.append(play_img2)
    botao2 = Button(
        player_canvas,
        text="Pausar",
        command=pauseTrack,
        font="Terminal",
        bg="#98F5FF",
        borderwidth=0,
        image=play_img2,
        activebackground=preto,
    )
    botao2.grid(column=1, row=0, sticky=N, padx=10, pady=10)

    play_img3 = createImage("Imagens/backward-button.png", 32, 32)
    images.append(play_img3)
    botao3 = Button(
        player_canvas,
        text="Voltar",
        command=previousTrack,
        font="Terminal",
        bg=preto,
        borderwidth=0,
        image=play_img3,
        activebackground=preto,
    )
    botao3.grid(column=0, row=0, sticky=N, padx=10, pady=10)

    play_img4 = createImage("Imagens/play.png", 32, 32)
    images.append(play_img4)
    botao4 = Button(
        player_canvas,
        text="play",
        command=playOneTrack,
        font="Terminal",
        bg="#98F5FF",
        borderwidth=0,
        image=play_img4,
        activebackground=preto,
    )
    botao4.grid(column=2, row=0, sticky=N, padx=10, pady=10)

    play_img5 = createImage("Imagens/13.png", 32, 32)
    images.append(play_img5)
    botao5 = Button(
        player_canvas,
        text="+ Volume",
        command=grow_volume,
        font="Terminal",
        bg=preto,
        borderwidth=0,
        image=play_img5,
        activebackground=preto,
    )
    botao5.grid(column=2, row=1, sticky=N, padx=10, pady=10)

    play_img6 = createImage("Imagens/12.png", 32, 32)
    images.append(play_img6)
    botao6 = Button(
        player_canvas,
        text="- Volume",
        command=shrink_volume,
        font="Terminal",
        bg=preto,
        borderwidth=0,
        image=play_img6,
        activebackground=preto,
    )
    botao6.grid(column=1, row=1, sticky=N, padx=10, pady=10)


def createImage(file, x, y):
    img = PhotoImage(file=file)
    return img


def warning_device():
    global warning_msg
    warning_msg = Label(
        window,
        text="Nenhum aparelho conectado",
        fg="yellow",
        bg=preto,
        font="Terminal",
    )
    warning_msg.place(x=300, y=53)
    t = Timer(2.0, warning_msg.destroy)
    t.start()


def start_music(controle):
    global window
    global playlists_canvas
    global player_canvas
    global is_session_active
    window = controle
    playlists_canvas = Canvas(
        window, width=500, height=300, background=preto, bd=0, highlightthickness=0
    )

    playlists_canvas.rowconfigure(0, weight=1)
    playlists_canvas.rowconfigure(1, weight=1)
    playlists_canvas.rowconfigure(2, weight=1)
    playlists_canvas.rowconfigure(4, weight=1)

    player_canvas = Canvas(window, width=270, height=400, background=preto)

    playlists_canvas.place(x=50, y=110)
    player_canvas.place(x=261, y=430)
    mostrar_subtitulo()
    get_user_playlists()
    show_buttons()
    is_session_active = True


def mostrar_subtitulo():
    global playlists_canvas
    sub = Label(
        playlists_canvas,
        text="Escolha uma playlist:",
        fg=neon,
        bg=preto,
        font="Terminal",
    )
    sub.grid(column=0, row=0, sticky=W, padx=10, pady=10)


# é preciso chamar a função abaixo no programa principal (mostraMenuInicial)
# if music.is_session_active:
#         music.leave_music()


def leave_music():
    global is_session_active
    is_session_active = False
    playlists_canvas.destroy()
    player_canvas.destroy()