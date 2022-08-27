from abc import ABC, abstractmethod

class Subject(ABC):
    @abstractmethod
    def registerObserver(self,o):
        pass

    @abstractmethod
    def removeObserver(self,o):
        pass

    @abstractmethod
    def notifyObserver(self):
        pass



class Observer(ABC):
    @abstractmethod
    def update(self):
        pass



class Displayable(ABC):
    @abstractmethod
    def display():
        pass    



class House(Displayable):
    def __init__(self, address, squareFeet, numRooms, price):
        self.__address = address
        self.__squareFeet = squareFeet
        self.__numRooms = numRooms
        self.__price = price
    
    @property
    def address(self):
        return self.__address

    @property
    def squareFeet(self):
        return self.__squareFeet

    @property
    def numRooms(self):
        return self.__numRooms

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self,price):
        self.__price = price

    def display(self):
        print("Address = ", self.__address, "Square feet =", self.__squareFeet, "Num of Rooms =", self.__numRooms, "Price =",self.__price)



class Contact(Observer,Displayable):
    def __init__(self, firstName, lastName, phoneNumber, email):
        self.__lastName = lastName
        self.__firstName = firstName
        self.__email = email
        self.__phoneNumber = phoneNumber
    
    @property
    def firstName(self):
        return self.__firstName

    @firstName.setter
    def firstName(self, firstName):
        self.__firstName = firstName

    @property
    def lastName(self):
        return self.__lastName

    @lastName.setter
    def lastName(self,lastName):
        self.__lastName = lastName

    @property
    def phoneNumber(self):
        return self.__phoneNumber

    @phoneNumber.setter
    def phoneNumber(self,phoneNumber):
        return self.__phoneNumber

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self,email):
        return self.__email

    def display(self):
        print("Last Name =", self.__lastName, "First Name =", self.__firstName, "Phone number =", self.__phoneNumber, "Email =", self.__email)

    def update(self):
        pass



class Owner(Contact, Observer):
    def __init__(self, lastName, firstName, phoneNumber, email):
        super().__init__(lastName, firstName, phoneNumber, email)
        self.__houses = []

    @property
    def houses(self):
        return self.__houses

    def addHouse(self, house):
        self.__houses.append(house)
    
    def display(self):    
        super().display()
        print("owns the following houses: ")
        for house in self.__houses:
            house.display()
        print()

    def update(self):
        print("Owner get notification ", self.firstName, self.lastName)



class Buyer(Contact, Observer):
    def __init__(self, lastName, firstName, phoneNumber, email):
        super().__init__(lastName, firstName, phoneNumber, email)
        self.__watchList = []

    @property
    def watchList(self):
        return self.__watchList

    #  Save the house in his watch list 
    def saveForLater(self, house):
        self.__watchList.append(house)
  

    # Remove the house from his watch list
    def removeFromSaveForLater(self, house):
        if house in self.__watchList:
            self.__watchList.remove(house)

    def display(self):
        super().display()
        print("Watching the following house: ")
        for house in self.__watchList:
            house.display()
        print()

    def update(self):
        print("Buyer gets notification ", self.firstName, self.lastName)



class Company(Subject,Displayable):
    def __init__(self, companyName):
        self.__companyName = companyName
        self.__owners = []
        self.__buyers = []
        self.__agents = []
        self.__houses = []
        self.__observers = []

    @property
    def companyName(self):
        return self.__companyName

    @property
    def owners(self):
        return self.__owners

    @property
    def buyers(self):
        return self.__buyers

    @property
    def agents(self):
        return self.__agents

    @property
    def houses(self):
        return self.__houses

    def registerObserver(self,o):
        self.__observers.append(o)

    def removeObserver(self,o):
        self.__observers.remove(o)

    def notifyObserver(self, type, house=None):
        if type == "Agent":
            self.notifyAgentObservers()
        elif type == "Buyer":
            self.notifyProspectiveBuyerObservers(house)
        elif type == "Owner":
            self.notifyOwnerObservers(house)

    def notifyAgentObservers(self):
        for o in self.__observers:
            if isinstance(o, Agent):
                o.update()
    
    def notifyProspectiveBuyerObservers(self,house):
        for o in self.__observers:
            if isinstance(o, Buyer) and house in o.watchList:
                o.update()

    def notifyOwnerObservers(self, house):
        for o in self.__observers:
            if isinstance(o, Owner) and house in o.houses:
                o.update()

    def addOwner(self, owner):
        
        self.__owners.append(owner)
        self.registerObserver(owner)
        
    def addBuyer(self, buyer):
        
        self.__buyers.append(buyer)
        self.registerObserver(buyer)

    def addAgent(self, agent):
        self.__agents.append(agent)
        self.registerObserver(agent)

    def addHouseToListing(self, house):
        if house not in self.__houses:
            self.__houses.append(house)
            self.notifyObserver("Agent")
            self.notifyObserver("Buyers", house)
            self.notifyObserver("Owner", house)

    def saveHouseForLater(self, house):
        self.__buyers.append(house)

    def getHouseByAddress(self, address):
        for house in self.__houses:
            if house.address == address:
                return house
        return None

    def removeHouseFromListing(self, house):
        if house in self.__houses:
            self.__houses.remove(house)
            self.notifyObserver("Agent")
            self.notifyObserver("BUyer", house)
            self.notifyObserver("Owner", house)

    # Help to remove that house from all buyers' watch list.
    def removeHouseFromSaveForLater(self, house):
        for buyer in self.__buyers:
            buyer.removeFromSaveForLater(house)

    def getBuyersByHouse(self, house):
        buyersList =[]
        for buyer in self.__buyers:
            for i in buyer.watchList:
                if i == house:
                    buyersList.append(buyer)
        return buyersList 

    def editPrice(self,address, price):
        for house in self.__houses:
            if house.address == address:
                house.price = price    

    def display(self):
        print("Company Name =", self.__companyName)
        print("=================The list of agents================================")
        for agent in self.__agents:
            agent.display()

        print("===========The house listing ======================================")
        for house in self.__houses:
            house.display()
            
        print("===============The list of owers =================================")
        for owner in self.__owners:
            owner.display()
        print("=================The list of buyers===============================")
        for buyer in self.__buyers:
            buyer.display()

    
    
