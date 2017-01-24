# Pokemon HTTP Request
# This program pulls additional data from the Pokemon GL website
# to obtain more in-depth statistics
#!python2

from lxml import html
import requests
import json
from fractions import Fraction
import os

def PrintData(section, name):
    '''A debugging function to print out individual blocks of data'''
    for block in section:
        print block['ranking'], block[name], block['usageRate']
    print "\n ---------- \n"

def GetData(pokemonID):
    '''Pulls the json data from PGL and converts it to a usable dictionary'''
    requestDataList = [
        'languageId=2',
        'seasonId=115',
        'battleType=5',
        'timezone=EDT',
        'pokemonId=%d-0' % (pokemonID),
        'displayNumberWaza=20',
        'displayNumberTokusei=3',
        'displayNumberSeikaku=20',
        'displayNumberItem=20',
        'displayNumberLevel=20',
        'displayNumberPokemonIn=20',
        'displayNumberPokemonDown=20',
        'displayNumberPokemonDownWaza=20',
        'timeStamp=1460576717081'
        ]
    requestDataString = "&".join(requestDataList)
    pokemonData = json.loads(requests.post(url, data=requestDataString, headers=headersDictionary).text)
    return pokemonData

def GetFormeData():
    '''Need to make manual HTTP requests for pokemon with alternate formes
        yes it's supposed to be spelled that way. I hate it too.'''
    returnList = []
    pokemonWithFormes = {
        'Rotom-H' : '479-1',
        'Rotom-W' : '479-2',
        'Rotom-Frost' : '479-3',
        'Rotom-Fan' : '479-4',
        'Rotom-M' : '479-5',
        'Giratina-O' : '487-1',
        'Tornadus-T' : '641-1',
        'Thundurus-T' : '642-1',
        'Landorus-T' : '645-1',
        'Kyurem-W' : '646-1',
        'Kyurem-B' : '646-2',
        'Meowstic-F' : '678-1',
        'Gourgeist-Small' : '711-1',
        'Gourgeist-Large' : '711-2',
        'Gourgeist-Super' : '711-3'
        }
    for pokemon in pokemonWithFormes:
        requestDataList = [
        'languageId=2',
        'seasonId=115',
        'battleType=5',
        'timezone=EDT',
        'pokemonId=%s' % (pokemonWithFormes[pokemon]),
        'displayNumberWaza=20',
        'displayNumberTokusei=3',
        'displayNumberSeikaku=20',
        'displayNumberItem=20',
        'displayNumberLevel=20',
        'displayNumberPokemonIn=20',
        'displayNumberPokemonDown=20',
        'displayNumberPokemonDownWaza=20',
        'timeStamp=1460576717081'
        ]
        requestDataString = "&".join(requestDataList)
        print "Now obtaining %s!" % (pokemon)
        pokemonData = json.loads(requests.post(url, data=requestDataString, headers=headersDictionary).text)
        pokemonData['rankingPokemonInfo']['name'] = pokemon
        print "We obtained %s!" % (pokemon)
        returnList.append(Pokemon(pokemonData))
    return returnList
        
