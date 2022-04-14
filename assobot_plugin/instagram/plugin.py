import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions

from assobot import INSTA_LOGIN
from assobot.core.plugin import AbstractPlugin
from instagram_scraper import InstagramScraper

BASE_URL = 'https://www.instagram.com/'


class instagramPlugin(AbstractPlugin):

    def __init__(self) -> None:
        super().__init__('instagram', 'Fetch and send all new posts of instagram account')

    @has_permissions(administrator=True)
    @commands.command(name="insta")
    async def instagram(self, ctx):
        await self.automated_instagram.start(ctx)
        await ctx.message.delete()

    @tasks.loop(hours=24)
    async def automated_instagram(self, ctx):
        await self.send_all_last_insta_post(ctx)

    async def send_all_last_insta_post(self, ctx):
        settings_manager = self.get_settings_manager(ctx.guild)
        if not bool(settings_manager.get("enabled")): return
        profils = settings_manager.get('profils')

        settings_manager.set("instagram_channel_id", ctx.guild.id)
        settings_manager.save()

        insta_scraper = self.get_authentified_insta_scraper()

        for index, profil_id in enumerate(profils):
            await self.send_last_insta_post_if_new(ctx, insta_scraper, profil_id, index)

    def get_last_post_infos(self, insta_scraper, shared_data):
        if not shared_data['is_private']:
            generator = insta_scraper.query_media_gen(shared_data)
            return next(generator, None)
        else:
            return None

    def get_shared_data(self, insta_scraper, profil_id):
        return insta_scraper.get_shared_data_userinfo(username=profil_id)

    def get_authentified_insta_scraper(self):
        insta_scraper = InstagramScraper(**INSTA_LOGIN)
        insta_scraper.authenticate_with_login()
        return insta_scraper

    def create_embed_from_infos(self, user_infos, last_post):
        thumbnail_url = last_post['display_url']
        description = last_post['edge_media_to_caption']['edges'][0]['node'][
            'text']
        post_url = BASE_URL + 'p/' + last_post['shortcode']
        embed = discord.Embed(title=f"Last post of {user_infos['username']}",
                              url=post_url, description=description)

        embed.set_image(url=thumbnail_url)
        embed.set_author(name=user_infos['username'], icon_url=user_infos['profile_pic_url'],
                         url=BASE_URL + user_infos['username'])
        return embed

    async def send_last_insta_post_if_new(self, ctx, insta_scraper, profil_id, index):
        settings_manager = self.get_settings_manager(ctx.guild)
        user_infos = self.get_shared_data(insta_scraper, profil_id)
        if user_infos is not None:
            last_post = self.get_last_post_infos(insta_scraper, user_infos)
            if last_post is not None:
                if self.is_last_post_new(settings_manager, last_post, index):
                    message = await ctx.send(embed=self.create_embed_from_infos(user_infos, last_post))
                    await self.delete_old_message_and_save_message_id(ctx, settings_manager, index, message)
                else:
                    return
            else:
                await ctx.send(f"{profil_id} is a private profile")
        else:
            await ctx.send(f"Error when getting {profil_id}'s account infos")

    def is_last_post_new(self, settings_manager, last_post, index):
        post_ids = settings_manager.get('last_post_ids')
        last_post_id = int(last_post['id'])
        saved_post_id = int(post_ids[index])
        if last_post_id != saved_post_id:
            post_ids[index] = last_post_id
            settings_manager.set('last_post_ids', post_ids)
            settings_manager.save()
            return True
        else:
            return False

    async def delete_old_message_and_save_message_id(self, ctx, settings_manager, index, message):
        last_message_id = int(message.id)

        message_ids = settings_manager.get('last_message_ids')
        old_message_id = int(message_ids[index])

        if old_message_id != -1:
            try:
                msg = await ctx.channel.fetch_message(old_message_id)
                await msg.delete()
            except:
                pass

        message_ids[index] = last_message_id
        settings_manager.set('last_message_ids', message_ids)
        settings_manager.save()