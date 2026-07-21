import pygame

from sound.effects import (DEATH, FRIGHTENED, GAME_OVER, MENU_MUSIC, PACGUM,
                           REVIVE, SIREN, SUPER_PACGUM, WAKA, load_effects)

# Niveaux du mixage. Les fonds (sirene, waka) restent discrets,
# les evenements ressortent clairement au dessus.
VOLUMES: dict[str, float] = {
    "music": 0.55,
    "siren": 0.28,
    "frightened": 0.32,
    "revive": 0.32,
    "waka": 0.22,
    "chomp": 0.45,
    "super": 0.60,
    "death": 0.85,
    "game_over": 0.70,
}

# Facteur et duree du ducking: quand un evenement fort joue,
# les fonds baissent a ce niveau pendant ce temps.
DUCK_FACTOR = 0.35
DUCK_MS = 650

NUM_CHANNELS = 8


class AudioMixer:
    """
    Point central du son du jeu. Possede tous les canaux, applique
    les volumes du mixage et gere le ducking des fonds.
    """

    CH_MUSIC = 0
    CH_AMBIENCE = 1
    CH_WAKA = 2
    CH_CHOMP = 3
    CH_EVENT = 4
    CH_JINGLE = 5

    def __init__(self) -> None:
        """Ouvre les canaux, charge les sons et règle les volumes."""
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.set_num_channels(NUM_CHANNELS)

        sounds = load_effects(pad=0.0)
        self.music = sounds[MENU_MUSIC]
        self.siren = sounds[SIREN]
        self.frightened = sounds[FRIGHTENED]
        self.revive = sounds[REVIVE]
        self.waka = sounds[WAKA]
        self.chomp = sounds[PACGUM]
        self.super = sounds[SUPER_PACGUM]
        self.death = sounds[DEATH]
        self.game_over = sounds[GAME_OVER]

        self.music.set_volume(VOLUMES["music"])
        self.siren.set_volume(VOLUMES["siren"])
        self.frightened.set_volume(VOLUMES["frightened"])
        self.revive.set_volume(VOLUMES["revive"])
        self.waka.set_volume(VOLUMES["waka"])
        self.chomp.set_volume(VOLUMES["chomp"])
        self.super.set_volume(VOLUMES["super"])
        self.death.set_volume(VOLUMES["death"])
        self.game_over.set_volume(VOLUMES["game_over"])

        self.ch_music = pygame.mixer.Channel(self.CH_MUSIC)
        self.ch_ambience = pygame.mixer.Channel(self.CH_AMBIENCE)
        self.ch_waka = pygame.mixer.Channel(self.CH_WAKA)
        self.ch_chomp = pygame.mixer.Channel(self.CH_CHOMP)
        self.ch_event = pygame.mixer.Channel(self.CH_EVENT)
        self.ch_jingle = pygame.mixer.Channel(self.CH_JINGLE)

        self._ambience_state: str | None = None
        self._waka_paused = False
        self._duck_until = 0

        self._ambience_sounds = {
            "siren": self.siren,
            "frightened": self.frightened,
            "revive": self.revive,
        }

    # ----- Menu -------------------------------------------------------
    def play_music(self) -> None:
        """Lance la musique du menu en boucle si elle ne joue pas déjà."""
        if not self.ch_music.get_busy():
            self.ch_music.play(self.music, loops=-1)

    def stop_music(self) -> None:
        """Coupe la musique du menu."""
        self.ch_music.stop()

    # ----- Boucle de jeu ---------------------------------------------
    def update_gameplay(self, ambience_state: str) -> None:
        """Appele a chaque frame pendant le jeu."""
        self._update_ambience(ambience_state)
        self._update_waka()
        self._update_duck()

    def _update_ambience(self, state: str) -> None:
        """Relance l'ambiance quand l'état change ou qu'elle s'arrête."""
        if (state != self._ambience_state
                or not self.ch_ambience.get_busy()):
            self.ch_ambience.play(self._ambience_sounds[state], loops=-1)
            self._ambience_state = state

    def _update_waka(self) -> None:
        """Met le waka en pause tant qu'un son de gomme joue."""
        eating = self.ch_chomp.get_busy() or self.ch_event.get_busy()
        if eating:
            if not self._waka_paused:
                self.ch_waka.pause()
                self._waka_paused = True
        elif self._waka_paused:
            self.ch_waka.unpause()
            self._waka_paused = False
        elif not self.ch_waka.get_busy():
            self.ch_waka.play(self.waka, loops=-1)

    def _update_duck(self) -> None:
        """Rétablit le volume des fonds à la fin du ducking."""
        if self._duck_until and pygame.time.get_ticks() >= self._duck_until:
            self.ch_ambience.set_volume(1.0)
            self.ch_waka.set_volume(1.0)
            self._duck_until = 0

    def _duck(self) -> None:
        """Baisse le volume des fonds pour la durée du ducking."""
        self.ch_ambience.set_volume(DUCK_FACTOR)
        self.ch_waka.set_volume(DUCK_FACTOR)
        self._duck_until = pygame.time.get_ticks() + DUCK_MS

    # ----- Evenements -------------------------------------------------
    def play_chomp(self) -> None:
        """Joue le son d'une pacgum mangée."""
        self.ch_chomp.play(self.chomp)

    def play_super(self) -> None:
        """Joue le son de super pacgum et baisse les fonds."""
        self.ch_event.play(self.super)
        self._duck()

    def play_death(self) -> None:
        """Coupe les sons de jeu et joue le jingle de mort."""
        self.stop_gameplay()
        self.ch_jingle.play(self.death)

    def play_game_over(self) -> None:
        """Coupe les sons de jeu et joue le jingle de fin de partie."""
        self.stop_gameplay()
        self.ch_jingle.play(self.game_over)

    def stop_gameplay(self) -> None:
        """Arrête les fonds du jeu et remet le mixage à zéro."""
        self.ch_ambience.stop()
        self.ch_waka.stop()
        self.ch_ambience.set_volume(1.0)
        self.ch_waka.set_volume(1.0)
        self._ambience_state = None
        self._waka_paused = False
        self._duck_until = 0


_MIXER: AudioMixer | None = None


def get_mixer() -> AudioMixer:
    """Retourne l'unique mixeur du jeu (cree au premier appel)."""
    global _MIXER
    if _MIXER is None:
        _MIXER = AudioMixer()
    return _MIXER