class Pokemon:
    '''Holds all the data for a pokemon. Probably too big.'''
    def __init__(self, pokemonData):
        self.thisPokemonData = pokemonData
        self.thisPokemonName = pokemonData['rankingPokemonInfo']['name'].encode('utf8')
        if(pokemonData['rankingPokemonTrend']):
            self.thisPokemonRanking = pokemonData['rankingPokemonInfo']['ranking']
            self.movesThatThisPokemonKOsWith = pokemonData['rankingPokemonSuffererWaza']
            self.pokemonThatThisPokemonKOs = pokemonData['rankingPokemonSufferer']
            self.pokemonOnTheSameTeamWithThisPokemon = pokemonData['rankingPokemonIn']
            self.movesThatThisPokemonUses = pokemonData['rankingPokemonTrend']['wazaInfo']
            self.itemsThatThisPokemonUses = pokemonData['rankingPokemonTrend']['itemInfo']
            self.abilitiesThatThisPokemonUses = pokemonData['rankingPokemonTrend']['tokuseiInfo']
            self.naturesThatThisPokemonUses = pokemonData['rankingPokemonTrend']['seikakuInfo']
            self.pokemonThatKOThisPokemon = pokemonData['rankingPokemonDown']
            self.movesThatKOThisPokemon = pokemonData['rankingPokemonDownWaza']
            self.listOfPercentages = []
            self.listOfDenominators = []
            self.PopulatePercentages(self.movesThatThisPokemonUses)
            self.PopulatePercentages(self.itemsThatThisPokemonUses)
            self.PopulatePercentages(self.abilitiesThatThisPokemonUses)
            self.PopulatePercentages(self.naturesThatThisPokemonUses)
            self.totalNumberOfThisPokemon = self.CalculateTotalNumber()
            self.CorrectBlankEntries(self.movesThatThisPokemonKOsWith, 'wazaName')
            self.CorrectBlankEntries(self.movesThatThisPokemonUses, 'name')
            self.CorrectBlankEntries(self.itemsThatThisPokemonUses, 'name')
            self.CorrectBlankEntries(self.naturesThatThisPokemonUses, 'name')
            self.CorrectBlankEntries(self.movesThatKOThisPokemon, 'wazaName')
    def __repr__(self):
        return self.thisPokemonName
    def PopulatePercentages(self, numericalData):
        if(numericalData):
            for element in numericalData:
                self.listOfPercentages.append(element['usageRate']/100)
            for percentage in self.listOfPercentages:
                self.listOfDenominators.append((Fraction(percentage).limit_denominator()).denominator)
    def CalculateTotalNumber(self):
        return lcmForList(self.listOfDenominators)
    def WriteNumericalData(self, numericalData, name, textFile):
        if(numericalData):
            for element in numericalData:
                textFile.write(str(element['ranking'])+':'+ element[name]+','+ str(element['usageRate'])+"%"+','+ str(self.totalNumberOfThisPokemon*element['usageRate']/100)+'\n')
    def WriteNonNumericalData(self, nonNumericalData, textFile):
        if(nonNumericalData):
            for element in nonNumericalData:
                textFile.write(str(element['ranking'])+':'+ element['name']+'\n')
    def CorrectBlankEntries(self, data, name):
        if(data):
            for element in data:
                if(element['ranking'] == 0):
                    if(element[name] == None):
                        element[name] = 'Other'
    def WriteAllData(self):
        os.makedirs(os.path.join('.','Data',str(self.thisPokemonRanking)+'-'+self.thisPokemonName.decode('utf8')))
        textFile = open(os.path.join('.','Data',str(self.thisPokemonRanking)+'-'+self.thisPokemonName.decode('utf8'),str(self.thisPokemonRanking)+'-'+self.thisPokemonName.decode('utf8')+'.txt'),'w')

        textFile.write(str(self.thisPokemonRanking)+':'+ self.thisPokemonName+'|'+str(self.totalNumberOfThisPokemon))
        textFile.write("\n ---------- \n")
        textFile.write("Moves used:\n")
        self.WriteNumericalData(self.movesThatThisPokemonUses, 'name', textFile)
        textFile.write("\n ---------- \n")
        textFile.write("Items used:\n")
        self.WriteNumericalData(self.itemsThatThisPokemonUses, 'name', textFile)
        textFile.write("\n ---------- \n")
        textFile.write("Abilities used:\n")
        self.WriteNumericalData(self.abilitiesThatThisPokemonUses, 'name', textFile)
        textFile.write("\n ---------- \n")
        textFile.write("Natures used:\n")
        self.WriteNumericalData(self.naturesThatThisPokemonUses, 'name', textFile)
        textFile.write("\n ---------- \n")
        textFile.write("Top teammates:\n")
        self.WriteNonNumericalData(self.pokemonOnTheSameTeamWithThisPokemon, textFile)
        textFile.write("\n ---------- \n")
        textFile.write("Moves that this pokemon KOs with:\n")
        self.WriteNumericalData(self.movesThatThisPokemonKOsWith, 'wazaName', textFile)
        textFile.write("\n ---------- \n")
        textFile.write("Moves that KO this pokemon:\n")
        self.WriteNumericalData(self.movesThatKOThisPokemon, 'wazaName', textFile)
        textFile.write("\n ---------- \n")
        textFile.write("Pokemon that this pokemon KOs:\n")
        self.WriteNonNumericalData(self.pokemonThatThisPokemonKOs,textFile)
        textFile.write("\n ---------- \n")
        textFile.write("Pokemon that KO this pokemon:\n")
        self.WriteNonNumericalData(self.pokemonThatKOThisPokemon, textFile)
        textFile.close()

        
