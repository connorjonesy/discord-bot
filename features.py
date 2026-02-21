import random
from asyncio import TimeoutError


class Blackjack:
    def __init__(self, channel, player, bot):
        self.channel = channel
        self.player = player
        self.bot = bot
        self.royals = ['Jack', 'Queen', 'King']
        self.playerScore = 0
        self.dealerScore = 0

    async def playgame(self):
        # Deal initial cards
        hand = self.generateHand()
        await self.channel.send(f"{self.player.mention} gets a {hand[0]} and a {hand[1]}. Hit or stay?")

        gameover = False

        while not gameover:
            def check(m):
                return m.author == self.player and m.channel == self.channel

            try:
                response = await self.bot.wait_for('message', check=check, timeout=60.0)
            except TimeoutError:
                await self.channel.send(f"{self.player.mention} took too long! Game over.")
                return

            if response.content.lower() in ['hit','hit me']:
                newCard = self.hit()
                await self.channel.send(f"You got a {newCard}!")
                await self.channel.send(f"{self.player.mention}'s Score: {self.playerScore}")
                if self.playerScore > 21:
                    await self.channel.send(f"{self.player.mention} Busted! You lose, hombre")
                    gameover = True
                else:
                    await self.channel.send(f"Hit or stay?")

            elif response.content.lower() == 'stay':
                #TODO: Don't hardcode the dealer score
                dealerScore = random.randint(16,21)
                await self.channel.send(f"berda bot score:{dealerScore}")
                if self.playerScore < dealerScore:
                    await self.channel.send(f"{self.player.mention} berda_bot wins! You lose, hombre")
                elif self.playerScore == self.dealerScore:
                    await self.channel.send(f"{self.player.mention} ties with the berda bot! Game over.")
                else:
                    await self.channel.send(f"{self.player.mention} beats berda bot! You win!.")
                gameover = True

            else:
                await self.channel.send(f"Invalid input: Try again, hit or stay?")

    #TODO: Add logic for using an Ace as a 1 or a 10
    def generateHand(self):
        card1 = random.randint(1,10)
        self.playerScore += card1
        if card1 == 1:
            card1 = 'Ace'
        if card1 == 10:
            card1 = self.royals[random.randint(0,2)]

        card2 = random.randint(1,10)
        self.playerScore += card2
        if card2 == 1:
            card2 = 'Ace'
        if card2 == 10:
            card2 = self.royals[random.randint(0,2)]

        hand = [card1,card2]
        return hand

    def hit(self):
        card = random.randint(1,10)
        self.playerScore += card
        if card == 1:
            return 'Ace'
        if card == 10:
            return self.royals[random.randint(0,2)]


