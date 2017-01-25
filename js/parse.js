var pokemonList = [];
var htmlarray = [];

var currentMon = 0;

var formes = {"porygon-z":"474",
"jangmo-o":"782", 
"hakamo-o":"783", 
"kommo-o":"784", 
"oricorio-pom-pom":"741-1",
"oricorio-pa'u":"741-2",
"oricorio-sensu":"741-3",
"type:null":"772",
"lycanroc-midnight":"745-1",
"lycanroc-midday":"745",
"zygarde-10%":"718-1",
"zygarde-complete":"718-4",};

$( document ).ready(function() {
    readFile();
});


var readFile = function(data){
 	var results = 'Data/results.txt';
  $.get(results, function(data) {
    var dataset = data.split('\n');
    parseMons(dataset) 
  }, 'text');
}

var parseMons = function(dataset){
  for(line in dataset){
    var lineset = dataset[line].split('/');
    var numberset = dataset[line].split('-');
    var monName = lineset[1];
    var monNumber = numberset[0];
    parsePokemon(monName, monNumber, currentMon, dataset.length);
    ++currentMon;
  }
}

var parsePokemon = function(name, dexNumber, thisNumber, lengthOfMons){
  var pokemonFile = 'Data/'+name+'/usage.txt';
  $.get(pokemonFile, function(data) {
      var pokemonData = JSON.parse(data);

      thisPokemonName = pokemonData['rankingPokemonInfo']['name'];
      if(pokemonData['rankingPokemonInfo']['pokemonId'][pokemonData['rankingPokemonInfo']['pokemonId'].indexOf('-')+1] == 0)
        thisPokemonID = pokemonData['rankingPokemonInfo']['pokemonId'].slice(0, pokemonData['rankingPokemonInfo']['pokemonId'].indexOf('-'));
      else
        thisPokemonID = pokemonData['rankingPokemonInfo']['pokemonId'];
      thisPokemonRanking = pokemonData['rankingPokemonInfo']['ranking'];
      movesThatThisPokemonKOsWith = pokemonData['rankingPokemonSuffererWaza'];
      pokemonThatThisPokemonKOs = pokemonData['rankingPokemonSufferer'];
      pokemonOnTheSameTeamWithThisPokemon = pokemonData['rankingPokemonIn'];
      movesThatThisPokemonUses = pokemonData['rankingPokemonTrend']['wazaInfo'];
      itemsThatThisPokemonUses = pokemonData['rankingPokemonTrend']['itemInfo'];
      abilitiesThatThisPokemonUses = pokemonData['rankingPokemonTrend']['tokuseiInfo'];
      naturesThatThisPokemonUses = pokemonData['rankingPokemonTrend']['seikakuInfo'];
      pokemonThatKOThisPokemon = pokemonData['rankingPokemonDown'];
      movesThatKOThisPokemon = pokemonData['rankingPokemonDownWaza'];
      totalNumberOfThisPokemon = pokemonData['rankingPokemonInfo']['totalNumberOfThisPokemon'];
      pokemonList[thisNumber] = new Pokemon(movesThatThisPokemonUses, itemsThatThisPokemonUses, abilitiesThatThisPokemonUses, naturesThatThisPokemonUses, 
  pokemonOnTheSameTeamWithThisPokemon, movesThatThisPokemonKOsWith, movesThatKOThisPokemon, pokemonThatThisPokemonKOs, pokemonThatKOThisPokemon);
      if(name.includes("-Alola")){
        dexNumber = dexNumber +"-1";
      }
      else if(formes[name.toLowerCase().trim()] != undefined){
        dexNumber = formes[name.toLowerCase().trim()];
      }

      htmlarray[thisNumber] = ("<tr id = " + thisNumber + " class = trChild>\
            <td class = rankTD>" + (thisNumber+1) + "</td>\
            <td class = nameTD><img style = 'vertical-align: middle' src=sprites/" + dexNumber + ".png>" + name + "</img></td>\
            </tr>");
      console.log(thisNumber + " " + currentMon);

      handleElement(thisNumber);
      if(thisNumber==lengthOfMons-1){
        for(var i = 0; i < lengthOfMons; ++i){
        $('#tbl1.tbl-body').append(htmlarray[i]);
          handleElement(i);
        }
        $('#0').css("background-color","");
        display(0);
      }
  }, 'text');
}

function handleElement(id) {
    $('#'+id).children().click(function(){
      display(id);
    })
}