def orderByRanking(listOfPokemon):
    '''Orders the list of pokemon by their ranking on Battle Spot'''
    numberOfRankedPokemon = 0
    rankingNotFound = 0
    numberOfPokemonWithoutThisRanking = 0
    lowestNumber = 1
    for pokemon in listOfPokemon:
        if(hasattr(pokemon, 'thisPokemonRanking')):
            numberOfRankedPokemon+=1
    orderedList = []
    print numberOfRankedPokemon
    while(len(orderedList) < numberOfRankedPokemon):
        numberOfPokemonWithoutThisRanking = 0
        if(rankingNotFound==1): lowestNumber+=1
        print "We are looking for rank %d" % (lowestNumber)
        for pokemon in pokemonList:
            if(hasattr(pokemon, 'thisPokemonRanking')):
                if(pokemon.thisPokemonRanking == lowestNumber):
                    orderedList.append(pokemon)
                    lowestNumber+=1
                    rankingNotFound = 0
                    print pokemon, pokemon.thisPokemonRanking
                else:
                    numberOfPokemonWithoutThisRanking+=1
                    if(numberOfPokemonWithoutThisRanking == numberOfRankedPokemon):
                        rankingNotFound = 1

    return orderedList

def gcd(a,b):
    '''Calculates Greatest Common Denominator for two numbers'''
    while b:
        a,b = b, a%b
    return a

def lcm(a,b):
    '''Calculates the Least Common Multiple for two numbers'''
    return a * b // gcd(a,b)

def lcmForList(inputList):
    '''Calculates the Least Common Multiple for a list of numbers'''
    temp_lcm = 1
    for number in inputList:
        temp_lcm = lcm(temp_lcm, number)
    return temp_lcm

'''These hold some data for the HTTP request
    As far as I know, the cookie and timestamp don't affect anything,
    but the request returns an error if they are blank.'''
headersDictionary = {
	'Accept' : '*/*',
	'Accept-Encoding' : 'gzip, deflate',
	'Accept-Language' : 'en-US,en;q=0.8',
	'Connection' : 'keep-alive',
	'Content-Length' : '288',
	'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
	'Cookie' : '__ulfpc=201601211137474391; __utma=234147713.361904851.1453394265.1458005816.1458005816.1; __utmz=234147713.1458005816.1.1.utmcsr=pokemon-gl.com|utmccn=(referral)|utmcmd=referral|utmcct=/; region=1; language_id=2; site=2; _ga=GA1.2.361904851.1453394265; NO_MEMBER_DATA=%7B%22language_id%22%3A2%2C%22site%22%3A2%2C%22region%22%3A1%7D; JSESSIONID=7EF2250378221ABEE5A25264E4028FAD; AWSELB=99C3FF770EA3504C46F25D799674203D12E259AC7A4F0A5E1E369671A8F7594F0BEAC14B139D4F6D01FB26DFB85A3B6351067549EB45A267DB7E496BEA70327F1D05B86B10902FD1F8AC29087BDAD59C796899B4B7',
	'Host' : '3ds.pokemon-gl.com',
	'Origin' : 'http://3ds.pokemon-gl.com',
	'Referer' : 'http://3ds.pokemon-gl.com/battle/oras/',
	'User-Agent' : '/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
        }

url = "https://3ds.pokemon-gl.com/frontendApi/gbu/getSeasonPokemonDetail"


pokemonList = [0]
alternateFormesList = GetFormeData()

'''Populates the pokemonList with every pokemon'''
for dexNumber in range(720):
    pokemonList.append(Pokemon(GetData(dexNumber+1)))
    print pokemonList[dexNumber+1].thisPokemonName.decode('utf8')

pokemonList = pokemonList + alternateFormesList

'''Creates an ordered list, ordered by Battle Spot ranking'''
orderedListByRank = orderByRanking(pokemonList)
print orderedListByRank

print "Length of ordered list: %d" % len(orderedListByRank)
'''Writes the data to text files'''
for x in orderedListByRank:
    print x.thisPokemonRanking, x.thisPokemonName.decode('utf8'), x.totalNumberOfThisPokemon

for pokemon in orderedListByRank:
    pokemon.WriteAllData()

movesFile = open(os.path.join('.','Data','MovesData.txt'),'w')
for pokemon in orderedListByRank:
    movesFile.write(str(pokemon.thisPokemonRanking)+'.'+ pokemon.thisPokemonName+'|'+str(pokemon.totalNumberOfThisPokemon)+'\n')
    movesFile.write('---\n')
    pokemon.WriteNumericalData(pokemon.movesThatThisPokemonUses, 'name', movesFile)
    movesFile.write("\n ---------- \n")

movesFile.close()
