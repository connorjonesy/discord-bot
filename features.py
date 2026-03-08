import random
from asyncio import TimeoutError

class Blackjack:

    CARD_EMOJIS = {
        'A♠': '🂡', '2♠': '🂢', '3♠': '🂣', '4♠': '🂤', '5♠': '🂥', '6♠': '🂦', 
        '7♠': '🂧', '8♠': '🂨', '9♠': '🂩', '10♠': '🂪', 'J♠': '🂫', 'Q♠': '🂭', 'K♠': '🂮',
        'A♥': '🂱', '2♥': '🂲', '3♥': '🂳', '4♥': '🂴', '5♥': '🂵', '6♥': '🂶',
        '7♥': '🂷', '8♥': '🂸', '9♥': '🂹', '10♥': '🂺', 'J♥': '🂻', 'Q♥': '🂽', 'K♥': '🂾',
        'A♦': '🃁', '2♦': '🃂', '3♦': '🃃', '4♦': '🃄', '5♦': '🃅', '6♦': '🃆',
        '7♦': '🃇', '8♦': '🃈', '9♦': '🃉', '10♦': '🃊', 'J♦': '🃋', 'Q♦': '🃍', 'K♦': '🃎',
        'A♣': '🃑', '2♣': '🃒', '3♣': '🃓', '4♣': '🃔', '5♣': '🃕', '6♣': '🃖',
        '7♣': '🃗', '8♣': '🃘', '9♣': '🃙', '10♣': '🃚', 'J♣': '🃛', 'Q♣': '🃝', 'K♣': '🃞',
        'BACK': '🂠'
    }

    def __init__(self, channel, player, bot):
        self.channel = channel
        self.player = player
        self.bot = bot
        self.royals = ['Jack', 'Queen', 'King']
        self.playerScore = 0
        self.dealerScore = 0
        self.dealerHand = []
        self.playerHand = []
        self.possibleSplit
        self.playerSplit = []
        self.splitScore = 0

    async def playgame(self):
        # Deal initial cards
        hand = self.generateHand()
        self.hit('Dealer', False)
        await self.channel.send(f"Dealer reveals his first card: {self.dealerHand[0]}")
        if self.playerHand[0] == self.playerHand[1]:
            #split is possible
            self.possibleSplit = True
            await self.channel.send(f"{self.player.mention} gets a {hand[0]} and a {hand[1]}. Split, Hit or stay?")
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
                newCard = self.hit('Player', False)
                await self.channel.send(f"You got a {newCard}!")
                await self.channel.send(f"{self.player.mention}'s Score: {self.playerScore}")
                if self.playerScore > 21:
                    await self.channel.send(f"{self.player.mention} Busted! You lose, hombre")
                    gameover = True
                else:
                    await self.channel.send(f"Hit or stay?")

            elif response.content.lower() == 'split':
                if self.possibleSplit != True:
                    await self.channel.send(f"Invalid input: Try again, hit or stay?")
                    continue
                self.possibleSplit = False #just in case
                self.playerSplit.append(self.playerHand.pop)
                self.splitScores()
                self.hit('Player', True)
                #pick best hand
                if self.playerScore < self.splitScore:
                    self.playerScore = self.splitScore
                    self.playerHand = self.playerSplit

                """
                TODO:: allow a splits loop for multiple hits and stays here
                TODO:: create a seperate function/structure for dialogue
                """
                dealerBust = False

                while self.dealerScore < 17:
                    dealerCard = self.hit('Dealer', False)
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


            elif response.content.lower() == 'stay':
                dealerBust = False

                while self.dealerScore < 17:
                    dealerCard = self.hit('Dealer', False)
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

    def hit(self, caller, split):
        hand = None
        if caller == 'Player':
            if split:
                card = random.randint(1,10)
                hand = self.playerSplit
                self.splitScore += card
                if card == 1:
                    card =  'Ace'
                if card == 10:
                    card =  self.royals[random.randint(0,2)]
                self.playerSplit.append(card)

                if self.splitScore > 21:
                    #check for Aces to change so as to not Bust
                    for i in hand:
                        if i == 'Ace':
                            self.splitScore -= 10 #make the found Ace into a 1
                            break
                    
            card = random.randint(1,10)
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
            return card

        elif caller == 'Dealer':
            card = random.randint(1,10)
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

    def splitScores(self):
        #error check
        if self.splitScores == 0 or self.playerScore == 0:
            print("Split Error")
        #need to remove score from players OG hand and add score to split hand
        #this means an extra check for cards that are ace or face
        splitHand = self.playerSplit
        if splitHand[0] == 'Ace':
            self.splitScore += 11
            self.playerScore -= 11
        elif splitHand[0] in self.royals:
            self.splitscore = 10
            self.playerScore -= 10
        else:
            self.splitScore += splitHand[0]
            self.playerScore -= splitHand[0]
        return
        



