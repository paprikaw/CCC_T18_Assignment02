// Map
function (doc) {
    var location = "none";
    if (doc["doc"]["includes"]["places"][0]["full_name"]) {
        states = ["australian capital territory", "new south wales", "victoria", 
                      "queensland", "south australia", "western australia", "tasmania", 
                      "northern territory"];
        location = doc["doc"]["includes"]["places"][0]["full_name"].trim().toLowerCase();
        split_location = location.split(",");
        state = "default";
        for (var i = 0; i < split_location.length; i++){
            if(states.includes(split_location[i].trim())){
                state = split_location[i].trim();
            }    
        }
        emit(state, doc.doc.data.sentiment);
    }
}
//Reduce
function (keys, values, rereduce) {
    if (!rereduce) {
        return values[0]
    } else {
        return values[0]
    }
}
