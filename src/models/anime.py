class Anime():

    def get_title(self, obj, return_romaji):
        title_obj = obj["title"]
        english_title = str(title_obj["english"])
        romaji_title = str(title_obj["romaji"])

        if return_romaji:
            return romaji_title
        else:
            return english_title

    def __init__(self, anime_obj):
        self.name = self.get_title(anime_obj, True)
        self.english_name = self.get_title(anime_obj, False)
        self.episodes_out = anime_obj["nextAiringEpisode"]["episode"] - 1
        self.description = anime_obj["description"]
        self.studio = 'Jigger :D'
        self.rating = anime_obj["averageScore"]
        self.genres = anime_obj["genres"]
        self.image = anime_obj["coverImage"]["medium"]
        self.source = anime_obj["source"]
        self.id = anime_obj["id"]
