// Map
function (doc) {
    function clean(text) {
        words = text.split("|");
        lowercasedWords = words.map(word => word.toLowerCase());
        return words;
    }
    if (doc["value"]["tokens"]) {
        var text = doc["value"]["tokens"];
        var cleanedWords = clean(text);
        cleanedWords.forEach(function(word) {
            emit(word, 1); 
        });
    }
}
// Reduce funcion here is the _sum in CouchDB
