
from deck import Deck

class Dirigent():
    def __init__(self, name):
        self.name=name
        self.state="WACHTEN_OP_SPELERS"
        self.gamebids=["regular","regular","regular","regular"]
        self.users=dict()
        self.playerorder=[]
        self.currentplayer=0
        self.currentplayercounter = 0
        self.acecount = [0, 0, 0, 0]
        self.nowbidding = -1
        self.userplayinggame=dict()
        self.rondekaarten=dict()
        self.returnedhands=dict()
        self.chineesdelencounter=0
        self.slagteller=dict()


        self.deck=Deck()
        #self.deck.shufle()

    def add_player(self,playerid,client):
        self.users[playerid]=client
        self.playerorder.append(playerid)
        if len(self.playerorder) == 4:
            self.setcurrentplayer(self.playerorder[0])
            self.start_game()
        else:
             togo = 4-len(self.users)
             self.wall("Waiting for {} more players".format(togo))

    def remove_player(self,playerid):
        if playerid in self.users.keys():
            del self.users[playerid]
        if playerid in self.playerorder:
            self.abort_game()

    def start_game(self):
        self.state="DELEN"
        self.returnedhands.clear()
        for i in self.playerorder:
            self.slagteller[i]=0
        #laatse kaart is troefkaart
        self.troefkaart = self.deal()
        #als we niet chniees delen dan mag iedereen troefkaart zien
        print("Laatst geven kaart is {}".format(self.troefkaart) )
        self.wall("Troefkaart is {}".format(self.troefkaart))
        self.nextplayer()
        self.start_bidding()

    def start_chineesdelen(self):
        self.state="CHINEES_DELEN"
        self.returnedhands.clear()
        #laatse kaart is troefkaart
        self.troefkaart = self.deal(chinees=True)
        self.chineesdelencounter = 0
        #als we niet chniees delen dan mag iedereen troefkaart zien
        print("niet omgedraaide kaart is {}".format(self.troefkaart) )
        print("vraag vier kaarten aan niet delers")
        for i in self.playerorder:
            if i != self.currentplayer:
                print("vraag drie kaarten aan {}".format(self.users[i].name))
                self.users[i].sendLine("-:4".encode("utf-8"))

    def cont_chineesdelen(self,client,parameter):
        print("Ontvangen van {}({}) kaart {} door gegeven aan {}({})".format(client.name,client.clientid,parameter,self.users[self.currentplayer].name,self.currentplayer))
        self.users[self.currentplayer].sendCard(parameter)
        self.chineesdelencounter = self.chineesdelencounter + 1
        if self.chineesdelencounter == 12:
            self.wall("Troefkaart is {}".format(self.troefkaart))
            self.nextplayer()
            self.start_bidding()


    def start_bidding(self):
        self.playerbidcounter=4
        if 3 in self.acecount:
            self.wall("Troel")
            self.playinggame="Troel"
        elif 4 in self.acecount:
            self.wall("Troela")
            self.playinggame = "Troela"
        else:
            self.wall("Geen troel")
            self.playinggame = "Gewoon"
        self.state = "BIEDEN"
        self.sendBidMessage()

    def huidigspel(self):
        spelbeschrijving="Volgende spel wordt gespeeld {} door ".format(self.playinggame)
        for i in self.playerorder:
            print("{} speelt {}".format(self.users[i].name, self.userplayinggame[i]) )

        if self.playinggame == "Troel" or self.playinggame == "Troela":
            for i in self.playerorder:
                if self.userplayinggame[i] == "TroelCaller":
                    spelbeschrijving = spelbeschrijving + self.users[i].name + " en "
            for i in self.playerorder:
                if self.userplayinggame[i] == "TroelFollower":
                    spelbeschrijving = spelbeschrijving + self.users[i].name
        elif self.playinggame == "VraagEnMee":
            for i in self.playerorder:
                if self.userplayinggame[i] == "Vraag":
                    spelbeschrijving = spelbeschrijving + self.users[i].name + " en "
            for i in self.playerorder:
                if self.userplayinggame[i] == "Ga Mee":
                    spelbeschrijving = spelbeschrijving + self.users[i].name
        else:
            for i in self.playerorder:
                if self.playinggame == self.userplayinggame[i]:
                    spelbeschrijving = spelbeschrijving + self.users[i].name + " "

        return spelbeschrijving

    def sendBidMessage(self):
        message="unknow bidmessage"
        if self.playinggame == "Troel":
            message="Troel spelen:Open Miserie:Solo:Solo Slim"
        if self.playinggame == "Troela":
            message="Troela spelen:Open Miserie:Solo:Solo Slim"
        pastext="Pas"
        if self.state != "BIEDEN":
            pastext="Ok"
        if self.playinggame == "Gewoon":
            message="{}:Vraag:Abondance:Miserie:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "Vraag":
            message="{}:Ga Mee:Abondance:Miserie:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "VraagEnMee":
            message = "{}:Abondance:Miserie:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "Abondance":
            message = "{}:AbondanceTroef:Miserie:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "AbondanceTroef":
            message = "{}:AbondanceTien:Miserie:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "AbondanceTien":
            message = "{}:AbondanceTienTroef:Miserie:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "Miserie":
            message = "{}:Miserie:AbondanceElf:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "AbondanceElf":
            message = "{}:AbondanceElfTroef:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "AbondanceElf":
            message = "{}:AbondanceElfTroef:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "AbondanceElfTroef":
            message = "{}:AbondanceTwaalf:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "AbondanceTwaalf":
            message = "{}:AbondanceTwaalfTroef:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "Open Miserie":
            message = "{}:Open Miserie:Solo:Solo Slim".format(pastext)
        if self.playinggame == "Solo":
            message = "{}:Solo Slim".format(pastext)

        message = "B:%s"%message
        if self.state != "BIEDEN":
            self.users[self.currentplayer].sendLine(self.huidigspel().encode("utf-8"))
        self.users[self.currentplayer].sendLine(message.encode("utf-8"))
        self.wall_excl(self.currentplayer, "Asking bid to {}".format(self.users[self.currentplayer].name))
        self.nowbidding = self.currentplayer

    def cont_bidding(self,client,message):
        self.playerbidcounter = self.playerbidcounter - 1
        self.userplayinggame[self.currentplayer] = message
        if message != "Pas" and message != "Ok":
            self.playinggame = message
            if message == "Ga Mee":
                self.playinggame="VraagEnMee"
        self.nextplayer()
        if self.playerbidcounter > 0:
            self.sendBidMessage()
        else:
            #bidding round over, what to do next ?
            countpas=0
            for i in self.playerorder:
                if self.userplayinggame[i]=="Pas":
                    countpas = countpas +1
            if countpas == 4:
                self.state = "RETURNHAND1"
                self.wall("Rondje pas, dus Chinees delen")
                self.wall("^:RETURNHAND")
                self.handreturncounter=4
            elif self.playinggame=="Vraag":
                self.state="ALLEEN_5_SPELEN"
                #send question to the player
                for i in self.playerorder:
                    if self.userplayinggame[i] == "Vraag":
                        self.wall("Wil vrager alleen gaan voor vijf slagen?")
                        message = "B:Voor5:Pas"
                        self.users[i].sendLine(message.encode("utf-8"))
            else:
                # do we need an extra round of bidding?
                # for now simply start playing
                self.start_speel_slag()

    def start_speel_slag(self):
        self.playerbidcounter = 4
        self.state = "SPEELSLAG"
        self.rondekaarten.clear()
        self.speel_slag()

    def speel_slag(self):
        message = "-:1"
        print("Asking card from {} ({})".format(self.users[self.currentplayer].name, self.currentplayer))
        self.users[self.currentplayer].sendLine(message.encode("utf-8"))
        self.wall_excl(self.currentplayer,"Asking card from {}".format(self.users[self.currentplayer].name))

    def cont_speel_slag(self,client,message):
        self.playerbidcounter = self.playerbidcounter -1
        if self.playerbidcounter == 3:
            #dit was eerste kaart van de slag dus dit is de vraag kaart/soort die gespeekld wordt
            #belangrijk om te weeten wie de slag wint
            self.vraagkaart=message
        self.rondekaarten[self.currentplayer]=message
        #also but back in the deck in order they are played :-)
        self.deck.addCard(message)
        # inform card played to other players, this makes it simple for clients to show cards on
        # a board and decouples player representation from board representation
        self.wall("P:{},{}".format(self.currentplayer,message))
        if self.playerbidcounter > 0:
            self.nextplayer()
            self.speel_slag()
        else:
            # laat klant weten dat slag gespeeld is. Dit maakt het gemakkelijker voor clients
            # om dan evntueel de kaarten van de slag van het bord te verwijderen of opzij
            # te zetten voor vorig gespeelde slag.
            cardsplayed=[]
            for i in self.playerorder:
                cardsplayed.append("{}={}".format(self.users[i].name,self.rondekaarten[i]))
            self.wall("^:TRIKFINISHED:{}".format(','.join(cardsplayed)))
            #
            # bepaal wie er nu moet uitkomen en of er nog een slag gespeeld moet worden
            # oorspronkelijke persoon die uitkwam in currentplayer zetten
            winkaart=""
            nieuwedeler=-1
            for i in range(4):
                if self.wint_slag(self.troefkaart,winkaart,self.rondekaarten[self.currentplayer]):
                    winkaart = self.rondekaarten[self.currentplayer]
                    nieuwedeler = self.currentplayer
                self.nextplayer()
            self.slagteller[nieuwedeler] = 1 + self.slagteller[nieuwedeler]
            if len(self.deck.cards)<51:
                self.setcurrentplayer(nieuwedeler)
                self.start_speel_slag()
            else:
                # laat klant weten dat het spel gespeeld is. Dit maakt het gemakkelijker
                # voor clients om dan de kaarten van het bord te verwijderen
                self.wall("^:GAMEFINISHED")
                self.state="PUNTEN"
                self.wall("All cards played")
                print("All cards played")
                self.berekenpunten()


    def  berekenpunten(self):
        print("here we go")
        pass

    def abort_game(self):
        self.state="ABORTING"
        self.wall("Player has disconnected")


    def wall(self, message):
        for client in self.users.values():
            client.sendLine(message.encode("utf-8"))

    def wall_excl(self, exclclient, message):
        for client in self.users.values():
            if not exclclient == client.clientid:
                client.sendLine(message.encode("utf-8"))

    def wint_slag(self,troefkaart,huidigewinner,gespeeldekaart):
        if len(huidigewinner)<2:
            return True
        if huidigewinner[0] != troefkaart[0] and gespeeldekaart[0]==troefkaart[0]:
            return True
        if huidigewinner[0] != gespeeldekaart[0]:
            return False
        #dus nu is gespeelde kaart van de zelfde soort als de huig winnende kaart (eerste gespeelde kaart of reeds met troef gekocht)
        huidigewinner = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'].index(huidigewinner[1:])
        gespeeldekaart = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'].index(gespeeldekaart[1:])
        return gespeeldekaart > huidigewinner


    def deal(self,chinees = False):
        self.acecount=[0,0,0,0]
        lastcard=''
        if not chinees:
            hands=[4,4,5]
            for i in hands:
                for j in range(4):
                    for k in range(i):
                        lastcard=self.deck.takeUppercard()
                        if lastcard[1]=='A':
                            self.acecount[self.currentplayer] = self.acecount[self.currentplayer] + 1
                        self.users[self.currentplayer].sendCard(lastcard)
                    self.nextplayer()
        else:
            hands = [5, 5, 7]
            for i in hands:
                for j in range(3):
                    for k in range(i):
                        lastcard = self.deck.takeUppercard()
                        if lastcard[1] == 'A':
                            self.acecount[self.currentplayer] = self.acecount[self.currentplayer] + 1
                        self.users[self.currentplayer].sendCard(lastcard)
                    self.nextplayer()
                self.nextplayer()
            #now last card to dealer
            self.nextplayer()
            self.nextplayer()
            self.nextplayer()
            lastcard = self.deck.takeUppercard()
            if lastcard[1] == 'A':
                self.acecount[self.currentplayer] = self.acecount[self.currentplayer] + 1
            self.users[self.currentplayer].sendCard(lastcard)
            #self.nextplayer()
        return lastcard

    def returninghand(self,client,message):
        #collect hands
        cards=message.split("=")[1]
        if client.clientid in self.returnedhands:
            print ("somebody is returning hands twice!!!!")
        self.returnedhands[client.clientid]=cards
        self.handreturncounter = self.handreturncounter - 1
        if self.handreturncounter == 0:
            if self.state.endswith("1"):
                #all hands returned, so reassemble the deck and start chinees delen
                for i in range(4):
                    for card in self.returnedhands[self.currentplayer].split(","):
                        self.deck.addCard(card)
                    self.nextplayer()
                self.start_chineesdelen()
            elif self.state.endswith("2"):
                self.nextplayer()
                self.start_game()
    def nextplayer(self):
        #toddo follow the playerorderlist! this is quick hack
        self.currentplayercounter = (self.currentplayercounter +1 ) % 4
        self.currentplayer = self.playerorder[self.currentplayercounter]

    def setcurrentplayer(self,nieuwedeler):
        self.currentplayer=nieuwedeler
        self.currentplayercounter=self.playerorder.index(nieuwedeler)

    def receiveMessage(self,client,message):
        print("Recevied from {0} (id:{1}) :  '{2}'".format(client.name, client.clientid, message))
        if ':' in message:
            command,parameter = str(message).split(':',1)
            if command == "C":
                self.wall("{0}: \"{1}\"".format(client.name,parameter))
            elif (self.state=="BIEDEN" or self.state=="OPBIEDEN")  and command=="B" and client.clientid==self.nowbidding:
                self.cont_bidding(client,parameter)
            elif self.state=="ALLEEN_5_SPELEN"  and command=="B":
                if parameter=="Pas":
                    #do return hand en dan volgende delen
                    self.state = "RETURNHAND2"
                    self.wall("Speler gaat niet allen")
                    self.wall("^:RETURNHAND")
                    self.handreturncounter = 4
                else:
                    self.wall("Speler gaat allen")
                    self.wall("speler {} komt uit".format(self.users[self.currentplayer].name))
                    self.start_speel_slag()
            elif self.state.startswith("RETURNHAND") and command=="^" and parameter.startswith("RETURNHAND="):
                self.returninghand(client,parameter)
            elif self.state=="CHINEES_DELEN" and command=="+":
                self.cont_chineesdelen(client,parameter)
            elif self.state=="SPEELSLAG" and command=="+"  and client.clientid==self.currentplayer:
                self.cont_speel_slag(client,parameter)
