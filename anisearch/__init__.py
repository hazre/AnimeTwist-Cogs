from .anisearch import AniSearch


def setup(bot):
    n = AniSearch()
    bot.add_cog(n)
