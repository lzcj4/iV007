function Dictionary() {
    var items = {};

    this.has = function (key) {
        return key in items;
    };

    this.put = function (key, value) {
        items[key] = value;
    };

    this.remove = function (key) {
        if (this.has(key)) {
            delete items[key];
            return true;
        }
        return false;
    };

    this.get = function (key) {
        return this.has(key) ? items[key] : undefined;
    };

    this.values = function () {
        var values = [];
        for (var k in items) {
            if (this.has(k)) {
                values.push(items[k]);
            }
        }
        return values;
    };

    this.clear = function () {
        items = {};
    };

    this.size = function () {
        var count = 0;
        for (var prop in items) {
            if (items.hasOwnProperty(prop)) {
                ++count;
            }
        }
        return count;
    };

    this.getItems = function () {
        return items;
    };
}


function mousePosition(ev) {
    var scrollLeft = document.documentElement.scrollLeft || document.body.scrollLeft;
    var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    return {
        x: ev.clientX + scrollLeft - document.documentElement.clientLeft,
        y: ev.clientY + scrollTop - document.documentElement.clientTop
    };
}


function addVidePlayerEvent(videoPlayer,ev, func) {
    videoPlayer.addEventListener(ev, func, false);
}

