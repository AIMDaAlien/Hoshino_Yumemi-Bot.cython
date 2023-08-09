import discord
import youtube_dl
import spotipy
import material

def main():
    # Create a new Discord bot client.
    client = discord.Client()

    # Create a queue of songs.
    queue = []

    # Create a volume slider.
    volume_slider = material.MessageEmbedField(
        name="Volume",
        value=f"{50}%",
        inline=True,
        custom_id="volume"
    )

    # Create a Material You theme.
    theme = material.Theme()
    theme.typography.title.color = material.Color("lavender")
    theme.typography.body1.color = material.Color("deep-purple")
    theme.color_scheme.primary = material.Color("lavender")
    theme.color_scheme.secondary = material.Color("deep-purple")

    # Volume slider in theme
    volume_slider = material.MessageEmbedField(
        name="Volume",
        value=f"{50}%",
        inline=True,
        custom_id="volume",
        color=theme.color_scheme.primary
    )

    # Register a handler for the "play" command.
    client.on("message", lambda message: play(message, queue, volume_slider))

    # Register a handler for the "volume" command.
    client.on("message", lambda message: volume(message, volume_slider))

    # Run the bot.
    client.run(os.getenv("DISCORD_BOT_TOKEN"))

def play(message, queue, volume_slider):
    if message.author.bot:
        return

    if message.content == "!play":
        # Get the user's input.
        args = message.content[6:]

        # If the user is queuing a song, add it to the queue.
        if len(args) > 0:
            queue.append(args)

        # If the queue is not empty, play the next song in the queue.
        if len(queue) > 0:
            song = queue[0]
            queue = queue[1:]

            # Play the song.
            if song.startswith("http"):
                # Play the song from YouTube.
                ydl = youtube_dl.YoutubeDL()
                with ydl.download([song]) as f:
                    song = f.name
                client.play(message.guild.voice_client, song)
            else:
                # Play the song from Spotify.
                sp = spotipy.Spotify()
                track = sp.search(q=song, type="track")["tracks"]["items"][0]
                client.play(message.guild.voice_client, track["uri"])

def volume(message, volume_slider):
    if message.author.bot:
        return

    if message.content == "!volume":
        # Get the volume from the message.
        try:
            volume = int(message.content[7:])
        except ValueError:
            return

        # Update the volume slider.
        volume_slider.value = f"{volume}%"

        # Send the embed to the channel.
        client.send_message(message.channel, embed=material.MessageEmbed(
            title="Now Playing",
            description=f"Volume: {volume}%",
            url=song.url,
            image=material.MessageEmbedImage(url=song.thumbnail_url),
            fields=[volume_slider],
            color=theme.primary_color
        ))

if __name__ == "__main__":
    main()
