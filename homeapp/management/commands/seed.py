from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import UploadedFile
from browserapp.models import *

import os

# class command(BaseCommand):

#     def handle(self, *args, **options):

#         popcap = Publishers(publisherName = "PopCap Games", publisherDescription = "PopCap Games, Inc. is an American video game developer based in Seattle, and a subsidiary of Electronic Arts")
#         popcap.publisherImage = ImageFile(open("../static/popcapLogo.jpg", "rb"))
#         popcap.save()

class Command(BaseCommand):

    def handle(self, *args, **options):

        # Delete all publishers in the database, also deletes all games
        Publishers.objects.all().delete()

        #print(os.listdir())

        # Adding Armour Games
        popcap = Publishers(publisherName = "Armor Games", publisherDescription = "Armor Games is an American video game publisher and free web gaming portal. The website hosts over a thousand HTML5 browser games. Based in Irvine, California, the site was founded in 2004 by Daniel McNeely. Armor Games primarily hosts curated HTML5/JavaScript games and MMOs, sometimes sponsoring their creation.")
        popcap.publisherImage = UploadedFile(file = open("static/armourGamesLogo.png", 'rb'))
        popcap.save()

        # Adding Exit Path 2
        pubArmour = Publishers.objects.get(publisherName = "Armor Games")
        exitpath2 = Games(
            title = "Exit Path 2",
            description = "Exit Path is a multiplayer and uniplayer gauntlet-style racing game through perilous traps and platforms. Advance through 30 uniplayer levels or take on other challengers in multiplayer.",
            cheatData = "Infinite Flow: RUNLIKETHEWIND",
            coverImage = UploadedFile(file = open("static/exitpath2.png", 'rb')),
            gamePublisher = pubArmour
        )

        exitpath2.save()

        # Adding Miniclip
        miniclip = Publishers(publisherName = "Miniclip SA", publisherDescription = "Miniclip SA is a mobile game publisher and former browser game website that launched in 2001. It was started by Robert Small and Tihan Presbie with a budget of £40,000. In 2008, the company was valued at over £275 million. In 2009, Miniclip hosted over 400 applications on its website.")
        miniclip.publisherImage = UploadedFile(file = open("static/miniclipLogo.jpg", 'rb'))
        miniclip.save()

        # Adding BLOXORZ
        pubMiniclip = Publishers.objects.get(publisherName = "Miniclip SA")
        bloxorz = Games(
            title = "BLOXORZ",
            description = "Bloxorz is a tricky puzzle game that tests your logical skills and sheer brain power. The objective is to get the block into the square hole and avoid falling off the edge. Put your brain to the test and see how far you get!",
            cheatData = "Level 33 - code : 614955",
            coverImage = UploadedFile(file = open("static/bloxorz.jpg", 'rb')),
            gamePublisher = pubMiniclip
        )

        bloxorz.save()

        # Adding Newgrounds
        newgrounds = Publishers(publisherName = "Newgrounds", publisherDescription = "Newgrounds is an entertainment website and company founded by Tom Fulp in 1995. It hosts user-generated content such as games, films, audio, and artwork. Fulp produces in-house content at the headquarters and offices in Glenside, Pennsylvania.")
        newgrounds.publisherImage = UploadedFile(file = open("static/newgroundsLogo.png", 'rb'))
        newgrounds.save()

        # Adding Madness Combat Nexus
        pubNewgrounds = Publishers.objects.get(publisherName = "Newgrounds")
        mcpn = Games(
            title = "Madness Combat: Project Nexus",
            description = "MADNESS: Project Nexus is a third-person Run n' Gun / Beat'Em Up filled with arcade-style action and button-mashing brutality. Gun your way through droves of bad guys in the Story Campaign, or build your perfect killing machine in the neverending onslaught of Arena Mode",
            cheatData = "Armstrong. Gives the player double the punch distance.",
            coverImage = UploadedFile(file = open("static/madnessCombat.png", 'rb')),
            gamePublisher = pubNewgrounds
        )


        mcpn.save()

        # Adding Electric Man 2

        electricman2 = Games(
            title = "Electric Man 2: The Tournament of Voltagen",
            description = "Electric Man 2 is the sequel to the action stickman game, Electric Man. You're in a tournament against other stickmen who are trying to beat you for the grand prize. Beat out every one of these stickmen using your electrifying power moves. There are no rules and several rounds with a varying of opponents that you need to defeat. Your goal is to keep your title and be the best of the stickmen universe.",
            cheatData = "Unlimited Electricity and 200 Health: HAPPY2008!",
            coverImage = UploadedFile(file = open("static/electricman2logo.png", 'rb')),
            gamePublisher = pubNewgrounds
        )


        electricman2.save()

        

        # Adding Flipline Studios
        flipline = Publishers(publisherName = "Flipline Studios", publisherDescription = "Flipline Studios (also called simply Flipline) is an American-based Flash game development company founded in 2004 that is best known for its series of Papa Louie's restaurant time-management games and Cactus McCoy. It was founded by Tony Solary and Matt Neff.")
        flipline.publisherImage = UploadedFile(file = open("static/fliplineStudioLogo.jpg", 'rb'))
        flipline.save()

        # Adding Papa's Pizzeria
        pubFlipline = Publishers.objects.get(publisherName = "Flipline Studios")
        pizzeria = Games(
            title = "Papa's Pizzeria",
            description = "Papa Louie has left the pizza shop! It is up to you to take over the business. You are playing as Roy, who must take over the pizzeria and make the orders accurately and on time!",
            cheatData = "Begin the game with a new profile, and enter your name as 'almostpapa', which will allow you to pass day 99 with a rank of 30.",
            coverImage = UploadedFile(file = open("static/papa-s-pizzeria.jpg", 'rb')),
            gamePublisher = pubFlipline
        )

        pizzeria.save()

        # Adding Fancy Pants
        fancypants = Games(
            title = "The Fancy Pants Adventures",
            description = "In this game you take control of Fancy Pants - a cool stickman character who wears awesome and colorful pants! You must help our fancy hero work his way through a myriad of cool levels and avoid various obstacles, monsters and creatures on his way!",
            cheatData = "10000 Squiggles collected: Squiggle Hunter",
            coverImage = UploadedFile(file = open("static/fancypants.png", 'rb')),
            gamePublisher = pubArmour
        )

        fancypants.save()

        # Adding PopCap Games
        popcap = Publishers(publisherName = "PopCap Games", publisherDescription = "PopCap Games, Inc. is an American video game developer based in Seattle, and a subsidiary of Electronic Arts")
        popcap.publisherImage = UploadedFile(file = open("static/popcapLogo.jpg", 'rb'))
        popcap.save()

        # Adding Bejeweled 2
        pubPopcap = Publishers.objects.get(publisherName = "PopCap Games")
        bejeweled2 = Games(
            title = "Bejeweled 2",
            description = "Bejeweled 2 is a tile-matching puzzle video game developed and published by PopCap Games. Released as a sequel to Bejeweled, Bejeweled 2 introduces new game mechanics such as Special Gems and extra game modes, along with new visuals and sounds.",
            cheatData = "All gems lose color: blackandwhite",
            coverImage = UploadedFile(file = open("static/bejeweled2.jpg", 'rb')),
            gamePublisher = pubPopcap
        )

        bejeweled2.save()

        # Adding Ninja Kiwi
        ninjakiwi = Publishers(publisherName = "Ninja Kiwi", publisherDescription = "Ninja Kiwi, previously known as Kaiparasoft Ltd, is a mobile and online video game developer founded in Auckland, New Zealand, in 2006 by brothers Chris and Stephen Harris. Ninja Kiwi's first game was a browser based game called Cash Sprint, developed on the Adobe Flash Platform.")
        ninjakiwi.publisherImage = UploadedFile(file = open("static/ninjakiwilogo.png", 'rb'))
        ninjakiwi.save()

        # Adding Bloons TD 5
        pubNinjakiwi = Publishers.objects.get(publisherName = "Ninja Kiwi")
        bloonstd5 = Games(
            title = "Bloons™ TD: 5",
            description = "Bloons TD5 has awesome new features including all your favourite towers from BTD4 with 8 awesome upgrades each instead of 4, and two brand new never before seen tower types. Use the towers brand-new and unbelievably cool 'Super Activated Abilities' to lay waste to the endless swarms of Bloons. You'll need all the firepower you can get to combat the new Bloon types and fun new tracks with moving parts and tunnels.",
            cheatData = "99999 Cash: MONKEYECONOMY",
            coverImage = UploadedFile(file = open("static/btd5.jpg", 'rb')),
            gamePublisher = pubNinjakiwi
        )

        bloonstd5.save()

        # Adding Bloons TD 4
        pubNinjakiwi = Publishers.objects.get(publisherName = "Ninja Kiwi")
        bloonstd4 = Games(
            title = "Bloons™ TD: 4",
            description = "Bloons Tower Defense 4 is a classic tower defense game initially released in Flash. Defend the path by placing various defenses tactically around the map. Upgrade them and unlock more as you get further through the game.",
            cheatData = "99999 Cash: MOREBANANAS",
            coverImage = UploadedFile(file = open("static/btd4.jpg", 'rb')),
            gamePublisher = pubNinjakiwi
        )

        bloonstd4.save()


        self.stdout.write('done.') 
