import json
from typing import Any


class Scores:
    """Gère les meilleurs scores persistants du jeu."""

    def __init__(self) -> None:
        """Initialise les scores et charge le fichier existant."""
        self.dict_scores: dict[str, int] = {}
        self._import_scores()

    def _import_scores(self) -> None:
        """
        Importe les scores depuis le fichier scores.json
        Gère les erreurs si le fichier n'existe pas
        """
        data: dict[str, int] | Any
        try:
            with open("scores.json", "r") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.dict_scores = data
                else:
                    self.dict_scores = {}
            self._parse_scores()

        except (FileNotFoundError, PermissionError) as e:
            print(f"Unable to import scores : {e}")
            self.dict_scores = {}
        except json.decoder.JSONDecodeError as e:
            print(f"Unable to import scores : {e}")
            self.dict_scores = {}
            self._copy_file()

    def _copy_file(self) -> None:
        """
        Copie l'integralité du fichier
        des scores dans un backup.json
        """
        try:
            with open("scores.json", "r") as file:
                data = file.read()
        except (FileNotFoundError, PermissionError):
            print("Impossible to make the backup")
            return

        try:
            with open("scores_backup.json", "w") as file:
                file.write(data)
        except (FileNotFoundError, PermissionError):
            print("Impossible to make the backup")
            return
        print("A backup—score_backup.json contains your configuration.")

    def _verify_name(self, name: str) -> tuple[bool, str]:
        """
        Verifie si le nom name correspond aux exigances
        Return true / false + une phrase d'erreur si false
        """

        def is_valid() -> bool:
            """Indique si le nom est alphanumérique ou espace."""
            return all(caract.isalnum() or caract.isspace()
                       for caract in name)

        if not isinstance(name, str):
            return (False, f"Player name: {name} must be a string")
        if not is_valid():
            return (False,
                    f"Player name: {name} must consist of "
                    "alphanumeric characters or spaces.")
        if len(name) < 1 or len(name) > 10:
            return (False,
                    f"Player name {name} must contain between "
                    "1 and 10 characters.")
        return (True, "All good")

    def _parse_scores(self) -> None:
        """
        Parse les scores enregistrés.
        Garde en memoire que ceux souhaités
        """
        name_check: tuple[bool, str]
        to_pop: list[Any] = []

        for name, score in self.dict_scores.items():
            name_check = self._verify_name(name)

            if not name_check[0]:
                print(name_check[1])
                to_pop.append(name)
            elif not isinstance(score, int):
                to_pop.append(name)
                print(f"Palyer {name}: score must be an integer value.")
            elif score < 0:
                to_pop.append(name)
                print(f"Player {name}: score must be a positive value.")
        for elem in to_pop:
            self.dict_scores.pop(elem)

    def export_scores(self) -> None:
        """
        Exporte les scores et créer le fichier si il n'existe pas
        """
        self._sort_scores()
        score = self.dict_scores
        try:
            with open("scores.json", "w") as file:
                json.dump(score, file, indent=4)
        except (PermissionError, FileNotFoundError,
                json.decoder.JSONDecodeError) as e:
            print(f"Unable to export: {e}")

    def _sort_scores(self) -> None:
        """
        Trie les scores de maniere croissante
        NE garde que 10 scores
        """
        self.dict_scores = dict(
            sorted(self.dict_scores.items(),
                   key=lambda item: item[1],
                   reverse=True))

        while len(self.dict_scores.items()) > 10:
            self.dict_scores.popitem()

    def add_player_scores(self, name: str, score: int) -> None:
        """
        Ajoute l'utilisateur et le score
        """
        verif = self._verify_name(name)
        if verif[0] and score >= 0:
            self.dict_scores[name] = score
        elif not verif[0]:
            print(verif[1])
        else:
            print(f"Player: {name} score must be positive")

    def get_scores(self) -> tuple[str, ...]:
        """
        Return un tuple de phrase pour dire
        Nom a fais un score de x
        """
        list_score: list[str] = []
        i: int = 1
        self._sort_scores()
        for name, score in self.dict_scores.items():
            list_score.append(f"{i}. {name} - {score} pts")
            i += 1
        return tuple(list_score)


if __name__ == "__main__":
    scores = Scores()
    scores.export_scores()