class Agent(Contact, Observer):
    def __init__(self, lastName, firstName, phoneNumber, email, position, company):
        super().__init__(lastName, firstName, phoneNumber, email)
        self.__position = position
        self.__company = company
    
    @property
    def position(self):
        return self.__position

    @property
    def company(self):
        return self.__company

    def addHouseToListingForOwner(self, owner, house):
        self.__company.addHouseToListing(house)
        self.__company.addOwner(owner)

    def helpBuyerToSaveForLater(self, buyer, house):
        buyer.saveForLater(house)
        #self.__company.saveHouseForLater(house)
        self.__company.addBuyer(buyer)

    def editHousePrice(self, address, newPrice):
        house = self.__company.getHouseByAddress(address)
        self.__company.editPrice(address, newPrice)
        self.__company.notifyObserver("Agent")
        self.__company.notifyObserver("Buyer", house)
        self.__company.notifyObserver("Owner", house)

    def soldHouse(self, house):
        self.__company.removeHouseFromListing(house)
        self.__company.removeHouseFromSaveForLater(house)

    # print all potential buyers who are interested in buying that house
    def printPotentalBuyers(self, house):
        for i in self.__company.getBuyersByHouse(house):
            i.display()

    def display(self):
        print("Last Name =", self.lastName, "First Name =", self.firstName, "Phone Number =", self.phoneNumber, "Email =", self.email)
    def update(self):
        print("Agent gets notification", self.firstName, self.lastName)



def main():
    owner1 = Owner('Peter', 'Li', '510-111-2222', 'peter@yahoo.com')
    owner2 = Owner('Carl', 'Buck', '408-111-2222', 'carl@yahoo.com')

    house1 = House('1111 Mission Blvd', 1000, 2, 1000000)
    house2 = House('2222 Mission Blvd', 2000, 3, 1500000)
    house3 = House('3333 Mission Blvd', 3000, 4, 2000000)

    owner1.addHouse(house1)
    owner2.addHouse(house2)
    owner2.addHouse(house3)

    buyer1 = Buyer('Tom', 'Buke', '408-555-2222', 'tom@yahoo.com')
    buyer2 = Buyer('Lily', 'Go', '510-222-3333', 'lily@yahoo.com')

    company = Company('Good Future Real Estate')
    agent1 = Agent('Dave', 'Henderson', '408-777-3333',
                   'dave@yahoo.com', 'Senior Agent', company)
    company.addAgent(agent1)

    agent1.addHouseToListingForOwner(owner1, house1)
    agent1.addHouseToListingForOwner(owner2, house2)
    agent1.addHouseToListingForOwner(owner2, house3)

    agent1.helpBuyerToSaveForLater(buyer1, house1)
    agent1.helpBuyerToSaveForLater(buyer1, house2)
    agent1.helpBuyerToSaveForLater(buyer1, house3)

    agent1.helpBuyerToSaveForLater(buyer2, house2)
    agent1.helpBuyerToSaveForLater(buyer2, house3)

    agent1.editHousePrice('2222 Mission Blvd', 1200000)

    company.display()

    print('\nAfter one house was sold ..........................')
    agent1.soldHouse(house3)
    company.display()

    print('\nDisplaying potential buyers for house 1 ..........................')
    agent1.printPotentalBuyers(house1)

if __name__ == "__main__":
    main()
