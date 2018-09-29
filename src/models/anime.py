class Anime():

    def get_title(self, obj):
        title_obj = obj["title"]
        english_title = str(title_obj["english"])
        romaji_title = str(title_obj["romaji"])

        return romaji_title
        # if title_obj["english"] is None:
        #     return romaji_title
        # else:
        #     return english_title

    def __init__(self, anime_obj):
        self.name = self.get_title(anime_obj)
        self.episodes_out = anime_obj["nextAiringEpisode"]["episode"]
        self.description = anime_obj["description"]
        self.studio = 'Jigger :D'
        self.rating = anime_obj["averageScore"]
        self.genres = anime_obj["genres"]
        self.image = anime_obj["coverImage"]["medium"]
