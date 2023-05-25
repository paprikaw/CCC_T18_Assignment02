//Map
function (doc) {
    var location = "none";
    if (doc["doc"]["includes"]["places"][0]["full_name"]) {
        location = doc["doc"]["includes"]["places"][0]["full_name"].trim().toLowerCase();
        bbox = doc["doc"]["includes"]["places"][0]["geo"]["bbox"]
        longitudeCenter = (bbox[0] + bbox[2]) / 2;
        latitudeCenter = (bbox[1] + bbox[3]) / 2;
        emit(location, [latitudeCenter,longitudeCenter]);
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