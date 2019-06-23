from .confessions import Confessions

def setup(bot):
    bot.add_cog(Confessions(bot))