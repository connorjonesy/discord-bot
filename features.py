import random
from asyncio import TimeoutError

#TODO
#TASK:: Double down and Splits


class Blackjack:
    def __init__(self, channel, player, bot):
        self.channel = channel
        self.player = player
        self.bot = bot
        self.royals = ['Jack', 'Queen', 'King']
        self.playerScore = 0
        self.dealerScore = 0
        self.dealerHand = []
        self.playerHand = []

    async def playgame(self):
        # Deal initial cards
        hand = self.generateHand()
        dealerFirstCard = self.hit('Dealer')
        await self.channel.send(f"Dealer reveals his first card: {dealerFirstCard}")
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
                newCard = self.hit('Player')
                await self.channel.send(f"You got a {newCard}!")
                await self.channel.send(f"{self.player.mention}'s Score: {self.playerScore}")
                if self.playerScore > 21:
                    await self.channel.send(f"{self.player.mention} Busted! You lose, hombre")
                    gameover = True
                else:
                    await self.channel.send(f"Hit or stay?")

            elif response.content.lower() == 'stay':
                dealerBust = False

                while self.dealerScore < 17:
                    dealerCard = self.hit('Dealer')
                    await self.channel.send(f"Dealer draws {dealerCard}")

                if self.dealerScore > 21:
                    dealerBust = True

                dealer_cards = ", ".join(str(card) for card in self.dealerHand)
                player_cards = ", ".join(str(card) for card in self.playerHand)

                message = f"""
                **Dealer's Hand:** {dealer_cards}
                **Score:** {self.dealerScore}

                **{self.player.display_name}'s Hand:** {player_cards}
                **Score:** {self.playerScore}
                """
                await self.channel.send(message)
                
                if not dealerBust:
                    if self.playerScore < self.dealerScore:
                        await self.channel.send(f"{self.player.mention} berda_bot wins! You lose, hombre")
                    elif self.playerScore == self.dealerScore:
                        await self.channel.send(f"{self.player.mention} ties with the berda bot! Game over.")
                    else:
                        await self.channel.send(f"{self.player.mention} beats berda bot! You win!.")
                    gameover = True

            else:
                await self.channel.send(f"Invalid input: Try again, hit or stay?")

    def generateHand(self):
        card1 = random.randint(1,10)
        self.playerScore += card1
        if card1 == 1:
            card1 = 'Ace'
            self.playerScore += 10 #start with 11
        if card1 == 10:
            card1 = self.royals[random.randint(0,2)]
        self.playerHand.append(card1)

        card2 = random.randint(1,10)
        self.playerScore += card2
        if card2 == 1:
            card2 = 'Ace'
            if card1 != 'Ace':
                self.playerScore += 10 #11 for an ace
        if card2 == 10:
            card2 = self.royals[random.randint(0,2)]
        self.playerHand.append(card2)

        hand = [card1,card2]
        return hand

    def hit(self, caller):
        hand = None
        card = random.randint(1,10)

        if caller == 'Player':
            hand = self.playerHand
            self.playerScore += card

            if card == 1:
                card =  'Ace'
            if card == 10:
                card =  self.royals[random.randint(0,2)]
            self.playerHand.append(card)

            if self.playerScore > 21:
                #check for Aces to change so as to not Bust
                for i in hand:
                    if i == 'Ace':
                        self.playerScore -= 10 #make the found Ace into a 1
                        break

        elif caller == 'Dealer':
            hand = self.dealerHand
            self.dealerScore += card

            if card == 1:
                card =  'Ace'
            if card == 10:
                card =  self.royals[random.randint(0,2)]
            self.dealerHand.append(card)

            if self.dealerScore > 21:
                #check for Aces to change so as to not Bust
                for i in hand:
                    if i == 'Ace':
                        self.dealerScore -= 10 #make the found Ace into a 1
                        break

        return card
