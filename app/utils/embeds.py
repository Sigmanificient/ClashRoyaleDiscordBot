from __future__ import annotations
import embed_templator


class Embed(embed_templator.Embed):
    """
    bot's own Embed class that automate the embeds color and footer.
    Use this like a normal embed
    """

    def setup(self) -> Embed:
        self.set_footer(
            text=f"command {self.client.prefix}{self.ctx.command} | "
                 f"{self.client.prefix}help"
        )
        self.colour = self.client.embed_color
        return self