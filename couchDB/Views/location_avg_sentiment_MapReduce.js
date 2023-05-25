//Map
function (doc) {
    var location = "none";
    if (doc["doc"]["includes"]["places"][0]["full_name"]) {
        location = doc["doc"]["includes"]["places"][0]["full_name"].trim().toLowerCase();
        emit(location, doc.doc.data.sentiment);
    }
}

//Reduce
function (keys, values, rereduce) {
    if (!rereduce) {
        var length = values.length
        return [sum(values) / length, length]
    } else {
        var length = sum(values.map(function(v){return v[1]}));
        var avg = sum(values.map(function(v){
            return v[0] * (v[1] / length)
        }));
        return [avg, length]
    }
}