function Pokemon(movesThatThisPokemonUses, itemsThatThisPokemonUses, abilitiesThatThisPokemonUses, naturesThatThisPokemonUses, 
  pokemonOnTheSameTeamWithThisPokemon, movesThatThisPokemonKOsWith, movesThatKOThisPokemon, pokemonThatThisPokemonKOs, pokemonThatKOThisPokemon){
  
  this.moves = movesThatThisPokemonUses;
  this.items = itemsThatThisPokemonUses;
  this.abilities = abilitiesThatThisPokemonUses;
  this.natures = naturesThatThisPokemonUses;
  this.teammates = pokemonOnTheSameTeamWithThisPokemon;
  this.movesThatThisPokemonKOsWith = movesThatThisPokemonKOsWith;
  this.movesThatKOThisPokemon = movesThatKOThisPokemon;
  this.pokemonThatThisPokemonKOs = pokemonThatThisPokemonKOs;
  this.pokemonThatKOThisPokemon = pokemonThatKOThisPokemon;

  for(element in this.moves){
    this.moves[element]["usageRate"] = parseFloat(this.moves[element]["usageRate"]).toFixed(2);
    this.moves[element] = this.moves[element]["name"] + ": " + this.moves[element]["usageRate"] + "%";
  }

  for(element in this.items){
    this.items[element]["usageRate"] = parseFloat(this.items[element]["usageRate"]).toFixed(2);
    this.items[element] = this.items[element]["name"] + ": " + this.items[element]["usageRate"] + "%";
  }

  for(element in this.abilities){
    this.abilities[element]["usageRate"] = parseFloat(this.abilities[element]["usageRate"]).toFixed(2);
    this.abilities[element] = this.abilities[element]["name"] + ": " + this.abilities[element]["usageRate"] + "%";
  }

  for(element in this.natures){
    this.natures[element]["usageRate"] = parseFloat(this.natures[element]["usageRate"]).toFixed(2);
    this.natures[element] = this.natures[element]["name"] + ": " + this.natures[element]["usageRate"] + "%";
  }

  for(element in this.teammates){
    this.teammates[element] = this.teammates[element]["name"];
  }

  for(element in this.movesThatThisPokemonKOsWith){
    this.movesThatThisPokemonKOsWith[element] = this.movesThatThisPokemonKOsWith[element]["wazaName"];
  }

  for(element in this.movesThatKOThisPokemon){
    this.movesThatKOThisPokemon[element] = this.movesThatKOThisPokemon[element]["wazaName"];
  }

  for(element in this.pokemonThatThisPokemonKOs){
    this.pokemonThatThisPokemonKOs[element] = this.pokemonThatThisPokemonKOs[element]["name"];
  }

  for(element in this.pokemonThatKOThisPokemon){
    this.pokemonThatKOThisPokemon[element] = this.pokemonThatKOThisPokemon[element]["name"];
  }
}

var display = function(mon){
  $('#'+currentMon).css("background-color","");
  $('#'+mon).css("background-color","#e64946");
  currentMon = mon;
  $('#tbl2.tbl-body').html("");
  var lengths = [pokemonList[mon].moves.length, pokemonList[mon].abilities.length, pokemonList[mon].items.length, pokemonList[mon].abilities.length, pokemonList[mon].natures.length,
  pokemonList[mon].teammates.length, pokemonList[mon].movesThatThisPokemonKOsWith.length, pokemonList[mon].movesThatKOThisPokemon.length,
  pokemonList[mon].pokemonThatThisPokemonKOs.length, pokemonList[mon].pokemonThatKOThisPokemon.length]; //I am lazy and need the longest list
  lengths.sort(function(a, b){return a-b});

  for(var i =0; i < lengths[lengths.length-1] - 1; ++i){
  if(pokemonList[mon].moves[i] == undefined) pokemonList[mon].moves[i] = "";
  if(pokemonList[mon].items[i] == undefined) pokemonList[mon].items[i] = "";
  if(pokemonList[mon].abilities[i] == undefined) pokemonList[mon].abilities[i] = "";
  if(pokemonList[mon].natures[i] == undefined) pokemonList[mon].natures[i] = "";
  if(pokemonList[mon].teammates[i] == undefined) pokemonList[mon].teammates[i] = "";
  if(pokemonList[mon].movesThatThisPokemonKOsWith[i] == undefined) pokemonList[mon].movesThatThisPokemonKOsWith[i] = "";
  if(pokemonList[mon].movesThatKOThisPokemon[i] == undefined) pokemonList[mon].movesThatKOThisPokemon[i] = "";
  if(pokemonList[mon].pokemonThatThisPokemonKOs[i] == undefined) pokemonList[mon].pokemonThatThisPokemonKOs[i] = "";
  if(pokemonList[mon].pokemonThatKOThisPokemon[i] == undefined) pokemonList[mon].pokemonThatKOThisPokemon[i] = "";
   $('#tbl2.tbl-body').append("<tr>\
            <td>" + pokemonList[mon].moves[i] + "</td>\
            <td>" + pokemonList[mon].abilities[i] + "</td>\
            <td>" + pokemonList[mon].items[i] + "</td>\
            <td>" + pokemonList[mon].natures[i] + "</td>\
            <td>" + pokemonList[mon].teammates[i] + "</td>\
            <td>" + pokemonList[mon].movesThatThisPokemonKOsWith[i] + "</td>\
            <td>" + pokemonList[mon].movesThatKOThisPokemon[i] + "</td>\
            <td>" + pokemonList[mon].pokemonThatThisPokemonKOs[i] + "</td>\
            <td style = 'border-right: 2px solid black'>" + pokemonList[mon].pokemonThatKOThisPokemon[i] + "</td>\
            </tr>");
  }
}